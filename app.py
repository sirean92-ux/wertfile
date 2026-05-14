import streamlit as st
from PIL import Image
import io

# 1. Page Config
st.set_page_config(page_title="Wertfile | Dashboard", page_icon="🛡️", layout="wide")

# 2. Finom Dashboard CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Hintergrund: Das typische Finom-Hellgrau */
    .stApp {
        background-color: #F4F7F9;
        font-family: 'Inter', sans-serif;
    }

    /* Verstecke Streamlit-Elemente */
    header, footer, .stDeployButton {display:none !important;}

    /* Sidebar-Ersatz Look */
    .nav-header {
        background-color: white;
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 2rem;
    }

    /* 3D-Kreis Animation */
    .circle-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .animated-3d-circle {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #FF7EB3 0%, #FF758C 50%, #FF7EB3 100%);
        border-radius: 50%;
        box-shadow: inset -10px -10px 20px rgba(0,0,0,0.1), 10px 10px 30px rgba(255, 117, 140, 0.4);
        animation: rotate3d 4s infinite linear;
    }

    @keyframes rotate3d {
        0% { transform: perspective(500px) rotateY(0deg) rotateX(0deg) scale(1); }
        50% { transform: perspective(500px) rotateY(180deg) rotateX(20deg) scale(1.1); }
        100% { transform: perspective(500px) rotateY(360deg) rotateX(0deg) scale(1); }
    }

    /* Finom-Cards (Weiß, dezent schattiert) */
    .finom-card {
        background-color: white;
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }

    .finom-title {
        font-size: 28px;
        font-weight: 700;
        color: #121926;
        margin-bottom: 10px;
    }

    /* Uploader & Button Styling */
    .stFileUploader section {
        border-radius: 16px !important;
        border: 1px dashed #D1D5DB !important;
        background-color: #FAFAFB !important;
    }

    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #121926;
        color: white;
        height: 55px;
        font-weight: 600;
        border: none;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- App Struktur ---

# 1. Custom Top Bar
st.markdown("""
    <div class="nav-header">
        <span style="font-size: 24px; font-weight: 800; color: #121926;">finom</span>
        <span style="margin: 0 15px; color: #D1D5DB;">|</span>
        <span style="font-weight: 500; color: #4B5565;">Wertfile</span>
    </div>
    """, unsafe_allow_html=True)

col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("""
        <div class="finom-card">
            <div class="circle-container">
                <div class="animated-3d-circle"></div>
            </div>
            <h2 style="text-align:center; font-size: 22px;">Konvertierung</h2>
            <p style="text-align:center; color: #6B7280; font-size: 14px;">Besser. Schneller. Günstiger.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="finom-card">
            <p style="color: #6B7280; font-size: 12px; margin-bottom: 5px;">Status</p>
            <p style="font-weight: 700; color: #10B981;">● Einsatzbereit</p>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="finom-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="finom-title">JPEG → PDF</h1>', unsafe_allow_html=True)
    st.write("Wähle deine Dateien für eine sichere Verarbeitung.")
    
    uploaded_files = st.file_uploader("", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("Datei erstellen"):
            with st.spinner(""):
                images = [Image.open(f).convert('RGB') for f in uploaded_files]
                pdf_buffer = io.BytesIO()
                images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
                
                st.download_button(
                    label="📥 PDF herunterladen",
                    data=pdf_buffer.getvalue(),
                    file_name="wertfile_export.pdf",
                    mime="application/pdf"
                )
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 12px; margin-top: 50px;'>© 2026 Wertfile Technology</p>", unsafe_allow_html=True)
