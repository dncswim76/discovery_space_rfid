import os
from app import app, db, login_manager
from datetime import datetime
from flask import flash, g, jsonify, redirect, render_template, request, session, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from sqlalchemy import text
from werkzeug import secure_filename

from .forms import LoginForm
from .models import Device, Game, game_device_link, GameMode, Member, MemberVisit, Question, question_answer_link, User
from .utils import allowed_file, media_type


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


# AJAX
@app.route('/_validate_learning_tag')
def validate_learning_tag():
    ''' JSON view to check if scanned RFID tag is valid
        tag for learning mode game.'''

    # Get tag and game id from request
    tag = request.args.get('tag', 0, type=str)
    game_id = request.args.get('game_id', 0, type=int)

    # Check if RFID tag is associated with game
    device = Device.query.join(Game.devices).filter(
                    Game.id == game_id).filter(
                    Device.rfid_tag == tag).first()

    # If device exists, return JSON
    if device:
        return jsonify(valid="true",
                       device__name=device.name,
                       device__description=device.description,
                       file_loc="/static/media/" + device.file_loc,
                       media=media_type(device.file_loc.split('.')[-1]))
    # Otherwise, return None
    else:
        return jsonify(valid="false")


#AJAX
@app.route('/_validate_challenge_tag')
def validate_challenge_tag():
    ''' JSON view to check if scanned RFID tag answers question
        to challenge mode game.'''

    # Get tag, game id, and question_id from request
    tag = request.args.get('tag', 0, type=str)
    game_id = request.args.get('game_id', 0, type=int)
    question_id = request.args.get('question_id', 0, type=int)

    # Make sure question corresponds to game
    if Question.query.get(question_id).game != game_id:
        return jsonify(valid="false")

    # Check if RFID tag answers question
    device = Device.query.join(Question.answers).filter(
                Question.id == question_id).filter(
                Device.rfid_tag == tag).first()
   
    # If device exists, return JSON
    if device:
        return jsonify(valid="true",
                       device__name=device.name,
                       device__description=device.description,
                       file_loc="/static/media/" + device.file_loc,
                       media=media_type(device.file_loc.split('.')[-1]))
    # Otherwise, return None
    else:
        return jsonify(valid="false")

    
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

    # Get game
    game = Game.query.get_or_404(game_id)

    # If game is of incorrect mode, return to games page
    if GameMode.query.get(game.game_mode).mode != "learning":
        flash(u'%s is not a learning mode game.' % game.title)
        return redirect(url_for('games'))
    
    return render_template('learning_game.html', game=game)


@app.route('/games/challenge')
def challenge():
    ''' Listing of challenge games.'''

    # Get list of all games of type challenge
    games = Game.query.join(GameMode).filter(
                GameMode.mode == "challenge").order_by('title')
    return render_template('challenge.html', games=games)


@app.route('/games/challenge/<int:game_id>', methods=['GET', 'POST'])
def challenge_game(game_id):
    ''' Format for challenge games.'''

    # Get game
    game = Game.query.get_or_404(game_id)

    # POST moves to next or previous question
    if request.method == "POST":
        # Increment question id
        if "next_question" in request.form:
            session['question'] += 1
            return redirect(url_for('challenge_game', game_id=game_id))
        # Decrement question id
        elif "previous_question" in request.form:
            session['question'] -= 1
            return redirect(url_for('challenge_game', game_id=game_id))
        # If they are finished, remove session variables
        elif "finish" in request.form:
            session.pop('challenge_id', None)
            session.pop('question', None)
            return redirect(url_for('games'))
    else:
        # If game is of incorrect mode, return to games page
        if GameMode.query.get(game.game_mode).mode != "challenge":
            flash(u'%s is not a challenge mode game.' % game.title)
            return redirect(url_for('games'))

        # Check that session variable corresponds to correct challenge game
        game_check = 'challenge_id' in session and game_id == session['challenge_id']
        # If session variable for game is correct and session contains a question, try to get question
        if game_check and 'question' in session:
            # Try to get valid question
            try:
                question = Question.query.join(Game).filter(
                            Game.id == game_id).order_by('id')[session['question']]
            # Otherwise, get first question and reset session variable
            except:
                question = Question.query.join(Game).order_by('id').first()
                session['question'] = 0
        # Otherwise, add variables to session and get first question
        else:
            question = Question.query.join(Game).order_by('id').first()
            session['question'] = 0
            session['challenge_id'] = game_id
        
        # Determine minimum and maximum question id
        questions = Question.query.join(Game).filter(
                            Game.id == game_id).order_by(Question.id)

        # Pass game and question to template
        return render_template('challenge_game.html',
                    game=game,
                    question=question,
                    min_id=questions[0].id,
                    max_id=questions[-1].id)


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
            flash(u'Successfully deleted %s.' % title)
            return redirect(url_for('manage_games'))
        # if a game is to be created, make a new game and redirect to its page
        elif "create" in request.form:
            # default to first game mode
            game_mode = GameMode.query.all()[0].id
            game = Game(title="Default", description="default", game_mode=game_mode)
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


@app.route('/games/manage/<int:game_id>', methods=['GET', 'POST'])
@login_required
def edit_game(game_id):
    ''' Interface for admin to create or edit games.'''

    # if POST, handle edits
    if request.method == "POST":
        # Get game it exists
        game = Game.query.get_or_404(game_id)
        game_mode = GameMode.query.get_or_404(game.game_mode)
        # Check if game attribtues need to be changed
        if "edit_game" in request.form:
            edit = True
            # Check if title needs to be changed
            title = request.form.get('game_title', type=str)
            if not title:
                edit = False
                flash(u'Invalid title.')
            # Check if description needs to changed
            description = request.form.get('game_description', type=str)
            if not description:
                edit = False
                flash(u'Invalid description.')
            # Check if game mode needs to be changed
            mode = request.form.get('mode', type=int)
            # if new mode is present in request, update game mode
            if not mode:
                edit = False
                flash(u'Invalid game mode selected.')
            # if we can edit, apply changes
            if edit:
                game.title = title
                game.description = description
                game_mode = GameMode.query.get(mode)
                game.game_mode = game_mode.id
                db.session.commit()

        # Handle adding RFID
        elif "add_rfid" in request.form:
            # Make sure a valid name is entered
            name = request.form.get('device_name', type=str)
            if not name:
                flash(u'Invalid device name.')
                return redirect(url_for('edit_game', game_id=game_id))
            # Make sure a valid description is entered
            description = request.form.get('device_description', type=str)
            if not description:
                flash(u'Invalid device description.')
                return redirect(url_for('edit_game', game_id=game_id))
            # Make sure valid RFID tag is entered
            tag = request.form.get('device_tag', type=str)
            if not tag:
                flash(u'Invalid rfid tag.')
                return redirect(url_for('edit_game', game_id=game_id))
            # Get file to upload
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_loc)
            else:
                flash(u'Invalid file.')
                return redirect(url_for('edit_game', game_id=game_id))
            # Now that everything is good, create Device and link it
            device = Device(name=name, description=description, rfid_tag=tag, file_loc=filename)
            db.session.add(device)
            db.session.commit()
            # Add entry to linking table
            device_link = game_device_link.insert().values(game_id=game_id, device_id=device.id)
            db.session.execute(device_link)
            db.session.commit()

        # Handle deleting RFID and associated media
        elif "the_device" in request.form:
            # Get rfid to delete
            device_id = request.form.get('device_id', type=int)
            device = Device.query.get(device_id)
            device_name = device.name
            # get file location to delete
            filename = os.path.join(app.config['UPLOAD_FOLDER'], device.file_loc)
            # try to delete file
            try:
                os.remove(filename)
            except OSError:
                flash(u'File %s does not exist.' % device.file_loc)
            # Delete rfid
            db.session.delete(device)
            db.session.commit()
            flash(u'Successfully deleted %s.' % device_name)

        # Handle adding new Question and associated answers
        elif "add_question" in request.form:
            # Get question prompt and create Question
            question_text = request.form.get('question_text', type=str)
            q = Question(question=question_text, game=game_id)
            db.session.add(q)
            # Get answers to question
            answers = request.form.getlist('answers')
            # Return an error if no answers are selected
            if not answers:
                flash(u'Question must have at least one answer.')
                return redirect(url_for('edit_game', game_id=game_id))
            # Otherwise, create question and link answers
            else:
                db.session.commit()
                for answer in answers:
                    answer_link = question_answer_link.insert().values(question_id=q.id, device_id=answer)
                    db.session.execute(answer_link)
                    db.session.commit()
        
        # Handle deleting Question and associated answers
        elif "the_question" in request.form:
            # Get question to delete
            question_id = request.form.get('question_id', type=int)
            question = Question.query.get(question_id)
            question_name = question.question
            # Delete question
            db.session.delete(question)
            db.session.commit()
            flash(u'Successfully deleted %s.' % question_name)

        # if we get here, render GET request
        return redirect(url_for('edit_game', game_id=game_id))

    # otherwise, GET data for template
    else:
        # Get Game and GameMode
        game = Game.query.get(game_id)
        current_mode = GameMode.query.get(game.game_mode)
        # Get all game modes
        game_modes = GameMode.query.order_by('mode').all()
        # Get all RFIDs associated with game
        devices = Device.query.join(Game.devices).filter(
                    Game.id == game_id).all()
        # if game is of type challenge, get questions and answers
        questions = None
        answers = []
        if current_mode.mode == "challenge":
            # Get all Questions associated with game
            questions = Question.query.join(Game).filter(
                    Game.id == game_id).order_by('question')
            # Get answers for each question
            for question in questions:
                answers.append(Device.query.join(Question.answers).filter(
                                    Question.id == question.id).all())
        # Render template with attributes
        return render_template('edit_games.html',
                    game=game,
                    current_mode=current_mode,
                    game_modes=game_modes,
                    devices=devices,
                    questions=questions,
                    answers=answers)


@app.route('/members', methods=['GET', 'POST'])
def members():
    ''' Track member visits to Discovery Space.'''

    if request.method == "POST":
        # Check that tag belongs to active member
        if "member_tag" in request.form:
            member_tag = request.form.get('member_tag', type=str)
            # Get member corresponding to tag or None
            member = Member.query.filter(
                        Member.card_number == member_tag).first()
            # If active member, increment visits and redirect to member page
            if member:
                visit = MemberVisit(member=member.id, date=datetime.now())
                # Commit visit
                db.session.add(visit)
                db.session.commit()
                # Redirect home if an administrator is not logged in
                if session['authenticated']:
                    return redirect(url_for('member_info', member_id=member.id))
                else:
                    flash(u'Thank you for visiting!')
                    return redirect(url_for('home'))
            # Otherwise, report that tag does not belong to active member
            else:
                flash(u'Card does not correspond to active member. Select "Add \
                    Member" to add a new member.')
                return redirect(url_for('members'))
        # Create new member
        elif "new_member" in request.form:
            member = Member(
                        member_first_name="First Name",
                        member_last_name="Last Name",
                        card_number="Card Number")
            db.session.add(member)
            db.session.commit()
            # redirect to new member's page
            return redirect(url_for('member_info', member_id=member.id))
    # Render template on GET request
    else:
        return render_template('members.html')


@app.route('/members/<int:member_id>', methods=['GET', 'POST'])
def member_info(member_id):
    ''' View and edit member information.'''

    # Get member
    member = Member.query.get_or_404(member_id)

    if request.method == "POST":
        # Delete member
        if "the_member" in request.form:
            db.session.delete(member)
            db.session.commit()
            # Redirect to member page
            return redirect(url_for('members'))
    else:
        return render_template('member_info.html',
                    member=member)


@app.route('/manage_members', methods=['GET', 'POST'])
@login_required
def manage_members():
    ''' Admin interface for searching and editing members.'''

    if request.method == "POST":
        pass
    else:
        pass

