from src import db
from src.models import *

wes = User(username='wesdutton', password='pleasework',email='wes@hotmail.com', role='student', email_verified=True)

def add_test_user_to_db():
    db.session.add(wes)
    db.session.commit()