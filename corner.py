# -*- coding: utf-8 -*-

'''The app module, containing the app factory function.'''

from printobject import pp
from flask import Flask

from extensions import (
    db, migrate
)
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
    # print config_object.__dict__
    register_blueprints(app)
    register_errorhandlers(app)
    register_db(app)

    app.local_cache = SimpleCache()

    return app


def register_blueprints(app):
    app.register_blueprint(api.api.api, url_prefix='/v1')
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


from config import DBConfig
myapp = create_app(config_object=DBConfig)
pp(myapp.config)
# myapp.run()
