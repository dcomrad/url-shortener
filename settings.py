import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True if os.getenv('DEBUG_MODE', 'False') == 'True' else False
    SQLALCHEMY_ECHO = True if os.getenv('DEBUG_MODE', 'False') == 'True' else False
    JSON_AS_ASCII = False
