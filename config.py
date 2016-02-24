''' Configuration variables specific to application.'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.getenv("SECRET_KEY", "local-key")
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "discovery_rfid.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = True
