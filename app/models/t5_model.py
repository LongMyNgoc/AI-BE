import random
from nltk.tokenize import word_tokenize
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Tải mô hình T5
model_name = "valhalla/t5-small-qg-prepend"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def extract_answer(context):
    words = [word for word in word_tokenize(context) if word.isalnum()]
    if not words:
        return None
    important_words = [word for word in words if word.lower() not in [
        'the', 'a', 'of', 'and', 'in', 'to', 'from', 'is', 'are', 'on', 'am', 'an', 'was', 'were', 'had', 'have', 'has']]
    if important_words:
        return random.choice(important_words)
    return random.choice(words)

def generate_question(context):
    input_text = f"generate question: {context}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    try:
        outputs = model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)
        question = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return question.strip()
    except Exception as e:
        print(f"Error generating question: {e}")
        return None

def generate_distractors(answer, sentences):
    distractors = set()
    for sentence in sentences:
        words = [word for word in word_tokenize(sentence) if word.isalnum() and word.lower() != answer.lower()]
        distractors.update(words)
    distractors = list(distractors)
    random.shuffle(distractors)
    return distractors[:3]
