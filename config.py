import os
import urllib
from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY='Clave_Nueva'
    SESSION_COOKIE_SECURE=False
    

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URL='mysql+pymysql://javier:root@localhost/bdidgs803'