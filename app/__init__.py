from flask import Flask
from flask_cors import CORS
from app.routes.quiz import quiz_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS
    app.register_blueprint(quiz_bp)  # Register the quiz route
    return app
