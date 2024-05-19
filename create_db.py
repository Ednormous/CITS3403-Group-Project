### This script creates the database and the admin user. ###

from src import db, app
from src.models import User, Role

# Create the database
with app.app_context():
    db.create_all()

# Create the admin user
    existing_user = User.query.filter_by(username='admin').first()
    # delete the account
    if existing_user:
        db.session.delete(existing_user)

    admin = User(username='admin', password='admin', email='', role='admin')
    db.session.add(admin)
    db.session.commit()


# This page includes code generated with the assistance of git-hub copilot & ChatGTP

# **Citation:** ChatGPT, OpenAI, 2024.
