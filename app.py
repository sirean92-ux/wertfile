import streamlit as st
from PIL import Image, ImageOps
import io
from datetime import datetime

# =========================================================
# WERTFILE — Premium Streamlit Web App
# Clean SaaS/Product-App Layout mit beweglichen 3D-Orbs
# =========================================================

st.set_page_config(
    page_title="Wertfile | Smart File Workspace",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- State ----------
if "active_tool" not in st.session_state:
    st.session_state.active_tool = "pdf"


def set_tool(tool_name: str):
    st.session_state.active_tool = tool_name


# ---------- CSS ----------
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {
            --bg: #F6F8FC;
            --ink: #08111F;
            --muted: #64748B;
            --line: rgba(148, 163, 184, 0.24);
            --white-glass: rgba(255, 255, 255, 0.72);
            --white-strong: rgba(255, 255, 255, 0.92);
            --primary: #101828;
            --purple: #7C3AED;
            --pink: #DB2777;
            --blue: #2563EB;
            --green: #10B981;
            --shadow-soft: 0 22px 70px rgba(15, 23, 42, 0.10);
            --shadow-hover: 0 34px 100px rgba(15, 23, 42, 0.16);
            --radius-xl: 34px;
            --radius-lg: 24px;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 18%, rgba(124,58,237,0.13), transparent 28%),
                radial-gradient(circle at 88% 16%, rgba(34,211,238,0.14), transparent 30%),
                radial-gradient(circle at 50% 100%, rgba(219,39,119,0.10), transparent 34%),
                linear-gradient(180deg, #F8FAFC 0%, #EEF3F9 100%) !important;
            color: var(--ink);
        }

        header, footer, .stDeployButton, #MainMenu {
            display: none !important;
        }

        .block-container {
            max-width: 1320px;
            padding-top: 98px !important;
            padding-bottom: 54px !important;
        }

        h1, h2, h3, h4, p, span, label, div {
            color: var(--ink);
        }

        p { line-height: 1.62; }

        /* ---------- Motion ---------- */
        @keyframes orb-dance {
            0%, 100% { transform: translate3d(0, 0, 0) rotate(0deg) scale(1); }
            20% { transform: translate3d(4px, -9px, 0) rotate(8deg) scale(1.045); }
            45% { transform: translate3d(-3px, -3px, 0) rotate(-5deg) scale(0.99); }
            70% { transform: translate3d(5px, 6px, 0) rotate(6deg) scale(1.03); }
        }

        @keyframes orb-glow {
            0%, 100% { filter: saturate(1.02) brightness(1); }
            50% { filter: saturate(1.25) brightness(1.08); }
        }

        @keyframes soft-float {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-7px) scale(1.006); }
        }

        @keyframes shine-sweep {
            0% { transform: translateX(-140%) rotate(18deg); opacity: 0; }
            35% { opacity: .55; }
            100% { transform: translateX(160%) rotate(18deg); opacity: 0; }
        }

        @keyframes background-orb-1 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(18px, -16px) scale(1.08); }
        }

        @keyframes background-orb-2 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(-14px, 12px) scale(0.96); }
        }

        /* ---------- Nav ---------- */
        .wf-nav {
            position: fixed;
            top: 18px;
            left: 50%;
            transform: translateX(-50%);
            width: min(1260px, calc(100% - 32px));
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 13px 16px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.75);
            background: rgba(255,255,255,0.72);
            backdrop-filter: blur(24px) saturate(1.35);
            -webkit-backdrop-filter: blur(24px) saturate(1.35);
            box-shadow: 0 20px 70px rgba(15,23,42,0.08);
        }

        .wf-brand {
            display: flex;
            align-items: center;
            gap: 11px;
            font-weight: 900;
            letter-spacing: -0.7px;
            font-size: 23px;
        }

        .wf-nav-links {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 4px;
            border-radius: 999px;
            background: rgba(248,250,252,0.75);
            border: 1px solid rgba(226,232,240,0.78);
        }

        .wf-nav-links span {
            padding: 10px 16px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 800;
            color: #475569 !important;
        }

        .wf-nav-links span:first-child {
            background: white;
            color: #101828 !important;
            box-shadow: 0 10px 24px rgba(15,23,42,0.06);
        }

        .wf-nav-cta {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .wf-nav-pill {
            border-radius: 999px;
            padding: 10px 14px;
            background: #101828;
            color: white !important;
            font-weight: 850;
            font-size: 13px;
            box-shadow: 0 14px 30px rgba(16,24,40,0.18);
        }

        /* ---------- Orbs ---------- */
        .wf-orb {
            width: 72px;
            height: 72px;
            border-radius: 999px;
            position: relative;
            overflow: hidden;
            isolation: isolate;
            flex: 0 0 auto;
            background:
                radial-gradient(circle at 28% 22%, rgba(255,255,255,0.98) 0 7%, transparent 20%),
                radial-gradient(circle at 72% 28%, rgba(255,255,255,0.52) 0 8%, transparent 25%),
                radial-gradient(circle at 64% 78%, rgba(255,255,255,0.34) 0 9%, transparent 30%),
                linear-gradient(135deg, rgba(255,130,210,0.98), rgba(139,92,246,0.92), rgba(34,211,238,0.86));
            box-shadow:
                inset 13px 14px 24px rgba(255,255,255,0.42),
                inset -18px -20px 30px rgba(88,28,135,0.20),
                0 22px 44px rgba(124,58,237,0.24),
                0 8px 18px rgba(15,23,42,0.08);
            animation: orb-dance 5.2s ease-in-out infinite, orb-glow 3.8s ease-in-out infinite;
            will-change: transform, filter;
            transition: transform .35s cubic-bezier(.2,.8,.2,1), box-shadow .35s ease;
        }

        .wf-orb::before {
            content: "";
            position: absolute;
            inset: 8px;
            border-radius: 50%;
            border: 1px solid rgba(255,255,255,0.58);
            background:
                linear-gradient(112deg, transparent 18%, rgba(255,255,255,0.58) 31%, transparent 43%),
                linear-gradient(30deg, transparent 30%, rgba(255,255,255,0.28) 47%, transparent 60%);
            transform: rotate(-26deg) scale(1.08);
            z-index: 1;
        }

        .wf-orb::after {
            content: "";
            position: absolute;
            width: 96px;
            height: 38px;
            left: -11px;
            top: 25px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.50);
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.34), transparent);
            transform: rotate(-31deg);
            z-index: 2;
        }

        .wf-orb:hover {
            animation-play-state: paused;
            transform: translateY(-10px) rotate(9deg) scale(1.13) !important;
            box-shadow:
                inset 13px 14px 24px rgba(255,255,255,0.46),
                inset -18px -20px 30px rgba(88,28,135,0.22),
                0 30px 70px rgba(124,58,237,0.34),
                0 10px 22px rgba(15,23,42,0.10);
        }

        .wf-orb.small { width: 44px; height: 44px; }
        .wf-orb.medium { width: 62px; height: 62px; }
        .wf-orb.large { width: 112px; height: 112px; }

        .blue-orb {
            background:
                radial-gradient(circle at 28% 22%, rgba(255,255,255,0.98) 0 7%, transparent 20%),
                radial-gradient(circle at 72% 28%, rgba(255,255,255,0.54) 0 8%, transparent 25%),
                linear-gradient(135deg, #A5B4FC 0%, #7C3AED 42%, #0EA5E9 100%);
            box-shadow: inset 13px 14px 24px rgba(255,255,255,0.42), inset -18px -20px 30px rgba(30,64,175,0.20), 0 22px 44px rgba(59,130,246,0.25), 0 8px 18px rgba(15,23,42,0.08);
        }

        .pink-orb {
            background:
                radial-gradient(circle at 28% 22%, rgba(255,255,255,0.98) 0 7%, transparent 20%),
                radial-gradient(circle at 72% 28%, rgba(255,255,255,0.54) 0 8%, transparent 25%),
                linear-gradient(135deg, #FDBA74 0%, #F472B6 42%, #7C3AED 100%);
            box-shadow: inset 13px 14px 24px rgba(255,255,255,0.42), inset -18px -20px 30px rgba(157,23,77,0.18), 0 22px 44px rgba(219,39,119,0.24), 0 8px 18px rgba(15,23,42,0.08);
            animation-delay: -1.2s;
        }

        .green-orb {
            background:
                radial-gradient(circle at 28% 22%, rgba(255,255,255,0.98) 0 7%, transparent 20%),
                radial-gradient(circle at 72% 28%, rgba(255,255,255,0.54) 0 8%, transparent 25%),
                linear-gradient(135deg, #A7F3D0 0%, #34D399 40%, #2563EB 100%);
            box-shadow: inset 13px 14px 24px rgba(255,255,255,0.42), inset -18px -20px 30px rgba(6,95,70,0.18), 0 22px 44px rgba(16,185,129,0.24), 0 8px 18px rgba(15,23,42,0.08);
            animation-delay: -2.2s;
        }

        /* ---------- Hero ---------- */
        .wf-hero {
            position: relative;
            display: grid;
            grid-template-columns: 0.95fr 1.05fr;
            gap: 26px;
            align-items: center;
            margin-bottom: 22px;
            min-height: 390px;
        }

        .wf-floating-bg {
            position: absolute;
            right: 7%;
            top: 24px;
            width: 230px;
            height: 230px;
            border-radius: 50%;
            background:
                radial-gradient(circle at 30% 20%, rgba(255,255,255,0.95), transparent 13%),
                linear-gradient(135deg, rgba(244,114,182,0.42), rgba(124,58,237,0.34), rgba(34,211,238,0.32));
            filter: blur(0.2px);
            box-shadow: 0 34px 110px rgba(124,58,237,0.20);
            animation: background-orb-1 7s ease-in-out infinite;
            pointer-events: none;
        }

        .wf-floating-bg.two {
            width: 82px;
            height: 82px;
            right: 1%;
            top: 215px;
            opacity: .72;
            animation: background-orb-2 6s ease-in-out infinite;
        }

        .wf-kicker {
            width: fit-content;
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 9px 13px;
            border-radius: 999px;
            background: rgba(255,255,255,0.72);
            border: 1px solid rgba(255,255,255,0.82);
            backdrop-filter: blur(18px);
            box-shadow: 0 14px 32px rgba(15,23,42,0.06);
            font-size: 13px;
            font-weight: 850;
            color: #7C3AED !important;
            margin-bottom: 20px;
        }

        .wf-hero h1 {
            font-size: clamp(45px, 5.2vw, 76px);
            line-height: .96;
            letter-spacing: -4.2px;
            margin: 0 0 20px 0;
            font-weight: 900;
        }

        .gradient-word {
            background: linear-gradient(90deg, #2563EB, #7C3AED, #DB2777);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent !important;
        }

        .wf-hero-copy {
            color: #64748B !important;
            font-size: 17px;
            max-width: 610px;
            margin-bottom: 26px;
        }

        .wf-hero-actions {
            display: flex;
            align-items: center;
            gap: 14px;
            flex-wrap: wrap;
        }

        .wf-main-btn, .wf-soft-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            min-height: 48px;
            padding: 0 18px;
            border-radius: 16px;
            font-size: 14px;
            font-weight: 850;
        }

        .wf-main-btn {
            color: white !important;
            background: #101828;
            box-shadow: 0 16px 34px rgba(16,24,40,0.22);
        }

        .wf-soft-btn {
            color: #475569 !important;
            background: rgba(255,255,255,0.72);
            border: 1px solid rgba(255,255,255,0.78);
        }

        .wf-hero-tools {
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }

        /* ---------- Cards ---------- */
        .glass-card {
            position: relative;
            overflow: hidden;
            border-radius: var(--radius-xl);
            background: linear-gradient(145deg, rgba(255,255,255,0.92), rgba(255,255,255,0.58));
            border: 1px solid rgba(255,255,255,0.78);
            backdrop-filter: blur(26px) saturate(1.35);
            -webkit-backdrop-filter: blur(26px) saturate(1.35);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.88),
                var(--shadow-soft);
            transition: transform .35s cubic-bezier(.2,.8,.2,1), box-shadow .35s ease, border-color .35s ease;
        }

        .glass-card::before {
            content: "";
            position: absolute;
            top: -30%;
            left: -70%;
            width: 52%;
            height: 160%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.55), transparent);
            transform: rotate(18deg);
            opacity: 0;
            pointer-events: none;
        }

        .glass-card:hover {
            transform: translateY(-8px) scale(1.01);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.94),
                var(--shadow-hover);
        }

        .glass-card:hover::before {
            animation: shine-sweep 1s ease forwards;
        }

        .tool-card {
            min-height: 270px;
            padding: 26px;
            animation: soft-float 7s ease-in-out infinite;
        }

        .tool-card:nth-child(2) { animation-delay: -1.6s; }
        .tool-card:nth-child(3) { animation-delay: -3.2s; }

        .tool-card h3 {
            margin: 18px 0 8px 0;
            font-size: 21px;
            letter-spacing: -0.6px;
            font-weight: 900;
        }

        .tool-card p {
            color: #64748B !important;
            margin: 0 0 18px 0;
            font-size: 14px;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(248,250,252,0.88);
            border: 1px solid rgba(226,232,240,0.78);
            color: #334155 !important;
            font-size: 12px;
            font-weight: 850;
        }

        .green-dot, .gray-dot, .pink-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            display: inline-block;
        }
        .green-dot { background: #10B981; box-shadow: 0 0 0 5px rgba(16,185,129,0.12); }
        .gray-dot { background: #94A3B8; }
        .pink-dot { background: #F472B6; box-shadow: 0 0 0 5px rgba(244,114,182,0.12); }

        /* ---------- Native Streamlit Buttons for Tool Selection ---------- */
        div[data-testid="stHorizontalBlock"] .stButton > button {
            min-height: 48px !important;
        }

        .stButton > button, .stDownloadButton > button {
            border-radius: 17px !important;
            min-height: 54px !important;
            border: none !important;
            color: white !important;
            background: #101828 !important;
            font-weight: 850 !important;
            box-shadow: 0 16px 34px rgba(16,24,40,0.18) !important;
            transition: transform .23s ease, box-shadow .23s ease !important;
        }

        .stButton > button:hover, .stDownloadButton > button:hover {
            transform: translateY(-2px) scale(1.006);
            box-shadow: 0 20px 46px rgba(16,24,40,0.25) !important;
        }

        /* ---------- Workspace ---------- */
        .workspace-shell {
            margin-top: 20px;
            padding: 26px;
            border-radius: 36px;
        }

        .workspace-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 18px;
            margin-bottom: 22px;
        }

        .workspace-title {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .workspace-title h2 {
            margin: 0;
            font-size: 27px;
            letter-spacing: -1px;
            font-weight: 900;
        }

        .workspace-title h2 span {
            color: #DB2777 !important;
        }

        .workspace-title p {
            margin: 4px 0 0 0;
            color: #64748B !important;
            font-size: 14px;
            font-weight: 650;
        }

        .workspace-grid {
            display: grid;
            grid-template-columns: 1.02fr 0.98fr;
            gap: 18px;
        }

        .panel {
            border-radius: 28px;
            padding: 22px;
        }

        .panel h3 {
            margin: 0 0 14px 0;
            font-size: 17px;
            letter-spacing: -0.4px;
            font-weight: 900;
        }

        .empty-preview {
            min-height: 315px;
            display: grid;
            place-items: center;
            text-align: center;
            border-radius: 24px;
            background: rgba(248,250,252,0.72);
            border: 1px solid rgba(226,232,240,0.75);
        }

        .empty-preview p {
            color: #64748B !important;
            margin: 8px 0 0 0;
            max-width: 360px;
        }

        .file-list {
            margin-top: 14px;
            display: grid;
            gap: 8px;
        }

        .file-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 11px 13px;
            border-radius: 15px;
            background: rgba(248,250,252,0.82);
            border: 1px solid rgba(226,232,240,0.72);
            font-size: 13px;
            font-weight: 750;
        }

        .file-row span:last-child {
            color: #64748B !important;
        }

        /* ---------- Form Elements ---------- */
        .stFileUploader section {
            border-radius: 26px !important;
            border: 1.5px dashed rgba(124,58,237,0.36) !important;
            background:
                radial-gradient(circle at 50% 0%, rgba(124,58,237,0.08), transparent 32%),
                linear-gradient(145deg, rgba(255,255,255,0.94), rgba(255,255,255,0.68)) !important;
            padding: 34px !important;
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.88),
                0 18px 46px rgba(15,23,42,0.08) !important;
            backdrop-filter: blur(20px) saturate(1.3);
            -webkit-backdrop-filter: blur(20px) saturate(1.3);
            transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
        }

        .stFileUploader section:hover {
            transform: translateY(-3px);
            border-color: rgba(124,58,237,0.58) !important;
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.95),
                0 24px 64px rgba(124,58,237,0.12) !important;
        }

        .stFileUploader section svg,
        .stSelectbox svg,
        .stTextInput svg {
            color: #0F172A !important;
            fill: #0F172A !important;
            opacity: 1 !important;
            filter: drop-shadow(0 3px 6px rgba(15,23,42,0.16));
        }

        .stFileUploader label, .stTextInput label, .stSelectbox label, .stCheckbox label {
            font-weight: 850 !important;
            color: #101828 !important;
        }

        .stTextInput input,
        .stSelectbox [data-baseweb="select"],
        .stSelectbox [data-baseweb="select"] > div {
            min-height: 56px !important;
            border-radius: 18px !important;
            border: 1px solid rgba(100,116,139,0.38) !important;
            background: rgba(255,255,255,0.96) !important;
            color: #0B1020 !important;
            font-weight: 800 !important;
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.95),
                0 14px 34px rgba(15,23,42,0.08) !important;
            transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease !important;
        }

        .stTextInput input:focus,
        .stSelectbox [data-baseweb="select"]:focus-within {
            border-color: rgba(124,58,237,0.62) !important;
            box-shadow:
                0 0 0 5px rgba(124,58,237,0.10),
                0 18px 44px rgba(15,23,42,0.12) !important;
            transform: translateY(-1px);
        }

        .stTextInput input::placeholder {
            color: #94A3B8 !important;
            font-weight: 700 !important;
        }

        .stAlert {
            border-radius: 20px !important;
        }

        /* ---------- Footer ---------- */
        .wf-footer {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-top: 18px;
            padding: 14px;
            border-radius: 24px;
            background: rgba(255,255,255,0.52);
            border: 1px solid rgba(255,255,255,0.72);
            backdrop-filter: blur(18px);
        }

        .wf-footer-item {
            text-align: center;
            color: #64748B !important;
            font-size: 13px;
            font-weight: 750;
        }

        @media (max-width: 1050px) {
            .wf-hero, .workspace-grid { grid-template-columns: 1fr; }
            .wf-hero-tools { grid-template-columns: 1fr; }
            .wf-floating-bg { opacity: .35; }
            .wf-nav-links { display: none; }
            .wf-footer { grid-template-columns: 1fr 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------- UI Blocks ----------
def render_nav():
    st.markdown(
        """
        <div class="wf-nav">
            <div class="wf-brand">
                <div class="wf-orb small blue-orb"></div>
                <div>Wertfile.</div>
            </div>
            <div class="wf-nav-links">
                <span>Workspace</span>
                <span>Tools</span>
                <span>Preise</span>
                <span>Ressourcen</span>
            </div>
            <div class="wf-nav-cta">
                <span class="wf-nav-pill">Kostenlos starten</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <section class="wf-hero">
            <div class="wf-floating-bg"></div>
            <div class="wf-floating-bg two"></div>
            <div>
                <div class="wf-kicker">
                    <div class="wf-orb small pink-orb"></div>
                    File Operations. Smarter.
                </div>
                <h1>Ein Workspace.<br><span class="gradient-word">Mehrere Tools.</span></h1>
                <p class="wf-hero-copy">
                    Wertfile kombiniert leistungsstarke Module für Konvertierung,
                    Verarbeitung und sichere Datenflüsse — schnell, zuverlässig und audit-ready.
                </p>
                <div class="wf-hero-actions">
                    <span class="wf-main-btn">Loslegen →</span>
                    <span class="wf-soft-btn">▷ So funktioniert’s</span>
                </div>
            </div>
            <div class="wf-hero-tools">
                <div class="glass-card tool-card">
                    <div class="wf-orb blue-orb"></div>
                    <h3>Document Converter</h3>
                    <p>JPG und PNG hochladen, Reihenfolge prüfen und als sauberes PDF exportieren.</p>
                    <span class="status-pill"><span class="green-dot"></span>Live verfügbar</span>
                </div>
                <div class="glass-card tool-card">
                    <div class="wf-orb pink-orb"></div>
                    <h3>Video Tools</h3>
                    <p>Geplant für Video-Komprimierung, Audio-Export und Format-Workflows.</p>
                    <span class="status-pill"><span class="pink-dot"></span>Coming soon</span>
                </div>
                <div class="glass-card tool-card">
                    <div class="wf-orb green-orb"></div>
                    <h3>Security</h3>
                    <p>Klare Session-Logik, lokale Verarbeitung und optionale Audit-Logs.</p>
                    <span class="status-pill"><span class="green-dot"></span>Foundation ready</span>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_tool_selector():
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        if st.button("PDF Workspace öffnen", use_container_width=True):
            set_tool("pdf")
    with c2:
        if st.button("Video Tools öffnen", use_container_width=True):
            set_tool("video")
    with c3:
        if st.button("Security ansehen", use_container_width=True):
            set_tool("security")


# ---------- PDF Logic ----------
def make_pdf(uploaded_files, page_fit="A4 Portrait", sort_by_name=True):
    files = list(uploaded_files)
    if sort_by_name:
        files = sorted(files, key=lambda f: f.name.lower())

    images = []
    for file in files:
        img = Image.open(file)
        img = ImageOps.exif_transpose(img).convert("RGB")

        if page_fit == "A4 Portrait":
            canvas = Image.new("RGB", (1240, 1754), "white")
            img.thumbnail((1120, 1634), Image.Resampling.LANCZOS)
            canvas.paste(img, ((1240 - img.width) // 2, (1754 - img.height) // 2))
            img = canvas
        elif page_fit == "A4 Landscape":
            canvas = Image.new("RGB", (1754, 1240), "white")
            img.thumbnail((1634, 1120), Image.Resampling.LANCZOS)
            canvas.paste(img, ((1754 - img.width) // 2, (1240 - img.height) // 2))
            img = canvas

        images.append(img)

    pdf_buffer = io.BytesIO()
    images[0].save(
        pdf_buffer,
        format="PDF",
        save_all=True,
        append_images=images[1:],
        resolution=150.0,
        quality=95,
    )
    pdf_buffer.seek(0)
    return pdf_buffer


def render_pdf_workspace():
    st.markdown(
        """
        <div class="glass-card workspace-shell">
            <div class="workspace-head">
                <div class="workspace-title">
                    <div class="wf-orb medium blue-orb"></div>
                    <div>
                        <h2><span>PDF</span> Workspace</h2>
                        <p>Upload, Reihenfolge, Seitenformat und Export in einem Premium-Flow.</p>
                    </div>
                </div>
                <span class="status-pill"><span class="green-dot"></span>Production Module</span>
            </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.markdown('<div class="glass-card panel">', unsafe_allow_html=True)
        st.markdown("<h3>Dateien hochladen</h3>", unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Ziehe deine Bilder hier rein oder wähle Dateien aus",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            help="Unterstützt JPG, JPEG und PNG. Mehrere Bilder werden zu einem PDF zusammengeführt.",
        )

        st.markdown("<h3 style='margin-top:20px;'>Einstellungen</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            page_fit = st.selectbox("Seitenformat", ["A4 Portrait", "A4 Landscape", "Original"], index=0)
        with c2:
            sort_by_name = st.checkbox("Nach Dateiname sortieren", value=True)

        if uploaded_files:
            files_for_display = sorted(uploaded_files, key=lambda f: f.name.lower()) if sort_by_name else uploaded_files
            total_size_mb = sum(file.size for file in uploaded_files) / (1024 * 1024)
            st.markdown('<div class="file-list">', unsafe_allow_html=True)
            for file in files_for_display:
                st.markdown(
                    f'<div class="file-row"><span>📄 {file.name}</span><span>{file.size / (1024 * 1024):.2f} MB</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

            st.caption(f"Gesamtgröße: {total_size_mb:.2f} MB · {len(uploaded_files)} Datei(en)")

            if st.button("PDF erstellen", use_container_width=True):
                try:
                    pdf_buffer = make_pdf(uploaded_files, page_fit, sort_by_name)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                    st.success("Dein PDF ist bereit.")
                    st.download_button(
                        "PDF herunterladen",
                        data=pdf_buffer.getvalue(),
                        file_name=f"wertfile_export_{timestamp}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"PDF konnte nicht erstellt werden: {e}")
        else:
            st.info("Lade mindestens ein Bild hoch, um dein PDF zu erstellen.")

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="glass-card panel">', unsafe_allow_html=True)
        st.markdown("<h3>Vorschau & Informationen</h3>", unsafe_allow_html=True)

        if uploaded_files:
            files_for_preview = sorted(uploaded_files, key=lambda f: f.name.lower()) if sort_by_name else uploaded_files
            img = Image.open(files_for_preview[0])
            img = ImageOps.exif_transpose(img)
            st.image(img, caption=f"Erste Seite: {files_for_preview[0].name}", use_container_width=True)
            st.markdown(
                f"""
                <div class="file-list">
                    <div class="file-row"><span>Dateien</span><span>{len(uploaded_files)}</span></div>
                    <div class="file-row"><span>Seitenformat</span><span>{page_fit}</span></div>
                    <div class="file-row"><span>Verarbeitung</span><span>Session-basiert</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="empty-preview">
                    <div>
                        <div class="wf-orb medium pink-orb" style="margin:0 auto 18px auto;"></div>
                        <h3>Deine Dateien erscheinen hier.</h3>
                        <p>Sortiere, prüfe die Reihenfolge und exportiere ein sauberes, optimiertes PDF.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_video_workspace():
    st.markdown(
        """
        <div class="glass-card workspace-shell">
            <div class="workspace-head">
                <div class="workspace-title">
                    <div class="wf-orb medium pink-orb"></div>
                    <div>
                        <h2><span>Video</span> Tools</h2>
                        <p>Vorbereitet für Komprimierung, Audio-Export und Format-Workflows.</p>
                    </div>
                </div>
                <span class="status-pill"><span class="pink-dot"></span>Coming soon</span>
            </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown('<div class="glass-card panel">', unsafe_allow_html=True)
        st.markdown("<h3>Video Workflow</h3>", unsafe_allow_html=True)
        st.text_input("Video URL", placeholder="https://www.example.com/video")
        st.selectbox("Zielformat", ["MP3 Audio", "MP4 Video", "Compressed MP4", "WebM"])
        st.selectbox("Qualität", ["High", "Balanced", "Small File"])
        if st.button("Workflow vorbereiten", use_container_width=True):
            st.warning("Backend noch nicht verbunden. Die UI ist vorbereitet.")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown(
            """
            <div class="glass-card panel">
                <h3>Geplante Pipeline</h3>
                <div class="empty-preview">
                    <div>
                        <div class="wf-orb medium pink-orb" style="margin:0 auto 18px auto;"></div>
                        <h3>Sauberer Backend-Flow</h3>
                        <p>Upload prüfen → Job Queue → ffmpeg → Download Token → Auto Delete.</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def render_security_workspace():
    st.markdown(
        """
        <div class="glass-card workspace-shell">
            <div class="workspace-head">
                <div class="workspace-title">
                    <div class="wf-orb medium green-orb"></div>
                    <div>
                        <h2><span>Security</span> Layer</h2>
                        <p>Vertrauen, Datenschutz und saubere File-Verarbeitung als Produktbasis.</p>
                    </div>
                </div>
                <span class="status-pill"><span class="green-dot"></span>Foundation ready</span>
            </div>
            <div class="workspace-grid">
                <div class="glass-card panel">
                    <div class="wf-orb green-orb"></div>
                    <h3>Session-basiert</h3>
                    <p style="color:#64748B !important;">Dateien werden aktuell nur während der Session verarbeitet und nicht dauerhaft gespeichert.</p>
                </div>
                <div class="glass-card panel">
                    <div class="wf-orb blue-orb"></div>
                    <h3>Audit-ready</h3>
                    <p style="color:#64748B !important;">Später möglich: Verarbeitungsprotokolle, Löschfristen, Nutzerrollen und Export-Historie.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="wf-footer">
            <div class="wf-footer-item">🔒 DSGVO-konform gedacht</div>
            <div class="wf-footer-item">⚡ Schnelle Verarbeitung</div>
            <div class="wf-footer-item">🧾 Audit-ready Roadmap</div>
            <div class="wf-footer-item">🇩🇪 Produktidee Germany</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Render ----------
inject_css()
render_nav()
render_hero()
render_tool_selector()

if st.session_state.active_tool == "pdf":
    render_pdf_workspace()
elif st.session_state.active_tool == "video":
    render_video_workspace()
else:
    render_security_workspace()

render_footer()
