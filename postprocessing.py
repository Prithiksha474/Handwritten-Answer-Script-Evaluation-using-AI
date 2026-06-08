import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ---------------- NLTK downloads ----------------
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_folder = os.path.join(BASE_DIR, "segmented_answers")
output_file = os.path.join(BASE_DIR, "post_processed_text", "student_postprocessed.txt")

os.makedirs(os.path.dirname(output_file), exist_ok=True)

# ---------------- NLP tools ----------------
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    """Lowercase, remove punctuation, lemmatize, remove stopwords"""
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    words = nltk.word_tokenize(text)
    cleaned_words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words and len(word) > 2
    ]
    return " ".join(cleaned_words)

# ---------------- NATURAL SORT FUNCTION ----------------
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

# ---------------- Process all segmented answers ----------------
all_answers = []

for filename in sorted(os.listdir(input_folder), key=extract_number):
    if not filename.endswith(".txt"):
        continue

    input_path = os.path.join(input_folder, filename)

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into QUESTION / ANSWER if available
    parts = content.split("ANSWER:")

    if len(parts) == 2:
        question_part = parts[0].strip()
        answer_part = parts[1].strip()
        cleaned_answer = clean_text(answer_part)

        combined_text = question_part + "\n\nANSWER:\n" + cleaned_answer
        all_answers.append(combined_text)
    else:
        # If no ANSWER: found, just clean whole content
        cleaned_answer = clean_text(content)
        all_answers.append("ANSWER:\n" + cleaned_answer)

# ---------------- Write single post-processed file ----------------
with open(output_file, "w", encoding="utf-8") as f:
    for idx, ans_text in enumerate(all_answers, start=1):
        f.write(f"Q{idx}.\n\n")
        f.write(ans_text)
        f.write("\n\n")  # Separate answers

print(f"Post-processing completed! Single file created at:\n{output_file}")