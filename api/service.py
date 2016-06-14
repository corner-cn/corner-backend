import json
from sqlalchemy import desc, and_, or_

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
        filter_query = CornerBooth.all()
        return BoothService.order_by_flag(SpecialFlag.CHECK_IN, filter_query=filter_query)

    @staticmethod
    def by_priority():
        filter_query = CornerBooth.all()
        return BoothService.order_by_flag(SpecialFlag.PRIORITY, filter_query=filter_query)

    @staticmethod
    def by_keyword(keyword):
        filter_query = CornerBooth.all().filter(
            or_(
                CornerBooth.booth_name.like('%{}%'.format(keyword)),
                CornerBooth.booth_owner.like('%{}%'.format(keyword)),
                CornerBooth.category.like('%{}%'.format(keyword))
            )
        )
        return filter_query

    @staticmethod
    def by_distance(distance, filter_query=None):
        # TODO: query by redis features.
        pass

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
            return None
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
    def getNearestBoothById(cls, boothId, scale=10, limit=50):
        return cls._geo.georadiusbymember(cls._element, boothId, scale, 'km', 'withdist', 'asc', 'count', limit)

    @classmethod
    def getNearestBoothByLocation(cls, latitude, longitude, scale=10, limit=50):
        return cls._geo.georadius(cls._element, latitude, longitude, scale, 'km', 'withdist', 'asc', 'count', limit)

    def all(self):
        if self.city:
            return CornerBooth.all(city=self.city)
        else:
            return CornerBooth.all()


# def queryBooths():
#   ret = {"rows": [], "total": 0, "msg": ""}
#   return json.dumps(ret)

# def getBoothById(id):
#   ret = {"status": "ok", "data": None}
#   booth = db.session.query(BoothInfo).filter_by(
#     id = id
#   ).one()
#   ret['data'] = json.dumps(booth2json(booth))
#   return json.dumps(ret)

# def createBooth(info):
#   booth = BoothInfo()
#   booth.id = uuid.uuid4()
#   booth.booth_name = info['booth_name']
#   booth.loc_text = info['loc_text']
#   booth.loc_lo = info['loc_lo']
#   booth.loc_la = info['loc_la']
#   booth.phone_numb = info['phone_numb']
#   booth.email = info['email']
#   booth.open_time = info['open_time']
#   booth.category = info['category']
#   booth.booth_owner = info['booth_owner']
#   booth.booth_story = info['booth_story']
#   booth.checkin_num = 0
#   booth.create_time = datetime.now(pytz.utc)
#   # booth.update_time = info.loc_text
#   booth.disabled = False
#   booth.save()
#   ret = {"status": "ok", "msg": "Add successfully"}
#   return json.dumps(ret)
#
# def thumbBooth():
#   ret = {"rows": [], "total": 0, "msg": ""}
#   return json.dumps(ret)

def uploadImg():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)

# def deleteBooth():
#   ret = {"rows": [], "total": 0, "msg": ""}
#   return json.dumps(ret)

# def queryBooths():
#   ret = {"rows": [], "total": 0, "msg": ""}
#   return json.dumps(ret)

def getImageByBooth():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)
#
# def booth2json(booth):
#   ret = booth.__dict__
#   timefmt = '%Y-%m-%d %H:%M:%S'
#   ret['create_time'] = ret['create_time'].strftime(timefmt) if 'create_time' in ret else None
#   ret['update_time'] = ret['update_time'].strftime(timefmt) if 'update_time' in ret else None
#   ret['_sa_instance_state'] = None
#   return ret

