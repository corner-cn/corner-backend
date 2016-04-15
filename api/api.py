# -*- coding: utf-8 -*-

import simplejson
import json
import datetime
import time
import os
import sys
import re
import logging
from sqlalchemy import and_, or_, text, desc, cast, String
from sqlalchemy.sql import func
import operator
import calendar
import requests
import collections
import copy
import pytz
import thread
import uuid
import pickle
from flask import (
    Blueprint, request, render_template, redirect, current_app, flash, session, url_for)
from flask.ext.login import login_required
from werkzeug import secure_filename
from models import (BoothInfo, BoothOwner)
from werkzeug.contrib.cache import SimpleCache

from flask.ext.login import login_user, login_required, current_user
from flask.ext.principal import (Permission, RoleNeed)
import commands

from booth import Booth

reload(sys)
sys.setdefaultencoding('utf8')

api = Blueprint('api', __name__)

logger = logging.getLogger('api')

cache = SimpleCache()

booth = Booth.as_view('booth')
api.add_url_rule('/booth/', view_func=booth, defaults={'id': None})
api.add_url_rule('/booth/<id>', view_func=booth)
