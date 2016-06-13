import json
from flask import current_app, request
from flask.views import MethodView

import subprocess
from multiprocessing import Process
import redis
from service import getBoothById, createBooth, thumbBooth, uploadImg, deleteBooth, queryBooths, getImageByBooth


class Booth(MethodView):

    def get(self, id):
        # TODO: getBoothById
        return getBoothById(id)

    def post(self, id):
        if id is None:
            # TODO: createBooth
            boothInfo = json.loads(request.data)
            print boothInfo
            return createBooth(boothInfo)
        else:
            # TODO: thumbBooth(like or dislike)
            pass
        ret = {"status": 200}
        return json.dumps(ret)

        # r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
        # dist = r.execute_command('GEODIST Sicily Palermo Catania', )


    def put(self, id):
        # TODO: uploadImg
        ret = {"status": 200}
        return json.dumps(ret)

    def delete(self, id):
        # TODO: deleteBooth
        if id is None:
            pass
        else:
            pass
        ret = {"status": 200}
        return json.dumps(ret)


class Booths(MethodView):

    def post(self):
        # TODO: queryBooths
        ret = {"status": 200}
        return json.dumps(ret)

        r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
        dist = r.execute_command('GEODIST Sicily Palermo Catania', )


class Image(MethodView):

    def get(self, id):
        if id is None:
            pass
        else:
            # TODO: getImageByBooth
            pass
        ret = {"rows": [], "total": 0, "msg": ""}
        return json.dumps(ret)
