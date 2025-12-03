import os
import cv2
import re
from paddleocr import PaddleOCR
from src.preprocessing import preprocess_image

class OCREngine:
    def __init__(self):
        """Initialize OCR engine."""
        print("Initializing OCR engine...")
        # Minimal arguments to avoid environment conflicts
        self.ocr = PaddleOCR(
            use_angle_cls=False,
            lang="en",
            use_gpu=False,
            show_log=False,
        )
        print("OCR engine started.")

    def _extract_candidate(self, text):
        """
        Extract ID using regex.
        Returns cleaned ID string or None.
        """
        # Normalize separators to single space
        clean_text = text.replace("-", " ").replace(".", " ").replace("_", " ")

        # Strict pattern: digits + marker + suffix
        pattern_strict = re.compile(r"(\d{8,})\s+([1lI|])\s+(.+)", re.IGNORECASE)
        m = pattern_strict.search(clean_text)
        if m:
            main_id = m.group(1)
            suffix = m.group(3).strip()
            # Minor correction: likely 'o' instead of '0' in alpha contexts
            if re.search(r"[a-z]0[a-z]", suffix):
                suffix = suffix.replace("0", "o")
            return f"{main_id}_1_{suffix}"

        # Loose fallback: ends with marker
        pattern_loose = re.compile(r"(\d{8,})\s+([1lI|])$", re.IGNORECASE)
        m2 = pattern_loose.search(clean_text)
        if m2:
            return f"{m2.group(1)}_1"

        return None

    def extract_text(self, image_path):
        """
        Run OCR on image and return best candidate ID and the image used.
        Returns (id_str, image) or (None, original_image).
        """
        original_image = cv2.imread(image_path)
        if original_image is None:
            return None, None

        candidates = []  # (id, confidence, image_variant)

        # Try multiple rotations
        for angle in (0, 90, -90):
            if angle == 0:
                rotated = original_image
            elif angle == 90:
                rotated = cv2.rotate(original_image, cv2.ROTATE_90_CLOCKWISE)
            else:
                rotated = cv2.rotate(original_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Generate preprocess variations (e.g., binary, contrast, etc.)
            variations = preprocess_image(rotated)

            for img_input in variations:
                result = self.ocr.ocr(img_input, cls=False)
                if not result or not result[0]:
                    continue

                for line in result[0]:
                    text = line[1][0]
                    confidence = line[1][1]
                    found_id = self._extract_candidate(text)
                    if found_id:
                        candidates.append((found_id, confidence, img_input))

        if not candidates:
            return None, original_image

        # Select highest-confidence candidate
        candidates.sort(key=lambda x: x[1], reverse=True)
        best_id, best_conf, best_img = candidates[0]
        return best_id, best_img
