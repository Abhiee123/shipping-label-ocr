import cv2
import numpy as np

def add_padding(img, border=100):
    return cv2.copyMakeBorder(
        img, border, border, border, border, 
        cv2.BORDER_CONSTANT, value=[255, 255, 255]
    )

def preprocess_image(img):
    
    variations = []
    
    # Standard (Resized)
    h, w = img.shape[:2]
    target_w = 1600
    if w > target_w:
        scale = target_w / w
        img = cv2.resize(img, (target_w, int(h * scale)))
    
    # Base Padded Image
    padded = add_padding(img)
    variations.append(padded)
    
    # Convert to Gray for filters
    gray = cv2.cvtColor(padded, cv2.COLOR_BGR2GRAY)

    # Binarized (Black & White) -> Good for faded text
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    variations.append(cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR))

    # High Contrast (CLAHE) -> Good for low light / shadows
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    contrast = clahe.apply(gray)
    variations.append(cv2.cvtColor(contrast, cv2.COLOR_GRAY2BGR))

    # Erosion (Thinned Text) -> Good if letters are "bleeding" into each other (like 'rn' vs 'm')
    kernel = np.ones((2,2), np.uint8)
    eroded = cv2.erode(binary, kernel, iterations=1)
    variations.append(cv2.cvtColor(eroded, cv2.COLOR_GRAY2BGR))

    # Dilation (Thickened Text) -> Good for broken/dotty text
    dilated = cv2.dilate(binary, kernel, iterations=1)
    variations.append(cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR))
    
    return variations