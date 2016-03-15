from app import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    ''' User model.'''

    __tablename__ = 'admin_user'
    
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('Username', db.String(50), unique=True, nullable=False)
    password = db.Column('Password', db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    @property
    def is_active(self):
        ''' User is implicitly active.'''
        return True

    @property
    def is_authenticated(self):
        ''' Return True is user is authenticated.'''

        if 'authenticated' in session:
            return session['authenticated']
        else:
            return False

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


class GameMode(db.Model):
    ''' Game modes that application supports.

        Application currently supports
        "learning" and "challenge" mode.'''
    
    __tablename__ = 'game_modes'

    id = db.Column('id', db.Integer, primary_key=True)
    mode = db.Column('Mode', db.String(50))
    games = db.relationship('Game', backref='game_mode_id', lazy='dynamic')

    def __repr__(self):
        return self.mode


# A Game has many Devices and a Device can belong to many games, therefore
# we define the following helper table for this relationship.
game_device_link = db.Table('GameDeviceLink', 
            db.Column('id', db.Integer, primary_key=True),
            db.Column('game_id', db.Integer,
                    db.ForeignKey('games.id'), nullable=False),
            db.Column('device_id', db.Integer,
                    db.ForeignKey('devices.id'), nullable=False))

class Game(db.Model):
    ''' Represents a game that was created.'''

    __tablename__ = 'games'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('Title', db.String(50))
    description = db.Column('Description', db.Text)
    game_mode = db.Column('Mode', db.Integer, db.ForeignKey('game_modes.id'))
    questions = db.relationship('Question', backref='game_id', lazy='dynamic')
    devices = db.relationship('Device',
            secondary=game_device_link,
            backref='game',
            lazy='dynamic')

    def __repr__(self):
        return self.title


class Device(db.Model):
    ''' Object with an embedded RFID chip.

        Each objects points to a file on the 
        Raspberry Pi (/dev/null by default).'''

    __tablename__ = 'devices'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('Name', db.String(50))
    description = db.Column('Description', db.Text)
    rfid_tag = db.Column('Tag', db.String(50))
    file_loc = db.Column('FileLocation', db.Text, default='/dev/null')

    def __repr__(self):
        return self.name


# A Question can have many RFID tags as an answer and an RFID tag can be
# an answer to many Questions, so we define the following helper table.
question_answer_link = db.Table('QuestionAnswerLink', 
            db.Column('id', db.Integer, primary_key=True),
            db.Column('question_id', db.Integer,
                    db.ForeignKey('questions.id'), nullable=False),
            db.Column('device_id', db.Integer,
                    db.ForeignKey('devices.id'), nullable=False))


class Question(db.Model):
    ''' Certain game modes prompt for a specific set of RFID tags.

        Each Question is linked to the game that it belongs to.'''

    __tablename__ = 'questions'

    id = db.Column('id', db.Integer, primary_key=True)
    question = db.Column('Question', db.Text)
    game = db.Column('Game', db.Integer, db.ForeignKey('games.id'))
    answers = db.relationship('Device',
            secondary=question_answer_link,
            backref='question',
            lazy='dynamic')


class Member(db.Model):
    ''' RFID membership card for patrons.'''

    __tablename__ = 'members'

    id = db.Column('id', db.Integer, primary_key=True)
    member_first_name = db.Column('FirstName', db.String(50))
    member_last_name = db.Column('LastName', db.String(50))
    card_number = db.Column('CardNumber', db.String(50))
    visits = db.relationship('MemberVisit', backref='member_id', lazy='dynamic')

    def __repr__(self):
        return self.first_name + " " + self.last_name


class MemberVisit(db.Model):
    ''' Log of visits by member.'''

    __tablename__ = 'member_visits'

    id = db.Column('id', db.Integer, primary_key=True)
    member = db.Column('MemberID', db.Integer, db.ForeignKey('members.id'))
    date = db.Column('Date', db.DateTime)       
