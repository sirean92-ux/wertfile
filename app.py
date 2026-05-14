import streamlit as st
from PIL import Image
import io

# 1. Grundkonfiguration
st.set_page_config(page_title="Wertfile | Business Dashboard", page_icon="🛡️", layout="wide")

# 2. Finom Premium CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Hintergrund & Font */
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
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

    /* 3D-Sphere Animation (Finom Style) */
    .sphere-wrapper {
        perspective: 800px;
        display: flex;
        justify-content: center;
        padding: 20px;
    }
    .sphere {
        width: 100px;
        height: 100px;
        background: radial-gradient(circle at 30% 30%, #5D5FEF, #3B82F6);
        border-radius: 50%;
        box-shadow: 0 20px 50px rgba(59, 130, 246, 0.3);
        animation: float 6s infinite ease-in-out;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0) rotateX(0deg); }
        50% { transform: translateY(-20px) rotateX(20deg); }
    }

    /* Cards */
    .card {
        background: white;
        border-radius: 20px;
        padding: 24px;
        border: 1px solid #F1F5F9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }

    .stat-val { font-size: 24px; font-weight: 700; color: #1E293B; }
    .stat-label { font-size: 13px; color: #64748B; font-weight: 500; }

    /* Main Tool Button */
    .stButton>button {
        width: 100%;
        border-radius: 14px;
        background-color: #1E293B;
        color: white;
        height: 56px;
        font-weight: 600;
        border: none;
        transition: 0.2s;
    }
    .stButton>button:hover { background-color: #0F172A; transform: translateY(-1px); }
    
    /* Spacer für fixed nav */
    .main-content { margin-top: 80px; }
    </style>
    """, unsafe_allow_html=True)

# --- UI Struktur ---

# Top Navigation
st.markdown("""
    <div class="nav-bar">
        <div><span style="font-weight:800; font-size:22px; color:#1E293B;">Wertfile.</span></div>
        <div style="color:#64748B; font-size:14px; font-weight:500;">
            Konto: Business Pro &nbsp;&nbsp; | &nbsp;&nbsp; <span style="color:#10B981;">● Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-content"></div>', unsafe_allow_html=True)

# Spalten-Layout
col_nav, col_main = st.columns([1, 3])

with col_nav:
    # Profil & 3D Element
    st.markdown("""
        <div class="card">
            <div class="sphere-wrapper"><div class="sphere"></div></div>
            <h3 style="text-align:center; margin-bottom:5px;">Dashboard</h3>
            <p style="text-align:center; color:#64748B; font-size:14px;">Alle Werkzeuge bereit</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats Sidebar
    st.markdown("""
        <div class="card">
            <div class="stat-label">DATEIEN HEUTE</div>
            <div class="stat-val">12</div>
            <br>
            <div class="stat-label">SICHERHEITS-LEVEL</div>
            <div class="stat-val" style="color:#10B981;">Maximum</div>
        </div>
    """, unsafe_allow_html=True)

with col_main:
    # Willkommens-Text
    st.markdown('<h1 style="font-size:32px; font-weight:800; color:#1E293B; margin-bottom:5px;">Guten Tag!</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B; margin-bottom:30px;">Wähle ein Modul aus, um mit der Arbeit zu beginnen.</p>', unsafe_allow_html=True)

    # Das Haupt-Tool in einer großen Karte
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📄 JPEG → PDF Konverter")
    st.write("Lade deine Dokumente hoch. Die Konvertierung erfolgt lokal im Speicher.")
    
    uploaded_files = st.file_uploader("", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    if uploaded_files:
        st.info(f"{len(uploaded_files)} Bilder bereit zur Verarbeitung.")
        if st.button("Jetzt PDF generieren"):
            with st.spinner("Verschlüsselte Verarbeitung..."):
                images = [Image.open(f).convert('RGB') for f in uploaded_files]
                pdf_buffer = io.BytesIO()
                images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
                
                st.success("Dokument erfolgreich erstellt.")
                st.download_button(
                    label="📥 Fertiges PDF herunterladen",
                    data=pdf_buffer.getvalue(),
                    file_name="wertfile_export.pdf",
                    mime="application/pdf"
                )
    st.markdown('</div>', unsafe_allow_html=True)

    # Zusätzliche Info-Karten unten
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="card">
                <p style="font-weight:700;">Datenschutz-Garantie</p>
                <p style="font-size:13px; color:#64748B;">Wir speichern keine Dateien. Sobald du den Tab schließt, sind alle Daten gelöscht.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="card">
                <p style="font-weight:700;">Nächstes Update</p>
                <p style="font-size:13px; color:#64748B;">Morgen verfügbar: PDF zu Word Konverter & Metadaten-Reiniger.</p>
            </div>
        """, unsafe_allow_html=True)
