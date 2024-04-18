### Specifies the routes for the application

from flask import request, render_template, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import emit
from src import app, db, socketio
from src.models import User

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
                return redirect(url_for('tutor'))
            
            # Role == student
            elif user.role == 'student':
                flash('Login successful.', category='success')
                return redirect(url_for('student'))
            
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

        existing_user = User.query.filter_by(username=retrieved_username).first()
        if existing_user:
            # Indicates that the username already exists
            flash('Username already exists. Please choose a different one.', category='error')
        else:
            # Check if the email's domain is 'amazingEdu.com.au'
            domain = retrieved_email.split('@')[-1]
            print("detected domainn is: ", domain)
            if domain == '123.com':
                r_role = 'tutor'
            else:
                r_role = 'student' 

            user = User(username=retrieved_username, password=generate_password_hash(retrieved_password), email=retrieved_email, role = r_role)
            db.session.add(user)
            db.session.commit()

            # Indicates regisration was successful
            flash('Registration successful. Please log in.', category='success')

            # Redirects user to login page
            # TODO: Prompt user to verify their email address with a verification code
            return redirect(url_for('login'))
    return render_template('register.html')

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

@app.route('/tutor')
@login_required
def tutor():
    # Need to implement conditions to check if user is a tutor
    return render_template('tutor.html')

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
        return "You do not have permission to view this page"
    
@app.route('/student')
@login_required
def student():
    # Need to implement conditions to check if user is a student
    return render_template('student.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    if not current_user.is_authenticated or current_user.role != 'admin':
        # Only allow admins to access this route
        abort(403)

    r_username = request.form.get('username')
    r_password = request.form.get('username') # Default password is the username
    r_email = request.form.get('email')
    r_role = request.form.get('role')

    user = User(username=r_username, password=generate_password_hash(r_password), email=r_email, role=r_role)
    db.session.add(user)
    db.session.commit()

    flash('User created successfully.', category='success')
    return redirect(url_for('admin'))

@app.route('/message_board')
def message_board():
    return render_template('message_board.html')

@socketio.on('post_message')
def handle_message(json, methods=['GET', 'POST']):
    emit('new_message', json, broadcast=True)