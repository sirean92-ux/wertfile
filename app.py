import streamlit as st
from PIL import Image
import io

# 1. Page Config
st.set_page_config(page_title="Wertfile | Business Tools", page_icon="🛡️", layout="wide")

# 2. Finom-Style Custom CSS
st.markdown("""
    <style>
    /* Hintergrund & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    /* Finom Blue-Black Header */
    h1 {
        color: #121926;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        letter-spacing: -0.04em !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }

    .sub-header {
        text-align: center;
        color: #4B5565;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }

    /* Tool Card - Extrem clean */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
        border-bottom: none;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #F8F9FB;
        border-radius: 30px;
        padding: 0px 30px;
        color: #4B5565;
        border: 1px solid #E5E7EB;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #121926 !important;
        color: white !important;
    }

    /* Uploader Styling */
    .stFileUploader section {
        background-color: #F8F9FB;
        border: 2px dashed #E5E7EB;
        border-radius: 16px;
        padding: 2rem;
    }

    /* Finom Primary Button */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #00E676; /* Finom Green Akzent */
        color: #121926;
        height: 3.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        box-shadow: 0 4px 14px 0 rgba(0,230,118,0.39);
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background-color: #00C864;
        transform: scale(1.02);
        color: #121926;
    }

    /* Verstecke Streamlit Branding */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- Layout ---

# Zentrierter Container für den Content
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    st.markdown('<h1>Wertfile</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">The financial-grade file manager for modern business.</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Overview", "JPEG → PDF", "Settings"])

    with tab1:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("""
        ### Simplify your file workflow
        Wertfile helps you to manage and convert files with bank-level privacy. 
        No data is ever stored on our servers.
        """)
        
        # Grid für Features
        c1, c2 = st.columns(2)
        with c1:
            st.info("**Fast Deployment**\n\nConvert files in milliseconds.")
        with c2:
            st.success("**Privacy First**\n\nEncrypted in-memory processing.")

    with tab2:
        st.write("<br>", unsafe_allow_html=True)
        files = st.file_uploader("", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
        
        if files:
            st.write(f"**{len(files)} files selected**")
            if st.button("Convert to PDF"):
                with st.spinner("Processing..."):
                    images = [Image.open(f).convert('RGB') for f in files]
                    pdf_buffer = io.BytesIO()
                    images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
                    
                    st.download_button(
                        label="Download PDF Document",
                        data=pdf_buffer.getvalue(),
                        file_name="wertfile_export.pdf",
                        mime="application/pdf"
                    )

    with tab3:
        st.write("<br>", unsafe_allow_html=True)
        st.write("Current Version: **1.0.4 (Pro)**")
        st.write("Region: **Europe (Frankfurt)**")

# Footer
st.markdown("<br><br><p style='text-align: center; color: #9CA3AF; font-size: 14px;'>© 2026 Wertfile Technology. All rights reserved.</p>", unsafe_allow_html=True)
