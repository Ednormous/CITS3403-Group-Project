### This file is used to run the application ###

# Imports the flask app instance from _init_.py in the src folder
from src import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True)
