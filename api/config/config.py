import os
from decouple import config 
from datetime import timedelta


BASE_DIRECTORY= os.path.dirname(os.path.realpath(__file__))
uri = config('DATABASE_URL')
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
class Config:
    SECRET_KEY = config('SECRET_KEY',"secret")
    SQLALCHEMY_TRACK_MODICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=365)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access','refresh']
    JWT_SECRET_KEY= config('JWT_SECRET_KEY')
    DEBUG =True

                           
class Dev (Config):
    Debug = config('DEBUG',cast = bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIRECTORY,'db.sqlite3')
class Prod (Config):
    Debug = config('DEBUG',cast = bool)
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODICATIONS = False
    # postgres://url_shortner_sn7w_user:aU0t8ENtxLdGBmyhGtEWfn8ASuiaOZri@dpg-cid8sflgkuvncfcha5vg-a.oregon-postgres.render.com/url_shortner_sn7w

class Test (Config):
    Testing = True
    DEBUG = config('DEBUG',cast = bool)
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_ECHO = True
    


config_dict = {
    'dev':Dev,
    'prod':Prod,
    'test':Test
}