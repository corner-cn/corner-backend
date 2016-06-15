import json
from sqlalchemy import desc, and_, or_, in_

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
        # TODO: Need discuss with Dan Yun Whether Cell Phone can resolve this or not.
        location = get_reverse(self.latitude, self.longitude)
        self.city = None
        if location:
            self.city = location[1]

    @staticmethod
    def by_id(id):
        booth = CornerBooth.first(booth_id=id)
        return booth

    @staticmethod
    def by_recommendation():
        return BoothService.order_by_flag(SpecialFlag.CHECK_IN, filter_query=None)

    @staticmethod
    def by_priority():
        return BoothService.order_by_flag(SpecialFlag.PRIORITY, filter_query=None)

    @staticmethod
    def by_keyword(keyword):
        filter_query = CornerBooth.where(disabled=False).filter(
            or_(
                CornerBooth.booth_name.like('%{}%'.format(keyword)),
                CornerBooth.booth_owner.like('%{}%'.format(keyword)),
                CornerBooth.category.like('%{}%'.format(keyword))
            )
        )
        return filter_query

    @staticmethod
    def by_distance(distance_ids, filter_query=None):
        # Query distance ids first with redis geo
        # Then query booths by distance ids
        if filter_query:
            return filter_query.filter(
                CornerBooth.id.in_(distance_ids)
            )
        else:
            return CornerBooth.all(
                CornerBooth.id.in_(distance_ids)
            )

    @staticmethod
    def by_district(city, district, filter_query=None):
        if filter_query:
            return filter_query.filter_by(
                city=city,
                district=district
            )
        else:
            return CornerBooth.all(
                city=city,
                district=district
            )

    @staticmethod
    def by_business_district(city, business_district, filter_query=None):
        if filter_query:
            return filter_query.filter_by(
                city=city,
                business_district=business_district
            )
        else:
            return CornerBooth.all(
                city=city,
                business_district=business_district
            )

    @staticmethod
    def by_category(category, filter_query=None):
        if filter_query:
            return filter_query.filter_by(
                category=category
            )
        else:
            return CornerBooth.all(
                category=category
            )

    @staticmethod
    def order_by_flag(special_flag, filter_query=None):
        if not filter_query:
            filter_query = CornerBooth.where(disabled=False)
        if special_flag == SpecialFlag.CHECK_IN:
            return filter_query.order_by(desc(CornerBooth.check_in_num))
        if special_flag == SpecialFlag.LATEST:
            return filter_query.order_by(desc(CornerBooth.create_time))
        if special_flag == SpecialFlag.PRIORITY:
            return filter_query.order_by(CornerBooth.check_in_num)

    @staticmethod
    def by_create_time(city, business_district):
        pass

    @classmethod
    def insertBoothGeo(cls, boothId, x, y):
        return cls._geo.geoadd(cls._element, x, y, boothId)

    @classmethod
    def getNearestBoothById(cls, boothId, scale=1000, unit='m', limit=50):
        return cls._geo.georadiusbymember(cls._element, boothId, scale, unit, 'withdist', 'asc', 'count', limit)

    @classmethod
    def getNearestBoothByLocation(cls, latitude, longitude, scale=1000, unit='m', limit=50):
        return cls._geo.georadius(cls._element, latitude, longitude, scale, unit, 'withdist', 'asc', 'count', limit)

    @classmethod
    def get_distance(cls, target_la, target_lo):
        # haversine Formula
        if target_la and target_lo and self.longitude and self.latitude:
            lon1, lat1, lon2, lat2 = map(radians, [self.longitude, self.latitude, target_la, target_lo])  
  
            dlon = lon2 - lon1   
            dlat = lat2 - lat1   
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
            c = 2 * asin(sqrt(a))   
            r = 6371 
            return c * r * 1000   
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


def uploadImg():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)

def getImageByBooth():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)

