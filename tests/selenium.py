import threading
from time import sleep
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from src import create_app, db
from config import TestConfig
from src.test_data import add_test_user_to_db  

localHost = "http://localhost:5000"

class SeleniumTestCase(TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

        #Replaced multiprocessing with threading to avoid pickling issue.
        self.server_thread = threading.Thread(target=self.testApp.run, kwargs={"use_reloader":False})
        self.server_thread.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

    def tearDown(self):
        self.testApp.do_teardown_appcontext()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    #This test is failing due to the ID's not being found.
    def test_register_page(self):

        self.driver.get(localHost + "/login")
        sleep(1)    

        loginElement = self.driver.find_element(By.ID, "username")
        loginElement.send_keys("wesdutton")

        loginElement = self.driver.find_element(By.ID, "password")
        loginElement.send_keys("wesdutton")

        submitElement = self.driver.find_element(By.ID, "submit")
        submitElement.click()
        
        sleep(1)
            
        
       
        