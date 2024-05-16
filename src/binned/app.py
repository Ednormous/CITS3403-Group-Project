### This file was originally the flask application. It is now split into smalled py files. 
### This file is retained in case the smaller files break. 

# from flask import Flask, render_template, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin


# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'we_love_writing_programs_123'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite' # Connects the database file to the app
# db = SQLAlchemy(app) # Creates the database instance

# # Creating table for database
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=True)
#     role = db.Column(db.String(20), nullable=False)
    
# class Role(db.Model): #A role table to store the roles of the users
#     id = db.Column(db.Integer, primary_key=True)
#     role = db.Column(db.String(20), nullable=False)

# # Create the database
# with app.app_context():
#     db.create_all()

#     existing_user = User.query.filter_by(username='admin').first()
#     if not existing_user:
#         admin = User(username='admin', password='admin', email='', role='admin')
#         db.session.add(admin)
#         db.session.commit()
#     else:
#         print('User already exists.')

# @app.route('/')
# def home():
#     return render_template('homepage.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# @app.route('/index')
# def login():
#     return render_template('login.html')

# @app.route('/register')
# def register():
#     return render_template('register.html')

# @app.route('/forgot-password')
# def forgot_password():
#     return render_template('forgot-password.html')

# if __name__ == '__main__':
#     app.run(debug=True)
