import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test" #need to set up an empty database
        self.username = "postgres"
        self.password = "postgres"
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.username, self.username,'localhost:5432', self.database_name)
        # .... make sure sample database is setup to test with
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # def test_422_unprocessable_entity(self):
    #     #Simulate a 422 error
    #     response = self.app.post('/questions',json={}) #sending an empty json
    #     print("unittest response:",response)
    #     self.assertEqual(response.status_code,422)
    #     self.assertIn('Unprocessable Entity',response.get_json()['error'])

    # Test Successful Retrieval of Questions  
    # to ensure that when the endpoint is hit successfully, it returns a 200 status code and the expected structure of the response  
    def test_retrieve_questions_success(self):
        res = self.client.get('/questions')
        print("res:",res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertIn('categories', data)
        self.assertIn('current_category', data)

    def test_404_error_handler(self):
        response = self.client.get('/non-existent-endpoint')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "EGN Resource not found"})

    def test_404_no_questions(self):
        # Simulate a request to /questions when there are no questions
        # for this test to pass the database questions table needs to be empty
        response = self.client.get('/questions')
        self.assertEqual(response.status_code, 404)

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()