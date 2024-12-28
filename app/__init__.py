from flask import Flask
from flask_cors import CORS
from app.routes.quiz_spacy import spacy_bp
from app.routes.quiz_qa import qa_bp
from app.routes.quiz_t5 import quiz_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Kích hoạt CORS
    app.register_blueprint(spacy_bp, url_prefix="/spacy")  # Đăng ký route cho spaCy
    app.register_blueprint(qa_bp, url_prefix="/qa")        # Đăng ký route cho QA
    app.register_blueprint(quiz_bp, url_prefix='/t5')        # Đăng ký route cho T5
    return app
