import random
from collections import Counter
import spacy

# Kiểm tra và tải mô hình nếu chưa có
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def generate_mcqs(text, num_questions=5):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    selected_sentences = random.sample(sentences, min(num_questions, len(sentences)))
    mcqs = []
    for sentence in selected_sentences:
        sent_doc = nlp(sentence)
        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN"]
        if len(nouns) < 2:
            continue
        noun_counts = Counter(nouns)
        if noun_counts:
            subject = noun_counts.most_common(1)[0][0]
            question_stem = sentence.replace(subject, "__________")
            answer_choices = [subject]
            for _ in range(3):
                distractor = random.choice(list(set(nouns) - set([subject])))
                answer_choices.append(distractor)
            random.shuffle(answer_choices)

            # Thêm a,b,c,d trước đáp án
            answer_choices_with_labels = [
                f"{chr(97 + i)}. {answer_choices[i]}" for i in range(len(answer_choices))
            ]

            correct_answer = chr(97 + answer_choices.index(subject))  # Đáp án đúng (a,b,c,d)
            mcqs.append((question_stem, answer_choices_with_labels, correct_answer))
    return mcqs
