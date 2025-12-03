Shipping Label OCR Extraction System

Project Overview

This project implements an automated Optical Character Recognition (OCR) system designed to extract specific tracking IDs from shipping label images. The system is engineered to handle real-world challenges such as rotated text, low-contrast/faded labels, and noisy backgrounds.

The core objective is to extract text lines containing the specific pattern _1_ (e.g., 163233702292313922_1_1wv) with high precision, filtering out barcodes and unrelated text.

Key Features

Robust OCR Engine: Built on PaddleOCR (v2.7.3), optimized for document text detection.

Smart Preprocessing:

Multi-Angle Scanning: Automatically checks 0°, 90°, and -90° rotations to handle vertical text.

Adaptive Binarization: Applies Otsu's thresholding to recover text from faded/thermal labels.

Padding Protection: Adds whitespace borders to prevent text near edges from being cut off during rotation.

Intelligent Extraction Logic:

Dual-Mode Regex: Prioritizes strict pattern matching (Middle _1_) but falls back to loose matching (End _1) if necessary.

Auto-Correction: Automatically fixes common OCR character confusions (e.g., 0 vs o, 1 vs I) using context-aware logic.

Interactive UI: A Streamlit-based web interface for easy drag-and-drop testing.

Technical Stack

Language: Python 3.8+

OCR Framework: PaddleOCR (CPU-optimized for stability)

Computer Vision: OpenCV (for image preprocessing)

Frontend: Streamlit

Data Handling: Pandas (for accuracy benchmarking)

Installation & Setup

Prerequisites

Ensure you have Python installed. It is recommended to use a virtual environment.

1. Clone the Repository

git clone <your-github-repo-link>
cd shipping-label-ocr


2. Create Virtual Environment

# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate


3. Install Dependencies

Critical: This project relies on specific library versions to ensure stability on Windows.

pip install -r requirements.txt


Usage Guide

Option 1: Run the Web App (Interactive Mode)

To test individual images visually:

# Run using the startup script (Recommended for Windows to prevent crashes)
run_app.bat

# OR manually via terminal
streamlit run src/app.py


The application will launch in your browser at http://localhost:8501.

Option 2: Run Accuracy Benchmark (Batch Mode)

To validate the model against the ground truth dataset:

Ensure your test images are in the test_images folder.

Ensure Testcheck.csv is in the root directory.

Run the benchmark script:

python benchmark.py


This will generate a detailed report in results/final_accuracy_report.csv.

Performance Report

The model has been validated against a test dataset of 27 real-world shipping labels.

Metric

Value

Total Images

27

Correctly Extracted

21

Accuracy

~77.78%

Target Requirement

> 75%

Key Success Cases:

Vertical Text: Successfully extracts IDs printed vertically on the side of labels.

Faded Text: Accurately reads IDs from thermal labels with low ink density.

Lookalikes: Distinguishes between 1 and l and corrects 0 to o in text contexts.

Project Structure

shipping-label-ocr/
├── src/
│   ├── __init__.py
│   ├── app.py              # Frontend: Streamlit Web Interface
│   ├── ocr_engine.py       # Core Logic: OCR Class, Regex, and Heuristics
│   ├── preprocessing.py    # Utilities: Image Rotation, Binarization, Padding
├── test_images/            # Dataset: Folder containing waybill images
├── results/
│   └── final_accuracy_report.csv  # Output: Generated accuracy metrics
├── benchmark.py            # Script: Runs validation against ground truth
├── requirements.txt        # Config: Project dependencies
├── run_app.bat             # Config: Windows startup script (Prevents crashes)
├── Testcheck.csv           # Data: Ground Truth CSV for benchmarking
└── README.md               # Documentation


Code Module Breakdown

1. Core Logic (src/ocr_engine.py)

This is the brain of the application. It initializes the PaddleOCR model and orchestrates the extraction process.

OCREngine Class: Manages the OCR session.

extract_text(): Iterates through image rotations (0°, 90°, -90°) and preprocessing variations to find the best text candidate.

_extract_candidate(): Applies regex patterns to validate extracted text. It prioritizes the "Strict" pattern (Digits + Marker + Suffix) and falls back to "Loose" (Ends with Marker) if needed.

Error Handling: Configured to run on CPU to avoid "OneDNN" crashes on standard Windows environments.

2. Image Processing (src/preprocessing.py)

Handles visual data preparation to maximize OCR accuracy.

add_padding(): Adds a white border to images. This is critical for vertical labels where text touching the edge might get cropped during rotation.

preprocess_image(): Generates multiple versions of the input image:

Standard: Resized to 1600px width.

Binarized: Converted to Black & White using thresholding (fixes faded text).

Contrast Enhanced: CLAHE applied for low-light conditions.

3. Benchmarking (benchmark.py)

Automates the validation process.

Loads the Ground Truth CSV (Testcheck.csv).

Iterates through every image in the test_images folder.

Compares the model's output against the expected ID.

Generates a PASS/FAIL report and calculates the final accuracy percentage.

4. Frontend (src/app.py)

Provides a user-friendly interface using Streamlit.

Allows file upload (JPG, PNG).

Visualizes the extraction result and the processed image used by the OCR engine.

Troubleshooting

Issue: "Black Screen" or app hanging on startup.
Fix: This is caused by PaddleOCR waiting for a GPU. Use the run_app.bat script, which forces CPU mode and disables conflicting Intel drivers.

Issue: "ModuleNotFoundError: No module named 'src'"
Fix: Ensure you are running python scripts from the root directory, or use python -m src.app.