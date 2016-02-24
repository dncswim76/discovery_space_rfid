from app import db
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    ''' User model.'''

    __tablename__ = 'admin_user'
    
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(120))
    authenticated = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    @property
    def is_active(self):
        ''' Admin user is implicitly active.'''
        return True

    @property
    def is_authenticated(self):
        ''' Return True is user is authenticated.'''
        return self.authenticated

    @property
    def is_anonymous(self):
        ''' Return False as anonymous users are not supported.'''
        return False

    def get_id(self):
        ''' Return user id.'''
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.username
