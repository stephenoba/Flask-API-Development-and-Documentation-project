# Trivia App

Trivia applucation based upon the Udacity API develioment amd documentation final project.

## The Stack
1. Python (Flask) Backend
2. React Frontend

The application:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## About the Stack

### Backend

The [backend](./backend/README.md) directory contains a Flask and SQLAlchemy server. Database and database tables are defined in `backend/models.py` file, and the endpoints are defined in the `backend/flaskr/__init__.py` file, tests are written in the `backend/test_flaskr.py` file.

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server.

> View the [Frontend README](./frontend/README.md) for more details.
