from flask import Blueprint, request, jsonify
from app.utils.generate_qa import generate_quiz_qa

qa_bp = Blueprint('qa', __name__)

@qa_bp.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    text = data.get('text', '')
    questions = data.get('questions', [])
    
    if not text or not questions:
        return jsonify({'error': 'Text and questions are required'}), 400
    
    quiz_questions = generate_quiz_qa(text, questions)
    return jsonify(quiz_questions)
