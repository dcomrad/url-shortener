import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import config

app_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, instance_path=app_dir)
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import api_views, error_handlers, views
