import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image

# Load model by name, autohandles downloading weights
model = YOLO("yolov8n")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    results = model(image_np)
    st.image(results[0].plot(), caption="Detected Objects", use_column_width=True)
