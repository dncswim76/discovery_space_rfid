from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

# instantiate app
app = Flask(__name__)
# load configuration settings
app.config.from_object('config')
# initialize database
db = SQLAlchemy(app)
# initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)

from app import views, models
