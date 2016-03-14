from app import app, db, login_manager
from datetime import datetime
from flask import flash, g, redirect, render_template, request, session, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import Game, GameMode, User


@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/home')
def home():
    ''' Home page for application.'''

    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' User login page.'''

    # make sure that user is not already logged in
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home'))

    # instantiate LoginForm
    form = LoginForm()
    # process form submission on POST
    if form.validate_on_submit():
        flash(u'Successfully logged in as %s' % form.user.username)
        session['user_id'] = form.user.id
        session['authenticated'] = True
        # check if user has access to next url
        next = request.args.get('next')

        return redirect(next or url_for('home'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    ''' User logout page.'''
    
    logout_user()
    # pop session variables
    session.pop('user_id', None)
    session.pop('authenticated', None)
    flash(u'Successfully logged out.')
    return redirect(url_for('home'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/games')
def games():
    ''' Choose game mode or edit games if admin.'''
    
    return render_template('games.html')


@app.route('/games/learn')
def learn():
    ''' Listing of learning games.'''

    # Get list of all games of type learning
    games = Game.query.join(GameMode).filter(
                GameMode.mode == "learning").order_by('title')
    return render_template('learning.html', games=games)


@app.route('/games/learn/<int:game_id>')
def learning_game(game_id):
    ''' Format for learning games.'''

    return "Hello, World"


@app.route('/games/challenge')
def challenge():
    ''' Listing of challenge games.'''

    return "Hello, World"


@app.route('/games/challenge/<int:game_id>')
def challenge_game(game_id):
    ''' Format for challenge games.'''

    return "Hello, World"


@app.route('/games/manage', methods=['GET', 'POST'])
@login_required
def manage_games():
    ''' Interface for admins to edit games.'''

    return "Hello, World"
