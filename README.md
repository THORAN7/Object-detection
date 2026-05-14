# 🎯 Object Detection Studio

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=220&color=0:0f172a,30:1d4ed8,70:6d28d9,100:06b6d4&text=Object%20Detection%20Studio&fontAlignY=38&fontSize=42&fontColor=e2e8f0&desc=YOLOv8%20%7C%20Streamlit%20%7C%20Modern%20AI%20UI&descAlignY=60&descSize=16&animation=fadeIn" alt="Object Detection Studio animated banner" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Inter&weight=600&size=22&pause=900&color=93C5FD&center=true&vCenter=true&width=900&lines=Real-time+Object+Detection+with+YOLOv8;Polished+Glassmorphism+Interface;Upload+Image+%E2%86%92+Detect+%E2%86%92+Analyze+in+Seconds" alt="Animated typing subtitle" />
</p>

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green?style=flat-square)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-MIT-gray?style=flat-square)](LICENSE)

> A modern, professional-grade object detection application powered by YOLOv8 with an elegant glassmorphism UI and real-time inference capabilities.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎨 **Glassmorphism UI** | Polished frosted glass design with smooth gradients |
| 🌊 **Animated Background** | Floating ambient orbs with smooth drift animations |
| ⚡ **Real-time Detection** | YOLOv8 nano model for fast inference |
| 🎛️ **Smart Controls** | Adjustable confidence, IoU, and image size parameters |
| 🖼️ **Side-by-side Preview** | Original and annotated images for easy comparison |
| ⚙️ **Performance** | Cached model loading and optimized GPU support |

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.10 or higher
- **Git**: For cloning and version control

### Installation

Clone the repository and set up the environment:

```bash
# Clone the repository
git clone https://github.com/THORAN7/Object-detection.git
cd Object-detection

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# On Windows CMD:
.venv\Scripts\activate.bat
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📖 Usage

### Launch the Application

```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

> **Note**: If `streamlit run app.py` doesn't work, use this alternative:
> ```bash
> .\.venv\Scripts\python.exe -m streamlit run app.py
> ```

### How to Use

1. **Upload Image** 📤
   - Click the upload area or drag & drop an image (JPG, PNG, JPEG)

2. **Configure Detection** ⚙️
   - **Confidence Threshold**: Control detection sensitivity (0.05–0.95)
     - Lower = more detections (more false positives)
     - Higher = fewer, more confident detections
   - **IoU Threshold**: Non-maximum suppression (0.10–0.90)
   - **Image Size**: Resolution for inference (320/416/640/960 pixels)

3. **View Results** 📊
   - Original image on the left
   - Annotated output on the right
   - Detection statistics and labels below

---

## 🏗️ Project Structure

```
Object-detection/
├── 📄 app.py                 Main Streamlit application
├── 📋 requirements.txt       Python dependencies
├── 📖 README.md             This file
└── 🔧 .venv/                Virtual environment
```

----

## ⚙️ Configuration

### Change Detection Model

Edit `app.py` and modify the `load_model()` function:

```python
@st.cache_resource
def load_model() -> YOLO:
    # ... existing patch code ...
    model = YOLO("yolov8s.pt")  # Change nano (n) to small (s), medium (m), large (l), or xlarge (x)
    # ... restore patch code ...
    return model
```

**Available Models:**
- `yolov8n.pt` - Nano (fastest, least accurate)
- `yolov8s.pt` - Small
- `yolov8m.pt` - Medium
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (slowest, most accurate)

### Adjust UI Colors/Styles

The glassmorphism theme is defined in the `inject_styles()` function. Customize CSS variables to match your brand.

---

## 📦 Dependencies

- **streamlit** ≥ 1.0 - Web framework
- **ultralytics** ≥ 8.0 - YOLOv8 object detection
- **torch** - Deep learning framework
- **torchvision** - Computer vision utilities
- **pillow** - Image processing
- **numpy** - Numerical computing

---

## 🔧 Troubleshooting

### Model Download Issues

The YOLOv8 model (~6.3 MB) auto-downloads on first run to `~/.cache/` or project directory.

**If download fails:**
```bash
# Download manually
yolo detect predict model=yolov8n.pt source=image.jpg
```

### GPU Acceleration

```bash
# For CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 📊 Performance Metrics

| Model | Speed (ms) | Accuracy | File Size |
|-------|-----------|----------|-----------|
| YOLOv8n | ~3-5ms | 63.4% | 6.3 MB |
| YOLOv8s | ~5-8ms | 66.6% | 22 MB |
| YOLOv8m | ~8-12ms | 70.3% | 49 MB |

---

## 📝 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ❓ FAQs

**Q: Why is the first run slow?**
> A: The model downloads and initializes on first run. Subsequent runs are much faster due to caching.

**Q: Can I use this with webcam input?**
> A: Currently supports static images. Webcam support can be added by modifying the file uploader section.

**Q: What GPU does it support?**
> A: CUDA (NVIDIA), ROCm (AMD), and MPS (Apple Silicon). Install PyTorch for your hardware accordingly.

---

## 📞 Support

For issues, questions, or suggestions:
- 📧 Open an issue on GitHub
- 💬 Check existing discussions
- 🔗 Visit [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com/)

---

**Built with ❤️ using Streamlit and YOLOv8**

