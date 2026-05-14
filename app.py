import streamlit as st

# --- WERTFILE BRANDING SETUP ---
st.set_page_config(
    page_title="Wertfile | Deutsche Datei-Werkzeuge", 
    page_icon="🛡️", 
    layout="centered"
)

# Custom CSS für den Finom-Look (Minimalismus pur)
st.markdown("""
    <style>
    /* Schriftart importieren */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    /* Globales Styling */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #FFFFFF;
        color: #111827;
    }

    /* Streamlit Branding verstecken für Profi-Look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Button Styling (Finom-Black) */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #000000;
        color: #FFFFFF;
        border: 1px solid #000000;
        padding: 12px 20px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.2s ease;
        margin-bottom: 10px;
    }
    .stButton>button:hover {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #000000;
    }

    /* Header Design */
    .brand-title {
        font-size: 52px;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 0px;
        color: #000000;
    }
    .brand-subtitle {
        font-size: 18px;
        color: #6B7280;
        margin-top: -10px;
        margin-bottom: 40px;
    }
    .germany-badge {
        background-color: #F3F4F6;
        color: #111827;
        padding: 4px 10px;
        border-radius: 5px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }
    
    /* Trenner */
    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
        border: 0;
        border-top: 1px solid #F3F4F6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SEKTION ---
st.markdown('<span class="germany-badge">🛡️ Made in Germany</span>', unsafe_allow_html=True)
st.markdown('<h1 class="brand-title">Wertfile</h1>', unsafe_allow_html=True)
st.markdown('<p class="brand-subtitle">Sichere Werkzeuge. Maximale Privatsphäre. Keine Speicherung.</p>', unsafe_allow_html=True)

# --- TOOL GRID (2 Spalten) ---
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("#### 📄 Dokumente")
    if st.button("JPEG → PDF"):
        st.toast("Werkzeug wird geladen...")
    if st.button("PDF Verkleinern"):
        st.toast("Werkzeug wird geladen...")
    if st.button("Metadaten löschen"):
        st.toast("Sicherheits-Tool startet...")

with col2:
    st.markdown("#### 🎥 Media")
    if st.button("YouTube Downloader"):
        st.toast("Bereite sicheren Download vor...")
    if st.button("Vocal Remover"):
        st.toast("KI-Analyse startet...")
    if st.button("Video → MP3"):
        st.toast("Konverter lädt...")

st.markdown("<hr>", unsafe_allow_html=True)

# --- ADSENSE / INFO BOX ---
st.markdown("""
    <div style="background-color: #F9FAFB; padding: 50px; border-radius: 12px; text-align: center; border: 1px solid #F3F4F6;">
        <p style="color: #9CA3AF; font-size: 14px; font-weight: 500;">
            Hier erscheint später die AdSense Werbung.<br>
            (Einnahmen finanzieren die deutschen Server)
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 Wertfile.de – Ein Projekt von Ilangai. Alle Prozesse sind DSGVO-konform verschlüsselt.")
