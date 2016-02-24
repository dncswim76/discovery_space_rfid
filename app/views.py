from app import app
from flask import render_template

@app.route('/')
@app.route('/home')
def home():
    ''' Home page for application.'''

    return render_template('home.html')
