import easyocr
import cv2
import re
import os

# Initialize EasyOCR reader once
reader = easyocr.Reader(['en'], gpu=False)

# INPUT & OUTPUT PATHS
#ocr is input is the preprocessed module output
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_folder = os.path.join(BASE_DIR, "images", "output")
output_folder = os.path.join(BASE_DIR, "ocr_output_txtdoc")

os.makedirs(output_folder, exist_ok=True)

output_text_file = os.path.join(output_folder, "ocr_output.txt")


def perform_ocr(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print(f"Skipping unreadable image: {image_path}")
        return []

    results = reader.readtext(
        img,
        detail=1,
        paragraph=False,
        text_threshold=0.65,
        low_text=0.4,
        link_threshold=0.4
    )

    # Sort top to bottom
    results = sorted(results, key=lambda x: x[0][0][1])

    lines = []
    current_line = []
    current_y = None
    y_threshold = 40

    for bbox, text, conf in results:

        if conf < 0.4 and len(text) > 3:
            continue

        if re.fullmatch(r"\d+", text):
            continue

        y = bbox[0][1]

        if current_y is None:
            current_y = y
            current_line.append((bbox[0][0], text))

        elif abs(y - current_y) < y_threshold:
            current_line.append((bbox[0][0], text))

        else:
            current_line.sort(key=lambda x: x[0])
            line_text = " ".join([w[1] for w in current_line])
            if len(line_text) > 3:
                lines.append(line_text)

            current_line = [(bbox[0][0], text)]
            current_y = y

    if current_line:
        current_line.sort(key=lambda x: x[0])
        line_text = " ".join([w[1] for w in current_line])
        if len(line_text) > 3:
            lines.append(line_text)

    return lines


# ---------------- MAIN EXECUTION ----------------

with open(output_text_file, "w", encoding="utf-8") as out_file:

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):

            image_path = os.path.join(input_folder, filename)
            print(f"Processing: {filename}")

            lines = perform_ocr(image_path)

            out_file.write(f"\n===== OCR OUTPUT FOR {filename} =====\n\n")
            for line in lines:
                out_file.write(line + "\n")

print("\n OCR completed for all images.")
print(f" OCR output saved at:\n{output_text_file}")
