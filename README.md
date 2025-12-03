<h1 align="center"> Shipping Label OCR Extraction System </h1>

<p align="center">
  <i>An automated Optical Character Recognition (OCR) system designed to extract specific tracking IDs from shipping label images.</i>
</p>

---

## **Project Overview**

Efficient data extraction from logistics documents is critical for supply chain automation.
This project implements a robust system to handle real-world challenges such as **rotated text, low-contrast/faded labels, and noisy backgrounds**.

The core objective is to extract text lines containing specific patterns (e.g., `163233702292313922_1_1wv`) with high precision, filtering out barcodes and unrelated text using **PaddleOCR** and intelligent preprocessing.

---

## **Objective**

The main goal of this project is to build an **automated extraction engine** that:
- Detects text regardless of orientation (0°, 90°, -90°)
- Recovers readable text from faded or thermal labels
- Distinguishes between similar characters (e.g., `1` vs `l`, `0` vs `o`)
- Provides an interactive interface for testing and validation

---

## **System Capabilities**

The system utilizes advanced preprocessing and logic to ensure accuracy. Key features include:

| Feature | Description |
|----------|-------------|
| **Robust OCR Engine** | Built on **PaddleOCR (v2.7.3)**, optimized for document text detection. |
| **Multi-Angle Scanning** | Automatically checks **0°, 90°, and -90°** rotations to handle vertical text. |
| **Adaptive Binarization** | Applies **Otsu's thresholding** to recover text from faded/thermal labels. |
| **Padding Protection** | Adds whitespace borders to prevent edge-text cropping during rotation. |
| **Dual-Mode Regex** | Prioritizes **Strict** pattern matching (Middle `_1_`) but falls back to **Loose** matching. |
| **Auto-Correction** | Context-aware logic to fix common OCR confusions (e.g., `0` vs `o`). |

---

##  **Project Structure & Modules**

The codebase is modularized for maintainability and scalability:

```text
shipping-label-ocr/
├── src/
│   ├── app.py             # Frontend: Streamlit Web Interface
│   ├── ocr_engine.py      # Core Logic: OCR Class, Regex, and Heuristics
│   ├── preprocessing.py   # Utilities: Image Rotation, Binarization, Padding
├── test_images/           # Dataset: Folder containing waybill images
├── results/               # Output: Generated accuracy metrics
├── benchmark.py           # Script: Runs validation against ground truth
├── run_app.bat            # Config: Windows startup script (Prevents crashes)
└── Testcheck.csv          # Data: Ground Truth CSV for benchmarking

Core Logic Breakdown
ocr_engine.py: The brain of the application. It orchestrates the extraction process, iterates through image rotations, and applies regex validation.

preprocessing.py: Handles visual data preparation, including resizing, contrast enhancement (CLAHE), and padding.

benchmark.py: Automates validation by comparing model output against the Testcheck.csv ground truth.

## **Performance Report**

The model was validated against a test dataset of real-world shipping labels to ensure reliability.

| Metric | Value |
|--------|-------|
| **Total Images** | 27 |
| **Correctly Extracted** | 21 |
| **Accuracy** | **~77.78%** |
| **Target Requirement** | > 75% |

**Key Success Cases:**
* **Vertical Text:** Successfully extracts IDs printed vertically on label edges.
* **Faded Text:** Accurately reads IDs from thermal labels with low ink density.
* **Lookalikes:** Distinguishes between `1` and `l` using context-aware logic.

---

## **Tech Stack**

| Category | Tools Used |
|-----------|-------------|
| **Language** | Python 3.8+ |
| **OCR Framework** | PaddleOCR (CPU-optimized) |
| **Computer Vision** | OpenCV |
| **Frontend** | Streamlit |
| **Data Handling** | Pandas |
| **Environment** | VS Code, Virtualenv |

---

## **Installation & Setup**

### **1. Clone the Repository**
```bash
git clone <your-github-repo-link>
cd shipping-label-ocr

# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
