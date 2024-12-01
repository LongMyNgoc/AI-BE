from transformers import pipeline
import nltk

# Tải mô hình QA
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

# Tải WordNet
nltk.download('wordnet')
