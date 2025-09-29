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
    #     """
    #     Test the API endpoint for handling unprocessable entity errors (HTTP 422).

    #     This test simulates a scenario where POST request is made to the 
    #     "/questions" endpoint with an empty JSON payload. It verifies that
    #     the server responds with a 422 status code & checks that the 
    #     response contains the appropriate error message indicating that
    #     the request was unprocessable.

    #     Steps:
    #     1. Send a POST request to the "/questions" endpoint with an empty 
    #         JSON object.
    #     2. Assert that the response status code is 422.
    #     3. Assert that the response contains an "error" key with the
    #         message "Unprocessable Entity".

    #     Expected Outcome:
    #     The test should pass if the API correctly identifies the empty
    #     request as unprocessable and returns the expected status code
    #     and error message.
    #     """
    #     #Simulate a 422 error
    #     response = self.client.post('/questions',json={}) #sending an empty json
    #     data = response.get_json()
    #     print("test_422_unprocessable_entity-response:",data)
    #     self.assertEqual(response.status_code,422)
    #     self.assertEqual(data['error'],'Unprocessable Entity')

    # # Test Successful Retrieval of Questions  
    # # to ensure that when the endpoint is hit successfully, it returns a 200 status code and the expected structure of the response  
    # def test_retrieve_questions_success(self):
    #     """
    #     Test the API endpoint for successfully retrieving all questions.

    #     This test sends a GET request to the "/questions" endpoint &
    #     verifies that the response is successful (HTTP 200). It checks
    #     that the response contains the expected keys: "questions",
    #     "total questions", "categories", & "current_category".

    #     Steps:
    #     1. Send a GET request to the "/questions" endpoint.
    #     2. Assert that the response status code is 200.
    #     3. Parse the response data from JSON.
    #     4. Assert that the response data contains following keys: 
    #         - "questions"
    #         - "total_questions" 
    #         - "categories"
    #         - "current_category"

    #     Expected Outcome:
    #     The test should pass if the API correctly returns a successful
    #     response with the expected structure and data.
    #     """
    #     res = self.client.get('/questions')
    #     print("res:",res)
    #     print("Response Status Code:", res.status_code)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertIn('questions', data)
    #     self.assertIn('total_questions', data)
    #     self.assertIn('categories', data)
    #     self.assertIn('current_category', data)

    
    # def test_404_error_handler(self):
    #     """
    #     Test the API endpoint for handling 404 errors (Not found).

    #     This test simulates a scenario where a GET request is made to a
    #     non-existent endpoint. It verifies that the server responds with 
    #     a 404 status code and checks that the response contains the
    #     appropriate error message indicating that the requestion resouce
    #     was not found.

    #     Steps:
    #     1. Send a GET request to a non-existent endpoint ("/non-existent-endpoint").
    #     2. Assert that the response status code is 404.
    #     3. Assert that the response JSON contains an "error" key with the 
    #         message "Resource not found".

    #     Expected Outcome:
    #     The test should pass of the API correctly identifies the non-existent
    #     endpoint and returns the expected status code and error message.
    #     """
    #     response = self.client.get('/non-existent-endpoint')
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response.json, {"error": "Resource not found"})

    # def test_404_no_questions(self):
    #     """
    #     Test the API endpoint for retrieving questions when no questions exist.

    #     This test simulates a scenario where a GET request is made to the
    #     "/questions" endpoint, but the questions table in the database
    #     is empty. It verifies that the server responds with a 404 status
    #     code, indicating that no questions were found.

    #     Steps:
    #     1. Ensure that the questions table in the database is empty
    #         before running this test.
    #     2. Send a GET request to the "/questions" endpoint.
    #     3. Assert that the response status code is 404.

    #     Expected Outcomes:
    #     The test should pass if the API correctly identifies that there
    #     are no questions available and returns the expected status code.
    #     """
    #     # Simulate a request to /questions when there are no questions
    #     # for this test to pass the database questions table needs to be empty
    #     response = self.client.get('/questions')
    #     self.assertEqual(response.status_code, 404)

    # def test_add_question_success(self):
    #     """
    #     Test the API endpoint for successfully adding a new question.

    #     This test simulates a scenario where a POST request is made to 
    #     the "/questions" endpoint with a valid question payload. It
    #     verifies that the server responds with a 201 status code,
    #     indicating that the question was created successfully. The test 
    #     also prints the response JSON for verification.

    #     Steps:
    #     1. Define a new question with the required fields: question,
    #         answer, category, and difficulty.
    #     2. Send a POST request to the "/questions" endpoint with the 
    #         new question as JSON.
    #     3. Assert that the response status code is 201 (Created).
    #     4. Print the response JSON for verification.

    #     Expected Outcome:
    #     The test should pass if the API correctly adds the new question
    #     and returns the expected status code and response data.
    #     """
    #     new_question = {
    #         "question":"What is the capitol of France?",
    #         "answer":"Paris",
    #         "category":1,
    #         "difficulty":1
    #     }
    #     response = self.client.post("/questions",json=new_question)
    #     self.assertEqual(response.status_code, 201)
    #     print("test_add_questions_success-response.json:")
    #     print(response.json)
    #     # self.assertIn('question',response.json)


    # def test_delete_question_success(self):
    #     """
    #     Test the API endpoint for successfully deleting a question.

    #     This test simulates a scenario where a new question is first
    #     added to the database, and then a DELETE request is made to 
    #     remove that question. It verifies that the question is created 
    #     successfully and that the DELETE request returns a 200 status
    #     code, indicating that the deletion was successful.

    #     Steps:
    #     1. Define a new question with the required fields: question, 
    #         answer, category, and difficulty.
    #     2. Send a POST request to the "/questions" endpoint to and
    #         the new question.
    #     3. Assert that the response status code is 201 (Created).
    #     4. Retrieve the ID of the newly created question from the 
    #         response data.
    #     5. Send a DELETE request to the "/questions/<question_id>"
    #         endpoint to delete the question.
    #     6. Assert that the response status code is 200 (OK).
    #     7. Assert that the response indicates success.

    #     Expected Outcome:
    #     The test should pass if the API correctly adds the new question
    #     and successfully deletes it, returning the expected status code
    #     and response data.
    #     """
    #     # question_id = self.add_sample_question()
    #     new_question = {
    #         "question":"What is the capital of Italy?",
    #         "answer":"Rome",
    #         "category":1,
    #         "difficulty":1
    #     }
    #     print("test_delete_question_success new question:")
    #     print(new_question)
    #     response = self.client.post("/questions",json=new_question)
    #     print("Test Question Post Status: ")
    #     print(response.status_code)
    #     self.assertEqual(response.status_code, 201)
    #     data = response.get_json()
    #     print("data received back after adding question: ")
    #     print(data)
    #     new_question_id = data['created']

    #     response = self.client.delete(f"/questions/{new_question_id}")
    #     self.assertEqual(response.status_code,200)
    #     print("test_delete_question_success-response.json:")
    #     print(response.json)
    #     # self.assertEqual(response.json,{"success":True})
    #     self.assertEqual(response.json['success'], True)

    # def test_delete_question_failure(self):
    #     """
    #     Test the API endpoint for handling deletion of a non-existent question.

    #     This test simulates a scenario where a DELETE request is made to
    #     the "/questions/<question_id>" endpoint with an invalid question ID
    #     (1000 in this case), assuming it does not exist). It verifies that
    #     the server responds with a 422 status code, indicating that the 
    #     request to delete the question was unprocessable.

    #     Steps:
    #     1. Send a DELETE request to the "/questions/1000" endpoint.
    #     2. Assert that the response status code is 422.
    #     3. Print the response JSON for verification.

    #     Expected Outcome:
    #     The test should pass if the API correctly identifies that the
    #     specified question does not exist and returns the expected status
    #     code and error message.
    #     """
    #     # question_id = self.add_sample_question()
        
    #     response = self.client.delete(f"/questions/1000")
    #     self.assertEqual(response.status_code,422)
    #     print("test_delete_question_success-response.json:")
    #     print(response.json)

    # def test_get_questions_by_category_success(self):
    #     """
    #     Test the API endpoint for retrieving questions by category.

    #     This test sends a GET request to the "/categories/<category_id>/questions"
    #     endpoint and verifies that the response is successful (HTTP 200). It checks
    #     that the response contains the expected structure, including the total number
    #     of questions and that the questions are returned as a list.

    #     Steps:
    #     1. Send a GET request to the "/categories/1/questions" endpoint.
    #     2. Assert that the response status code is 200.
    #     3. Assert that the "total_questions" in the response data is greater than or
    #         equal to 0.
    #     4. Assert that the "questions" in the response data is a list.

    #     Expected Outcome:
    #     The test should pass if the API correctly returns a successful response with
    #     the expected structure and data for the specified category.
    #     """
    #     res = self.client.get('/categories/1/questions')
    #     data = res.get_json()
    #     self.assertEqual(res.status_code,200)
    #     self.assertTrue(data["total_questions"] >= 0)
    #     self.assertIsInstance(data["questions"],list)

    # def test_get_questions_by_category_failure(self):
    #     """
    #     Test the API endpoint for retrieving questions by a non-existent category.

    #     This test simulates a scenario where a GET request is made to the 
    #     "/categories/<category_id>/questions" endpoint with an invalid
    #     category ID (999 in this case). It verifies that the server responds 
    #     with a 404 status code, indicating that the requested category was
    #     not found.

    #     Steps:
    #     1. Send a GET request to the "/catagories/999/questions" endpoint.
    #     2. Assert that the response status code is 404.
    #     3. Optionally, assert that the response contains an appropriate error message.

    #     Expected Outcome:
    #     The test should pass if the API correctly identifies that the requested
    #     category does not exist and returns the expected status code.
    #     """
    #     res = self.client.get('/categories/999/questions')
    #     data = res.get_json()
    #     self.assertEqual(res.status_code,404)

    """
    Possible unit tests for the /quizzes POST request endpoint

    1. Test Successful Retrieval of a Random Question:
        - Test that when valid previous_questions and quiz_category are provided, the
          function returns a random questions that is not in previous_questions.
    2. Test No More Available Questions:
        - Test that when all questions in the specified category have been answered (i.e., 
          available_questions is empty), the function returns a success message indicating
          no more questions are available.
    3. Test Invalid Category ID:
        - Test that when an invalid category ID is provided (e.g., a non_existent category), the
          function should return a 422 error.
    4. Test Handling of Missing Request Body:
        - Test that if the request body is missing or improperly formatted, the function raises
          a 422 error.
    5. Test Retrieval of Questions from All Categories:
        - Test that when quiz_category ID is 0, the function retrieves questions from all 
          categories.
    6. Test Handling of Non-JSON Request:
        - Test that is the request is not JSON, the function raises a 422 error.
    """
    def test_successful_retrieval_of_question(self):
        """
        Test Successful Retrieval of a Random Question:
        - Test that when valid previous_questions and quiz_category are provided, the
          function returns a random questions that is not in previous_questions.
        """
        # Mock the database query to return a question
        # This is to make sure that there is a question 
        ##### that can be retrieved. #####
        new_question = {
            "question":"Sample Question?",
            "answer":"Sample Answer",
            "category":1,
            "difficulty":1
        }
        response = self.client.post("/questions",json=new_question)
        self.assertEqual(response.status_code,201)
        ##################################
        print("BREAK")
        
        response = self.client.post("/quizzes",
                                    json={"previous_questions":[],
                                          "quiz_category":{"id":1}})
        # print("\n RESPONSE:")
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertIn("question",data)


    # def test_no_more_available_questions(self):
    #     """
    #     Test No More Available Questions:
    #     - Test that when all questions in the specified category have been answered (i.e., 
    #       available_questions is empty), the function returns a success message indicating
    #       no more questions are available.
    #     """
    #     response = self.client.post("/quizzes",
    #                                 json={"previous_questions":[],
    #                                       "quiz_category":1})
    #     pass

    # def test_retrieve_categories(self):
    #     """
    #     Test retrieve a list of all the categories found in the categories table in trivia database
    #     """
    #     print("TEST_RETRIEVE_CATEGORIES")
    #     response = self.client.get("/categories")
    #     data = response.get_json
    #     print(data)
    #     self.assertEqual(response.status_code,200)
    #     self.assertEqual(data['success'],True)
    #     self.assertIn('categories',data)
    #     self.assertEqual(len(data['categories']),6) #Adjust depending on how many catagories there are in the db.
    #     # Adjust as needed
    #     self.assertEqual(data['categories'][1],'Science')
    #     self.assertEqual(data['categories'][2],'Math')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()