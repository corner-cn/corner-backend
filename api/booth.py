import json
from flask import current_app, request
from flask.views import MethodView

import subprocess
from multiprocessing import Process
import redis


class Booth(MethodView):

    def get(self, id):
        if id is None:
            pass
        else:
            pass
        ret = {"rows": [], "total": 0, "msg": ""}
        return json.dumps(ret)

    def post(self, id):
        if id is None:
            pass
        else:
            pass
        ret = {"status": 200}
        return json.dumps(ret)

        r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
        dist = r.execute_command('GEODIST Sicily Palermo Catania', )


    def put(self):
        ret = {"status": 200}
        return json.dumps(ret)

    def delete(self, id):
        if id is None:
            pass
        else:
            pass
        ret = {"status": 200}
        return json.dumps(ret)
