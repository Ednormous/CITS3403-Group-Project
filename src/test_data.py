from src import db
from src.models import *

wes = User(username='wesdutton', password='pleasework')

def add_test_user_to_db():
    db.session.add(wes)
    db.session.commit()