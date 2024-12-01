from flask import Blueprint, request, jsonify
from app.utils.generate_mcqs import generate_mcqs

spacy_bp = Blueprint('spacy', __name__)

@spacy_bp.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.json
    text = data.get('text', '')
    num_questions = data.get('num_questions', 5)
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    questions = generate_mcqs(text, num_questions)
    return jsonify({"questions": questions})
