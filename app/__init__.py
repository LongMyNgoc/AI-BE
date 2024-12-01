from flask import Flask
from flask_cors import CORS
from app.routes.quiz_spacy import spacy_bp
from app.routes.quiz_qa import qa_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Kích hoạt CORS
    app.register_blueprint(spacy_bp, url_prefix="/spacy")  # Đăng ký route cho spaCy
    app.register_blueprint(qa_bp, url_prefix="/qa")        # Đăng ký route cho QA
    return app
