from flask import Blueprint, request, jsonify
from app.utils.generate_mcqs import generate_mcqs

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.json
    text = data.get('text', '')
    num_questions = data.get('num_questions', 5)
    questions = generate_mcqs(text, num_questions)
    return jsonify({"questions": questions})
