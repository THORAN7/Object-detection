import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import tempfile

# Load a YOLO model (you can replace this with your own .pt file)
model = YOLO("yolov8n.pt")  # Downloaded automatically if not found

st.title("Object Detection with YOLOv8")
st.markdown("Upload an image and detect objects using YOLOv8")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Convert uploaded file to OpenCV format
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    # Run YOLO inference
    results = model(image)

    # Get rendered image (with boxes)
    rendered = results[0].plot()

    # Display
    st.image(rendered, caption="Detected Objects", channels="BGR")
