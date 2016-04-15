# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.migrate import Migrate
migrate = Migrate()

from flask.ext.login import LoginManager
login_manager = LoginManager()

from flask.ext.principal import Principal
principals = Principal()

from flask.ext.security import Security
security = Security()
