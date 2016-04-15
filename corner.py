# -*- coding: utf-8 -*-

'''The app module, containing the app factory function.'''

import os
import redis
import json
from printobject import pp
from flask import Flask, render_template, session

from config import settings
from extensions import (
    db, migrate, bcrypt, login_manager, principals
)
from flask.ext.principal import (
    PermissionDenied, RoleNeed, identity_loaded)
from flask.ext.login import current_user
from werkzeug.contrib.cache import SimpleCache
import api


def create_app(config_object=None):
    '''
    An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/
    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    principals.init_app(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_listeners(app)
    register_db(app)

    app.local_cache = SimpleCache()

    return app


def register_extensions(app):
    bcrypt.init_app(app)
    login_manager.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(api.api.api, url_prefix='/api/v1')
    return None


def register_errorhandlers(app):
    def render_error(error):
        return str(error)
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_db(app):
    db.init_app(app)
    app.db = db
    migrate.init_app(app, db)
    return None


def register_listeners(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        if session.get('permissions'):
            for role in session.get('permissions'):
                identity.provides.add(RoleNeed(role))

        app.logger.debug('on_identity_loaded: {}'.format(identity))


myapp = None
from config import DBConfig
myapp = create_app(config_object=DBConfig)
pp(myapp.config)
# from werkzeug.contrib.fixers import ProxyFix
# myapp.wsgi_app = ProxyFix(myapp.wsgi_app)
myapp.run()
