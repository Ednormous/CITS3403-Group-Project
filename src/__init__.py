### This file is the entry point of the application. It initialises the Flask app and the database.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .database import db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'we_love_writing_programs_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)

@login_manager.user_loader
def load_user(id):
    from src.models import User
    return User.query.get(int(id))

from src import routes

