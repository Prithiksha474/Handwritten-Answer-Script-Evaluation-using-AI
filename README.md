**Handwritten Answer Script Evaluation Using Artificial Intelligence
Overview**

The Handwritten Answer Script Evaluation System is an AI-powered application designed to automate the evaluation of handwritten subjective answer sheets. The system uses Optical Character Recognition (OCR) and Natural Language Processing (NLP) techniques to extract, process, and evaluate handwritten answers against model answers, reducing manual grading effort and improving consistency.

**Features**
•	Upload handwritten answer sheets in image or PDF format
•	Image preprocessing for improved OCR accuracy
•	Handwritten text extraction using OCR
•	Automatic question and answer segmentation
•	NLP-based text cleaning and preprocessing
•	Hybrid evaluation using:
•	Keyword Matching
•	Semantic Similarity Analysis
•	Automated score generation with feedback
•	PDF and Excel report generation
•	User-friendly web interface built with Flask
•	System Workflow
•	Upload Answer Scripts
•	Image Preprocessing
•	OCR Text Extraction
•	Question & Answer Segmentation
•	Text Preprocessing
•	Answer Evaluation
•	Report Generation


**Technologies Used**

**Frontend**
•	HTML
•	CSS

**Backend**
•	Python
•	Flask

**Libraries & Frameworks**
•	OpenCV
•	EasyOCR
•	NLTK
•	Scikit-learn
•	Pandas
•	ReportLab
•	pdf2image
•	RapidFuzz

**Evaluation Methodology**

**Keyword Matching**
•	Extracts important keywords from model answers
•	Compares student responses using fuzzy matching
•	Assigns marks based on keyword coverage

**Semantic Similarity**
Uses TF-IDF Vectorization
•	Calculates Cosine Similarity between model and student answers
•	Evaluates conceptual understanding

**Hybrid Scoring
**Final Score = 40% Keyword Matching + 60% Semantic Similarity****

**Project Structure**
appln.py – Flask web application and user interface integration
run_pipeline.py – Main evaluation pipeline execution
preprocessing.py – Image preprocessing and enhancement
ocr_module.py – Handwritten text extraction using EasyOCR
answer_segmentation.py – Question and answer segmentation
postprocessing.py – NLP-based text cleaning and preprocessing
keyword_scores.py – Keyword matching evaluation
similarity_scores.py – Semantic similarity scoring using TF-IDF and Cosine Similarity
hybrid_scores.py – Hybrid scoring and feedback generation
templates/index.html – Frontend user interface
images/input – Uploaded handwritten answer scripts
images/output – Preprocessed images
model_answers – Reference/model answers
ocr_output_txtdoc – OCR extracted text files
segmented_answers – Segmented question-answer files
post_processed_text – NLP processed student answers
final_report – Generated PDF and Excel evaluation reports

**Output**

The system generates:
Question-wise evaluation scores
Feedback for each answer
PDF Evaluation Report
Excel Evaluation Report

**Authors**

Developed as an academic project to demonstrate the application of Artificial Intelligence, OCR, and NLP in automated educational assessment systems
