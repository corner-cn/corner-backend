import json
from sqlalchemy import desc, and_, or_
import uuid

from utils.constants import SpecialFlag
from utils.location import get_reverse, GeoApi
from modules.corner_booth import CornerBooth
from extensions import corner_redis


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
        nearby_booth_ids = BoothService.geo_redius(self.longitude, self.latitude, distance)
        if filter_query:
            return filter_query.filter_by(
                CornerBooth.booth_id.in_(
                    nearby_booth_ids
                )
            )
        else:
            return CornerBooth.where(
                disabled=False
            ).filter_by(
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
        return dist

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


def uploadImg():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)

def getImageByBooth():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)

