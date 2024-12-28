from nltk.tokenize import sent_tokenize
from app.models.t5_model import extract_answer, generate_question, generate_distractors
import random

def create_mcq(context, sentences):
    answer = extract_answer(context)
    if not answer:
        return None, None, None
    question = generate_question(context)
    if not question:
        return None, None, None
    distractors = generate_distractors(answer, sentences)
    options = distractors + [answer]
    random.shuffle(options)
    return question, options, answer

def create_exam(paragraph):
    sentences = sent_tokenize(paragraph)
    exam = []
    for sentence in sentences:
        question, options, correct_answer = create_mcq(sentence, sentences)
        if question and correct_answer:
            exam.append({"question": question, "options": options, "correct_answer": correct_answer})
    return exam
