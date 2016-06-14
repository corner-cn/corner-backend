import json
from flask import request
from flask.views import MethodView
import logging

from service import BoothService
from utils.constants import QueryType, QueryParams
from modules.corner_booth import CornerBooth

logger = logging.getLogger(__name__)


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
            CornerBooth.create_from_dict(info_dict=booth_info)
            return json.dumps(ret)
        else:
            booth_op = json.loads(request.data)
            operation = booth_op.get("operation")
            booth = CornerBooth.first(booth_id=id)
            booth.perform_ops(operation)
        return json.dumps(ret)

    def put(self, id):
        # TODO: uploadImg
        ret = {"status": 200}
        return json.dumps(ret)

    def delete(self, id):
        # TODO: need some validation and expiration token here.
        if id is None:
            pass
        else:
            booth = CornerBooth.first(booth_id=id)
            booth.disable()
        ret = {"status": 200}
        return json.dumps(ret)


class Booths(MethodView):

    def post(self):
        data = json.loads(request.data)
        logger.info("Query Booth list with params {}".format(data))
        my_position = data.get('my_position')
        longitude = my_position.get('longitude')
        latitude = my_position.get('latitude')
        query_type = data.get('query_type')
        query_params = data.get('query_params')
        ret = {"status": 0, "msg": "success", "data": []}

        booth_service = BoothService(longitude, latitude)

        if query_type == QueryType.RECOMMENDATION:
            recommend = booth_service.by_recommendation().first()
            if recommend:
                ret["data"].append(recommend.to_dict())

        elif query_type == QueryType.PRIORITY:
            priorities = booth_service.by_priority().first()
            priorities_list = list(priorities)
            for priority in priorities_list[:3]:
                ret["data"].append(priority.to_dict())

        elif query_type == QueryType.KEYWORDS:
            keywords = query_params.get(QueryParams.KEYWORDS)
            for keyword in keywords:
                booths = booth_service.by_keyword(keyword)
                for booth in list(booths):
                    ret["data"].append(booth.to_dict())

        elif query_type == QueryType.COMBINED:
            distance = query_params.get(QueryParams.DISTANCE)
            city = query_params.get(QueryParams.CITY)
            category = query_params.get(QueryParams.CATEGORY)
            district = query_params.get(QueryParams.DISTRICT)
            business_district = query_params.get(QueryParams.BUSINESS_DISTRICT)
            order_by = query_params.get(QueryParams.ORDER_BY)

            booth_query = booth_service.all()
            if category:
                booth_query = booth_service.by_category(category)

            if distance:
                pass
            elif district:
                booth_query = booth_service.by_district(city, district, booth_query)

            if order_by:
                booth_query = booth_service.order_by_flag(order_by, booth_query)

            booth_list = []
            if distance:
                # TODO: distinguish km, m,  and leave process later.
                booth_list = booth_service.by_distance(distance, booth_query)
            else:
                booth_list = list(booth_query)

            for booth in booth_list:
                ret["data"].append(booth.to_dict())

        else:
            msg = "Invalid query type {}".format(query_type)
            ret = {"status": -1, "msg": msg, "data": []}
            logger.error(msg)

        return json.dumps(ret)


class Image(MethodView):

    def get(self, id):
        if id is None:
            pass
        else:
            # TODO: getImageByBooth
            pass
        ret = {"rows": [], "total": 0, "msg": ""}
        return json.dumps(ret)


class Category(MethodView):

    def get(self):
        # TODO: get category list.
        # TODO: define category in backend
        pass
