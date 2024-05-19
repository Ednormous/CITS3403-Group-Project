from unittest import TestCase  # add_test_data_to_db
from flask import url_for
from src import create_app, socketio, TestConfig, db, User
from src.test_data import add_test_user_to_db


class BasicTest(TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        add_test_user_to_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_user_to_db(self):
        s = User.query.get("wesdutton")
        self.assertTrue(s is not None)

    # each test must start with '`test'
    def test_password_hashing(self):
        s = User.query.get("wesdutton")
        s.set_password('pleasework')
        self.assertTrue(s.check_password('pleasework'))
        self.assertFalse(s.check_password('workplease'))


class FlaskTestCase(TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.socketio = socketio

    def tearDown(self):
        self.app_context.pop()

    def test_home_page(self):
        # Replace 'home' with your actual route name
        response = self.client.get(url_for('main.home'))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()


# This page includes code generated with the assistance of git-hub copilot & ChatGTP

# **Citation:** ChatGPT, OpenAI, 2024.
