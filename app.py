import streamlit as st
from PIL import Image
import torch
import tempfile

# Load YOLOv5 model
@st.cache_resource
def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)
    return model

model = load_model()

st.title("YOLOv5 Object Detection")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_column_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        img.save(tmp.name)
        results = model(tmp.name)

    results.render()
    st.image(Image.fromarray(results.ims[0]), caption="Detected Objects", use_column_width=True)

    st.subheader("Detection Results")
    st.dataframe(results.pandas().xyxy[0])
