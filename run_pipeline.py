# ---------------- run_pipeline.py ----------------
import os
import subprocess
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from hybrid_scores import (
    load_model_answers,
    load_student_answers,
    evaluate_all_questions
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_FOLDER = os.path.join(BASE_DIR, "final_report")
os.makedirs(REPORT_FOLDER, exist_ok=True)


# ---------------- 🔥 NEW: Trim Function ----------------
def trim_answer(text, word_limit=15):
    if not text or text == "Not Answered":
        return text

    words = text.split()
    if len(words) <= word_limit:
        return text

    return " ".join(words[:word_limit]) + "..."


# ---------------- Run external scripts ----------------
def run_script(script_name):
    print(f"Running {script_name}...")
    subprocess.run(["python", script_name], check=True)


# ---------------- Collect scores ----------------
def collect_scores(model_file, student_file, top_n=10):

    model_answers = load_model_answers(model_file)
    student_answers = load_student_answers(student_file)

    if not student_answers:
        print("No student answers found.")
        return []

    results_dict = evaluate_all_questions(
        student_answers,
        model_answers,
        top_n=top_n
    )

    results = []

    for qnum in sorted(results_dict.keys(), key=lambda x: int(x[1:])):
        q_data = results_dict[qnum]

        # 🔥 APPLY TRIM HERE
        student_ans = trim_answer(q_data.get("student_answer", "Not Answered"))

        results.append([
            qnum,
            student_ans,
            round(q_data.get("keyword_score", 0), 2),
            round(q_data.get("similarity_score", 0), 2),
            q_data.get("hybrid_score", 0),
            q_data.get("feedback", "")
        ])

    return results


# ---------------- Export Excel ----------------
def export_excel(results):
    df = pd.DataFrame(results, columns=[
        "Q No",
        "Student Answer",
        "Keyword Marks (/2)",
        "Similarity Marks (/2)",
        "Hybrid Marks (/2)",
        "Feedback"
    ])

    excel_path = os.path.join(REPORT_FOLDER, "Final_Report.xlsx")
    df.to_excel(excel_path, index=False)

    print("Excel Report Saved:", excel_path)


# ---------------- Export PDF ----------------
def export_pdf(results):
    pdf_path = os.path.join(REPORT_FOLDER, "Final_Report.pdf")
    doc = SimpleDocTemplate(pdf_path)

    elements = []
    style = getSampleStyleSheet()

    elements.append(Paragraph(
        "<b>Handwritten Answer Evaluation Report</b>",
        style["Title"]
    ))
    elements.append(Spacer(1, 0.3 * inch))

    table_data = [[
        "Q No", "Student Answer", "Keyword /2",
        "Similarity /2", "Hybrid /2", "Feedback"
    ]]

    for row in results:
        wrapped_row = [
            Paragraph(str(row[0]), style["Normal"]),
            Paragraph(str(row[1]), style["Normal"]),
            Paragraph(str(row[2]), style["Normal"]),
            Paragraph(str(row[3]), style["Normal"]),
            Paragraph(str(row[4]), style["Normal"]),
            Paragraph(str(row[5]), style["Normal"])
        ]
        table_data.append(wrapped_row)

    table = Table(table_data, colWidths=[40, 140, 60, 60, 60, 180])

    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ])

    elements.append(table)
    doc.build(elements)

    print("PDF Report Saved:", pdf_path)


# ---------------- MAIN PIPELINE ----------------
if __name__ == "__main__":

    print("\n========== STARTING FULL PIPELINE ==========\n")

    run_script("preprocessing.py")
    run_script("ocr_module.py")
    run_script("answer_segmentation.py")
    run_script("postprocessing.py")

    model_file = os.path.join(BASE_DIR, "model_answers", "model_answers.txt")
    student_file = os.path.join(BASE_DIR, "post_processed_text", "student_postprocessed.txt")

    results = collect_scores(model_file, student_file, top_n=10)

    if not results:
        print("No results found.")
        exit()

    export_excel(results)
    export_pdf(results)

    print("\n========== PIPELINE COMPLETED SUCCESSFULLY ==========\n")