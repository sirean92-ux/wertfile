import streamlit as st
from PIL import Image
import io

# 1. Grundkonfiguration
st.set_page_config(page_title="Wertfile | Business Dashboard", page_icon="🛡️", layout="wide")

# 2. Finom Premium UX CSS (Farben fixiert)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Hintergrund & Font */
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

    /* 3D-Sphere Animation */
    .sphere {
        width: 60px; height: 60px;
        background: radial-gradient(circle at 30% 30%, #5D5FEF, #3B82F6);
        border-radius: 50%;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        animation: float 4s infinite ease-in-out;
        margin: 0 auto 15px;
    }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }

    /* Cards & Container */
    .main-content { margin-top: 100px; padding: 0 10%; }
    
    .hero-card {
        background: white;
        border-radius: 32px;
        padding: 60px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.02);
        border: 1px solid #F1F5F9;
        margin-bottom: 30px;
    }

    /* TEXTFARBEN FIXIEREN */
    .hero-card h1 { color: #1E293B !important; font-size: 48px !important; font-weight: 800 !important; letter-spacing: -1.5px !important; margin-bottom: 15px; }
    .hero-card p { color: #64748B !important; font-size: 20px !important; }
    
    .step-box {
        background: #F1F5F9;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 10px;
        color: #1E293B !important; /* Fix für die Zahl/Text in der Box */
    }
    .step-box b { color: #1E293B !important; }

    /* Uploader Text Fix */
    .stFileUploader label { color: #1E293B !important; font-weight: 600 !important; }
    .stFileUploader section {
        border-radius: 24px !important;
        border: 2px dashed #3B82F6 !important;
        background-color: #F0F7FF !important;
        padding: 40px !important;
    }

    /* Action Button */
    .stButton>button {
        width: 100%;
        border-radius: 16px;
        background-color: #1E293B !important;
        color: white !important;
        height: 64px;
        font-weight: 700;
        font-size: 18px;
        border: none;
    }
    .stButton>button:hover { background-color: #000000 !important; color: white !important; }
    
    /* Allgemeine Text-Farben für Streamlit-Elemente erzwingen */
    p, span, label, div { color: #1E293B; }
    </style>
    """, unsafe_allow_html=True)

# --- UI Struktur ---

# Top Nav
st.markdown("""
    <div class="nav-bar">
        <div><span style="font-weight:800; font-size:22px; color:#1E293B;">Wertfile.</span></div>
        <div style="color:#64748B; font-size:14px;">Status: <b style="color:#1E293B;">Bereit</b> <span style="color:#10B981;">●</span></div>
    </div>
    """, unsafe_allow_html=True)

# Main Area
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Hero Sektion
st.markdown("""
    <div class="hero-card">
        <div class="sphere"></div>
        <h1>Bilder in PDF umwandeln.</h1>
        <p>
            Sicher, schnell und ohne Speicherung auf Servern. <br>Einfach Bilder hochladen und Dokument generieren.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tool Bereich (Zentriert)
col1, col2, col3 = st.columns([1, 2.5, 1])

with col2:
    # 3-Schritte Erklärung
    s1, s2, s3 = st.columns(3)
    s1.markdown('<div class="step-box"><span style="font-size:24px;">📸</span><br><b>1. Bilder wählen</b></div>', unsafe_allow_html=True)
    s2.markdown('<div class="step-box"><span style="font-size:24px;">⚙️</span><br><b>2. Verarbeiten</b></div>', unsafe_allow_html=True)
    s3.markdown('<div class="step-box"><span style="font-size:24px;">📩</span><br><b>3. Download</b></div>', unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    # Das eigentliche Tool
    uploaded_files = st.file_uploader("Wähle JPG oder PNG Dateien aus", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    if uploaded_files:
        st.markdown(f"<p style='text-align:center; font-weight:700; color:#1E293B;'>{len(uploaded_files)} Datei(en) ausgewählt</p>", unsafe_allow_html=True)
        if st.button("🚀 Jetzt PDF Dokument erstellen"):
            with st.spinner("Erstelle Dokument..."):
                images = [Image.open(f).convert('RGB') for f in uploaded_files]
                pdf_buffer = io.BytesIO()
                images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
                
                st.balloons()
                st.success("Dein Dokument ist fertig!")
                st.download_button(
                    label="📥 Datei jetzt herunterladen",
                    data=pdf_buffer.getvalue(),
                    file_name="wertfile_export.pdf",
                    mime="application/pdf"
                )

st.markdown('</div>', unsafe_allow_html=True) 

# Footer
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 13px; margin-top: 100px; padding-bottom: 50px;'>Wertfile. – 100% Privacy-Focused File Processing.</p>", unsafe_allow_html=True)
