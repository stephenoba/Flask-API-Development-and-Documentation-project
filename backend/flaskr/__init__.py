import os

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from exceptions import ValidationError

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
    len_total_items = len(selection)
    total_pages = round(len_total_items / 10)
    page = request.args.get("page", 1, type=int)
    next_page = page + 1 if page < total_pages else None
    previous_page = page - 1 if page > 1 else None
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items, total_pages, page, next_page,  previous_page


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    def serialize_categories(query):
        categories = query.order_by(Category.id).all()
        serialized_data = {
            "categories": {}
        }

        if categories:
            for category in categories:
                serialized_data["categories"].update({str(category.id): category.type})
        return serialized_data

    @app.route('/categories', methods=['GET'])
    def get_categories():
        category_query = Category.query
        data = serialize_categories(category_query)

        return jsonify(data)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        (
            questions,
            total_pages,
            current_page,
            next_page,
            previous_page
        ) = paginate(request, selection)
        categories = serialize_categories(Category.query).get("categories")

        data = {
            "questions": questions,
            "categories": categories,
            "current_category": None,
            "totalQuestions": len(questions),
            "total_pages": total_pages,
            "current_page": current_page,
            "previous_page": previous_page,
            "next_page": next_page
        }
        return jsonify(data)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        try:
            if not question:
                abort(404)
            question.delete()
            data = {"question_id": question_id}
            return jsonify(data)
        except:
            abort(422)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    def validate_new_question(data):
        difficulty = data.get("difficulty", None)
        category = data.get("category", None)
        if difficulty and category:
            if int(difficulty) > 5 or int(category) > 6:
                raise ValidationError
        else:
            raise ValidationError

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            body = request.get_json()
            validate_new_question(body)

            question = body.get("question", None)
            answer = body.get("answer", None)
            difficulty = body.get("difficulty", None)
            category = body.get("category", None)
            search = body.get("searchTerm", None)

            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                ).all()
                (
                    questions,
                    total_pages,
                    current_page,
                    next_page,
                    previous_page
                ) = paginate(request, selection)

                data = {
                    "questions": questions,
                    "current_category": None,
                    "totalQuestions": len(questions),
                    "total_pages": total_pages,
                    "current_page": current_page,
                    "previous_page": previous_page,
                    "next_page": next_page
                }

                return jsonify(data)
            else:
                question = Question(
                    answer=answer,
                    difficulty=difficulty,
                    category=category,
                    question=question
                )
                question.insert()

                return jsonify(
                    {
                        "created": question.id
                    }
                )
        except ValidationError as e:
            abort(400)
        except Exception as e:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    return app

