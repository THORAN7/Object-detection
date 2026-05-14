import numpy as np
import streamlit as st
from PIL import Image, ImageOps
from ultralytics import YOLO
from ultralytics.nn import tasks as ultralytics_tasks


st.set_page_config(
    page_title="Object Detection Studio",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_model() -> YOLO:
    # PyTorch 2.6+ fix: Patch ultralytics to load weights with weights_only=False
    original_torch_safe_load = ultralytics_tasks.torch_safe_load

    def patched_torch_safe_load(weights):
        """Load PyTorch checkpoint with weights_only=False for compatibility with PyTorch 2.6+"""
        from pathlib import Path
        import torch

        file = Path(weights)
        return torch.load(file, map_location='cpu', weights_only=False), file

    ultralytics_tasks.torch_safe_load = patched_torch_safe_load
    model = YOLO("yolov8n.pt")
    ultralytics_tasks.torch_safe_load = original_torch_safe_load
    return model


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.30), transparent 24%),
                    radial-gradient(circle at 85% 15%, rgba(14, 165, 233, 0.24), transparent 20%),
                    radial-gradient(circle at 90% 80%, rgba(168, 85, 247, 0.18), transparent 22%),
                    linear-gradient(135deg, #08111f 0%, #0b1324 45%, #101827 100%);
                color: #e5eefb;
            }

            .stApp::before {
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
                background-image:
                    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
                background-size: 48px 48px;
                mask-image: linear-gradient(to bottom, rgba(0,0,0,0.7), transparent 85%);
            }

            .hero-card, .content-card {
                background: rgba(8, 17, 31, 0.68);
                border: 1px solid rgba(148, 163, 184, 0.16);
                box-shadow: 0 20px 80px rgba(0, 0, 0, 0.35);
                backdrop-filter: blur(18px);
                border-radius: 22px;
            }

            .hero-card {
                padding: 2rem 2rem 1.6rem 2rem;
                animation: fadeUp 0.8s ease-out both;
            }

            .hero-title {
                font-size: clamp(2.1rem, 4vw, 4.2rem);
                line-height: 1.05;
                font-weight: 800;
                margin: 0;
                background: linear-gradient(90deg, #f8fafc 0%, #93c5fd 35%, #c4b5fd 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .hero-subtitle {
                color: #cbd5e1;
                font-size: 1.02rem;
                max-width: 68ch;
                margin-top: 0.75rem;
                margin-bottom: 1rem;
            }

            .pill-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.7rem;
                margin-top: 0.9rem;
            }

            .pill {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                padding: 0.45rem 0.8rem;
                border-radius: 999px;
                background: rgba(15, 23, 42, 0.68);
                border: 1px solid rgba(148, 163, 184, 0.16);
                color: #dbeafe;
                font-size: 0.86rem;
            }

            .section-label {
                color: #93c5fd;
                text-transform: uppercase;
                letter-spacing: 0.16em;
                font-size: 0.74rem;
                margin-bottom: 0.4rem;
            }

            .metric-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.8rem;
                margin: 1rem 0 1.2rem;
            }

            .metric-card {
                padding: 1rem 1.1rem;
                border-radius: 18px;
                background: linear-gradient(180deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.75));
                border: 1px solid rgba(148, 163, 184, 0.14);
            }

            .metric-label {
                color: #94a3b8;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
            }

            .metric-value {
                font-size: 1.6rem;
                font-weight: 800;
                margin-top: 0.2rem;
                color: #f8fafc;
            }

            .feature-card {
                padding: 1rem 1rem 0.9rem;
                border-radius: 18px;
                background: rgba(15, 23, 42, 0.66);
                border: 1px solid rgba(148, 163, 184, 0.12);
                height: 100%;
            }

            .feature-title {
                font-weight: 700;
                color: #e2e8f0;
                margin-bottom: 0.35rem;
            }

            .feature-text {
                color: #94a3b8;
                font-size: 0.93rem;
                line-height: 1.5;
            }

            .floating-orb {
                position: fixed;
                border-radius: 50%;
                filter: blur(18px);
                pointer-events: none;
                opacity: 0.55;
                animation: drift 14s ease-in-out infinite;
            }

            .orb-a { width: 240px; height: 240px; top: 8%; left: -60px; background: rgba(59, 130, 246, 0.25); }
            .orb-b { width: 180px; height: 180px; bottom: 10%; right: 2%; background: rgba(168, 85, 247, 0.22); animation-duration: 18s; }
            .orb-c { width: 140px; height: 140px; top: 54%; left: 40%; background: rgba(20, 184, 166, 0.18); animation-duration: 16s; }

            @keyframes fadeUp {
                from { opacity: 0; transform: translateY(18px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes drift {
                0%, 100% { transform: translate3d(0, 0, 0) scale(1); }
                50% { transform: translate3d(24px, -18px, 0) scale(1.07); }
            }

            @keyframes bannerSlideIn {
                from { opacity: 0; transform: translateY(-30px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            @keyframes pulseGlow {
                0%, 100% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
                50% { box-shadow: 0 0 40px rgba(59, 130, 246, 0.6); }
            }

            .banner-container {
                animation: bannerSlideIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
                margin-bottom: 1.5rem;
            }

            .banner {
                background: linear-gradient(
                    135deg,
                    rgba(30, 58, 138, 0.4),
                    rgba(79, 39, 131, 0.3),
                    rgba(14, 165, 233, 0.25)
                );
                background-size: 300% 300%;
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 20px;
                padding: 2.5rem 2rem;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
                animation: pulseGlow 3s ease-in-out infinite;
            }

            .banner-title {
                font-size: 2.5rem;
                font-weight: 800;
                margin: 0 0 0.5rem 0;
                background: linear-gradient(90deg, #60a5fa, #818cf8, #c084fc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: fadeUp 1s ease-out 0.2s both;
            }

            .banner-subtitle {
                font-size: 1rem;
                color: #cbd5e1;
                margin: 0;
                animation: fadeUp 1s ease-out 0.4s both;
            }

            .banner-accent {
                display: inline-block;
                width: 3px;
                height: 24px;
                background: linear-gradient(180deg, #3b82f6, #ec4899);
                border-radius: 2px;
                margin-right: 0.75rem;
                animation: fadeUp 1s ease-out 0.1s both;
            }

            .stButton > button {
                border-radius: 999px;
                border: 0;
                background: linear-gradient(90deg, #2563eb, #7c3aed);
                color: white;
                padding: 0.75rem 1.2rem;
                font-weight: 700;
                box-shadow: 0 10px 25px rgba(59, 130, 246, 0.25);
            }

            .stButton > button:hover {
                transform: translateY(-1px);
            }
        </style>
        <div class="floating-orb orb-a"></div>
        <div class="floating-orb orb-b"></div>
        <div class="floating-orb orb-c"></div>
        """,
        unsafe_allow_html=True,
    )


def image_to_array(image: Image.Image) -> np.ndarray:
    fixed = ImageOps.exif_transpose(image).convert("RGB")
    return np.asarray(fixed)


def display_banner() -> None:
    """Display animated startup banner with modern effects"""
    st.markdown(
        """
        <div class="banner-container">
            <div class="banner">
                <div style="display: flex; align-items: center;">
                    <div class="banner-accent"></div>
                    <div class="banner-title">Object Detection Studio</div>
                </div>
                <p class="banner-subtitle">✨ Powered by YOLOv8 • Professional-grade AI object detection</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_styles()
display_banner()
model = load_model()

st.markdown(
    """
    <div class="hero-card">
        <h2 class="hero-title" style="font-size: 1.8rem; margin-top: 0;">How it works</h2>
        <p class="hero-subtitle" style="font-size: 0.95rem;">
            Upload any image to instantly detect objects using advanced AI. Our glassmorphism interface provides
            real-time feedback with adjustable confidence levels and side-by-side comparisons.
        </p>
        <div class="pill-row">
            <span class="pill">🚀 Lightning-fast inference</span>
            <span class="pill">🎯 High accuracy detection</span>
            <span class="pill">⚙️ Fully customizable</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Detection controls")
    confidence = st.slider("Confidence threshold", 0.05, 0.95, 0.25, 0.01)
    iou = st.slider("IoU threshold", 0.10, 0.90, 0.45, 0.01)
    image_size = st.select_slider("Image size", options=[320, 416, 640, 960], value=640)
    st.caption("Tune these controls for a cleaner preview or stricter detections.")



st.markdown('<div class="content-card" style="padding: 1.1rem 1.1rem 1rem;">', unsafe_allow_html=True)
st.markdown("<div class='section-label'>Upload</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Upload a JPG, PNG, or JPEG image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-label">Model</div>
            <div class="metric-value">YOLOv8n</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Style</div>
            <div class="metric-value">Ambient</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Layout</div>
            <div class="metric-value">Wide</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


if uploaded_file:
    image = Image.open(uploaded_file)
    image_np = image_to_array(image)

    with st.spinner("Running YOLOv8 detection..."):
        results = model.predict(image_np, conf=confidence, iou=iou, imgsz=image_size, verbose=False)

    result = results[0]
    annotated = result.plot()
    detected_boxes = result.boxes
    detections = int(len(detected_boxes)) if detected_boxes is not None else 0

    st.markdown("### Detection results")

    stats_a, stats_b, stats_c = st.columns(3)
    stats_a.metric("Objects detected", detections)
    stats_b.metric("Confidence", f"{confidence:.2f}")
    stats_c.metric("Image size", f"{image_size}px")

    preview_left, preview_right = st.columns(2, gap="large")
    with preview_left:
        st.markdown("#### Original image")
        st.image(image_np, use_container_width=True)
    with preview_right:
        st.markdown("#### Annotated output")
        st.image(annotated, use_container_width=True)

    if detections:
        labels = []
        names = result.names
        for box in detected_boxes:
            cls_id = int(box.cls.item())
            class_name = names.get(cls_id, str(cls_id))
            conf_value = float(box.conf.item())
            labels.append(f"{class_name} ({conf_value:.2%})")

        st.markdown("#### Detected items")
        st.write(" • ".join(labels))
    else:
        st.info("No objects detected at the current confidence threshold. Try lowering the confidence slider.")
else:
    st.markdown(
        """
        <div class="content-card" style="padding: 1.25rem 1.1rem; margin-top: 0.5rem;">
            <div class="section-label">Getting started</div>
            <div style="color: #dbeafe; font-size: 1rem; line-height: 1.6;">
                Choose an image from the upload area to see the detection pipeline in action.
                The interface is designed to feel more professional, polished, and responsive.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption("Built with Streamlit and YOLOv8 • Ambient UI refresh")

