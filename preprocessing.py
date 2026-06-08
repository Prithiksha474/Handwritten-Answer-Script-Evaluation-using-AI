import os
import cv2
import numpy as np
from pdf2image import convert_from_path

# ==============================
# 🔹 SET YOUR POPPLER PATH HERE
# ==============================
POPPLER_PATH = r"C:/Users/prith/Downloads/Release-25.12.0-0/poppler-25.12.0/Library/bin"

# ==============================
# 🔹 INPUT & OUTPUT FOLDERS
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_folder = os.path.join(BASE_DIR, "images", "input")
output_folder = os.path.join(BASE_DIR, "images", "output")

os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# ==============================
# 🔹 IMAGE PREPROCESSING FUNCTION
# ==============================
def preprocess_image(img, output_path):
    if img is None:
        print(f"Skipping invalid image.")
        return

    h, w = img.shape[:2]

    # Resize if width < 1200px
    if w < 1200:
        scale = 1200 / w
        img = cv2.resize(img, None, fx=scale, fy=scale)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Slight blur for OCR improvement
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Optional: threshold (uncomment if needed)
    # gray = cv2.adaptiveThreshold(
    #     gray, 255,
    #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #     cv2.THRESH_BINARY,
    #     11, 2
    # )

    cv2.imwrite(output_path, gray)
    print(f"Processed: {output_path}")


# ==============================
# 🔹 PDF PROCESSING FUNCTION
# ==============================
def process_pdf(pdf_path):
    print(f"Processing PDF: {pdf_path}")

    try:
        pages = convert_from_path(
            pdf_path,
            dpi=300,
            poppler_path=POPPLER_PATH
        )
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for i, page in enumerate(pages):
        # Convert PIL → OpenCV format
        img = np.array(page)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        output_path = os.path.join(
            output_folder,
            f"{base_name}_page_{i+1}.jpg"
        )

        preprocess_image(img, output_path)


# ==============================
# 🔹 MAIN LOOP
# ==============================
def main():
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # -------- IMAGE FILES --------
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            img = cv2.imread(input_path)

            if img is None:
                print(f"Skipping: {input_path}")
                continue

            output_path = os.path.join(output_folder, filename)
            preprocess_image(img, output_path)

        # -------- PDF FILES --------
        elif filename.lower().endswith(".pdf"):
            process_pdf(input_path)

        else:
            print(f"Unsupported file type: {filename}")


# ==============================
# 🔹 RUN SCRIPT
# ==============================
if __name__ == "__main__":
    main()