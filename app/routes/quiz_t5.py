from flask import Blueprint, request, jsonify
from app.utils.generate_t5 import create_exam

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    quiz = create_exam(text)
    return jsonify(quiz), 200
