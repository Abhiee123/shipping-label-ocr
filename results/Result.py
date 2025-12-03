import os
import sys
import pandas as pd

# Add parent directory to path to allow importing from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ocr_engine import OCREngine

# Configuration
CSV_PATH = r"C:\Users\ABHI\Desktop\shipping-label-ocr\Testcheck.csv"
IMG_DIR = r"C:\Users\ABHI\Desktop\shipping-label-ocr\ReverseWay Bill-20251129T145929Z-1-001\ReverseWay Bill"

COL_FILENAME = "image name"
COL_TRUTH = "correct_id"

def normalize(text):
    """Standardize text for consistent comparison."""
    if pd.isna(text) or str(text).lower() == "nan":
        return "N/A"
    return str(text).strip().replace(" ", "")

def run_benchmark():
    # Verify input file exists
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        return

    print(f"Loading data from: {CSV_PATH}")
    
    try:
        df = pd.read_csv(CSV_PATH)
        df.columns = df.columns.str.strip()  # Clean headers
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Validate required columns
    if COL_FILENAME not in df.columns or COL_TRUTH not in df.columns:
        print("Error: Missing required columns.")
        print(f"Expected: '{COL_FILENAME}' and '{COL_TRUTH}'")
        return

    # Initialize OCR engine
    try:
        print("\nInitializing OCR engine...")
        engine = OCREngine()
        print("Engine loaded.")
    except Exception as e:
        print(f"Failed to load engine: {e}")
        return

    # Begin accuracy testing
    print("\nStarting accuracy test...")
    print("-" * 80)
    print(f"{'Filename':<35} | {'Status':<10} | {'Expected vs Predicted'}")
    print("-" * 80)

    results = []
    correct = 0
    total = 0

    for _, row in df.iterrows():
        fname = str(row[COL_FILENAME]).strip()
        expected = normalize(row[COL_TRUTH])
        img_path = os.path.join(IMG_DIR, fname)

        if not os.path.exists(img_path):
            print(f"{fname[:35]:<35} | MISSING    | Image not found")
            continue

        # Run OCR inference
        total += 1
        raw_pred, _ = engine.extract_text(img_path)
        predicted = normalize(raw_pred) if raw_pred else "N/A"

        # Check for exact or partial match
        is_match = (expected == predicted) or (expected in predicted)
        
        # Handle valid negatives (both N/A)
        if expected == "N/A" and predicted == "N/A":
            is_match = True

        if is_match:
            status = "PASS"
            correct += 1
        else:
            status = "FAIL"

        print(f"{fname[:35]:<35} | {status:<10} | Exp: {expected} | Got: {predicted}")

        results.append({
            "Filename": fname,
            "Status": status,
            "Expected": expected,
            "Predicted": predicted
        })

    # Generate final report
    if total > 0:
        acc = (correct / total) * 100
        print("\n" + "=" * 50)
        print(f"Final Accuracy: {acc:.2f}%")
        print(f"Passed: {correct} / {total}")
        print("=" * 50)
        
        # Export results to CSV
        os.makedirs("results", exist_ok=True)
        out_path = "results/final_accuracy_report.csv"
        pd.DataFrame(results).to_csv(out_path, index=False)
        print(f"\nReport saved to: {out_path}")
    else:
        print("No images were processed.")

if __name__ == "__main__":
    run_benchmark()