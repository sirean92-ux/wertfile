import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError
import io
import zipfile
from datetime import datetime
from typing import List, Tuple

# Optional dependencies for PDF → Word
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from docx import Document
    from docx.shared import Pt
except ImportError:
    Document = None
    Pt = None

# =========================================================
# WERTFILE 1.1 — Stable MVP
# Fokus: zuverlässig, einfach, testbar
# Funktionen:
# 1. Bild → PDF
# 2. PDF → Word für Text-PDFs
# =========================================================

APP_NAME = "Wertfile"
MAX_FILES = 50
MAX_TOTAL_MB = 200
MAX_SINGLE_MB = 25
SUPPORTED_IMAGE_TYPES = ["jpg", "jpeg", "png", "webp"]
SUPPORTED_PDF_TYPES = ["pdf"]

st.set_page_config(
    page_title=f"{APP_NAME} | File Converter",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "active_tool" not in st.session_state:
    st.session_state.active_tool = "image_to_pdf"


# ---------- CSS ----------
def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {
            --bg: #F7F9FC;
            --card: #FFFFFF;
            --ink: #0F172A;
            --muted: #64748B;
            --line: #E2E8F0;
            --primary: #101828;
            --primary-soft: #EEF2FF;
            --blue: #2563EB;
            --green: #10B981;
            --red: #EF4444;
            --purple: #7C3AED;
            --shadow: 0 20px 60px rgba(15, 23, 42, 0.08);
            --radius: 26px;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 12%, rgba(37,99,235,0.10), transparent 28%),
                radial-gradient(circle at 92% 8%, rgba(16,185,129,0.10), transparent 28%),
                linear-gradient(180deg, #F8FAFC 0%, #EEF3F8 100%) !important;
            color: var(--ink);
        }

        header, footer, .stDeployButton, #MainMenu {
            display: none !important;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 44px !important;
            padding-bottom: 52px !important;
        }

        h1, h2, h3, h4, p, span, label, div {
            color: var(--ink);
        }

        p { line-height: 1.6; }

        .wf-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 24px;
        }

        .wf-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 900;
            font-size: 24px;
            letter-spacing: -0.8px;
        }

        .wf-logo {
            width: 42px;
            height: 42px;
            border-radius: 15px;
            display: grid;
            place-items: center;
            color: #FFFFFF !important;
            font-weight: 900;
            background: linear-gradient(135deg, #101828 0%, #2563EB 55%, #10B981 100%);
            box-shadow: 0 14px 30px rgba(37,99,235,0.23);
        }

        .wf-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border-radius: 999px;
            padding: 9px 13px;
            background: rgba(255,255,255,0.82);
            border: 1px solid var(--line);
            color: #475569 !important;
            font-size: 13px;
            font-weight: 800;
            box-shadow: 0 10px 28px rgba(15,23,42,0.04);
        }

        .wf-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: var(--green);
            box-shadow: 0 0 0 5px rgba(16,185,129,0.12);
        }

        .wf-hero {
            background: rgba(255,255,255,0.84);
            border: 1px solid rgba(226,232,240,0.92);
            border-radius: 34px;
            padding: 34px;
            box-shadow: var(--shadow);
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
        }

        .wf-hero::after {
            content: "";
            position: absolute;
            right: -90px;
            top: -120px;
            width: 300px;
            height: 300px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(37,99,235,0.14), transparent 70%);
        }

        .wf-hero > * {
            position: relative;
            z-index: 1;
        }

        .wf-hero h1 {
            font-size: clamp(34px, 4.5vw, 58px);
            line-height: 1;
            letter-spacing: -2.8px;
            margin: 0 0 14px 0;
            font-weight: 900;
        }

        .wf-gradient {
            background: linear-gradient(90deg, #2563EB, #7C3AED, #10B981);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent !important;
        }

        .wf-hero p {
            max-width: 760px;
            margin: 0;
            color: var(--muted) !important;
            font-size: 17px;
            font-weight: 550;
        }

        .wf-toolbar {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin: 20px 0;
        }

        .wf-tool-card {
            background: rgba(255,255,255,0.88);
            border: 1px solid var(--line);
            border-radius: 22px;
            padding: 18px;
            box-shadow: 0 14px 36px rgba(15,23,42,0.05);
        }

        .wf-tool-card b {
            display: block;
            font-size: 16px;
            margin-bottom: 4px;
        }

        .wf-tool-card span {
            color: var(--muted) !important;
            font-size: 13px;
            font-weight: 650;
        }

        .wf-stepbar {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin: 20px 0;
        }

        .wf-step {
            background: rgba(255,255,255,0.86);
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 16px;
            box-shadow: 0 12px 32px rgba(15,23,42,0.05);
        }

        .wf-step b {
            display: block;
            font-size: 14px;
            margin-bottom: 4px;
        }

        .wf-step span {
            color: var(--muted) !important;
            font-size: 12px;
            font-weight: 650;
        }

        .wf-card {
            background: rgba(255,255,255,0.90);
            border: 1px solid rgba(226,232,240,0.96);
            border-radius: var(--radius);
            padding: 24px;
            box-shadow: var(--shadow);
            margin-bottom: 18px;
        }

        .wf-card h2, .wf-card h3 {
            margin-top: 0;
            letter-spacing: -0.8px;
        }

        .wf-card-subtitle {
            color: var(--muted) !important;
            margin-top: -8px;
            margin-bottom: 18px;
            font-size: 14px;
            font-weight: 550;
        }

        .wf-info-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 14px;
        }

        .wf-info-box {
            background: #F8FAFC;
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 13px;
        }

        .wf-info-box b {
            display: block;
            font-size: 18px;
        }

        .wf-info-box span {
            color: var(--muted) !important;
            font-size: 12px;
            font-weight: 700;
        }

        .wf-file-list {
            display: grid;
            gap: 8px;
            margin-top: 12px;
        }

        .wf-file-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 12px 13px;
            border-radius: 15px;
            background: #F8FAFC;
            border: 1px solid var(--line);
            font-size: 13px;
            font-weight: 700;
        }

        .wf-file-row small {
            color: var(--muted) !important;
            font-weight: 700;
        }

        .wf-preview-empty {
            min-height: 300px;
            border-radius: 22px;
            background: #F8FAFC;
            border: 1px dashed #CBD5E1;
            display: grid;
            place-items: center;
            text-align: center;
            padding: 24px;
        }

        .wf-preview-empty h3 {
            margin-bottom: 6px;
        }

        .wf-preview-empty p {
            color: var(--muted) !important;
            margin: 0;
            max-width: 340px;
        }

        .wf-test-card {
            border-radius: 22px;
            padding: 18px;
            background: #F8FAFC;
            border: 1px solid var(--line);
        }

        .wf-test-card ul {
            margin-bottom: 0;
            color: #334155;
        }

        .wf-footer {
            text-align: center;
            color: #94A3B8 !important;
            font-size: 12px;
            font-weight: 700;
            margin-top: 20px;
        }

        .stFileUploader section {
            border-radius: 22px !important;
            border: 1.5px dashed #CBD5E1 !important;
            background: #FFFFFF !important;
            padding: 30px !important;
        }

        .stFileUploader section:hover {
            border-color: #2563EB !important;
            background: #F8FAFC !important;
        }

        .stTextInput input,
        .stSelectbox [data-baseweb="select"],
        .stSelectbox [data-baseweb="select"] > div,
        .stTextArea textarea {
            min-height: 50px !important;
            border-radius: 15px !important;
            border-color: #CBD5E1 !important;
            background: #FFFFFF !important;
            color: #0F172A !important;
            font-weight: 700 !important;
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 15px !important;
            min-height: 52px !important;
            border: none !important;
            background: #101828 !important;
            color: white !important;
            font-weight: 850 !important;
            box-shadow: 0 14px 30px rgba(16,24,40,0.18) !important;
            transition: transform .2s ease, box-shadow .2s ease !important;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 18px 40px rgba(16,24,40,0.25) !important;
        }

        .stAlert {
            border-radius: 16px !important;
        }

        @media (max-width: 900px) {
            .wf-topbar { align-items: flex-start; flex-direction: column; }
            .wf-stepbar, .wf-toolbar { grid-template-columns: 1fr; }
            .wf-info-grid { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------- Helpers ----------
def mb(size_bytes: int) -> float:
    return size_bytes / (1024 * 1024)


def validate_image_files(uploaded_files) -> Tuple[List[str], List[str]]:
    warnings = []
    errors = []

    if not uploaded_files:
        return warnings, errors

    if len(uploaded_files) > MAX_FILES:
        errors.append(f"Bitte maximal {MAX_FILES} Dateien hochladen.")

    total_mb = sum(mb(file.size) for file in uploaded_files)
    if total_mb > MAX_TOTAL_MB:
        errors.append(f"Die Gesamtgröße liegt bei {total_mb:.1f} MB. Erlaubt sind maximal {MAX_TOTAL_MB} MB.")

    for file in uploaded_files:
        file_mb = mb(file.size)
        if file_mb > MAX_SINGLE_MB:
            errors.append(f"{file.name} ist {file_mb:.1f} MB groß. Pro Datei sind maximal {MAX_SINGLE_MB} MB empfohlen/erlaubt.")

        ext = file.name.split(".")[-1].lower() if "." in file.name else ""
        if ext not in SUPPORTED_IMAGE_TYPES:
            errors.append(f"{file.name} hat ein nicht unterstütztes Format.")

    if len(uploaded_files) > 20:
        warnings.append("Viele Dateien können die Verarbeitung verlangsamen. Für Version 1.1 sind kleinere Batches stabiler.")

    return warnings, errors


def validate_pdf_file(uploaded_file) -> List[str]:
    errors = []
    if not uploaded_file:
        return errors

    file_mb = mb(uploaded_file.size)
    if file_mb > MAX_TOTAL_MB:
        errors.append(f"Die PDF ist {file_mb:.1f} MB groß. Erlaubt sind maximal {MAX_TOTAL_MB} MB.")

    ext = uploaded_file.name.split(".")[-1].lower() if "." in uploaded_file.name else ""
    if ext != "pdf":
        errors.append("Bitte eine PDF-Datei hochladen.")

    return errors


def open_image_safely(file) -> Image.Image:
    try:
        image = Image.open(file)
        image = ImageOps.exif_transpose(image)
        return image.convert("RGB")
    except UnidentifiedImageError:
        raise ValueError(f"{file.name} konnte nicht als Bild erkannt werden.")
    except Exception as exc:
        raise ValueError(f"{file.name} konnte nicht gelesen werden: {exc}")


def fit_to_page(image: Image.Image, page_format: str, margin: int, background: str = "white") -> Image.Image:
    if page_format == "Originalgröße":
        return image

    page_sizes = {
        "A4 Hochformat": (1240, 1754),
        "A4 Querformat": (1754, 1240),
        "Letter Hochformat": (1275, 1650),
        "Letter Querformat": (1650, 1275),
    }

    canvas_size = page_sizes.get(page_format, page_sizes["A4 Hochformat"])
    canvas = Image.new("RGB", canvas_size, background)

    max_w = max(100, canvas_size[0] - (margin * 2))
    max_h = max(100, canvas_size[1] - (margin * 2))

    img = image.copy()
    img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

    x = (canvas_size[0] - img.width) // 2
    y = (canvas_size[1] - img.height) // 2
    canvas.paste(img, (x, y))
    return canvas


def create_pdf(uploaded_files, page_format: str, margin_size: str, sort_mode: str, quality: int) -> bytes:
    files = list(uploaded_files)

    if sort_mode == "Dateiname A–Z":
        files = sorted(files, key=lambda f: f.name.lower())
    elif sort_mode == "Dateiname Z–A":
        files = sorted(files, key=lambda f: f.name.lower(), reverse=True)

    margin_map = {"Keine": 0, "Klein": 40, "Normal": 80, "Groß": 130}
    margin = margin_map.get(margin_size, 80)

    images = []
    for file in files:
        file.seek(0)
        image = open_image_safely(file)
        image = fit_to_page(image, page_format, margin)
        images.append(image)

    if not images:
        raise ValueError("Keine gültigen Bilder vorhanden.")

    buffer = io.BytesIO()
    images[0].save(
        buffer,
        format="PDF",
        save_all=True,
        append_images=images[1:],
        resolution=150.0,
        quality=quality,
        optimize=True,
    )
    buffer.seek(0)
    return buffer.getvalue()


def create_preview_image(uploaded_file, page_format: str, margin_size: str) -> Image.Image:
    uploaded_file.seek(0)
    image = open_image_safely(uploaded_file)
    margin_map = {"Keine": 0, "Klein": 40, "Normal": 80, "Groß": 130}
    return fit_to_page(image, page_format, margin_map.get(margin_size, 80))


def create_uploaded_zip(uploaded_files) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in uploaded_files:
            file.seek(0)
            zip_file.writestr(file.name, file.read())
    buffer.seek(0)
    return buffer.getvalue()


def extract_pdf_text(pdf_file) -> Tuple[List[dict], int, int]:
    if fitz is None:
        raise ImportError("PyMuPDF fehlt. Bitte installiere es mit: pip install pymupdf")

    pdf_file.seek(0)
    pdf_bytes = pdf_file.read()

    pages = []
    total_chars = 0

    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        page_count = doc.page_count
        for idx, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            total_chars += len(text)
            pages.append({"page": idx, "text": text})

    return pages, page_count, total_chars


def create_word_from_pdf_text(pdf_file, output_style: str, include_page_numbers: bool) -> Tuple[bytes, int, int]:
    if Document is None:
        raise ImportError("python-docx fehlt. Bitte installiere es mit: pip install python-docx")

    pages, page_count, total_chars = extract_pdf_text(pdf_file)

    if total_chars < 20:
        raise ValueError(
            "In dieser PDF wurde kaum Text gefunden. Wahrscheinlich ist es ein Scan/Bild-PDF. "
            "Dafür braucht Wertfile später OCR."
        )

    doc = Document()
    styles = doc.styles
    styles["Normal"].font.name = "Arial"
    styles["Normal"].font.size = Pt(10.5)

    doc.add_heading("Wertfile PDF to Word Export", level=1)
    intro = doc.add_paragraph()
    intro.add_run(f"Quelle: {pdf_file.name}\n").bold = True
    intro.add_run(f"Seiten: {page_count}\n")
    intro.add_run(f"Exportiert am: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

    doc.add_paragraph("")

    for page in pages:
        text = page["text"]
        if not text:
            continue

        if include_page_numbers:
            doc.add_heading(f"Seite {page['page']}", level=2)

        if output_style == "Absätze erhalten":
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            if not paragraphs:
                paragraphs = [line.strip() for line in text.split("\n") if line.strip()]
            for paragraph in paragraphs:
                doc.add_paragraph(paragraph)
        else:
            for line in text.split("\n"):
                line = line.strip()
                if line:
                    doc.add_paragraph(line)

        doc.add_paragraph("")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue(), page_count, total_chars


# ---------- UI ----------
def render_header() -> None:
    tool_text = "Bild → PDF" if st.session_state.active_tool == "image_to_pdf" else "PDF → Word"
    st.markdown(
        f"""
        <div class="wf-topbar">
            <div class="wf-brand">
                <div class="wf-logo">W</div>
                <div>Wertfile.</div>
            </div>
            <div class="wf-badge"><span class="wf-dot"></span>Version 1.1 · {tool_text}</div>
        </div>
        <section class="wf-hero">
            <h1>File Conversion.<br><span class="wf-gradient">Einfach, sauber, zuverlässig.</span></h1>
            <p>
                Wertfile 1.1 kann Bilder zu PDF konvertieren und normale Text-PDFs in Word-Dateien umwandeln.
                Diese Version bleibt bewusst stabil, verständlich und testbar.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_tool_selector() -> None:
    st.markdown(
        """
        <div class="wf-toolbar">
            <div class="wf-tool-card"><b>Bild → PDF</b><span>JPG, PNG oder WEBP zu einem sauberen PDF exportieren.</span></div>
            <div class="wf-tool-card"><b>PDF → Word</b><span>Text aus normalen PDFs extrahieren und als DOCX herunterladen.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Bild → PDF öffnen", use_container_width=True):
            st.session_state.active_tool = "image_to_pdf"
            st.rerun()
    with c2:
        if st.button("PDF → Word öffnen", use_container_width=True):
            st.session_state.active_tool = "pdf_to_word"
            st.rerun()


def render_image_to_pdf_steps() -> None:
    st.markdown(
        """
        <div class="wf-stepbar">
            <div class="wf-step"><b>1. Upload</b><span>Bilder auswählen</span></div>
            <div class="wf-step"><b>2. Prüfen</b><span>Vorschau & Reihenfolge</span></div>
            <div class="wf-step"><b>3. Einstellen</b><span>Format & Ränder</span></div>
            <div class="wf-step"><b>4. Export</b><span>PDF herunterladen</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pdf_to_word_steps() -> None:
    st.markdown(
        """
        <div class="wf-stepbar">
            <div class="wf-step"><b>1. PDF Upload</b><span>Text-PDF auswählen</span></div>
            <div class="wf-step"><b>2. Text prüfen</b><span>Seiten & Zeichen erkennen</span></div>
            <div class="wf-step"><b>3. Word erstellen</b><span>DOCX generieren</span></div>
            <div class="wf-step"><b>4. Download</b><span>Word herunterladen</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_image_to_pdf_converter() -> None:
    render_image_to_pdf_steps()
    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown('<div class="wf-card">', unsafe_allow_html=True)
        st.markdown("<h2>Bild → PDF</h2>", unsafe_allow_html=True)
        st.markdown(
            '<p class="wf-card-subtitle">Ziehe deine Bilder in das Feld oder wähle sie manuell aus.</p>',
            unsafe_allow_html=True,
        )

        uploaded_files = st.file_uploader(
            "Bilder hochladen",
            type=SUPPORTED_IMAGE_TYPES,
            accept_multiple_files=True,
            help=f"Unterstützt: {', '.join(SUPPORTED_IMAGE_TYPES).upper()} · Max. {MAX_FILES} Dateien · max. {MAX_TOTAL_MB} MB gesamt.",
        )

        warnings, errors = validate_image_files(uploaded_files)
        for warning in warnings:
            st.warning(warning)
        for error in errors:
            st.error(error)

        if uploaded_files:
            total_mb = sum(mb(file.size) for file in uploaded_files)
            st.markdown(
                f"""
                <div class="wf-info-grid">
                    <div class="wf-info-box"><b>{len(uploaded_files)}</b><span>Dateien</span></div>
                    <div class="wf-info-box"><b>{total_mb:.1f} MB</b><span>Gesamtgröße</span></div>
                    <div class="wf-info-box"><b>PDF</b><span>Export</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown('<div class="wf-file-list">', unsafe_allow_html=True)
            display_files = uploaded_files[:12]
            for file in display_files:
                st.markdown(
                    f'<div class="wf-file-row"><span>{file.name}</span><small>{mb(file.size):.2f} MB</small></div>',
                    unsafe_allow_html=True,
                )
            if len(uploaded_files) > 12:
                st.markdown(
                    f'<div class="wf-file-row"><span>+ {len(uploaded_files) - 12} weitere Dateien</span><small>nicht angezeigt</small></div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3>Einstellungen</h3>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            page_format = st.selectbox(
                "Seitenformat",
                ["A4 Hochformat", "A4 Querformat", "Letter Hochformat", "Letter Querformat", "Originalgröße"],
                index=0,
            )
        with c2:
            margin_size = st.selectbox("Rand", ["Normal", "Klein", "Keine", "Groß"], index=0)

        c3, c4 = st.columns(2)
        with c3:
            sort_mode = st.selectbox("Reihenfolge", ["Upload-Reihenfolge", "Dateiname A–Z", "Dateiname Z–A"], index=0)
        with c4:
            quality_label = st.selectbox("Qualität", ["Hoch", "Ausgewogen", "Kleinere Datei"], index=1)

        quality_map = {"Hoch": 95, "Ausgewogen": 85, "Kleinere Datei": 72}
        quality = quality_map[quality_label]

        disabled = not uploaded_files or bool(errors)

        if disabled:
            st.button("PDF erstellen", use_container_width=True, disabled=True)
        else:
            if st.button("PDF erstellen", use_container_width=True):
                with st.spinner("PDF wird erstellt..."):
                    try:
                        pdf_bytes = create_pdf(uploaded_files, page_format, margin_size, sort_mode, quality)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                        file_name = f"wertfile_export_{timestamp}.pdf"
                        st.success("PDF erfolgreich erstellt.")
                        st.download_button(
                            "PDF herunterladen",
                            data=pdf_bytes,
                            file_name=file_name,
                            mime="application/pdf",
                            use_container_width=True,
                        )
                    except Exception as exc:
                        st.error(str(exc))

        if uploaded_files:
            with st.expander("Originaldateien als ZIP herunterladen"):
                st.write("Optional: Lade die hochgeladenen Originaldateien gesammelt als ZIP herunter.")
                zip_bytes = create_uploaded_zip(uploaded_files)
                st.download_button(
                    "Originale als ZIP herunterladen",
                    data=zip_bytes,
                    file_name=f"wertfile_originale_{datetime.now().strftime('%Y%m%d_%H%M')}.zip",
                    mime="application/zip",
                    use_container_width=True,
                )

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="wf-card">', unsafe_allow_html=True)
        st.markdown("<h2>Vorschau</h2>", unsafe_allow_html=True)
        st.markdown(
            '<p class="wf-card-subtitle">Hier siehst du die erste Seite nach Format- und Rand-Einstellung.</p>',
            unsafe_allow_html=True,
        )

        if uploaded_files and not errors:
            preview_files = list(uploaded_files)
            if sort_mode == "Dateiname A–Z":
                preview_files = sorted(preview_files, key=lambda f: f.name.lower())
            elif sort_mode == "Dateiname Z–A":
                preview_files = sorted(preview_files, key=lambda f: f.name.lower(), reverse=True)

            try:
                preview_image = create_preview_image(preview_files[0], page_format, margin_size)
                st.image(preview_image, caption=f"Erste Seite: {preview_files[0].name}", use_container_width=True)
            except Exception as exc:
                st.error(str(exc))

            st.markdown(
                f"""
                <div class="wf-info-grid">
                    <div class="wf-info-box"><b>{page_format.split()[0]}</b><span>Format</span></div>
                    <div class="wf-info-box"><b>{margin_size}</b><span>Rand</span></div>
                    <div class="wf-info-box"><b>{quality_label}</b><span>Qualität</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="wf-preview-empty">
                    <div>
                        <h3>Noch keine Vorschau</h3>
                        <p>Lade mindestens ein Bild hoch. Danach erscheint hier die Vorschau der ersten PDF-Seite.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)


def render_pdf_to_word_converter() -> None:
    render_pdf_to_word_steps()

    if fitz is None or Document is None:
        st.error("Für PDF → Word fehlen noch Pakete. Bitte im Terminal ausführen: pip install pymupdf python-docx")

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.markdown('<div class="wf-card">', unsafe_allow_html=True)
        st.markdown("<h2>PDF → Word</h2>", unsafe_allow_html=True)
        st.markdown(
            '<p class="wf-card-subtitle">Konvertiert normale Text-PDFs zu einer bearbeitbaren Word-Datei. Scan-PDFs brauchen später OCR.</p>',
            unsafe_allow_html=True,
        )

        pdf_file = st.file_uploader(
            "PDF hochladen",
            type=SUPPORTED_PDF_TYPES,
            accept_multiple_files=False,
            help="Funktioniert am besten mit PDFs, deren Text markierbar/kopierbar ist.",
        )

        errors = validate_pdf_file(pdf_file)
        for error in errors:
            st.error(error)

        output_style = st.selectbox("Word-Struktur", ["Absätze erhalten", "Zeilenweise exportieren"], index=0)
        include_page_numbers = st.checkbox("Seitenüberschriften einfügen", value=True)

        disabled = not pdf_file or bool(errors) or fitz is None or Document is None

        if disabled:
            st.button("Word-Datei erstellen", use_container_width=True, disabled=True)
        else:
            if st.button("Word-Datei erstellen", use_container_width=True):
                with st.spinner("Text wird extrahiert und Word-Datei erstellt..."):
                    try:
                        docx_bytes, page_count, total_chars = create_word_from_pdf_text(
                            pdf_file,
                            output_style,
                            include_page_numbers,
                        )
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                        clean_name = pdf_file.name.rsplit(".", 1)[0].replace(" ", "_")
                        st.success(f"Word-Datei erstellt. Seiten: {page_count} · Zeichen: {total_chars}")
                        st.download_button(
                            "Word-Datei herunterladen",
                            data=docx_bytes,
                            file_name=f"wertfile_{clean_name}_{timestamp}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True,
                        )
                    except Exception as exc:
                        st.error(str(exc))

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="wf-card">', unsafe_allow_html=True)
        st.markdown("<h2>PDF-Analyse</h2>", unsafe_allow_html=True)
        st.markdown(
            '<p class="wf-card-subtitle">Prüft, ob Text im PDF gefunden wird.</p>',
            unsafe_allow_html=True,
        )

        if pdf_file and not errors and fitz is not None:
            try:
                pages, page_count, total_chars = extract_pdf_text(pdf_file)
                text_pages = sum(1 for page in pages if page["text"].strip())
                st.markdown(
                    f"""
                    <div class="wf-info-grid">
                        <div class="wf-info-box"><b>{page_count}</b><span>Seiten</span></div>
                        <div class="wf-info-box"><b>{text_pages}</b><span>mit Text</span></div>
                        <div class="wf-info-box"><b>{total_chars}</b><span>Zeichen</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if total_chars < 20:
                    st.warning("Es wurde kaum Text gefunden. Diese PDF ist wahrscheinlich gescannt. OCR folgt später.")
                else:
                    st.success("Text wurde gefunden. Die PDF eignet sich wahrscheinlich für PDF → Word.")

                first_text = ""
                for page in pages:
                    if page["text"].strip():
                        first_text = page["text"].strip()[:2200]
                        break

                if first_text:
                    st.text_area("Text-Vorschau", first_text, height=260)
            except Exception as exc:
                st.error(str(exc))
        else:
            st.markdown(
                """
                <div class="wf-preview-empty">
                    <div>
                        <h3>Noch keine PDF-Analyse</h3>
                        <p>Lade eine PDF hoch. Danach siehst du hier Seitenanzahl, erkannte Zeichen und eine Text-Vorschau.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)


def render_test_plan() -> None:
    with st.expander("Testplan für Wertfile 1.1"):
        st.markdown(
            """
            <div class="wf-test-card">
                <b>Bild → PDF testen:</b>
                <ul>
                    <li>1 JPG hochladen → PDF erstellen → Download öffnen</li>
                    <li>3 Bilder hochladen → Reihenfolge prüfen → PDF öffnen</li>
                    <li>PNG und WEBP testen</li>
                    <li>A4 Hochformat und A4 Querformat testen</li>
                </ul>
                <br>
                <b>PDF → Word testen:</b>
                <ul>
                    <li>Text-PDF hochladen → Analyse prüfen → Word erstellen</li>
                    <li>DOCX herunterladen und in Word/Pages/Google Docs öffnen</li>
                    <li>Gescannte PDF testen → Warnung sollte erscheinen</li>
                    <li>PDF ohne Text testen → OCR-Hinweis sollte erscheinen</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_footer() -> None:
    st.markdown(
        f'<div class="wf-footer">{APP_NAME}. Technology Germany · Version 1.1 · Dateien werden in dieser Session verarbeitet und nicht bewusst dauerhaft gespeichert.</div>',
        unsafe_allow_html=True,
    )


# ---------- Render ----------
inject_css()
render_header()
render_tool_selector()

if st.session_state.active_tool == "image_to_pdf":
    render_image_to_pdf_converter()
else:
    render_pdf_to_word_converter()

render_test_plan()
render_footer()
