### This file is used to run the application ###

# Imports the flask app instance from _init_.py in the src folder
from flask_migrate import Migrate
from src import create_app, socketio, db
from config import DeploymentConfig

app = create_app(DeploymentConfig)
migrate = Migrate(app, db)

if __name__ == '__main__':
    socketio.run(app, debug=True)
