import os

WTF_I18N_ENABLED = False
DEBUG = True
threaded = True

SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'zlkt'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False
