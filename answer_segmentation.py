import os

# =========================
# PATHS
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.join(BASE_DIR, "ocr_output_txtdoc", "ocr_output.txt")
output_folder = os.path.join(BASE_DIR, "segmented_answers")

os.makedirs(output_folder, exist_ok=True)

# =========================
# QUESTION KEYWORDS
# =========================

QUESTION_KEYWORDS = [
    "what", "describe", "explain", "list", "why", "when", "where",
    "state", "define", "compare", "differentiate", "how",
    "give", "write"
]

# =========================
# DETECT QUESTION ANYWHERE
# =========================

def is_question_line(line):
    clean = line.strip().lower()

    if len(clean) < 8:
        return False

    if clean.endswith("?"):
        return True

    for word in QUESTION_KEYWORDS:
        if clean.startswith(word):
            return True

    return False

# =========================
# SPLIT INTO PAGES
# =========================

def split_pages(lines):
    pages = []
    current = []

    for line in lines:
        if "=====" in line:
            if current:
                pages.append(current)
                current = []
        else:
            current.append(line.strip())

    if current:
        pages.append(current)

    return pages

# =========================
# CORE LOGIC (IMPORTANT)
# =========================

def extract_qa_from_page(page_lines):
    segments = []

    current_question = None
    current_answer = []

    for line in page_lines:

        if not line.strip():
            continue

        # 🔥 Detect new question ANYWHERE
        if is_question_line(line):

            # Save previous QA
            if current_question and current_answer:
                segments.append((current_question, "\n".join(current_answer)))

            current_question = line
            current_answer = []

        else:
            if current_question:
                current_answer.append(line)

    # Save last one
    if current_question and current_answer:
        segments.append((current_question, "\n".join(current_answer)))

    return segments

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    print("\n========== ADVANCED SEGMENTATION ==========\n")

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    pages = split_pages(lines)

    all_segments = []

    for page in pages:

        segments = extract_qa_from_page(page)

        # 🔥 HANDLE NO QUESTION CASE (fallback)
        if not segments:
            text = "\n".join(page).strip()
            if len(text) > 30:
                all_segments.append((page[0], text))
        else:
            all_segments.extend(segments)

    # =========================
    # SAVE FILES
    # =========================

    saved_count = 0

    for i, (question, answer) in enumerate(all_segments, start=1):

        if len(answer.strip()) < 30:
            continue

        output_path = os.path.join(output_folder, f"Question_{i}.txt")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("QUESTION:\n")
            f.write(question + "\n\n")
            f.write("ANSWER:\n")
            f.write(answer)

        print("Saved:", f"Question_{i}.txt")
        saved_count += 1

    print(f"\nSegmentation completed successfully! {saved_count} answers saved.\n")