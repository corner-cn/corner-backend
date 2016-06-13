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

    log_level = environ_setting("LOG_LEVEL", 'DEBUG', required=False)

    # secret_key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SESSION_COOKIE_SECURE = True
    # session_cookie_secure = True

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
