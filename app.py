import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Waybill OCR", layout="wide")
st.title("Shipping Label ID Extractor")

# Debug Message
st.write("App interface loaded. Initializing OCR engine...")

# Load OCR Engine (cached to avoid reloading)
@st.cache_resource
def load_ocr_engine():
    from src.ocr_engine import OCREngine
    return OCREngine()

try:
    with st.spinner("Starting OCR Engine..."):
        engine = load_ocr_engine()
    st.success("OCR engine is ready.")
except Exception as e:
    st.error(f"Engine initialization failed: {e}")

# File Uploader
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    temp_filename = "temp_upload.jpg"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    col1, col2 = st.columns(2)

    # Display original image
    with col1:
        st.subheader("Original Image")
        st.image(uploaded_file, use_column_width=True)

    # Extract button
    if st.button("Extract ID"):
        with st.spinner("Processing..."):
            extracted_id, processed_img = engine.extract_text(temp_filename)

        with col2:
            st.subheader("Extraction Result")
            if extracted_id:
                st.success(f"ID: `{extracted_id}`")
                if processed_img is not None:
                    st.image(cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB))
            else:
                st.error("No valid ID found.")

    # Cleanup temporary file
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
