### This file is the entry point of the application. It initialises the Flask app and the database.

from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from .database import db
from flask_migrate import Migrate
from config import Config

# Email Verification Imports
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


app = Flask(__name__)
app.config.from_object(Config)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#app.config['SECRET_KEY'] = 'we_love_writing_programs_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'


login_manager.init_app(app)

socketio = SocketIO(app)

# Initialise the mail
mail = Mail(app)

# Flask mail configuration
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'cits3403_bot@yahoo.com'
app.config['MAIL_PASSWORD'] = "It's so hard to think of a password"

## SendGrid Recovery code: NZU5JRJX3FKT2GKYC9ZDPPNJ

s = URLSafeTimedSerializer(app.config['SECRET_KEY'] )

db.init_app(app)
#migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(id):
    from src.models import User, Message
    return User.query.get(int(id))

from src import models, routes