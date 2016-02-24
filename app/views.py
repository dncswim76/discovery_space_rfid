from app import app, login_manager
from flask import flash, g, redirect, render_template, request, session, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User


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
        # get user
        user = User.query.get(
                    User.username == form.username)
        if user and user.check_password(form.password):
            login_user(user)
            flask.flash('Successfully logged in.')
            # get the next url
            next = flask.request.args.get('next')
            # check if user has permission to view next url
            if not next_is_valid(next):
                return flask.abort(400)
            
            # redirect to appropriate view
            return flask.redirect(next or url_for('home'))
        else:
            flash("Invalid username and password combination.")
            return redirect(url_for('home'))
    
    # render login page if not valid POST data
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    ''' User logout page.'''
    
    logout_user()
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id) 
