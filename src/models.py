# Creating the database models for the application
from src import db
from flask_login import UserMixin
from datetime import datetime
# Creating table for database

# User table to store the user information


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    role = db.Column(db.String(20), nullable=False)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)


class Units(db.Model):
    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(100), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timetable = db.Column(db.String(255), nullable=True)
    enrollments = db.Column(db.Text, nullable=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey(
        'message.id'), nullable=True)
    image_url = db.Column(db.String, nullable=True)
    label = db.Column(db.Text, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'))

    # reference to the User Class
    user = db.relationship('User', backref='messages')
    replies = db.relationship('Message', backref=db.backref(
        'parent', remote_side=[id]), lazy='dynamic')

    def __repr__(self):
        return f'<Message "{self.content}" by User ID {self.user_id}>'

# This page includes code generated with the assistance of git-hub copilot & ChatGTP

# **Citation:** ChatGPT, OpenAI, 2024.
