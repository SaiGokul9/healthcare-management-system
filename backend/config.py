import os

class Config(object):
    SECRET_KEY = 'sasds9wn'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = "mysql://root:passwd1@localhost:3306/HMS_DBMS"
    # if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    #     SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
    #         "postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    CORS_HEADERS = 'Content-Type'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')