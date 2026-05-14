import streamlit as st
from PIL import Image, ImageOps
import io
from datetime import datetime

# =========================================================
# WERTFILE — Premium Streamlit Web App
# Ziel: Moderne SaaS-/Fintech-Optik ähnlich Finom, Qonto, Linear
# Module placeholders, Security Layer
# =========================================================

st.set_page_config(
    page_title="Wertfile | Smart File Workspace",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Helper ----------
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {
            --bg: #F5F7FB;
            --surface: #FFFFFF;
            --surface-soft: #F8FAFC;
            --ink: #0B1020;
            --muted: #64748B;
            --line: #E2E8F0;
            --primary: #101828;
            --primary-2: #1D4ED8;
            --green: #10B981;
            --green-soft: #D1FAE5;
            --blue-soft: #DBEAFE;
            --violet-soft: #EDE9FE;
            --orange-soft: #FFEDD5;
            --shadow-sm: 0 8px 24px rgba(15, 23, 42, 0.06);
            --shadow-md: 0 18px 60px rgba(15, 23, 42, 0.10);
            --radius-xl: 28px;
            --radius-lg: 22px;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(59, 130, 246, 0.16), transparent 35%),
                radial-gradient(circle at 85% 8%, rgba(16, 185, 129, 0.15), transparent 28%),
                linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%) !important;
            color: var(--ink);
        }

        header, footer, .stDeployButton, #MainMenu {
            display: none !important;
        }

        .block-container {
            max-width: 1240px;
            padding-top: 108px !important;
            padding-bottom: 64px !important;
        }

        h1, h2, h3, h4, p, span, label, div {
            color: var(--ink);
        }

        p {
            line-height: 1.65;
        }

        /* Top Navigation */
        .wf-nav {
            position: fixed;
            top: 18px;
            left: 50%;
            transform: translateX(-50%);
            width: min(1180px, calc(100% - 32px));
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 14px 12px 18px;
            border: 1px solid rgba(226, 232, 240, 0.9);
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.78);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            box-shadow: 0 20px 80px rgba(15, 23, 42, 0.08);
        }

        .wf-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 900;
            letter-spacing: -0.6px;
            font-size: 21px;
        }

        .wf-logo {
            width: 36px;
            height: 36px;
            border-radius: 13px;
            display: grid;
            place-items: center;
            color: white;
            background: linear-gradient(135deg, #101828 0%, #1D4ED8 65%, #10B981 100%);
            box-shadow: 0 10px 28px rgba(29, 78, 216, 0.28);
        }

        .wf-nav-links {
            display: flex;
            align-items: center;
            gap: 22px;
            font-size: 14px;
            font-weight: 700;
            color: #334155;
        }

        .wf-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 14px;
            border-radius: 999px;
            background: #0B1020;
            color: #FFFFFF !important;
            font-size: 13px;
            font-weight: 800;
        }

        .wf-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: #10B981;
            display: inline-block;
            box-shadow: 0 0 0 6px rgba(16, 185, 129, 0.12);
        }

        /* Hero */
        .wf-hero {
            display: grid;
            grid-template-columns: 1.06fr 0.94fr;
            gap: 26px;
            align-items: stretch;
            margin-bottom: 26px;
        }

        .wf-hero-left {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(226, 232, 240, 0.95);
            border-radius: 36px;
            padding: 54px;
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
        }

        .wf-hero-left::after {
            content: '';
            position: absolute;
            right: -120px;
            bottom: -130px;
            width: 320px;
            height: 320px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(29, 78, 216, 0.17), transparent 70%);
        }

        .wf-kicker {
            width: fit-content;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 999px;
            background: #EEF2FF;
            color: #3730A3 !important;
            font-size: 13px;
            font-weight: 800;
            margin-bottom: 22px;
        }

        .wf-hero-title {
            font-size: clamp(44px, 5vw, 76px);
            line-height: 0.95;
            letter-spacing: -4px;
            font-weight: 900;
            margin: 0 0 22px 0;
        }

        .wf-gradient-text {
            background: linear-gradient(90deg, #101828 0%, #1D4ED8 50%, #10B981 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent !important;
        }

        .wf-hero-copy {
            font-size: 18px;
            color: #475569 !important;
            max-width: 660px;
            margin-bottom: 28px;
        }

        .wf-hero-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
        }

        .wf-btn-main, .wf-btn-secondary {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 48px;
            padding: 0 18px;
            border-radius: 16px;
            font-weight: 850;
            font-size: 14px;
        }

        .wf-btn-main {
            color: white !important;
            background: #101828;
            box-shadow: 0 14px 32px rgba(16, 24, 40, 0.22);
        }

        .wf-btn-secondary {
            color: #101828 !important;
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
        }

        .wf-hero-right {
            display: grid;
            gap: 16px;
        }

        .wf-app-card {
            border-radius: 34px;
            padding: 24px;
            background: #101828;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(255, 255, 255, 0.08);
            overflow: hidden;
            position: relative;
        }

        .wf-app-card::before {
            content: '';
            position: absolute;
            top: -100px;
            right: -70px;
            width: 240px;
            height: 240px;
            border-radius: 999px;
            background: rgba(16, 185, 129, 0.24);
            filter: blur(3px);
        }

        .wf-app-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
        }

        .wf-app-title {
            color: white !important;
            font-size: 17px;
            font-weight: 850;
        }

        .wf-app-badge {
            color: #A7F3D0 !important;
            background: rgba(16, 185, 129, 0.14);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-radius: 999px;
            padding: 7px 10px;
            font-size: 12px;
            font-weight: 800;
        }

        .wf-phone {
            margin-top: 26px;
            border-radius: 30px;
            padding: 18px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.10);
            position: relative;
        }

        .wf-mini-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 18px;
            padding: 13px 14px;
            margin-bottom: 10px;
        }

        .wf-mini-row span, .wf-mini-row strong {
            color: white !important;
        }

        .wf-mini-row span {
            color: #CBD5E1 !important;
            font-size: 13px;
        }

        .wf-status-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 14px;
        }

        .wf-status-item {
            padding: 14px;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .wf-status-item b {
            color: white !important;
            font-size: 18px;
        }

        .wf-status-item small {
            color: #CBD5E1 !important;
            display: block;
            margin-top: 3px;
        }

        .wf-trust-card {
            border-radius: 30px;
            padding: 24px;
            background: rgba(255,255,255,0.82);
            border: 1px solid #E2E8F0;
            box-shadow: var(--shadow-sm);
        }

        .wf-trust-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }

        .wf-trust-item {
            border-radius: 20px;
            padding: 16px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            text-align: center;
        }

        .wf-trust-item b {
            display: block;
            font-size: 18px;
            margin-bottom: 2px;
        }

        .wf-trust-item small {
            color: #64748B !important;
            font-weight: 700;
        }

        /* Sections */
        .wf-section-title {
            margin: 46px 0 18px 0;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            gap: 16px;
        }

        .wf-section-title h2 {
            font-size: clamp(28px, 3vw, 42px);
            letter-spacing: -1.8px;
            margin: 0;
            font-weight: 900;
        }

        .wf-section-title p {
            color: #64748B !important;
            margin: 8px 0 0 0;
            max-width: 560px;
        }

        .wf-module-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
            margin-bottom: 26px;
        }

        .wf-module-card {
            background: rgba(255,255,255,0.86);
            border: 1px solid #E2E8F0;
            border-radius: var(--radius-xl);
            padding: 24px;
            box-shadow: var(--shadow-sm);
            min-height: 210px;
            transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
        }

        .wf-module-card:hover {
            transform: translateY(-4px);
            border-color: #CBD5E1;
            box-shadow: var(--shadow-md);
        }

        .wf-icon {
            width: 54px;
            height: 54px;
            border-radius: 18px;
            display: grid;
            place-items: center;
            font-size: 27px;
            margin-bottom: 18px;
            box-shadow: inset 0 -12px 24px rgba(15, 23, 42, 0.05);
        }

        .blue { background: var(--blue-soft); }
        .green { background: var(--green-soft); }
        .violet { background: var(--violet-soft); }
        .orange { background: var(--orange-soft); }

        /* Finom-inspired 3D Orb */
        .wf-orb {
            width: 74px;
            height: 74px;
            border-radius: 999px;
            position: relative;
            isolation: isolate;
            margin-bottom: 18px;
            background:
                radial-gradient(circle at 28% 24%, rgba(255,255,255,0.95) 0 8%, transparent 20%),
                radial-gradient(circle at 72% 28%, rgba(255,255,255,0.55) 0 7%, transparent 24%),
                radial-gradient(circle at 66% 76%, rgba(255,255,255,0.38) 0 9%, transparent 28%),
                linear-gradient(135deg, rgba(255, 130, 210, 0.98) 0%, rgba(169, 110, 255, 0.94) 42%, rgba(76, 201, 240, 0.86) 100%);
            box-shadow:
                inset 12px 12px 22px rgba(255,255,255,0.36),
                inset -16px -18px 28px rgba(88, 28, 135, 0.20),
                0 18px 36px rgba(168, 85, 247, 0.24),
                0 7px 16px rgba(15, 23, 42, 0.08);
            overflow: hidden;
            transform: translateZ(0);
        }

        .wf-orb::before {
            content: "";
            position: absolute;
            inset: 9px;
            border-radius: 50%;
            border: 1px solid rgba(255,255,255,0.58);
            background:
                linear-gradient(115deg, transparent 18%, rgba(255,255,255,0.55) 30%, transparent 42%),
                linear-gradient(28deg, transparent 30%, rgba(255,255,255,0.28) 46%, transparent 58%);
            transform: rotate(-25deg) scale(1.08);
            filter: blur(0.1px);
            opacity: 0.86;
            z-index: 1;
        }

        .wf-orb::after {
            content: "";
            position: absolute;
            width: 92px;
            height: 38px;
            left: -9px;
            top: 25px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.48);
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.30), transparent);
            transform: rotate(-31deg);
            opacity: 0.72;
            z-index: 2;
        }

        .wf-orb.small {
            width: 58px;
            height: 58px;
            margin-bottom: 0;
            flex: 0 0 auto;
        }

        .wf-orb.blue-orb {
            background:
                radial-gradient(circle at 28% 24%, rgba(255,255,255,0.95) 0 8%, transparent 20%),
                radial-gradient(circle at 70% 30%, rgba(255,255,255,0.55) 0 7%, transparent 24%),
                linear-gradient(135deg, #93C5FD 0%, #8B5CF6 46%, #22D3EE 100%);
            box-shadow: inset 12px 12px 22px rgba(255,255,255,0.38), inset -16px -18px 28px rgba(30, 64, 175, 0.20), 0 18px 36px rgba(59, 130, 246, 0.24), 0 7px 16px rgba(15, 23, 42, 0.08);
        }

        .wf-orb.green-orb {
            background:
                radial-gradient(circle at 28% 24%, rgba(255,255,255,0.95) 0 8%, transparent 20%),
                radial-gradient(circle at 72% 28%, rgba(255,255,255,0.50) 0 7%, transparent 24%),
                linear-gradient(135deg, #A7F3D0 0%, #34D399 42%, #2563EB 100%);
            box-shadow: inset 12px 12px 22px rgba(255,255,255,0.40), inset -16px -18px 28px rgba(6, 95, 70, 0.20), 0 18px 36px rgba(16, 185, 129, 0.24), 0 7px 16px rgba(15, 23, 42, 0.08);
        }

        .wf-orb.orange-orb {
            background:
                radial-gradient(circle at 28% 24%, rgba(255,255,255,0.95) 0 8%, transparent 20%),
                radial-gradient(circle at 72% 28%, rgba(255,255,255,0.50) 0 7%, transparent 24%),
                linear-gradient(135deg, #FDBA74 0%, #F472B6 45%, #7C3AED 100%);
            box-shadow: inset 12px 12px 22px rgba(255,255,255,0.40), inset -16px -18px 28px rgba(154, 52, 18, 0.18), 0 18px 36px rgba(244, 114, 182, 0.24), 0 7px 16px rgba(15, 23, 42, 0.08);
        }

        .wf-product-title-row {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 18px;
        }

        .wf-product-title-row h3 {
            margin: 0;
            font-size: 28px;
            letter-spacing: -1.1px;
            font-weight: 900;
        }

        .wf-product-title-row h3 span {
            color: #DB2777 !important;
        }

        .wf-product-title-row p {
            margin: 3px 0 0 0;
            color: #64748B !important;
            font-weight: 600;
        }

        .wf-module-card h3 {
            margin: 0 0 8px 0;
            font-size: 20px;
            letter-spacing: -0.6px;
        }

        .wf-module-card p {
            color: #64748B !important;
            margin: 0 0 16px 0;
            font-size: 14px;
        }

        .wf-card-tag {
            display: inline-flex;
            padding: 7px 10px;
            border-radius: 999px;
            background: #F1F5F9;
            color: #334155 !important;
            font-size: 12px;
            font-weight: 800;
        }

        /* Streamlit native elements */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background: rgba(255,255,255,0.60);
            padding: 8px;
            border-radius: 22px;
            border: 1px solid #E2E8F0;
            box-shadow: var(--shadow-sm);
        }

        .stTabs [data-baseweb="tab"] {
            height: 48px;
            border-radius: 16px;
            padding: 0 18px;
            font-weight: 850;
            color: #334155 !important;
        }

        .stTabs [aria-selected="true"] {
            background: #101828 !important;
            color: #FFFFFF !important;
        }

        .stFileUploader section {
            border-radius: 28px !important;
            border: 1.5px dashed #CBD5E1 !important;
            background: rgba(255,255,255,0.78) !important;
            padding: 34px !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
        }

        .stFileUploader label, .stTextInput label, .stSelectbox label, .stCheckbox label {
            font-weight: 800 !important;
            color: #101828 !important;
        }

        .stTextInput input, .stSelectbox [data-baseweb="select"] {
            border-radius: 16px !important;
            border-color: #E2E8F0 !important;
            min-height: 48px !important;
        }

        .stButton > button, .stDownloadButton > button {
            border-radius: 16px !important;
            min-height: 54px !important;
            border: none !important;
            color: white !important;
            background: #101828 !important;
            font-weight: 850 !important;
            box-shadow: 0 14px 30px rgba(16, 24, 40, 0.18) !important;
            transition: transform .2s ease, box-shadow .2s ease !important;
        }

        .stButton > button:hover, .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 18px 40px rgba(16, 24, 40, 0.24) !important;
        }

        .wf-tool-shell {
            background: rgba(255,255,255,0.82);
            border: 1px solid #E2E8F0;
            border-radius: 34px;
            padding: 28px;
            box-shadow: var(--shadow-md);
            margin-top: 18px;
        }

        .wf-tool-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 18px;
            margin-bottom: 22px;
        }

        .wf-tool-head h3 {
            margin: 0;
            font-size: 26px;
            letter-spacing: -1px;
            font-weight: 900;
        }

        .wf-tool-head p {
            margin: 4px 0 0 0;
            color: #64748B !important;
            font-size: 14px;
        }

        .wf-preview-box {
            border-radius: 24px;
            padding: 18px;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            min-height: 180px;
        }

        .wf-preview-box h4 {
            margin-top: 0;
            font-size: 15px;
        }

        .wf-chip-row {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 10px;
        }

        .wf-chip {
            padding: 7px 10px;
            border-radius: 999px;
            background: white;
            border: 1px solid #E2E8F0;
            color: #475569 !important;
            font-size: 12px;
            font-weight: 800;
        }

        .wf-footer {
            margin-top: 56px;
            border-radius: 28px;
            padding: 26px;
            background: #101828;
            display: flex;
            justify-content: space-between;
            gap: 16px;
            align-items: center;
        }

        .wf-footer strong, .wf-footer span {
            color: white !important;
        }

        .wf-footer span {
            color: #CBD5E1 !important;
            font-size: 13px;
        }

        /* EASY UPDATE: mehr Sichtbarkeit + Bewegung + Liquid Glass */
        @keyframes wf-orb-float {
            0%, 100% { transform: translateY(0) rotate(0deg) scale(1); }
            50% { transform: translateY(-7px) rotate(3deg) scale(1.04); }
        }

        .wf-orb {
            animation: wf-orb-float 5.5s ease-in-out infinite;
            transition: transform .3s ease, filter .3s ease;
        }

        .wf-orb:hover {
            animation-play-state: paused;
            transform: translateY(-9px) rotate(5deg) scale(1.09);
            filter: saturate(1.18) contrast(1.05);
        }

        .wf-tool-shell,
        .wf-module-card,
        .wf-preview-box,
        .wf-trust-card {
            background: linear-gradient(145deg, rgba(255,255,255,0.92), rgba(255,255,255,0.62)) !important;
            border: 1px solid rgba(255,255,255,0.76) !important;
            backdrop-filter: blur(22px) saturate(1.25);
            -webkit-backdrop-filter: blur(22px) saturate(1.25);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.85),
                0 22px 60px rgba(15,23,42,0.10) !important;
            transition: transform .28s ease, box-shadow .28s ease;
        }

        .wf-tool-shell:hover,
        .wf-module-card:hover,
        .wf-preview-box:hover,
        .wf-trust-card:hover {
            transform: translateY(-4px) scale(1.006);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.92),
                0 30px 80px rgba(15,23,42,0.14) !important;
        }

        .stTextInput input,
        .stSelectbox [data-baseweb="select"],
        .stSelectbox [data-baseweb="select"] > div {
            min-height: 56px !important;
            border-radius: 18px !important;
            border: 1px solid rgba(100,116,139,0.42) !important;
            background: rgba(255,255,255,0.96) !important;
            color: #0B1020 !important;
            font-weight: 800 !important;
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.95),
                0 14px 34px rgba(15,23,42,0.09) !important;
        }

        .stTextInput input:focus,
        .stSelectbox [data-baseweb="select"]:focus-within {
            border-color: rgba(29,78,216,0.65) !important;
            box-shadow:
                0 0 0 5px rgba(29,78,216,0.10),
                0 18px 44px rgba(15,23,42,0.12) !important;
        }

        .stTextInput input::placeholder {
            color: #94A3B8 !important;
            font-weight: 700 !important;
        }

        .stFileUploader section {
            border: 1.5px dashed rgba(100,116,139,0.42) !important;
            background: linear-gradient(145deg, rgba(255,255,255,0.94), rgba(255,255,255,0.68)) !important;
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.9),
                0 18px 48px rgba(15,23,42,0.09) !important;
        }

        .stFileUploader svg,
        .stSelectbox svg,
        .stTextInput svg {
            color: #0F172A !important;
            fill: #0F172A !important;
            opacity: 1 !important;
            filter: drop-shadow(0 3px 6px rgba(15,23,42,0.18));
        }

        .stFileUploader section svg {
            transform: scale(1.16);
            padding: 10px;
            border-radius: 18px;
            background: rgba(255,255,255,0.82);
            box-shadow: 0 12px 28px rgba(15,23,42,0.12);
        }

        .stFileUploader button {
            border-radius: 14px !important;
            border: 1px solid rgba(100,116,139,0.35) !important;
            background: rgba(255,255,255,0.96) !important;
            color: #0B1020 !important;
            font-weight: 850 !important;
        }

        @media (max-width: 980px) {
            .wf-hero {
                grid-template-columns: 1fr;
            }
            .wf-module-grid {
                grid-template-columns: 1fr;
            }
            .wf-nav-links {
                display: none;
            }
            .wf-hero-left {
                padding: 34px;
            }
            .wf-hero-title {
                letter-spacing: -2.4px;
            }
            .wf-section-title {
                align-items: flex-start;
                flex-direction: column;
            }
            .wf-trust-grid, .wf-status-grid {
                grid-template-columns: 1fr;
            }
        }
        /* FIX: cleaner Streamlit tabs, no red underline, readable active tab */
        .stTabs [data-baseweb="tab-highlight"] {
            display: none !important;
            background: transparent !important;
        }

        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }

        .stTabs [data-baseweb="tab"] {
            color: #0B1020 !important;
            border-radius: 18px !important;
            border: 1px solid transparent !important;
            transition: all .24s ease !important;
        }

        .stTabs [data-baseweb="tab"] p,
        .stTabs [data-baseweb="tab"] span {
            color: #0B1020 !important;
            font-weight: 800 !important;
        }

        .stTabs [aria-selected="true"] {
            background: #101828 !important;
            border-color: #101828 !important;
            box-shadow: 0 14px 30px rgba(16,24,40,0.18) !important;
        }

        .stTabs [aria-selected="true"] p,
        .stTabs [aria-selected="true"] span {
            color: #FFFFFF !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            border-radius: 28px !important;
            padding: 10px !important;
            overflow: hidden !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def nav():
    st.markdown(
        """
        <div class="wf-nav">
            <div class="wf-brand">
                <div class="wf-logo">W</div>
                <div>Wertfile.</div>
            </div>
            <div class="wf-nav-links">
                <span>Converter</span>
                <span>Video Tools</span>
                <span>Security</span>
                <span>Business Pro</span>
            </div>
            <div class="wf-pill"><span class="wf-dot"></span> Local first</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero():
    st.markdown(
        """
        <section class="wf-hero">
            <div class="wf-hero-left">
                <div class="wf-kicker">🛡️ Smart File Workspace für Business-Use-Cases</div>
                <h1 class="wf-hero-title">Dateien verarbeiten.<br><span class="wf-gradient-text">Schneller. Sicherer. Schöner.</span></h1>
                <p class="wf-hero-copy">
                    Wertfile bündelt smarte Datei-Tools in einem modernen Workspace: Dokumente konvertieren,
                    Workflows vorbereiten und sensible Files mit einem klaren Business-Prozess bearbeiten.
                </p>
                <div class="wf-hero-actions">
                    <span class="wf-btn-main">Jetzt Datei verarbeiten</span>
                    <span class="wf-btn-secondary">Module ansehen</span>
                </div>
            </div>
            <div class="wf-hero-right">
                <div class="wf-app-card">
                    <div class="wf-app-top">
                        <div class="wf-app-title">Workspace Status</div>
                        <div class="wf-app-badge">Secure Session</div>
                    </div>
                    <div class="wf-phone">
                        <div class="wf-mini-row"><span>Aktives Modul</span><strong>JPEG → PDF</strong></div>
                        <div class="wf-mini-row"><span>Verarbeitung</span><strong>Lokal im Speicher</strong></div>
                        <div class="wf-mini-row"><span>Export</span><strong>PDF Ready</strong></div>
                        <div class="wf-status-grid">
                            <div class="wf-status-item"><b>3</b><small>Module</small></div>
                            <div class="wf-status-item"><b>0</b><small>Server Uploads</small></div>
                            <div class="wf-status-item"><b>PDF</b><small>Export</small></div>
                        </div>
                    </div>
                </div>
                <div class="wf-trust-card">
                    <div class="wf-trust-grid">
                        <div class="wf-trust-item"><b>Private</b><small>Session-basiert</small></div>
                        <div class="wf-trust-item"><b>Fast</b><small>Direkt im App-Flow</small></div>
                        <div class="wf-trust-item"><b>Clean</b><small>Business UI</small></div>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def module_cards():
    st.markdown(
        """
        <div class="wf-section-title">
            <div>
                <h2>Ein Workspace. Mehrere Tools.</h2>
                <p>Die Module sind so aufgebaut, dass Wertfile später zu einer echten File-Operations-Plattform erweitert werden kann.</p>
            </div>
        </div>
        <div class="wf-module-grid">
            <div class="wf-module-card">
                <div class="wf-orb blue-orb"></div>
                <h3>Document Converter</h3>
                <p>JPG und PNG hochladen, Reihenfolge prüfen und als sauberes PDF exportieren.</p>
                <span class="wf-card-tag">Live verfügbar</span>
            </div>
            <div class="wf-module-card">
                <div class="wf-orb orange-orb"></div>
                <h3>Video Tools</h3>
                <p>Geplant für Video-Komprimierung, Audio-Export und Format-Workflows.</p>
                <span class="wf-card-tag">Coming soon</span>
            </div>
            <div class="wf-module-card">
                <div class="wf-orb green-orb"></div>
                <h3>Secure Processing</h3>
                <p>Klare Session-Logik, lokale Verarbeitung und später optionaler Audit-Log.</p>
                <span class="wf-card-tag">Foundation ready</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def make_pdf(uploaded_files, page_fit="Original", sort_by_name=True):
    files = list(uploaded_files)
    if sort_by_name:
        files = sorted(files, key=lambda f: f.name.lower())

    images = []
    for file in files:
        img = Image.open(file)
        img = ImageOps.exif_transpose(img).convert("RGB")

        if page_fit == "A4 Portrait":
            # A4 at 150 DPI approx. 1240x1754 px
            canvas = Image.new("RGB", (1240, 1754), "white")
            img.thumbnail((1120, 1634), Image.Resampling.LANCZOS)
            x = (1240 - img.width) // 2
            y = (1754 - img.height) // 2
            canvas.paste(img, (x, y))
            img = canvas
        elif page_fit == "A4 Landscape":
            canvas = Image.new("RGB", (1754, 1240), "white")
            img.thumbnail((1634, 1120), Image.Resampling.LANCZOS)
            x = (1754 - img.width) // 2
            y = (1240 - img.height) // 2
            canvas.paste(img, (x, y))
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


def document_converter():
    st.markdown('<div class="wf-tool-shell">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="wf-tool-head">
            <div class="wf-product-title-row">
                <div class="wf-orb small blue-orb"></div>
                <div>
                    <h3><span>PDF</span> Workspace</h3>
                    <p>Upload, Reihenfolge, Seitenformat und Export in einem Premium-Flow.</p>
                </div>
            </div>
            <div class="wf-card-tag">Production Module</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        uploaded_files = st.file_uploader(
            "Bilder hier ablegen",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            help="Mehrere Bilder auswählen. Optional nach Dateiname sortieren lassen.",
        )

        c1, c2 = st.columns(2)
        with c1:
            page_fit = st.selectbox(
                "PDF-Seitenformat",
                ["Original", "A4 Portrait", "A4 Landscape"],
                index=1,
            )
        with c2:
            sort_by_name = st.checkbox("Nach Dateiname sortieren", value=True)

        if uploaded_files:
            total_size_mb = sum(file.size for file in uploaded_files) / (1024 * 1024)
            st.markdown(
                f"""
                <div class="wf-chip-row">
                    <span class="wf-chip">{len(uploaded_files)} Datei(en)</span>
                    <span class="wf-chip">{total_size_mb:.2f} MB</span>
                    <span class="wf-chip">{page_fit}</span>
                    <span class="wf-chip">Export: PDF</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("PDF generieren", use_container_width=True):
                try:
                    pdf_buffer = make_pdf(uploaded_files, page_fit, sort_by_name)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                    st.success("Dein PDF ist bereit.")
                    st.download_button(
                        "📥 PDF herunterladen",
                        data=pdf_buffer.getvalue(),
                        file_name=f"wertfile_export_{timestamp}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"PDF konnte nicht erstellt werden: {e}")
        else:
            st.info("Lade mindestens ein Bild hoch, um den Export zu starten.")

    with right:
        st.markdown('<div class="wf-preview-box">', unsafe_allow_html=True)
        st.markdown("<h4>Live Preview</h4>", unsafe_allow_html=True)

        if uploaded_files:
            preview_files = list(uploaded_files)
            if sort_by_name:
                preview_files = sorted(preview_files, key=lambda f: f.name.lower())

            preview = preview_files[0]
            img = Image.open(preview)
            img = ImageOps.exif_transpose(img)
            st.image(img, caption=f"Erste Seite: {preview.name}", use_container_width=True)

            if len(preview_files) > 1:
                with st.expander("Alle Dateien anzeigen"):
                    for idx, file in enumerate(preview_files, start=1):
                        st.write(f"{idx}. {file.name}")
        else:
            st.markdown(
                """
                <p style="color:#64748B !important;">Sobald du Bilder hochlädst, erscheint hier eine Vorschau der ersten PDF-Seite.</p>
                <div class="wf-chip-row">
                    <span class="wf-chip">Drag & Drop</span>
                    <span class="wf-chip">A4 Export</span>
                    <span class="wf-chip">Multi Page</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def video_tools():
    st.markdown('<div class="wf-tool-shell">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="wf-tool-head">
            <div class="wf-product-title-row">
                <div class="wf-orb small orange-orb"></div>
                <div>
                    <h3><span>Video</span> Tools</h3>
                    <p>UI vorbereitet. Die echte Conversion sollte später über eine saubere Backend-Pipeline laufen.</p>
                </div>
            </div>
            <div class="wf-card-tag">Coming soon</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1], gap="large")
    with left:
        video_url = st.text_input(
            "Video URL",
            placeholder="https://www.example.com/video",
            help="Später kann hier eine erlaubte Quelle oder ein eigener Upload verarbeitet werden.",
        )
        target_format = st.selectbox("Zielformat", ["MP3 Audio", "MP4 Video", "Compressed MP4", "WebM"])
        quality = st.selectbox("Qualität", ["High", "Balanced", "Small File"])

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎵 Audio vorbereiten", use_container_width=True):
                st.warning("Backend noch nicht verbunden. UI-Flow ist vorbereitet.")
        with c2:
            if st.button("🎞️ Video vorbereiten", use_container_width=True):
                st.warning("Backend noch nicht verbunden. UI-Flow ist vorbereitet.")

    with right:
        st.markdown(
            """
            <div class="wf-preview-box">
                <h4>Geplante Pipeline</h4>
                <p style="color:#64748B !important;">Für ein echtes Produkt würde ich dieses Modul als eigenen Worker bauen:</p>
                <div class="wf-chip-row">
                    <span class="wf-chip">Upload prüfen</span>
                    <span class="wf-chip">Job Queue</span>
                    <span class="wf-chip">ffmpeg</span>
                    <span class="wf-chip">Download Token</span>
                    <span class="wf-chip">Auto Delete</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)


def security_panel():
    st.markdown('<div class="wf-tool-shell">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="wf-tool-head">
            <div class="wf-product-title-row">
                <div class="wf-orb small green-orb"></div>
                <div>
                    <h3><span>Security</span> Layer</h3>
                    <p>Positionierung für Vertrauen: wichtig, wenn Wertfile später echte Kundendaten verarbeitet.</p>
                </div>
            </div>
            <div class="wf-card-tag">Business Trust</div>
        </div>
        <div class="wf-module-grid">
            <div class="wf-module-card">
                <div class="wf-orb green-orb"></div>
                <h3>Session-basiert</h3>
                <p>Dateien werden aktuell nur während der Session verarbeitet und nicht dauerhaft gespeichert.</p>
                <span class="wf-card-tag">Good start</span>
            </div>
            <div class="wf-module-card">
                <div class="wf-orb blue-orb"></div>
                <h3>Audit-ready</h3>
                <p>Später: Verarbeitungsprotokolle, Löschfristen, Nutzerrollen und Export-Historie.</p>
                <span class="wf-card-tag">Next step</span>
            </div>
            <div class="wf-module-card">
                <div class="wf-orb orange-orb"></div>
                <h3>Auto Delete</h3>
                <p>Für eine echte SaaS-Version: automatische Löschung nach Download oder Zeitfenster.</p>
                <span class="wf-card-tag">Roadmap</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


def footer():
    st.markdown(
        """
        <div class="wf-footer">
            <div>
                <strong>Wertfile.</strong><br>
                <span>Smart File Workspace — Technology Germany</span>
            </div>
            <span>Local first · Secure by design · Business Pro</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Render ----------
inject_css()
nav()
hero()
module_cards()

tab_pdf, tab_video, tab_security = st.tabs([
    "Document Converter",
    "Video Tools",
    "Security",
])

with tab_pdf:
    document_converter()

with tab_video:
    video_tools()

with tab_security:
    security_panel()

footer()
