### Creating the database models for the application

from src import db
from flask_login import UserMixin

# Creating table for database

# User table to store the user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    role = db.Column(db.String(20), nullable=False)
    
#A role table to store the roles of the users
class Role(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)