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
        print("Response Status Code:", res.status_code)
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

    def test_add_question_success(self):
        new_question = {
            "question":"What is the capitol of France?",
            "answer":"Paris",
            "category":1,
            "difficulty":1
        }
        response = self.client.post("/questions",json=new_question)
        self.assertEqual(response.status_code, 201)
        print("test_add_questions_success-response.json:")
        print(response.json)
        # self.assertIn('question',response.json)

    # def add_sample_question(self):
    #     new_question = {
    #         "questions":"What is the capital of Italy?",
    #         "answer":"Rome",
    #         "category":1,
    #         "difficulty":1
    #     }
    #     response = self.client.post("/questions",json=new_question)
    #     data = response.get_json()
    #     new_question_id = data["id"]
    #     return new_question_id

    def test_delete_question_success(self):
        # question_id = self.add_sample_question()
        new_question = {
            "question":"What is the capital of Italy?",
            "answer":"Rome",
            "category":1,
            "difficulty":1
        }
        print("test_delete_question_success new question:")
        print(new_question)
        response = self.client.post("/questions",json=new_question)
        print("Test Question Post Status: ")
        print(response.status_code)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        print("data received back after adding question: ")
        print(data)
        new_question_id = data['created']
        response = self.client.delete(f"/questions/{new_question_id}")
        self.assertEqual(response.status_code,200)
        print("test_delete_question_success-response.json:")
        print(response.json)
        # self.assertEqual(response.json,{"success":True})
        self.assertEqual(response.json['success'], True)

    

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()