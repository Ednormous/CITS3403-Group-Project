### Specifies the routes for the application

from src import app
from flask import render_template

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
@app.route('/index')
def login():
    return render_template('index.html')

# Register page
@app.route('/register')
def register():
    return render_template('register.html')

# Forgot password page
@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')