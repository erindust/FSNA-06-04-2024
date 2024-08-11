import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
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
    selection =Question.query.filter_by(category=str(category_id)).all()
    print("Selection:",selection)
    questions = []
    for question in selection:
      questions.append(question.format())
    print("Questions:",questions)

    current_category = Category.query.filter(Category.id==category_id).one_or_none()
    
    return jsonify({
      "questions":questions,
      "total_questions":len(questions),
      "current_category":current_category.type
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:question_id>",methods=['DELETE'])
  def delete_question(question_id):
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


  # @app.route('/questions',methods=['POST'])
  # def create_or_search():
  #   try:
  #     body = request.get_json()
  #     new_search = body.get('searchTerm',None)
  #     if new_search:
  #       search_questions(new_search)
  #     else:
  #       create_question(body)
  #   except:
  #     print("Error in create_or_search()")
  #     abort(422)

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
      abort(500) #Internal Server Error
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
    try:
      body = request.get_json()
      search_term = body.get('searchTerm',None)
      print("Search:",search_term)
      selection = Question.query.filter(Question.question.ilike('%{}%'.format(search_term)))
      print("Questions found:",selection)
      # questions = []
      # for question in selection:
      #   questions.append(question.format())
      questions = [question.format() for question in selection]
      formatted_questions = paginate_questions(request,selection)
      print("questions found:",questions)
      # formatted_questions = [question.format() for question in questions]
      # print("Formatted Questions:",formatted_questions)
      return jsonify({
        'success':True,
        # 'questions':formatted_questions,
        # 'total_questions':len(formatted_questions),
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
    try:
      body=request.get_json()
      print(body)
      previous_questions = body.get('previous_questions')
      quiz_category = body.get('quiz_category')
      print("Quiz Category:",quiz_category)
      print("Quiz Category Datatype:",type(quiz_category))  
      print("Quiz Category ID:",quiz_category["id"])
      print("Quiz Category ID DATAType:",type(quiz_category['id']))
      if quiz_category["id"] == 0:
        selection = Question.query.order_by(Question.id).all()
      else:
        selection = Question.query.filter(Question.category==quiz_category["id"]).all()
      print("\nSELECTION:",selection)
      questions = [question.format() for question in selection]
      print("\nQUESTIONS:",questions)
      # check to see if question is in the previous question list
      for i in questions:
        print("\nITERATING THROUGH LIST...",i['id'])
        if i['id'] in previous_questions:
          # remove question from list
          print("REMOVING:",i)
          questions.remove(i)
          
      print("\nPASSED REMOVING DICTIONARY FROM LIST")
      question = random.choice(questions)
      print("\nRANDOMLY CHOSEN QUESTION:",question)

      

      

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
    return jsonify({"error":"EGN Resource not found"}),404
  
  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({"error":"EGN Internal server error!"}),500
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({"error":"EGN Bad Request"}),400
  
  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({'error': 'EGN Unprocessable Entity', 'message': str(error)}), 422

  

  
  return app

    