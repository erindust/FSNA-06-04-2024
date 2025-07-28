import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
  """
  Paginate a list of questions based on the requested page number.

  This function takes a request object and a selection of questions
  and returns a subset of questions for the specified page. It 
  calculates the start and end of the page number and the predefined
  number of questions per page.

  Parameter:
  - request: The request object containing query parameters,
    including the page number
  - selection: A list of questions to be paginated.  Each 
    question should have a 'format()' method that returns a 
    formatted representation of the question.

  Returns:
  - A list of questions for the specified page.

  Example:
  - If QUESTIONS_PER_PAGE is set to 10 and the page number is 2,
    this function will return questions 11 to 20 from the selection

  Raises:
  - IndexError: If the page number is out of range for the selection.  
  """
  page = request.args.get("page", 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add(
          "Access-Control-Allow-Headers", "Content-Type,Authorization,True"
      )
      response.headers.add(
          "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
      )
      return response
  

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route("/questions")
  def retrieve_questions():
    """
    Retrieve a list of questions and their associated categories.

    This endpoint handels GET requests to the "/questions" route.
    It retrieves all questions from the database, 
    paginates them based on the request parameters,
    and returns them along with the total number of questions,
    available categories, and the current category.

    Steps:
    1. Retrieve all questions from the database and order them by ID.
    2. Paginate the questions based on the request parameters.
    3. If no questions are found, return a 404 error.
    4. Get the current category ID from the request arguments.
        If the category does not exist, 404 error.
    5. Retrieve all categories from the database and format them for
        the response.
    6. Return a JSON response containing:
        - 'questions': The list of paginated questions.
        - 'total_questions': The total number of questions
            in the database.
        - 'categories': A dictionary of available categories.
        - 'current_category': The type of the current category.

    Returns:
      JSON response containing the questions, total_questions count, categories, and the current category.

    Raises:
      404: If no questions are found or if the specified category does not exist.
    """
    print("@app.route(\'/questions\') request:",request)
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request,selection)
    if len(current_questions) == 0:
      abort(404)

    current_category_id = request.args.get("catagory_id", 1, type=int)
    current_category = Category.query.filter(Category.id==current_category_id).one_or_none()
    if current_category is None:
      abort(404)

    current_category = current_category.type
    categories = Category.query.order_by(Category.id).all()
    # formatted_categories = [category.format() for category in categories]
    formatted_categories = {}
    for category in categories:
      formatted_categories[category.id] = category.type

    return jsonify(
      {
        "questions":current_questions,
        "total_questions":len(selection),
        "categories":formatted_categories,
        "current_category":current_category
      }
    )

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories")
  def retrieve_categories():
    """
    Retrieve a list of all categories from the database.

    This endpoint handles GET request to the '/categories' route.
    It retrieves all categories from the database, orders them
    by their ID, and returns them in a formatted JSON response.

    Steps:
    1. Query the database to get all categories, ordered by
        their ID.
    2. Format the categories into a dictionary where the keys are
        category IDs and the values are category types.
    3. Return a JSON response containing the formatted categories.

    Return:
      JSON response containing:
      - 'catagories': A dictionary of category IDs and their 
          corresponding types.

    Example Response:
    {
      "categories":{
        1: "Science",
        2: "Math",
        3: "History"
      }
    }
    """
    categories=Category.query.order_by(Category.id).all()
    formatted_categories = {}
    for category in categories:
      formatted_categories[category.id] = category.type

    return jsonify(
      {
        "categories":formatted_categories
      }
    )

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<int:category_id>/questions")
  def question_by_category(category_id):
    """
    Retrieve questions for a specific category.

    This endpoint handles GET requests to the 
    "/categories/<int:category_id>/questions" route. It retrieves
    all questions associated with the specified category ID
    from the database and returns them in a JSON response. If the
    category does not exist, it returns a 404 error with an 
    appropriate message.

    Parameters:
    - category_id (int): The ID of the category for which to 
                          retrieve the questions.

    Steps:
    1. Query the database for questions that match the given category ID.
    2. Format the questions into a list.
    3. Check if the category exists in the database.
    4. If the catagory does not exist, return a 404 error with a message.
    5. If the category exists, return a JSON response containing:
        - "questions": A list of formatted questions.
        - "total_questions": The total number of questions retrieved.
        - "current_category": The type of the current category.

    Returns:
      JSON response containing:
      - "questions": List of questions for the specified category.
      - "total_questions": Total number of questions in the category.
      - "current_category": The type of current category.

    Raises:
      404: If the specified category ID does not correspond to an existing category.
    """
    selection =Question.query.filter_by(category=str(category_id)).all()
    print("Selection:",selection)
    questions = []
    for question in selection:
      questions.append(question.format())
    print("Questions:",questions)

    current_category = Category.query.filter(Category.id==category_id).one_or_none()

    if current_category is None:
      return jsonify({
        "success":False,
        "message":"Category not found."
      }),404
    
    return jsonify({
      "questions":questions,
      "total_questions":len(questions),
      "current_category":current_category.type if current_category else None
    })

  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:question_id>",methods=['DELETE'])
  def delete_question(question_id):
    """
    Delete a question from the database by its ID.

    This endpoint handles DELETE requests to the "/questions/<questions_id>" route.
    It attempts to find the question with the specified ID in the database. If the 
    question is found, it deletes the question and returns a JSON response 
    indicating success, along with the updated list of the questions and the 
    total number of questions remaining. If the question is not found, it returns 
    a 404 error. If an occurs during the deletion process, it returns a 422 error.

    Parameters:
    - question_id (int): The ID of the question to be deleted.

    Steps:
    1. Query the database to find the question by its ID.
    2. If the question is not found, abort with a 404 status code.
    3. If the question is found, delete it from the database.
    4. Retrieve the updated list of questions and paginate them
    5. Return a JSON response containing:
        - "success": A boolean indicating the deletion was successful.
        - "deleted": The ID of the deleted question.
        - "questions": The updated list of questions.
        - "total_questions": The total number of questions remaining.

    Returns:
      JSON response indicating the result of the deletion operation.

    Raises:
      404: If the question with the specified ID does not exist.
      422: If an error occurs during the deletion process.
    """
    try:
      question = Question.query.filter(Question.id==question_id).one_or_none()
      print("Questions Found: ",question)
      if question is None:
        abort(404)
      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request,selection)

      return jsonify({
        "success":True,
        "deleted":question_id,
        "questions":current_questions,
        "total_questions":len(selection)
      }), 200
    except Exception as e:
      print(f"Error occurred: {e}")
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions',methods=['POST'])
  def create_question():
    """
    Create a new trivia question.
    
    This endpoint allows user to add a question to the trivia database.
    The request must contain the question text, answer, difficulty level,
    and category. If any of these fields are missing or invalid, a 422
    Unprocessable Entity error will be returned.  On successful creation,
    a 201 Created response will be returned along with the ID of the created
    question and the total number of questions in the database.

    Requestion Body:
      - question (str): The text of the question to be added.
      - answer (str): The answer to the question.
      - difficulty (int): The difficulty level of the question (e.g. 1-5)
      - category (str): The category to which the question belongs
    
    Returns:
      - JSON response containing:
        - success (bool): Indicates if the operation was successful.
        - created (int): The ID of the newly created question.
        - total_questions (int): The total number of questions in the database

    Raises:
      - 422 Unprocessable Entity: If the question, answer, difficulty, or category 
        is missing or invalid.
      - 500 Internal Server Error: If there is an error during database operation.
    """
    body = request.get_json()
    print("New Question:",body)
    new_question = body.get("question",None)
    new_answer = body.get("answer",None)
    new_difficulty = body.get("difficulty",None)
    new_category = body.get("category",None)

    if (new_question is None) or (len(new_question)==0):
      abort(422, description = "Question is required.")
    if (new_answer is None) or (len(new_answer)==0):
      abort(422, description = "Answer is required.")
    if (new_difficulty is None):
      abort(422, description = "Difficulty is required.")
    if (new_category is None):
      abort(422, description = "Category is required.")
    selection = Question.query.order_by(Question.id).all()
    print("Total questions previous to operation: ",len(selection))

    try:
      question = Question(question=new_question,answer=new_answer,difficulty=new_difficulty,category=new_category)
      question.insert()
      selection = Question.query.order_by(Question.id).all()
      print("Total questions after operation: ",len(selection))

      return jsonify({
        'success':True,
        'created':question.id,
        'total_questions':len(selection)
      }),201 #201 = created status code

    except Exception as e:
      print("Error in create_question()",e)
      abort(500,description=str(e)) #Internal Server Error

  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search',methods=['POST'])
  def search_questions():
    """
    Search for questions based on a search term.

    This endpoint handles POST requests to the "/questions/search" route. 
    It retrieves a search term from the request body and queries the
    database for questions that contain the search term in their text.
    The results are then paginated and returned in a JSON response.

    Steps:
    1. Retrieve the search term from the request body.
    2. Query the database for questions that match the search term using
        a case-sensitive search.
    3. Format the found questions and paginate the results.
    4. Return a JSON response containing:
        - "success": A boolean indicating the search was successful.
        - "questions": A list of formatted questions that match the search term.
        - "total_questions": The total number of questions found.
        - "current_category": Currently set to None.

    Returns:
      JSON response containing the search results.

    Raises:
      422: If there is an error processing the search request.
    """
    try:
      body = request.get_json()
      search_term = body.get('searchTerm',None)
      print("Search:",search_term)
      selection = Question.query.filter(Question.question.ilike('%{}%'.format(search_term)))
      print("Questions found:",selection)
      questions = [question.format() for question in selection]
      formatted_questions = paginate_questions(request,selection)
      print("questions found:",questions)
      return jsonify({
        'success':True,
        'questions':formatted_questions,
        'total_questions':len(questions),
        'current_category':None
      })
    except:
      print("Error in search_questions")
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods=['POST'])
  def quiz():
    """
    Retrieve a random quiz question based on the specified category &
    previously answered questions.

    This endpoint handles POST requests to the "/quizzes" route.  It expects
    a JSON payload containing the previous questions and the quiz category.
    The function retrieves a random question that has not been previously
    answered by the user. If no questions are available in the specified
    category, it returns a message indicating that there are no more questions.

    Request Body:
    - previous_questions (list): A list of question IDs that have already 
      been answered.
    - quiz_category (dict): A dictionary containing the category ID. If
      the ID is 0, questions from all categories will be retrieved.

    Response:
    - On success, returns a JSON object containing:
      - "question": A dictionary with the details of the selected question,
        including "id", "questions", "answer", "difficulty", and "category".
    - If no available questions are found, returns a JSON object with:
      - "success": True
      - "message": A message indicating that no more questions are available 
        in the specified category.
    
    Raises:
    - 422: If there is an error processing the request.

    Example Request:
    {
      "previous_questions": [1,2,3],
      "quiz_category": {"id",1}
    }
    """
    try:
      body=request.get_json() 
      print("######################################")
      print(body)
      previous_questions = body.get('previous_questions',[])
      print("PREVIOUS QUESTIONS:",previous_questions)
      quiz_category = body.get('quiz_category',None)
      print("QUIZ_CATEGORY",quiz_category)

      if quiz_category['id']!=0:
        selection = Question.query.filter(Question.category==quiz_category["id"]).all()
      else:
        selection = Question.query.all()
      
      print("SELECTION",selection)

      questions = [question.format() for question in selection]
      print("QUESTIONS",questions)

      available_questions = [q for q in questions if q['id'] not in previous_questions]
      print("AVAILABLE QUESTIONS:",available_questions)
      if not available_questions:
        return jsonify({
          'success':True,
          'message':"No more questions available in this category."
        })
          
      question = random.choice(available_questions)

      return jsonify({
        'question': {
          'id':question['id'],
          'question':question['question'],
          'answer':question['answer'],
          'difficulty':question['difficulty'],
          'category':question['category']
        }
      })

    except:
      abort(422)
    


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found_error(error):
    return jsonify({"error":"Resource not found"}),404
  
  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({"error":"Internal server error!"}),500
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({"error":"Bad Request"}),400
  
  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({'error': 'Unprocessable Entity', 'message': str(error)}), 422

  

  
  return app

    