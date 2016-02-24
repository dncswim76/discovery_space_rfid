from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy


# instantiate app
app = Flask(__name__)
# load configuration settings
app.config.from_object('config')
# initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
# initialize manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app import views, models
