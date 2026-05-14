import streamlit as st
from PIL import Image
import io

# Branding & Layout
st.set_page_config(page_title="Wertfile | Werkzeuge", page_icon="🛡️")

# Finom-Style Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #000000; color: white; padding: 10px; border: none; font-weight: 700; }
    .stButton>button:hover { background-color: #333333; color: white; }
    .brand-title { font-size: 42px; font-weight: 800; letter-spacing: -1px; margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="brand-title">Wertfile 🛡️</h1>', unsafe_allow_html=True)
st.caption("Sichere Datei-Werkzeuge | Made in Germany")

st.markdown("---")

# Navigation
tabs = st.radio("Wähle ein Tool:", ["🏠 Start", "📄 JPEG → PDF", "🎥 Video (Bald)"], horizontal=True)

if tabs == "🏠 Start":
    st.write("### Willkommen")
    st.info("Deine Dateien werden nur im Arbeitsspeicher verarbeitet und niemals gespeichert. 100% Privatsphäre.")

elif tabs == "📄 JPEG → PDF":
    st.write("### 📄 Bilder in PDF umwandeln")
    
    # Der Datei-Uploader (Hier passiert die Magie)
    uploaded_files = st.file_uploader("Bilder hier reinziehen oder klicken", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

    if uploaded_files:
        if st.button("Jetzt PDF erstellen"):
            with st.spinner("Bilder werden verarbeitet..."):
                try:
                    images = []
                    for uploaded_file in uploaded_files:
                        img = Image.open(uploaded_file)
                        if img.mode in ("RGBA", "P"): # PNG Transparenz entfernen
                            img = img.convert('RGB')
                        images.append(img)
                    
                    # PDF im Speicher erstellen
                    pdf_buffer = io.BytesIO()
                    images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
                    
                    st.success("Erfolgreich konvertiert!")
                    st.download_button(
                        label="📥 PDF herunterladen",
                        data=pdf_buffer.getvalue(),
                        file_name="wertfile_export.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Fehler: {e}")

st.markdown("<br><br><p style='text-align:center; color:gray; font-size:12px;'>© 2026 Wertfile – Keine Datenspeicherung.</p>", unsafe_allow_html=True)
