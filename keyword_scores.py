# keyword_scores.py

import re
from typing import Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from rapidfuzz import fuzz

lemmatizer = WordNetLemmatizer()

# ---------------- Text preprocessing ----------------
def preprocess_text(text: str) -> list:
    words = re.findall(r'\w+', text.lower())
    return [lemmatizer.lemmatize(w) for w in words]

# ---------------- Keyword extraction ----------------
def extract_keywords(model_text: str, top_n: int = 10) -> list:
    if not model_text.strip():
        return []
    
    vectorizer = TfidfVectorizer(stop_words=None, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([model_text])
    scores = tfidf_matrix.toarray()[0]
    terms = vectorizer.get_feature_names_out()
    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    return [term for term, score in ranked[:top_n]]

# ---------------- Keyword Coverage ----------------
def keyword_coverage(student_text: str, keywords: list) -> float:
    if not keywords or not student_text.strip():
        return 0.0

    student_words = preprocess_text(student_text)
    total_score = 0

    for kw in keywords:
        kw_words = preprocess_text(kw)
        word_scores = []

        for w in kw_words:
            best_match = max([fuzz.ratio(w, sw) for sw in student_words])
            word_scores.append(best_match / 100)

        keyword_score = sum(word_scores) / len(word_scores)
        total_score += keyword_score

    return total_score / len(keywords)

# ❗ NO ROUNDING HERE
def map_to_marks(coverage_fraction: float) -> float:
    return max(0.0, min(2.0, coverage_fraction * 2))

# ---------------- Evaluate ----------------
def evaluate_keyword_score(student_text: str, model_text: str, top_n: int = 10) -> float:
    if not student_text or not student_text.strip():
        return None

    keywords = extract_keywords(model_text, top_n)
    coverage = keyword_coverage(student_text, keywords)
    return map_to_marks(coverage)


# 🔹 UPDATED: safer, mapping-friendly version
def evaluate_all_questions(student_answers: Dict, model_answers: Dict, top_n: int = 10) -> Dict:
    results = {}

    for qnum in model_answers.keys():
        model_text = model_answers.get(qnum, "")
        student_text = student_answers.get(qnum, "")

        if not student_text or not student_text.strip():
            continue  # unattended handled in pipeline

        score = evaluate_keyword_score(student_text, model_text, top_n)

        if score is not None:
            results[qnum] = score

    return results