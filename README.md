# Object Detection Studio

Modern Streamlit app for running YOLOv8 object detection on uploaded images.

## Features

- Polished glassmorphism-style UI with animated ambient background
- Real-time object detection with YOLOv8
- Adjustable confidence and IoU thresholds
- Side-by-side original and annotated image previews
- Cached model loading for optimal performance

## Requirements

- Python 3.10+
- Packages listed in `requirements.txt`

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the app

From the project directory, simply run:

```powershell
streamlit run app.py
```

If `streamlit` is not on your PATH, use:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The app will open automatically at `http://localhost:8501` in your browser.

## Usage

1. Upload an image (JPG, PNG, or JPEG)
2. Adjust detection controls in the sidebar:
   - **Confidence threshold**: Lower for more detections, higher for stricter filtering
   - **IoU threshold**: Adjusts non-maximum suppression
   - **Image size**: Model input resolution (320/416/640/960px)
3. View results with original and annotated images side-by-side

## Notes

- The model (`yolov8n.pt`, ~6.3 MB) will be automatically downloaded on the first run
- To use a different YOLO model, update `load_model()` in `app.py` (e.g., `YOLO("yolov8s.pt")`)

