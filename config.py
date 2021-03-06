''' Configuration variables specific to application.'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'jpeg', 'gif', 'mp3', 'mp4'])
DEPLOY_DATE = "04/20/2016"
SECRET_KEY = os.getenv("SECRET_KEY", "local-key")
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "discovery_rfid.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = basedir + '/app/static/media/'
WTF_CSRF_ENABLED = True
