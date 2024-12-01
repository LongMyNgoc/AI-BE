import random
from nltk.corpus import wordnet
from app.models.qa_pipeline import qa_pipeline

# Hàm tìm từ đồng nghĩa
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

# Hàm sinh đáp án nhiễu
def generate_distractors(answer, context, num_distractors=3):
    distractors = []
    words = list(set(context.split()) - set(answer.split()))
    
    for word in words:
        synonyms = get_synonyms(word)
        distractors.extend(synonyms)
    
    distractors = [d for d in distractors if len(d) > 2 and d.isalpha()]
    distractors = list(set(distractors))
    distractors = random.sample(distractors, min(num_distractors, len(distractors)))
    return distractors

# Hàm sinh quiz
def generate_quiz_qa(text, questions):
    quiz_questions = []
    for question in questions:
        result = qa_pipeline(question=question.strip(), context=text)
        answer = result['answer']
        distractors = generate_distractors(answer, text)
        options = [answer] + distractors
        random.shuffle(options)
        
        quiz_questions.append({
            'question': question.strip(),
            'options': options,
            'correct_answer': answer
        })
    return quiz_questions
