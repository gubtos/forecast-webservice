from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from vision_app.config import DATABASE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)
db.app = app

from .vision_app.models import City

db.create_all()

from .vision_app import urls


