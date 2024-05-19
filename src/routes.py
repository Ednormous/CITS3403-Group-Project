# Specifies the routes for the mainlication

from sqlite3 import Timestamp
from src.models import Message
from src import socketio, db
from flask_login import current_user, login_required
from flask import request, jsonify, abort
from flask import request, render_template, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message
from flask_socketio import emit
from src.blueprints import main
from src.models import User, Message, Units
from datetime import datetime
from webforms import searchForm, loginForm, registerForm

# Homepage


@main.route('/')
def home():
    return render_template('homepage.html')

# About page


@main.route('/about')
def about():
    return render_template('about.html')

# Contact page


@main.route('/contact')
def contact():
    return render_template('contact.html')

# Login page


@main.route('/login', methods=['GET', 'POST'])
def login():

    form = loginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data

        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        if not user:
            user = User.query.filter_by(email=username).first()

        # If credentials are correct, then redirect
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('Login successful.', 'success')

            # Role == admin
            if user.role == 'admin':
                #flash('Login successful.', category='success')
                return redirect(url_for('main.admin'))

            # Role == tutor
            elif user.role == 'tutor':
                #flash('Login successful.', category='success')
                return redirect(url_for('main.tutor', username=user.username))

            # Role == student
            elif user.role == 'student':

                # print("user name is: ", user.username)
                return redirect(url_for('main.student', username=user.username))

            # Unassigned Role
            else:
                # Redirect to another page if the user is not a student

                return redirect(url_for('main.dummy_login'))
        else:
            # Message to indicate user has incorrect credentials
            flash(f'Login failed. Please check your credentials and try again.', 'error')
            return redirect(url_for('main.login'))
    else:
        # GET request, show the login page
        return render_template('login.html', form=form)

# Register page


@main.route('/register', methods=['GET', 'POST'])
def register():

    form = registerForm()

    # If the user submits the form
    if form.validate_on_submit():
        retrieved_username = form.username.data
        retrieved_password = form.password.data
        retrieved_email = form.email.data

        existing_user = User.query.filter_by(
            username=retrieved_username).first()
        if existing_user:
            # Indicates that the username already exists
            flash(f'Username already exists. Please choose a different one.', 'error')
        else:
            # Check if the email's domain is 'amazingEdu.com.au'
            domain = retrieved_email.split('@')[-1]
            print("detected domainn is: ", domain)
            if domain == 'tuitiontalks.com':  # TODO Make this editable via the admin page
                r_role = 'admin'
            else:
                r_role = 'student'

            user = User(username=retrieved_username, password=generate_password_hash(
                retrieved_password), email=retrieved_email, role=r_role)
            db.session.add(user)
            db.session.commit()

            # Indicates regisration was successful
            flash('Registration successful.', category='success')
            return redirect(url_for('main.login'))
   
    #flash('Please fill out the form.', category='error')
    return render_template('register.html', form=form)



@main.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')

# Not yet implemented (future release)


@main.route('/dummy_login')
@login_required
def dummy_login():
    return render_template('dummy_login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@main.route('/tutor/<username>')
@login_required
def tutor(username):
    if username != current_user.username and not current_user.is_admin:
        abort(403)
    return render_template('tutor.html', user=current_user)


@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role != 'admin':
        flash("You do not have permission to view this page", 'error')
        return redirect(url_for('main.login'))

    # Get search parameters from the request
    search_id = request.args.get('search_id')
    search_username = request.args.get('search_username')
    search_email = request.args.get('search_email')
    search_role = request.args.get('search_role')

    # Start with all users
    users = User.query

    # Filter based on search parameters
    if search_id:
        users = users.filter(User.id == search_id)
    if search_username:
        users = users.filter(User.username.like(f"%{search_username}%"))
    if search_email:
        users = users.filter(User.email.like(f"%{search_email}%"))
    if search_role:
        users = users.filter(User.role.like(f"%{search_role}%"))

    units = Units.query.all()
    users = users.all()

    return render_template('admin.html', users=users, units=units)

# The following code is generated by ChatGPT entirely >>>


@main.route('/admin_search')
@login_required
def admin_search():
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorised"}), 403

    search_id = request.args.get('id', '')
    search_username = request.args.get('username', '')
    search_email = request.args.get('email', '')
    search_role = request.args.get('role', '')

    users = User.query

    if search_id:
        users = users.filter(User.id.like(f"%{search_id}%"))
    if search_username:
        users = users.filter(User.username.like(f"%{search_username}%"))
    if search_email:
        users = users.filter(User.email.like(f"%{search_email}%"))
    if search_role:
        users = users.filter(User.role.like(f"%{search_role}%"))

    users = users.all()

    users_list = [{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    } for user in users]

    return jsonify({"users": users_list})

# The above is generated by ChatGPT entirely <<<


@main.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        # Only allow admins to delete users
        abort(403)

    user = User.query.get(user_id)

    if user and user.role == 'admin':
        flash('Cannot delete admin user.', category='error')
        return redirect(url_for('main.admin'))
    if user:
        # Check if the user has posted any messages
        messages = Message.query.filter_by(user_id=user.id).all()
        if messages:
            # Update user details to indicate the user has been deleted
            user.username = f'deleted_user_{user.id}'
            user.email = f'deleted_{user.id}@deleted.com'
            user.password = generate_password_hash(
                'placeholder')  # reset password
            user.role = 'deleted'  # change role
        else:
            # If the user has no messages, delete the user
            db.session.delete(user)

        db.session.commit()
        flash('User deleted successfully.', category='success')
    else:
        flash('User not found.', category='error')

    return redirect(url_for('main.admin'))


@main.route('/edit_user/<int:user_id>', methods=['GET'])
@login_required
def edit_user(user_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        # Only allow admins to access this route
        abort(403)

    user = User.query.get(user_id)
    if user:
        return render_template('edit_user.html', user=user)
    else:
        flash('User not found.', category='error')
        return redirect(url_for('main.admin'))


@main.route('/update_user/<int:user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        # Only allow admins to access this route
        abort(403)

    user = User.query.get(user_id)
    if user:
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        db.session.commit()
        flash('User updated successfully.', category='success')
    else:
        flash('User not found.', category='error')

    return redirect(url_for('main.admin'))


@main.route('/create_unit', methods=['POST'])
@login_required
def create_unit():
    if current_user.role != 'admin':
        flash("You do not have permission to perform this action", 'error')
        return redirect(url_for('main.admin'))

    unit_name = request.form.get('unit_name')
    tutor_id = request.form.get('tutor_id')
    timetable = request.form.get('timetable')
    enrollments = request.form.get('enrollments')

    new_unit = Units(unit_name=unit_name, tutor_id=tutor_id,
                     timetable=timetable, enrollments=enrollments)
    db.session.add(new_unit)
    db.session.commit()

    flash('Unit created successfully.', 'success')
    return redirect(url_for('main.admin'))


@main.route('/delete_unit/<int:unit_id>', methods=['POST'])
@login_required
def delete_unit(unit_id):
    unit = Units.query.get_or_404(unit_id)
    db.session.delete(unit)
    db.session.commit()

    flash('Unit deleted successfully.', 'success')
    return redirect(url_for('main.admin'))


@main.route('/student/<username>')
@login_required
def student(username):
    if username != current_user.username and not current_user.is_admin:
        abort(403)  # Forbidden access if not the user or not an admin
    return render_template('student.html', user=current_user)


@main.route('/create_user', methods=['POST'])
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
    return redirect(url_for('main.admin'))


@main.route('/message_board')
@login_required
def message_board():
    class_id = request.args.get('class_id')
    if not class_id:
        return "Class ID is required", 400

    messages = Message.query.filter_by(unit_id=class_id).all()

    return render_template('message_board.html', messages=messages, class_id=class_id, current_user=current_user)

# Pass information to nav-bar


@main.context_processor
def base():
    form = searchForm()
    return dict(form=form)

# Create search function


@main.route('/search', methods=['POST'])
def search():
   #Extract form data
   form = searchForm()
   messages = Message.query
   if form.validate_on_submit():
        #Get data from submitted form
        Message.searched = form.searched.data
        # Query the database of messages
        messages = messages.filter(
            Message.label.like('%' + Message.searched + '%'))
        messages = messages.order_by(Message.timestamp).all()

        return render_template('search.html',
                               form=form,
                               searched=Message.searched,
                               messages=messages)
   
   messages = messages
   #if form not validated, return search page.
   return render_template('search.html', form=form, messages=messages)


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@main.route('/timetable')
@login_required
def timetable():
    return render_template('timetable.html')


@main.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@main.route('/forums')
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


# This page includes code generated with the assistance of git-hub copilot & ChatGTP

# **Citation:** ChatGPT, OpenAI, 2024.
