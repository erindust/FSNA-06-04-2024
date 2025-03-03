# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
################################################################################################
# Trivia API Test Suite

## Overview
This project contains a test suite for the Trivia API, which allows users to retrieve, add, and delete trivia questions. The tests are implemented using the `unittest` framework and cover various aspects of the API's functionality.

## Setup

### Dependencies
- Flask
- Flask-SQLAlchemy
- PostgreSQL

### Database Configuration
Make sure to set up an empty PostgreSQL database for testing. The database connection string is configured in the `setUp` method of the test class.

```python
self.database_name = "trivia_test"
self.username = "postgres"
self.password = "postgres"
self.database_path = "postgresql://{}:{}@{}/{}".format(self.username, self.username, 'localhost:5432', self.database_name)

### Test Cases
Test Case 1: Unprocessable Entity (422)
•	Description: Tests that an empty JSON request to the /questions endpoint returns a 422 status code.
•	Expected Outcome:
•	Status Code: 422
•	Error Message: "Unprocessable Entity"

Test Case 2: Retrieve Questions Success
•	Description: Tests successful retrieval of questions from the /questions endpoint.
•	Expected Outcome:
•	Status Code: 200
•	Response contains keys: questions, total_questions, categories, current_category

Test Case 3: 404 Error Handler
•	Description: Tests that a request to a non-existent endpoint returns a 404 status code.
•	Expected Outcome:
•	Status Code: 404
•	Error Message: "Resource not found"

Test Case 4: No Questions (404)
•	Description: Tests the response when there are no questions in the database.
•	Expected Outcome:
•	Status Code: 404

Test Case 5: Add Question Success
•	Description: Tests successful addition of a new question to the /questions endpoint.
•	Expected Outcome:
•	Status Code: 201
•	Response contains the created question details.

Test Case 6: Delete Question Success
•	Description: Tests successful deletion of a question by ID.
•	Expected Outcome:
•	Status Code: 200
•	Response indicates success.

Test Case 7: Delete Question Failure
•	Description: Tests deletion of a question that does not exist.
•	Expected Outcome:
•	Status Code: 422

Test Case 8: Get Questions by Category Success
•	Description: Tests retrieval of questions by category.
•	Expected Outcome:
•	Status Code: 200
•	Response contains a list of questions.

Test Case 9: Get Questions by Category Failure
•	Description: Tests retrieval of questions for a non-existent category.
•	Expected Outcome:
•	Status Code: 404

Running the Tests
To run the tests, execute the following command:

python -m unittest <test_file_name>.py
Replace <test_file_name> with the name of your test file.
