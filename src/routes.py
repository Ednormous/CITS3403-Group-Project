# Specifies the routes for the application

from src.models import Message
from src import app, db, socketio
from flask_login import current_user, login_required
from flask import request, jsonify, abort
from flask import request, render_template, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message
from flask_socketio import emit
from src import app, db, socketio, mail, s
from src.models import User, Message
from datetime import datetime
from webforms import searchForm

# Homepage


@app.route('/')
def home():
    return render_template('homepage.html')

# About page


@app.route('/about')
def about():
    return render_template('about.html')

# Contact page


@app.route('/contact')
def contact():
    return render_template('contact.html')

# Login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Extract credentials from form data
        username = request.form['username']
        password = request.form['password']

        print(password)
        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        # If credentials are correct, then redirect
        if user and check_password_hash(user.password, password):
            login_user(user)
            print("user role is: ", user.role)

            # Role == admin
            if user.role == 'admin':
                flash('Login successful.', category='success')
                return redirect(url_for('admin'))

            # Role == tutor
            elif user.role == 'tutor':
                flash('Login successful.', category='success')
                return redirect(url_for('tutor', username=user.username))

            # Role == student
            elif user.role == 'student':
                flash('Login successful.', category='success')
                # print("user name is: ", user.username)
                return redirect(url_for('student', username=user.username))

            # Unassigned Role
            else:
                # Redirect to another page if the user is not a student
                flash('Login successful.', category='success')
                return redirect(url_for('dummy_login'))
        else:
            # Message to indicate user has incorrect credentials
            flash('Login failed. Please check your credentials and try again.')
            return redirect(url_for('login'))
    else:
        # GET request, show the login page
        return render_template('index.html')

# Register page


@app.route('/register', methods=['GET', 'POST'])
def register():

    # If the user submits the form
    if request.method == 'POST':
        retrieved_username = request.form.get('username')
        retrieved_password = request.form.get('password')
        retrieved_email = request.form.get('email')
        # retrieved_first_name = request.form.get('firstname')
        # retrieved_last_name = request.form.get('lastname')

        existing_user = User.query.filter_by(
            username=retrieved_username).first()
        if existing_user:
            # Indicates that the username already exists
            flash('Username already exists. Please choose a different one.',
                  category='error')
        else:
            # Check if the email's domain is 'amazingEdu.com.au'
            domain = retrieved_email.split('@')[-1]
            print("detected domainn is: ", domain)
            if domain == '123.com':  # TODO Make this editable via the admin page
                r_role = 'tutor'
            else:
                r_role = 'student'

            user = User(username=retrieved_username, password=generate_password_hash(
                retrieved_password), email=retrieved_email, role=r_role)
            db.session.add(user)
            db.session.commit()

            # userDetail = user_detail(user_id=user.id, firstName=retrieved_first_name, lastName=retrieved_last_name)
            # db.session.add(userDetail)
            # db.session.commit()

            # Indicates regisration was successful
            flash('Registration successful.', category='success')
            return redirect(url_for('login'))
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!! #
            # The following does not work

            # # Redirects user to login page
            # # TODO: Prompt user to verify their email address with a verification code
            # token = s.dumps(retrieved_email, salt='email-confirm-salt')
            # confirm_url = url_for('confirm_email', token=token, _external=True)

            # # Send email to user
            # msg = Message('Confirm your Email', recipients=[retrieved_email])
            # msg.body = f'Click the link to confirm your email: {confirm_url}'
            # try:
            #     mail.send(msg)
            #     flash('Please verify your account.', category='success')
            # except Exception as e:
            #     print(e)
            #     flash('Failed to send email. Please try again later.',
            #           category='error')
            #     return redirect(url_for('register'))
            # return redirect(url_for(confirm_email))

    flash('Please fill out the form.', category='error')
    return render_template('register.html')


# The following would probably not be implemented
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm-salt', max_age=3600)
        user = User.query.filter_by(email=email).first()
        user.email_verified = True
        db.session.commit()
        flash('Email confirmed.', category='success')
    except SignatureExpired:
        flash('The confirmation link has expired.', category='error')
    return redirect(url_for('login'))

# Forgot password page


@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')


@app.route('/dummy_login')
@login_required
def dummy_login():
    return render_template('dummy_login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/tutor/<username>')
@login_required
def tutor(username):
    if username != current_user.username and not current_user.is_admin:
        abort(403)
    return render_template('tutor.html', user=current_user)


@app.route('/admin')
@login_required
def admin():
    # Need to implement conditions to check if user is an admin
    if current_user.role == 'admin':
        print(User.role)
        # users = User.query.limit(10).all()
        users = User.query.all()
        return render_template('admin.html', users=users)
    else:
        flash("You do not have permission to view this page")
        return render_template('login')


@app.route('/student/<username>')
@login_required
def student(username):
    if username != current_user.username and not current_user.is_admin:
        abort(403)  # Forbidden access if not the user or not an admin
    return render_template('student.html', user=current_user)


@app.route('/create_user', methods=['POST'])
def create_user():
    if not current_user.is_authenticated or current_user.role != 'admin':
        # Only allow admins to access this route
        abort(403)

    r_username = request.form.get('username')
    # Default password is the username
    r_password = request.form.get('username')
    r_email = request.form.get('email')
    r_role = request.form.get('role')

    user = User(username=r_username, password=generate_password_hash(
        r_password), email=r_email, role=r_role)
    db.session.add(user)
    db.session.commit()

    flash('User created successfully.', category='success')
    return redirect(url_for('admin'))


# @app.route('/message_board')
# def message_board():
#     class_id = request.args.get('class_id')
#     if not class_id:
#         return "Class ID is required", 400  # Return an error or redirect as needed

#     # Assuming 'unit_id' in 'Message' corresponds to 'class_id'
#     messages = Message.query.filter_by(unit_id=class_id).all()

#     return render_template('message_board.html', messages=messages, class_id=class_id)

# from flask_login import current_user, login_required

@app.route('/message_board')
@login_required
def message_board():
    class_id = request.args.get('class_id')
    if not class_id:
        return "Class ID is required", 400

    messages = Message.query.filter_by(unit_id=class_id).all()

    return render_template('message_board.html', messages=messages, class_id=class_id, current_user=current_user)


#Pass information to nav-bar
@app.context_processor
def base():
    form = searchForm()
    return dict(form=form)

#Create search function
@app.route('/search', methods=['POST'])
def search():
   form = searchForm()
   messages = Message.query 
   if form.validate_on_submit():
        #Get data from submitted form
        Message.searched = form.searched.data
        #Query the database of messages
        messages = messages.filter(Message.label.like('%' + Message.searched + '%'))
        messages = messages.order_by(Message.timestamp).all()

        return render_template('search.html', 
                               form=form, 
                               searched=Message.searched,
                               messages=messages)  
   


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/timetable')
@login_required
def timetable():
    return render_template('timetable.html')


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.route('/forums')
@login_required
def forums():
    return render_template('forums.html')

# Event handler for posting a message, broadcasts message details to connected clients


@socketio.on('post_message')
def handle_message(data):
    if not current_user.is_authenticated:
        emit('error', {'error': 'User not authenticated'})
        return False

    user_id = current_user.id
    text = data['text']
    parent_id = data.get('parent_id')
    message_label = data['message_label']
    unitCode = data['unitCode']

    try:
        # Create a new message and add to DB
        new_message = Message(user_id=user_id, content=text,
                              timestamp=datetime.utcnow(),
                              parent_id=parent_id,
                              image_url=None,
                              label=message_label,
                              unit_id=unitCode)
        db.session.add(new_message)
        db.session.commit()
        # emit new message event
        emit('new_message', {
            'message_id': new_message.id,
            'text': text,
            'label': message_label,
            'parent_id': parent_id,
            'user_id': user_id,
            'username': current_user.username
        }, broadcast=True)
    except Exception as e:
        # roll back if error
        db.session.rollback()
        emit('error', {'error': str(e)})


# handler for Delete message event, using message id by broadcasting to clients and deleting if parameters met
@socketio.on('delete_message')
def handle_delete_message(data):
    message_id = data.get('message_id')
    message = Message.query.get(message_id)

    if not message:
        emit('error', {'error': 'Message not found'})
        return
    # only user and admin can delete message
    if message.user_id != current_user.id and current_user.role != 'admin':
        emit('error', {'error': 'Unauthorized'})
        return

    try:
        db.session.delete(message)
        db.session.commit()
        emit('message_deleted', {'message_id': message_id}, broadcast=True)
    except Exception as e:
        db.session.rollback()
        emit('error', {'error': str(e)})
