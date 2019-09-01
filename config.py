import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRT_ENABLED = True
    SECRTE_KEY = ''
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_USER = 'xxx'
    SQLALCHEMY_PASSWORD = 'xxx'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://%s:%s@localhost/wordcount_dev" % (SQLALCHEMY_USER,SQLALCHEMY_PASSWORD)
    
class ProductionConfig(Config):
    pass

class StagingConfig(Config):
    DEBUG = True 
    DEVELOPMENT = True 

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

