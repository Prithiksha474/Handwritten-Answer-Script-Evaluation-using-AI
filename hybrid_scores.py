# ---------------- hybrid_scores.py ----------------
import re
from keyword_scores import evaluate_all_questions as keyword_all, extract_keywords, preprocess_text
from similarity_scores import compute_similarity
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

# ---------------- Normalize ----------------
def normalize_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return " ".join(text.lower().split())

# ---------------- Round only final score ----------------
def round_to_half(score: float) -> float:
    return round(score * 2) / 2

# ---------------- Load Model Answers ----------------
def load_model_answers(model_file: str) -> dict:
    with open(model_file, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(r"(Q\d+)[\.\:]?\s*")
    splits = pattern.split(content)

    model_answers = {}
    for i in range(1, len(splits), 2):
        qnum = splits[i].strip()
        ans_text = splits[i + 1].strip().replace("\n", " ")
        model_answers[qnum] = ans_text

    return model_answers

# ---------------- Load Student Answers ----------------
def load_student_answers(student_file: str) -> dict:
    with open(student_file, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(r"(Q\d+)[\.\:]?\s*(.*?)(?=(Q\d+[\.\:]?\s*|$))", re.DOTALL)
    matches = pattern.findall(content)

    student_answers = {}
    for match in matches:
        qnum = match[0].strip()
        block = match[1].strip().replace("\n", " ")
        if block:
            student_answers[qnum] = block

    return student_answers

# ---------------- Match Questions using Similarity ----------------
def match_questions(student_answers: dict, model_answers: dict):
    mapping = {}

    for s_q, s_text in student_answers.items():
        best_match = None
        best_score = -1

        for m_q, m_text in model_answers.items():
            score = compute_similarity(s_text, m_text)

            if score is not None and score > best_score:
                best_score = score
                best_match = m_q

        mapping[s_q] = best_match

    return mapping

# ---------------- Missing Keywords ----------------
def get_missing_keywords(student_text: str, model_text: str, top_n: int = 10):
    keywords = extract_keywords(model_text, top_n)
    student_words = preprocess_text(student_text)

    missing = []

    for kw in keywords:
        kw_words = preprocess_text(kw)

        meaningful_words = [
            w for w in kw_words
            if w not in stop_words and len(w) > 2
        ]

        if not meaningful_words:
            continue

        if not any(word in student_words for word in meaningful_words):
            missing.append(" ".join(meaningful_words))

    return missing

# ---------------- Feedback ----------------
def generate_feedback(score: float, missing_keywords: list) -> str:
    if score >= 2:
        base = "Excellent answer, covers almost all key points."
    elif score >= 1.5:
        base = "Good answer, minor points missing."
    elif score >= 1:
        base = "Partial answer, improvement needed."
    elif score >= 0.5:
        base = "Very limited answer."
    else:
        base = "No meaningful answer provided."

    if missing_keywords:
        missing_str = ", ".join(missing_keywords[:4])
        base += f" Missing keywords: {missing_str}."

    return base

# ---------------- Hybrid Evaluation ----------------
def evaluate_all_questions(student_answers: dict, model_answers: dict, top_n: int = 10) -> dict:

    results = {}
    seen_answers = {}

    # 🔥 Step 1: Match questions
    mapping = match_questions(student_answers, model_answers)

    # 🔥 Step 2: Prepare mapped answers for keyword scoring
    mapped_student_answers = {}
    mapped_model_answers = {}

    for s_q, m_q in mapping.items():
        if m_q:
            mapped_student_answers[m_q] = student_answers[s_q]
            mapped_model_answers[m_q] = model_answers[m_q]

    keyword_scores = keyword_all(mapped_student_answers, mapped_model_answers, top_n)

    # 🔥 Step 3: Iterate MODEL QUESTIONS (IMPORTANT FIX)
    for m_q in sorted(model_answers.keys(), key=lambda x: int(x[1:])):

        model_text = model_answers[m_q]

        # 🔍 find mapped student answer
        student_q = None
        for s_q, mapped_q in mapping.items():
            if mapped_q == m_q:
                student_q = s_q
                break

        # ❌ Not Answered
        if not student_q:
            results[m_q] = {
                "student_answer": "Not Answered",
                "keyword_score": 0,
                "similarity_score": 0,
                "hybrid_score": 0,
                "feedback": "Question not answered"
            }
            continue

        student_text = student_answers[student_q]
        normalized = normalize_text(student_text)

        # 🔁 Duplicate detection
        if normalized in seen_answers:
            original_q = seen_answers[normalized]

            results[m_q] = {
                "student_answer": student_text,
                "keyword_score": 0,
                "similarity_score": 0,
                "hybrid_score": 0,
                "feedback": f"Duplicate answer (same as {original_q})"
            }
            continue

        seen_answers[normalized] = student_q

        # ---------------- Scores ----------------
        k_score = keyword_scores.get(m_q, 0)
        s_score = compute_similarity(student_text, model_text) or 0

        hybrid_raw = min(0.4 * k_score + 0.6 * s_score, 2)
        hybrid = round_to_half(hybrid_raw)

        # ---------------- Missing Keywords ----------------
        missing = get_missing_keywords(student_text, model_text, top_n)

        # ---------------- Feedback ----------------
        feedback = generate_feedback(hybrid, missing)

        results[m_q] = {
            "student_answer": student_text,
            "keyword_score": round(k_score, 2),
            "similarity_score": round(s_score, 2),
            "hybrid_score": hybrid,
            "feedback": feedback
        }

    return results