# -*- coding: utf-8 -*-
import os
from confire import Configuration, environ_setting

import dotenv
dotenv.load_dotenv(os.path.join(os.path.join(os.path.dirname(__file__)), '.env'))

class Config(Configuration):

    app_dir = os.path.abspath(os.path.dirname(__file__))  # This directory
    project_root = os.path.abspath(os.path.join(app_dir, os.pardir))

    assets_debug = False
    debug_tb_enabled = False  # Disable Debug toolbar
    debug_tb_intercept_redirects = False
    cache_type = 'simple'  # Can be "memcached", "redis", etc.

    api_version = "v1"

    # secret_key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SESSION_COOKIE_SECURE = True

    def config_for_flask(self):
        return {
            'REDIS_HOST': self.get('REDIS_HOST'),
            'REDIS_PORT': self.get('REDIS_PORT'),
            'DEBUG': self.get('DEBUG'),
            'DEBUG_TB_ENABLED': self.get('DEBUG_TB_ENABLED'),
            'DEBUG_TB_INTERCEPT_REDIRECTS': self.get('DEBUG_TB_INTERCEPT_REDIRECTS'),
            'SECRET_KEY': self.get('SECRET_KEY'),
            'SQLALCHEMY_DATABASE_URI': self.get('SQLALCHEMY_DATABASE_URI'),
            'WTF_CSRF_ENABLED': False,
            'SECURITY_SEND_REGISTER_EMAIL': False,
        }


class DBConfig(Config):
    db_host = environ_setting("DB_HOST", required=True)
    db_port = environ_setting("DB_PORT", 5432, required=False)
    db_name = environ_setting("DB_NAME", required=True)
    db_user = environ_setting("DB_USER", required=True)
    db_pass = environ_setting("DB_PASS", required=True)
    # sqlalchemy_database_uri
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        db_user, db_pass, db_host, db_port, db_name
    )

settings = DBConfig.load()
