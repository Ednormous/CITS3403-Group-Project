### This file is the entry point of the application. It initialises the Flask app and the database.

from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
#from .database import db ------------------------------------------------------------------------------------------
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
#from run import app #Unsure if this is currently needed?

# Email Verification Imports
# from flask_mail import Mail, Message
# from itsdangerous import URLSafeTimedSerializer, SignatureExpired


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
socketio = SocketIO()
# mail = Mail()
# s = None

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

# migrate = Migrate(app, db)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
#login_manager.init_app(app)


#app.config['SECRET_KEY'] = 'we_love_writing_programs_123'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
# mail.init_app(app)
    # s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    # app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USE_SSL'] = True
    # app.config['MAIL_USERNAME'] = 'cits3403_bot@yahoo.com'
    # app.config['MAIL_PASSWORD'] = "It's so hard to think of a password"



# socketio = SocketIO(app)

#db.init_app(app)------------------------------------------------------------------- Moved up to create_app
#migrate = Migrate(app, db) --------------------------------------------------------- Moved to run.py

