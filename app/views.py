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

    # Get list of all games of type challenge
    games = Game.query.join(GameMode).filter(
                GameMode.mode == "challenge").order_by('title')
    return render_template('challenge.html', games=games)


@app.route('/games/challenge/<int:game_id>')
def challenge_game(game_id):
    ''' Format for challenge games.'''

    return "Hello, World"


@app.route('/games/manage', methods=['GET', 'POST'])
@login_required
def manage_games():
    ''' Links for admins to create, edit or delete games.'''
    
    # if POST request, handle changes
    if request.method == "POST":
        # if a game is to be deleted, get id of game
        if "the_game" in request.form:
            game_id = request.form.get('game_id', type=int)
            game = Game.query.get(game_id)
            title = game.title
            # delete associated game
            db.session.delete(game)
            db.session.commit()
            # report that game was deleted and reload page
            flash(u'Successfully deleted %s.' % game.title)
            return redirect(url_for('manage_games'))
        # if a game is to be created, make a new game and redirect to its page
        elif "create" in request.form:
            game = Game(title="Default", description="default", game_mode=None)
            db.session.add(game)
            db.session.commit()
            # redirect to game's edit page
            return redirect(url_for('edit_game', game_id=game.id))
    # otherwise, get data for template
    else:
        # list all learning games first
        learning_games = Game.query.join(GameMode).filter(
                GameMode.mode == "learning").order_by('title')
        challenge_games = Game.query.join(GameMode).filter(
                GameMode.mode == "challenge").order_by('title')
        return render_template('manage_games.html',
                learning_games=learning_games,
                challenge_games=challenge_games)


@app.route('/games/manage/<int:game_id>')
@login_required
def edit_game(game_id):
    ''' Interface for admin to create or edit games.'''

    return "Hello, World"
