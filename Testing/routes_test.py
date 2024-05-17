
import unittest
from flask import url_for
from src import create_app, socketio


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('src.config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.socketio = socketio

    def tearDown(self):
        self.app_context.pop()

    def test_home_page(self):
        # Replace 'home' with your actual route name
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
