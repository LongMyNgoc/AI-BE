from flask import Flask, request, jsonify
from transformers import pipeline
import random
import nltk
from nltk.corpus import wordnet
from flask_cors import CORS  # Import CORS

# Tải mô hình QA
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

# Tải từ điển đồng nghĩa (synonym) từ WordNet
nltk.download('wordnet')

# Hàm tìm từ đồng nghĩa của từ trong câu
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())  # lấy từ đồng nghĩa
    return synonyms

# Hàm sinh đáp án nhiễu từ ngữ cảnh
def generate_distractors(answer, context, num_distractors=3):
    distractors = []
    
    # Tách từ và loại bỏ từ đã trong đáp án chính xác
    words = list(set(context.split()) - set(answer.split()))
    
    # Lấy từ đồng nghĩa của từ trong ngữ cảnh, nếu có
    for word in words:
        synonyms = get_synonyms(word)
        distractors.extend(synonyms)
    
    # Lọc và loại bỏ các từ không hợp lý hoặc không liên quan
    distractors = [d for d in distractors if len(d) > 2 and d.isalpha()]
    distractors = list(set(distractors))  # loại bỏ trùng lặp
    distractors = random.sample(distractors, min(num_distractors, len(distractors)))
    
    # Đảm bảo các đáp án nhiễu có liên quan đến câu hỏi
    return distractors

# Khởi tạo Flask app
app = Flask(__name__)
CORS(app)  # Kích hoạt CORS cho toàn bộ ứng dụng Flask

@app.route('/qa/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    text = data.get('text', '')
    questions = data.get('questions', [])
    
    if not text or not questions:
        return jsonify({'error': 'Text and questions are required'}), 400
    
    quiz_questions = []
    
    for question in questions:
        # Lấy đáp án từ mô hình QA
        result = qa_pipeline(question=question.strip(), context=text)
        answer = result['answer']
        
        # Sinh đáp án nhiễu
        distractors = generate_distractors(answer, text)
        options = [answer] + distractors
        random.shuffle(options)  # Xáo trộn thứ tự đáp án
        
        # Thêm câu hỏi trắc nghiệm vào quiz_questions
        quiz_questions.append({
            'question': question.strip(),
            'options': options,
            'correct_answer': answer
        })
    
    return jsonify(quiz_questions)

if __name__ == '__main__':
    app.run(debug=True)
