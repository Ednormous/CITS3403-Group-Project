### Creating the database models for the application

from .database import db
from flask_login import UserMixin

# Creating table for database

# User table to store the user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    role = db.Column(db.String(20), nullable=False)

# Table to store classes
# class Class(db.Model):
#     class_id = db.Column(db.Integer, primary_key=True)
#     class_name = db.Column(db.String(100), nullable=False)
#     tutor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Table to store enrolments
# class Enrolment(db.Model):
#     enrolment_id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'), nullable=False)

# # Table to store posts
# class Communication(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'), nullable=False) # Reference to classes so that forums can be made independent
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text(2000), nullable=False) ### Limit the content to 2000 characters
#     date_posted = db.Column(db.DateTime, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Table to store timetables
# class Timetable(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     day = db.Column(db.String(20), nullable=False)
#     time = db.Column(db.String(20), nullable=False)
#     class_name = db.Column(db.String(100), nullable=False)
#     tutor = db.Column(db.String(100), nullable=False)

# TODO Create a View for users to individually view their own timetables