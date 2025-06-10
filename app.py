import streamlit as st
from PIL import Image
import torch
import os
from pathlib import Path
import tempfile

# Load YOLOv5 model from the cloned yolov5 directory
@st.cache_resource
def load_model():
    model = torch.hub.load('yolov5', 'yolov5s', source='local', force_reload=True)
    return model

model = load_model()

st.title("YOLOv5 Object Detection")
st.write("Upload an image and detect objects using YOLOv5.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Save the uploaded image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name)
        image_path = tmp.name

    # Perform object detection
    results = model(image_path)

    # Render results
    results.render()
    detected_image = Image.fromarray(results.ims[0])

    st.image(detected_image, caption='Detected Image', use_column_width=True)

    # Show detected labels
    st.write("Detected objects:")
    st.json(results.pandas().xyxy[0].to_dict(orient="records"))
