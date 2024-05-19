from unittest import TestCase  # add_test_data_to_db
from flask import url_for
from src import create_app, socketio, db
from src.models import User
from config import TestConfig
from src.test_data import add_test_user_to_db


class BasicTest(TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app = testApp.test_client()
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        add_test_user_to_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_user_to_db(self):

        dbUser = User.query.filter_by(username='wesdutton').first()

        self.assertIsNotNone(dbUser)


        self.assertEqual(dbUser.username, 'wesdutton')
        self.assertEqual(dbUser.password, 'pleasework')
        self.assertEqual(dbUser.email, 'wes@hotmail.com')
        self.assertEqual(dbUser.role, 'student')
        self.assertTrue(dbUser.email_verified)

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_contact(self):
        response = self.app.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact', response.data)


# This page includes code generated with the assistance of git-hub copilot & ChatGTP

# **Citation:** ChatGPT, OpenAI, 2024.
