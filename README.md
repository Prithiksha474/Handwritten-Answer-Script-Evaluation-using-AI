**Handwritten Answer Script Evaluation Using Artificial Intelligence
Overview**

The Handwritten Answer Script Evaluation System is an AI-powered application designed to automate the evaluation of handwritten subjective answer sheets. The system uses Optical Character Recognition (OCR) and Natural Language Processing (NLP) techniques to extract, process, and evaluate handwritten answers against model answers, reducing manual grading effort and improving consistency.

**Features**
Upload handwritten answer sheets in image or PDF format
Image preprocessing for improved OCR accuracy
Handwritten text extraction using OCR
Automatic question and answer segmentation
NLP-based text cleaning and preprocessing
Hybrid evaluation using:
Keyword Matching
Semantic Similarity Analysis
Automated score generation with feedback
PDF and Excel report generation
User-friendly web interface built with Flask
System Workflow
Upload Answer Scripts
Image Preprocessing
OCR Text Extraction
Question & Answer Segmentation
Text Preprocessing
Answer Evaluation
Report Generation

**Technologies Used
**
Frontend**
HTML
CSS

**Backend**
Python
Flask

**Libraries & Frameworks**
OpenCV
EasyOCR
NLTK
Scikit-learn
Pandas
ReportLab
pdf2image
RapidFuzz
NumPy

**Evaluation Methodology**

**Keyword Matching**
Extracts important keywords from model answers
Compares student responses using fuzzy matching
Assigns marks based on keyword coverage

**Semantic Similarity**
Uses TF-IDF Vectorization
Calculates Cosine Similarity between model and student answers
Evaluates conceptual understanding
Hybrid Scoring

**Final Score = 40% Keyword Matching + 60% Semantic Similarity**

**Project Structure**

├── appln.py
├── run_pipeline.py
├── preprocessing.py
├── ocr_module.py
├── answer_segmentation.py
├── postprocessing.py
├── keyword_scores.py
├── similarity_scores.py
├── hybrid_scores.py
├── templates/
├── images/
├── model_answers/
├── final_report/
└── requirements.txt

**Output**

The system generates:
Question-wise evaluation scores
Feedback for each answer
PDF Evaluation Report
Excel Evaluation Report

**Authors**
Developed as an academic project to demonstrate the application of Artificial Intelligence, OCR, and NLP in automated educational assessment systems
