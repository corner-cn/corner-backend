# -*- coding: utf-8 -*-
import sys
import logging
from flask import Blueprint

from booth import Booth

reload(sys)
sys.setdefaultencoding('utf8')

api = Blueprint('api', __name__)

logger = logging.getLogger('api')

booth = Booth.as_view('booth')
api.add_url_rule('/booth/', view_func=booth, defaults={'id': None})
api.add_url_rule('/booth/<id>', view_func=booth)

