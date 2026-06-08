# similarity_scores.py

from typing import Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# ---------------- Preprocessing ----------------
def preprocess_text(text: str) -> str:
    words = re.findall(r'\w+', text.lower())
    lemmatized = [lemmatizer.lemmatize(w) for w in words]
    return " ".join(lemmatized)

# ---------------- Similarity ----------------
def compute_similarity(student_text: str, model_text: str) -> float:
    if not student_text or not student_text.strip():
        return None

    if not model_text.strip():
        return 0.0

    student_text = preprocess_text(student_text)
    model_text = preprocess_text(model_text)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        analyzer='char_wb',
        min_df=1
    )

    tfidf_matrix = vectorizer.fit_transform([student_text, model_text])
    sim_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    marks = sim_score * 2

    if marks < 0.1 and len(student_text.split()) >= 3:
        marks = 0.1

    # ❗ NO ROUNDING HERE
    return max(0.0, min(2.0, marks))

# ---------------- Evaluate ----------------
def evaluate_all_questions(student_answers: Dict, model_answers: Dict) -> Dict:
    results = {}

    for qnum in model_answers.keys():
        model_text = model_answers.get(qnum, "")
        student_text = student_answers.get(qnum, "")

        if not student_text or not student_text.strip():
            continue  # unattended handled in pipeline

        score = compute_similarity(student_text, model_text)

        if score is not None:
            results[qnum] = score

    return results