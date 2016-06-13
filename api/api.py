# -*- coding: utf-8 -*-
import sys
import logging
from flask import Blueprint

from booth import Booth, Booths, Image

reload(sys)
sys.setdefaultencoding('utf8')

api = Blueprint('api', __name__)

logger = logging.getLogger('api')

booth = Booth.as_view('booth')
booths = Booths.as_view('booths')
image = Image.as_view('image')

api.add_url_rule('/booth/', view_func=booth, defaults={'id': None}, methods=['POST'])
api.add_url_rule('/booth/<id>', view_func=booth, methods=['GET', 'POST', 'PUT', 'DELETE'])

api.add_url_rule('/booths/', view_func=booths)

api.add_url_rule('/img/', view_func=image)
