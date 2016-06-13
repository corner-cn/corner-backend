import json
import subprocess
from multiprocessing import Process
import redis
from modules.models import BoothInfo, BoothImages, BoothAccusation
from extensions import db
from datetime import datetime
import pytz
import uuid

def queryBooths():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)

def getBoothById(id):
  ret = {"status": "ok", "data": None}
  booth = db.session.query(BoothInfo).filter_by(
    id = id
  ).one()
  ret['data'] = json.dumps(booth2json(booth))
  return json.dumps(ret)

def createBooth(info):
  booth = BoothInfo()
  booth.id = uuid.uuid4()
  booth.booth_name = info['booth_name']
  booth.loc_text = info['loc_text']
  booth.loc_lo = info['loc_lo']
  booth.loc_la = info['loc_la']
  booth.phone_numb = info['phone_numb']
  booth.email = info['email']
  booth.open_time = info['open_time']
  booth.category = info['category']
  booth.booth_owner = info['booth_owner']
  booth.booth_story = info['booth_story']
  booth.like_count = 0
  booth.create_time = datetime.now(pytz.utc)
  # booth.update_time = info.loc_text
  booth.disabled = False
  booth.save()
  ret = {"status": "ok", "msg": "Add successfully"}
  return json.dumps(ret)

def thumbBooth():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)

def uploadImg():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)

def deleteBooth():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)

def queryBooths():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)

def getImageByBooth():
  ret = {"rows": [], "total": 0, "msg": ""}
  return json.dumps(ret)

def booth2json(booth):
  ret = booth.__dict__
  timefmt = '%Y-%m-%d %H:%M:%S'
  ret['create_time'] = ret['create_time'].strftime(timefmt) if 'create_time' in ret else None
  ret['update_time'] = ret['update_time'].strftime(timefmt) if 'update_time' in ret else None
  ret['_sa_instance_state'] = None
  return ret

