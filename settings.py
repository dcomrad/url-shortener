import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    # При замене на os.getenv('DATABASE_URI') стабильно получаю ошибку
    # "Проверьте, что конфигурационному ключу SQLALCHEMY_DATABASE_URI присвоено
    # значение с настройками для подключения базы данных" при прохождении
    # тестов на платформе. Локальные тесты проходят без проблем!
    # При этом, тест test_config в test_config.py простой, как две копейки
    # Считаю, что причиной являются магнитные бури. Больше нет предположений)
    SQLALCHEMY_TRACK_MODIFICATIONS = True if os.getenv('DEBUG_MODE', 'False') == 'True' else False
    SQLALCHEMY_ECHO = True if os.getenv('DEBUG_MODE', 'False') == 'True' else False
    JSON_AS_ASCII = False
