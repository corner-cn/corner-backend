import json
from sqlalchemy import desc, and_, or_
import uuid
import logging
import sys
import os
from PIL import Image
import random
import string

from utils.constants import SpecialFlag, IMAGE_DIR_PREFIX, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from utils.location import get_reverse, GeoApi
from modules.corner_booth import CornerBooth
from extensions import corner_redis


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

class BoothService(object):

    _geo = GeoApi(corner_redis)
    _element = 'booths'

    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        location = get_reverse(self.latitude, self.longitude)
        self.city = None
        if location:
            self.city = location[1]

    @staticmethod
    def by_id(id):
        booth = CornerBooth.first(booth_id=id)
        return booth

    def by_recommendation(self):
        return self.order_by_flag(SpecialFlag.CHECK_IN, filter_query=None)

    def by_priority(self):
        return self.order_by_flag(SpecialFlag.PRIORITY, filter_query=None)

    def by_keyword(self, keyword):
        filter_query = CornerBooth.where(disabled=False).filter(
            or_(
                CornerBooth.booth_name.like('%{}%'.format(keyword)),
                CornerBooth.booth_owner.like('%{}%'.format(keyword)),
                CornerBooth.category.like('%{}%'.format(keyword))
            )
        )
        return filter_query

    def by_distance(self, distance, filter_query=None):
        # Query distance ids first with redis geo
        # Then query booths by distance ids
        nearby_booths = BoothService.geo_redius(self.longitude, self.latitude, distance)
        nearby_booth_ids = [booth[0] for booth in nearby_booths]
        logger.info("nearby booth ids should be {}".format(nearby_booth_ids))
        if filter_query:
            return filter_query.filter(
                CornerBooth.booth_id.in_(
                    nearby_booth_ids
                )
            )
        else:
            return CornerBooth.where(
                disabled=False
            ).filter(
                CornerBooth.booth_id.in_(
                    nearby_booth_ids
                )
            )

    def by_district(self, city, district, filter_query=None):
        if filter_query:
            return filter_query.filter_by(
                city=city,
                district=district
            )
        else:
            return CornerBooth.where(
                city=city,
                district=district,
                disabled=False
            )

    def by_business_district(self, city, business_district, filter_query=None):
        if filter_query:
            return filter_query.filter_by(
                city=city,
                business_district=business_district
            )
        else:
            return CornerBooth.where(
                city=city,
                business_district=business_district,
                disabled=False
            )

    def by_category(self, category, filter_query=None):
        if filter_query:
            return filter_query.filter_by(
                category=category
            )
        else:
            return CornerBooth.where(
                category=category
            )

    def order_by_flag(self, special_flag, filter_query=None):
        if not filter_query:
            filter_query = CornerBooth.where(disabled=False)
        if special_flag == SpecialFlag.CHECK_IN:
            return filter_query.order_by(desc(CornerBooth.check_in_num))
        if special_flag == SpecialFlag.LATEST:
            return filter_query.order_by(desc(CornerBooth.create_time))
        if special_flag == SpecialFlag.PRIORITY:
            return filter_query.order_by(CornerBooth.check_in_num)

    def by_create_time(self, city, business_district):
        pass

    @classmethod
    def geo_add(cls, boothId, longitude, latitude):
        return cls._geo.geoadd(cls._element, longitude, latitude, boothId)

    @classmethod
    def geo_redius(cls, longitude, latitude, scale=1000, unit='m', limit=50):
        return cls._geo.georadius(cls._element, longitude, latitude, scale, unit, 'withdist', 'asc', 'count', limit)

    @classmethod
    def geo_dist(cls, src_id, dst_id):
        return cls._geo.geodist(cls._element, src_id, dst_id, 'm')

    def get_distance(self, booth_id):
        my_id = str(uuid.uuid4())
        my_pos = BoothService.geo_add(my_id, self.longitude, self.latitude)
        dist = BoothService.geo_dist(my_id, booth_id)
        self._geo.zrem(self._element, my_pos)
        try:
            if dist:
                if float(dist) > 1000:
                    dist_rd = "%0.1f" %(float(dist) / 1000)
                    return "{} km".format(dist_rd)
                else:
                    return int(dist)
            return dist
        except Exception as e:
            return None


    def all(self):
        if self.city:
            return CornerBooth.where(
                city=self.city,
                disabled=False
            )
        else:
            return CornerBooth.where(
                disabled=False
            )


class ImageService(object):

    @staticmethod
    def get_image_work_dir(booth_id):
        return os.path.join(IMAGE_DIR_PREFIX, UPLOAD_FOLDER, booth_id)

    @staticmethod
    def get_image_full_path(booth_id, filename):
        file_dir = ImageService.get_image_work_dir(booth_id)
        return os.path.join(file_dir, filename)

    @staticmethod
    def gen_filename(extension=None):
        if extension:
            return "{}.{}".format(random_word(15), extension)
        else:
            return random_word(15)

    @classmethod
    def upload(cls, img_file, booth_id):
        logger.info("processing file {}".format(img_file))
        if not img_file:
            return None
        if not allowed_file(img_file.filename):
            return None

        extension = img_file.filename.rsplit('.', 1)[-1]
        filename = ImageService.gen_filename(extension)
        logger.info("current working dir {}".format(os.getcwd()))
        file_dir = os.path.join(IMAGE_DIR_PREFIX, UPLOAD_FOLDER, booth_id)
        file_path = os.path.join(file_dir, filename)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        logger.info("file path is {}".format(file_path))
        img_file.save(file_path)
        return filename

    @staticmethod
    def mk_default(filename):
        # NO need this feature currently
        pass

    @staticmethod
    def mk_thumbnail(booth_id, filename):
        # 4:3 -> 400 300
        try:
            logger.info("generating thumnail for file {}".format(filename))
            file_full_path = ImageService.get_image_full_path(booth_id, filename)
            with Image.open(file_full_path) as im:
                logger.info("source image size: {}".format(im.size))
                width, height = im.size
                if int(width / 4) >= int(height / 3):
                    newwidth = int(height / 3) * 4
                    newheight = height
                else:
                    newwidth = width
                    newheight = int(width / 4) * 3

                logger.info("new size {} {}".format(newwidth, newheight))
                newim = im.crop((0, 0, newwidth, newheight))
                newim.thumbnail((400, 300))
                extension = filename.rsplit('.', 1)[-1]
                import pdb
                pdb.set_trace()
                thumbnail_filename = ImageService.gen_filename(extension="JPEG")
                thumbnail_path = ImageService.get_image_work_dir(booth_id)
                logger.info("saving thumbnail file to {}".format(thumbnail_filename))
                newim.save("{}/{}".format(thumbnail_path, thumbnail_filename), "JPEG")
                return "{}.{}".format(thumbnail_filename, "JPEG")
        except IOError as e:
            print "error due to {}".format(unicode(e))
            return None


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           (filename.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS or
            filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS)


def random_word(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


