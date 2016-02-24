from flask.ext.wtf import Form
from wtforms import PasswordField, TextField
from wtforms.validators import DataRequired

class LoginForm(Form):
    ''' Form to log in users.'''

    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
