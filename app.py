import streamlit as st
from PIL import Image
import io

# 1. Grundkonfiguration
st.set_page_config(page_title="Wertfile | Business Pro", page_icon="🛡️", layout="wide")

# 2. Finom Premium 3D UX CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    .stApp { background-color: #F8FAFC !important; font-family: 'Inter', sans-serif; }
    header, footer, .stDeployButton {display:none !important;}

    /* Navigation Bar */
    .nav-bar {
        background-color: white;
        padding: 1rem 3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #E2E8F0;
        position: fixed;
        top: 0; left: 0; right: 0; z-index: 1000;
    }

    /* 3D Icons Style */
    .icon-3d {
        font-size: 50px;
        filter: drop-shadow(4px 6px 10px rgba(0,0,0,0.2));
        margin-bottom: 10px;
        display: inline-block;
        transition: transform 0.3s ease;
    }
    .icon-3d:hover { transform: translateY(-5px) scale(1.1); }

    /* Main Container */
    .main-content { margin-top: 100px; padding: 0 10%; }
    
    /* White Hero Card */
    .hero-card {
        background: white;
        border-radius: 32px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        border: 1px solid #F1F5F9;
        margin-bottom: 30px;
    }

    /* Uploader - JETZT IN WEISS */
    .stFileUploader section {
        border-radius: 24px !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #FFFFFF !important; /* Weißer Hintergrund */
        padding: 40px !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 16px;
        background-color: #121926 !important;
        color: white !important;
        height: 60px;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 12px;
        padding: 10px 25px;
        border: 1px solid #E2E8F0;
        color: #1E293B !important;
    }
    .stTabs [aria-selected="true"] { background-color: #121926 !important; color: white !important; }

    /* Text Colors Fix */
    h1, h2, h3, p, span, label { color: #121926 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- UI Struktur ---

# Top Nav
st.markdown("""
    <div class="nav-bar">
        <div><span style="font-weight:800; font-size:22px;">Wertfile.</span></div>
        <div style="font-size:14px; font-weight:600;">Business Pro <span style="color:#10B981;">●</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Hero Header
st.markdown("""
    <div class="hero-card">
        <h1 style="font-size:42px; font-weight:800; letter-spacing:-1.5px;">Workspace.</h1>
        <p style="color:#64748B !important; font-size:18px;">Wähle ein Modul für deine Datei-Verarbeitung.</p>
    </div>
    """, unsafe_allow_html=True)

# Werkzeuge Auswahl
tab_pdf, tab_video = st.tabs(["📄 Document Converter", "🎥 Video Tools"])

with tab_pdf:
    st.write("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align:center;"><span class="icon-3d">📑</span></div>', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>JPEG → PDF</h3>", unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader("Bilder hier ablegen (JPG, PNG)", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
        
        if uploaded_files:
            if st.button("PDF generieren"):
                images = [Image.open(f).convert('RGB') for f in uploaded_files]
                pdf_buffer = io.BytesIO()
                images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
                st.success("Bereit zum Download!")
                st.download_button("📥 Dokument herunterladen", data=pdf_buffer.getvalue(), file_name="wertfile.pdf")

with tab_video:
    st.write("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align:center;"><span class="icon-3d">🎬</span></div>', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>Video to MP3 / MP4</h3>", unsafe_allow_html=True)
        st.info("Kopiere die URL ein, um das Video umzuwandeln.")
        
        video_url = st.text_input("YouTube / Video URL", placeholder="https://www.youtube.com/watch?v=...")
        
        c_mp3, c_mp4 = st.columns(2)
        with c_mp3:
            if st.button("🎵 Convert to MP3"):
                st.warning("Video-Schnittstelle wird verbunden...")
        with c_mp4:
            if st.button("🎞️ Convert to MP4"):
                st.warning("Video-Schnittstelle wird verbunden...")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align:center; color:#9CA3AF; font-size:12px; margin-top:100px;'>Wertfile. Technology Germany</p>", unsafe_allow_html=True)
