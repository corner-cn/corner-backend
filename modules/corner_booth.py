from models import BoothInfo
from utils.constants import BoothOperation
from utils.location import get_reverse

import uuid
import datetime

class CornerBooth(BoothInfo):

    def __init__(self, **kw):
        BoothInfo.__init__(self, **kw)

    def to_dict(self):
        # this is funny, we must read a attribute then __dict__ comes available, should be due to sqlalchemy lazy init.
        booth_name = self.booth_name
        ret = self.__dict__
        time_fmt = '%Y-%m-%d %H:%M:%S'
        ret['create_time'] = ret['create_time'].strftime(time_fmt) if 'create_time' in ret and ret['create_time'] else None
        ret['update_time'] = ret['update_time'].strftime(time_fmt) if 'update_time' in ret and ret['update_time'] else None
        ret['_sa_instance_state'] = None
        # TODO: image urls
        return ret

    @classmethod
    def create_from_dict(cls, info_dict):
        booth = cls()
        booth.booth_id = str(uuid.uuid1())
        booth.booth_name = info_dict.get('booth_name')
        booth.loc_text = info_dict.get('loc_text')
        booth.loc_lo = info_dict.get('loc_lo')
        booth.loc_la = info_dict.get('loc_la')
        booth.phone_number = info_dict.get('phone_number')
        booth.email = info_dict.get('email')
        booth.open_time = info_dict.get('open_time')
        booth.category = info_dict.get('category')
        booth.booth_owner = info_dict.get('booth_owner')
        booth.booth_story = info_dict.get('booth_story')
        booth.check_in_num = 0
        booth.priority = 0
        # TODO: timezone issue
        booth.create_time = datetime.datetime.utcnow()
        booth.create_by = info_dict.get('create_by')
        booth.disabled = False

        location = get_reverse(booth.loc_la, booth.loc_lo)
        if location:
            booth.city = location[1]
            booth.district = location[2]

        booth.save()
        return booth

    def perform_ops(self, ops):
        if ops == BoothOperation.CHECK_IN:
            self.check_in_num += 1
            self.save()

    def disable(self):
        self.disabled = True
        self.save()

