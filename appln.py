# ---------------- app.py ----------------
import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file

app = Flask(__name__)
app.secret_key = "supersecretkey"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- FOLDERS ----------------
UPLOAD_FOLDER = os.path.join(BASE_DIR, "images", "input")
MODEL_ANSWER_FOLDER = os.path.join(BASE_DIR, "model_answers")
REPORT_FOLDER = os.path.join(BASE_DIR, "final_report")

PDF_PATH = os.path.join(REPORT_FOLDER, "Final_Report.pdf")
EXCEL_PATH = os.path.join(REPORT_FOLDER, "Final_Report.xlsx")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_ANSWER_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- UPLOAD FILES ----------------
@app.route("/upload", methods=["POST"])
def upload_files():
    try:
        if "student_files" not in request.files or "model_file" not in request.files:
            flash("❌ Upload both student answers and model answer!", "error")
            return redirect(url_for("index"))

        student_files = request.files.getlist("student_files")
        model_file = request.files["model_file"]

        # -------- Clear old files --------
        for folder in [UPLOAD_FOLDER, MODEL_ANSWER_FOLDER]:
            for f in os.listdir(folder):
                file_path = os.path.join(folder, f)
                try:
                    os.remove(file_path)
                except Exception:
                    pass

        # -------- Save student files --------
        saved_count = 0
        for file in student_files:
            if file and file.filename.strip():
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
                saved_count += 1

        # -------- Save model file --------
        if model_file and model_file.filename.strip():
            model_path = os.path.join(MODEL_ANSWER_FOLDER, "model_answers.txt")
            model_file.save(model_path)
        else:
            flash("❌ Model answer file missing!", "error")
            return redirect(url_for("index"))

        flash(f"✅ {saved_count} student files uploaded successfully!", "success")
        return redirect(url_for("index"))

    except Exception as e:
        flash(f"❌ Upload failed: {str(e)}", "error")
        return redirect(url_for("index"))


# ---------------- RUN EVALUATION ----------------
@app.route("/evaluate", methods=["POST"])
def evaluate():
    try:
        subprocess.run(["python", "run_pipeline.py"], check=True)

        return jsonify({
            "status": "done",
            "message": "✅ Evaluation completed successfully!"
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "message": f"❌ Pipeline failed: {str(e)}"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"❌ Unexpected error: {str(e)}"
        })


# ---------------- DOWNLOAD REPORTS ----------------
@app.route("/download/pdf")
def download_pdf():
    if os.path.exists(PDF_PATH):
        return send_file(PDF_PATH, as_attachment=True)
    return "❌ PDF file not found!", 404


@app.route("/download/excel")
def download_excel():
    if os.path.exists(EXCEL_PATH):
        return send_file(EXCEL_PATH, as_attachment=True)
    return "❌ Excel file not found!", 404


# ---------------- RESET SYSTEM ----------------
@app.route("/reset", methods=["POST"])
def reset_system():
    try:
        for folder in [UPLOAD_FOLDER, MODEL_ANSWER_FOLDER, REPORT_FOLDER]:
            for f in os.listdir(folder):
                file_path = os.path.join(folder, f)
                try:
                    os.remove(file_path)
                except Exception:
                    pass

        return jsonify({
            "status": "reset_done",
            "message": "System reset successful!"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)