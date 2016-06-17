import json
from flask import request
from flask.views import MethodView
import logging
import os
import sys

from service import BoothService, ImageService
from utils.constants import QueryType, QueryParams
from modules.corner_booth import CornerBooth
from utils.constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, BoothImageFlag, IMAGE_DIR_PREFIX
from modules.models import BoothImages

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class Booth(MethodView):

    def get(self, id):
        ret = {"status": 0, "msg": "success", "data": []}
        booth = BoothService.by_id(id)
        if booth:
            ret["data"].append(booth.to_dict())
        return json.dumps(ret)

    def post(self, id):
        ret = {"status": 0, "msg": "success", "data": []}
        if id is None:
            booth_info = json.loads(request.data)
            logger.info("Create booth with params {}".format(booth_info))
            booth = CornerBooth.create_from_dict(info_dict=booth_info)
            if booth.loc_la and booth.loc_lo:
                BoothService.geo_add(booth.booth_id, booth.loc_lo, booth.loc_la)
                ret["data"].append(booth.to_dict())
            return json.dumps(ret)
        else:
            booth_op = json.loads(request.data)
            operation = booth_op.get("operation")
            booth = CornerBooth.first(booth_id=id)
            booth.perform_ops(operation)
        return json.dumps(ret)

    def put(self, id):
        # TODO: disable this
        ret = {"status": 0, "msg": "success", "data": []}
        uploaded_files = request.files.getlist("file[]")
        logger.info("upload files {}".format(uploaded_files))
        filenames = []
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = file.filename
                # Move the file form the temporal folder to the upload
                # folder we setup
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                # Save the filename into a list, we'll use it later
                filenames.append(filename)
                # Redirect the user to the uploaded_file route, which
                # will basicaly show on the browser the uploaded file
        # Load an html page with a link to each uploaded file
        return json.dumps(ret)

    def delete(self, id):
        ret = {"status": 0, "msg": "success", "data": []}
        return json.dumps(ret)
        # Maybe later.
        # if id is None:
        #     pass
        # else:
        #     booth = CornerBooth.first(booth_id=id)
        #     booth.disable()
        # ret = {"status": 200}
        # return json.dumps(ret)


class Booths(MethodView):

    def post(self):
        data = json.loads(request.data)
        logger.error("Query Booth list with params {}".format(data))
        my_position = data.get('my_position')
        longitude = None
        latitude = None
        if my_position:
            longitude = my_position.get('longitude')
            latitude = my_position.get('latitude')
        logger.info("longitude is {} while latitude is {}".format(longitude, latitude))
        query_type = data.get('query_type')
        query_params = data.get('query_params')
        ret = {"status": 0, "msg": "success", "data": []}

        booth_service = BoothService(longitude, latitude)

        if query_type == QueryType.RECOMMENDATION:
            recommends = booth_service.by_recommendation()
            if recommends:
                for recommend in list(recommends)[:3]:
                    booth_info = recommend.to_dict()
                    if my_position:
                        logger.info("Getting distance between {} and {}".format(my_position, recommend.booth_id))
                        booth_info['distance'] = booth_service.get_distance(recommend.booth_id)
                    ret["data"].append(booth_info)

        elif query_type == QueryType.PRIORITY:
            priority = booth_service.by_priority().first()
            if priority:
                booth_info = priority.to_dict()
                if my_position:
                    logger.info("Getting distance between {} and {}".format(my_position, priority.booth_id))
                    booth_info['distance'] = booth_service.get_distance(priority.booth_id)
                ret["data"].append(booth_info)

        elif query_type == QueryType.KEYWORDS:
            keywords = query_params.get(QueryParams.KEYWORDS)
            for keyword in keywords:
                booths = booth_service.by_keyword(keyword)
                for booth in list(booths):
                    booth_info = booth.to_dict()
                    if my_position:
                        logger.info("Getting distance between {} and {}".format(my_position, booth.booth_id))
                        booth_info['distance'] = booth_service.get_distance(booth.booth_id)
                    ret["data"].append(booth_info)

        elif query_type == QueryType.COMBINED:
            distance = query_params.get(QueryParams.DISTANCE)
            city = query_params.get(QueryParams.CITY)
            category = query_params.get(QueryParams.CATEGORY)
            district = query_params.get(QueryParams.DISTRICT)
            business_district = query_params.get(QueryParams.BUSINESS_DISTRICT)
            order_by = query_params.get(QueryParams.ORDER_BY)

            booth_query = booth_service.all()
            if category and category != "all":
                booth_query = booth_service.by_category(category)

            if distance:
                pass
            elif district:
                booth_query = booth_service.by_district(city, district, booth_query)

            if order_by:
                booth_query = booth_service.order_by_flag(order_by, booth_query)

            boothGeos = {}
            if distance:
                # distance will looks like 100, 200, 500, 2000... we need implement by_distance
                # 100m 200m 500m ...
                # boothGeos: [[boothId1, distance],[boothId2, distance]...]
                # boothGeos = dict(booth_service.getNearestBoothByLocation(booth_service.latitude, booth_service.longitude, distance))
                booth_list = booth_service.by_distance(distance, booth_query)
            else:
                booth_list = list(booth_query)

            for booth in booth_list:
                # implement get_distance.
                # Current redis do not support this, only can get distance by location symbols
                # Use haversine Formula instead
                # Can we just give booths coordinates and display in client with map instead of computation in backend?
                # Backend do not have street info
                booth_info = booth.to_dict()
                if my_position:
                    logger.info("Getting distance between {} and {}".format(my_position, booth.booth_id))
                    booth_info['distance'] = booth_service.get_distance(booth.booth_id)

                ret["data"].append(booth_info)

        else:
            msg = "Invalid query type {}".format(query_type)
            ret = {"status": -1, "msg": msg, "data": []}
            logger.error(msg)

        return json.dumps(ret)


class Image(MethodView):

    def post(self, id):
        ret = {"status": 0, "msg": "success", "data": []}
        booth = CornerBooth.first(booth_id=id)
        if not booth:
            msg = "Can not get booth ID {}".format(id)
            ret = {"status": -1, "msg": msg, "data": []}
            return json.dumps(msg)

        logger.error("upload files with request {} and files {}".format(request.__dict__, request.files))
        files_hash = request.files.to_dict()
        logger.info("files hash {}".format(files_hash))
        filenames = []
        for img_file in files_hash.values():
            filename = ImageService.upload(img_file, id)
            filenames.append(filename)

        booth_images = []
        if booth:
            for image in filenames:
                booth_image = BoothImages.create(
                    booth_id=booth.booth_id,
                    image_path=image,
                    create_time=booth.create_time
                )
                booth_images.append(booth_image)

        default_img = booth_images[0]
        default_img.flag = BoothImageFlag.DEFAULT
        default_img.save()

        thumbnail_img = ImageService.mk_thumbnail(id, default_img.image_path)
        booth_image = BoothImages.create(
            booth_id=booth.booth_id,
            image_path=thumbnail_img,
            create_time=booth.create_time,
            flag=BoothImageFlag.THUMBNAIL
        )

        return json.dumps(ret)


    def get(self, id):
        # NOTE: This method seems no need to implement now.
        if id is None:
            pass
        else:
            pass
        ret = {"rows": [], "total": 0, "msg": ""}
        return json.dumps(ret)


class Category(MethodView):

    def get(self):
        # TODO: get category list.
        pass



