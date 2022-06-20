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
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgres://{}:{}@{}/{}'.format(
            'student', 'student', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "answer": "In the Universe",
            "category": 3,
            "difficulty": 1,
            "question": "Where is the earth?"
        }
        self.search_query = {"searchTerm": "What"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        categories = Category.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["categories"]), len(categories))

    def test_get_questions(self):
        page = 1
        res = self.client().get(f"/questions?page={page}")
        data = json.loads(res.data)
        categories = Category.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertLessEqual(len(data["questions"]), 10)
        self.assertLessEqual(len(data["questions"]), data["totalQuestions"])
        self.assertEqual(len(data["categories"]), len(categories))

    def test_create_question(self):
        total_que = len(Question.query.all())
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertLess(total_que, len(Question.query.all()))

    def test_search_question(self):
        res = self.client().post('/questions', json=self.search_query)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["totalQuestions"], 8)

    def test_new_question_validation(self):
        self.new_question["category"] = 7
        res = self.client().post('/questions', json=self.new_question)

        self.assertEqual(res.status_code, 400)

    def test_delete_new_question(self):
        question_id = Question.query.all()[-1].id
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(data['question_id'], question_id)
        self.assertEqual([], Question.query.filter(Question.id == question_id).all())

    def test_get_question_by_category(self):
        category_id = 3
        questions = Question.query.filter(Question.category == category_id).all()
        res = self.client().get(f"/categories/{category_id}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(questions), len(data["questions"]))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
