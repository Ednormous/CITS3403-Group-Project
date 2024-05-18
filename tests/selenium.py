import multiprocessing
from time import time
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from src import create_app, db
from config import TestConfig
from src.test_data import add_test_user_to_db  

localHost = "http://localhost:5000"

class SeleniumTestCase(TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()

        self.server_process = multiprocessing.Process(target=self.testApp.run)
        self.server_process.start()

        self.driver = webdriver.Chrome()
        self.driver.get(localHost)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()
        self.driver.close()


    def test_home_page(self):
        time.sleep(10)
        self.assertTrue(True)

        loginElement = self.driver.find_element(By.ID, "login")
        loginElement.send_keys("wesdutton")
        
       
        