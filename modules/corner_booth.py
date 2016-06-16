from models import BoothInfo, BoothImages
from utils.constants import BoothOperation, BoothImageFlag
from utils.location import get_reverse
from sqlalchemy import orm

import uuid
import datetime
from pytz import timezone

from utils.common import gen_image_url

class CornerBooth(BoothInfo):

    def __init__(self, **kw):
        BoothInfo.__init__(self, **kw)

    @orm.reconstructor
    def load_on_init(self, **kw):
        BoothInfo.__init__(self, **kw)
        return self

    def to_dict(self):
        # this is funny, we must read a attribute then __dict__ comes available, should be due to sqlalchemy lazy init.
        booth_name = self.booth_name
        ret = self.__dict__
        time_fmt = '%Y-%m-%d %H:%M:%S'
        ret['create_time'] = ret['create_time'].strftime(time_fmt) if 'create_time' in ret and ret['create_time'] else None
        ret['update_time'] = ret['update_time'].strftime(time_fmt) if 'update_time' in ret and ret['update_time'] else None
        ret['_sa_instance_state'] = None
        ret['image_urls'] = []
        booth_imgs = BoothImages.all(booth_id=self.booth_id)
        for booth_img in booth_imgs:
            img_url = gen_image_url(self.booth_id, booth_img.image_path)
            if booth_img.flag == BoothImageFlag.THUMBNAIL:
                # http://api.ijiejiao.cn/static/88cf9f2f-774b-4df2-a090-6889b9100a98/corner_pic_1.png
                ret['thumbnail_url'] = img_url
            else:
                if booth_img.flag == BoothImageFlag.DEFAULT:
                    ret['image_urls'].insert(0, img_url)
                else:
                    ret['image_urls'].append(img_url)
        ret['distance'] = '-'
        if not ret['open_time']:
            ret['open_time'] = '-'
        return ret

    @classmethod
    def create_from_dict(cls, info_dict):
        # booth = BoothInfo.create(
        #     booth_id = str(uuid.uuid4()),
        #     booth_name = info_dict.get('booth_name'),
        #     loc_text = info_dict.get('loc_text'),
        #     loc_lo = info_dict.get('loc_lo'),
        #     loc_la = info_dict.get('loc_la'),
        #     phone_number = info_dict.get('phone_number'),
        #     email = info_dict.get('email'),
        #     open_time = info_dict.get('open_time'),
        #     category = info_dict.get('category'),
        #     booth_owner = info_dict.get('booth_owner'),
        #     booth_story = info_dict.get('booth_story'),
        #     check_in_num = 0,
        #     priority = 0,
        #     create_time = datetime.datetime.utcnow(),
        #     create_by = info_dict.get('create_by'),
        #     disabled = False
        # )
        booth = cls()
        booth.booth_id = str(uuid.uuid4())
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
        eastern = timezone('Asia/Chongqing')
        booth.create_time = datetime.datetime.now(eastern)
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

