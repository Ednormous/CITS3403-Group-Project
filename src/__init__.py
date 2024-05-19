### This file is the entry point of the application. It initialises the Flask app and the database.

from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config



db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
socketio = SocketIO()


def create_app(config):
    global s
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    

    from src.blueprints import main
    app.register_blueprint(main)
    

    return app

@login_manager.user_loader
def load_user(id):
    from src.models import User, Message
    return User.query.get(int(id))

from src import models #removed routes & added to blueprints.py



# This page includes code generated with the assistance of git-hub copilot & ChatGTP 

# **Citation:** ChatGPT, OpenAI, 2024.