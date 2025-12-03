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

---

##  **Project Structure & Modules**

The codebase is modularized for maintainability and scalability:

```text


Core Logic Breakdown
ocr_engine.py: The brain of the application. It orchestrates the extraction process, iterates through image rotations, and applies regex validation.

Preprocessing Techniques
To maximize OCR accuracy, a robust image processing pipeline was implemented using OpenCV:

Multi-Angle Scanning: The system iteratively rotates the image at 0°, 90°, and -90°. This effectively handles vertically printed text on shipping labels without requiring a complex orientation detection model.

Adaptive Binarization: Otsu's thresholding is applied to convert the image to high-contrast black and white. This is critical for recovering text from faded thermal labels where ink density is low.

Padding: A white border is added around the image before rotation. This prevents text located at the extreme edges of the label from being cut off during the rotation process.

Text Extraction Logic
A intelligent regex-based filtering system is used to identify the correct ID among all text detected:

Dual-Mode Regex:

Strict Mode: Searches for the pattern Digits + Marker + Suffix (e.g., 12345_1_abc). This is the priority match.

Loose Mode: A fallback pattern that looks for IDs ending in _1.

Contextual Correction: A post-processing step fixes common OCR character confusions based on context. For example, if the digit 0 appears surrounded by letters in the suffix, it is automatically corrected to the letter o.

5. Accuracy Calculation Methodology
Accuracy is calculated by comparing the model's extracted output against a manually verified "Ground Truth" CSV file.

Formula: Accuracy = (Total Correct Matches / Total Images) * 100

Match Criteria: A match is considered "Correct" if the expected ground truth ID is exactly present within the extracted text string. Valid negatives (where both ground truth and prediction are "N/A") are also counted as correct.


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

Future Improvements
GPU Acceleration: Enable CUDA support for faster processing on supported hardware to reduce inference time per image.

Deep Learning Classification: Train a lightweight classifier (e.g., MobileNet) to detect the label type before extraction, allowing for more specific region-of-interest targeting.

API Deployment: Wrap the engine in a FastAPI or Flask service to allow for programmatic access and integration into larger logistical systems.
