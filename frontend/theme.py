import re
import time
import threading
import streamlit as st

# ======================================================
# Loading Messages (generative-style loader text)
# ======================================================

LOADING_MESSAGES = [
    "Reading your notes...",
    "Understanding the context...",
    "Identifying key concepts...",
    "Structuring the summary...",
    "Tailoring tone for the audience...",
    "Applying your custom instructions...",
    "Trimming the fluff...",
    "Polishing the language...",
    "Double-checking accuracy...",
    "Finalizing response...",
]

# ======================================================
# CSS
# ======================================================

def inject_theme_css():
    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at 20% 0%, #1a1c2e 0%, #0d0e17 45%, #0a0b12 100%);
            color: #e8e8f0;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }

        /* ---------- Hero ---------- */

        .hero-wrap { text-align: center; padding: 1.5rem 0 0.5rem 0; }

        .hero-badge {
            display: inline-flex; align-items: center; gap: 0.4rem;
            background: rgba(167, 139, 250, 0.1);
            border: 1px solid rgba(167, 139, 250, 0.3);
            color: #c4b5fd; font-size: 0.78rem; font-weight: 600;
            letter-spacing: 0.03em; text-transform: uppercase;
            padding: 0.35rem 0.9rem; border-radius: 999px; margin-bottom: 1.2rem;
        }

        .hero-title {
            font-size: 4rem; font-weight: 800; letter-spacing: -0.04em; line-height: 1.05;
            background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
            filter: drop-shadow(0 0 30px rgba(124, 58, 237, 0.35));
            margin-bottom: 0.9rem;
        }

        .hero-sub { font-size: 1.3rem; color: #e2e4ee; font-weight: 600; margin-bottom: 0.5rem; letter-spacing: -0.01em; }
        .hero-desc { font-size: 1.02rem; color: #8b8ea3; font-weight: 400; max-width: 560px; margin: 0 auto; }

        /* ---------- Section labels ---------- */

        .section-label {
            font-size: 0.95rem; font-weight: 700; letter-spacing: 0.03em;
            text-transform: uppercase; color: #a78bfa; margin-bottom: 0.6rem;
        }
        .section-label-sm {
            font-size: 0.78rem; font-weight: 700; letter-spacing: 0.04em;
            text-transform: uppercase; color: #6b6e85; margin: 1.2rem 0 0.6rem 0;
        }

        /* ---------- Glass cards ---------- */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255, 255, 255, 0.035);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        }

        /* ---------- Inputs ---------- */

        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px; color: #e8e8f0; font-size: 0.95rem; padding: 1rem;
        }
        .stTextArea textarea:focus {
            border: 1px solid #a78bfa; box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15);
        }

        .stTextInput input {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px; color: #e8e8f0; padding: 0.6rem 0.9rem;
        }
        .stTextInput input:focus {
            border: 1px solid #a78bfa; box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15);
        }
        .stTextInput label, .stRadio label, .stSelectbox label {
            color: #cbd5e1 !important; font-weight: 600;
        }

        div[data-baseweb="select"] > div {
            background: rgba(255, 255, 255, 0.04); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);
        }

        div[role="radiogroup"] { gap: 0.4rem; }

        /* ---------- File uploader (PDF) ---------- */

        [data-testid="stFileUploaderDropzone"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px dashed rgba(167, 139, 250, 0.35) !important;
            border-radius: 14px !important;
        }
        [data-testid="stFileUploaderDropzone"] button {
            background: rgba(167, 139, 250, 0.14) !important;
            color: #c4b5fd !important;
            border: 1px solid rgba(167, 139, 250, 0.35) !important;
            border-radius: 8px !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"] span,
        [data-testid="stFileUploaderDropzoneInstructions"] small { color: #8b8ea3 !important; }

        /* ---------- Buttons ---------- */

        .stButton button {
            background: linear-gradient(90deg, #7c3aed, #2563eb);
            color: white; font-weight: 700; border: none; border-radius: 12px;
            padding: 0.7rem 1rem; box-shadow: 0 0 20px rgba(124, 58, 237, 0.45);
            transition: all 0.2s ease-in-out;
        }
        .stButton button:hover {
            box-shadow: 0 0 30px rgba(124, 58, 237, 0.75); transform: translateY(-1px);
        }

        hr { border-color: rgba(255, 255, 255, 0.08) !important; }

        /* ---------- Stats card ---------- */

        .stat-row {
            display: flex; justify-content: space-between; align-items: center;
            padding: 0.6rem 0.9rem; background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; margin-bottom: 0.5rem;
        }
        .stat-label { color: #8b8ea3; font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em; }
        .stat-value {
            color: #e8e8f0; font-size: 0.88rem; font-weight: 700; text-align: right;
            max-width: 60%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
        }
        .stat-value.live { color: #34d399; }

        /* ---------- Loader ---------- */

        .loader-box { text-align: center; color: #c4b5fd; font-size: 1.05rem; font-weight: 600; padding: 2.2rem 0; min-height: 60px; }
        .loader-cursor { animation: blink 0.9s steps(1) infinite; }
        @keyframes blink { 50% { opacity: 0; } }

        /* ---------- Notices ---------- */

        .summary-empty { color: #7d8093; font-size: 0.95rem; text-align: center; padding: 1.5rem 0; }

        .error-box {
            color: #fca5a5; background: rgba(248, 113, 113, 0.08);
            border: 1px solid rgba(248, 113, 113, 0.3); border-radius: 12px;
            padding: 1rem 1.2rem; font-size: 0.9rem;
        }
        .warn-box {
            color: #fcd34d; background: rgba(251, 191, 36, 0.08);
            border: 1px solid rgba(251, 191, 36, 0.3); border-radius: 12px;
            padding: 0.85rem 1.1rem; font-size: 0.87rem; margin-bottom: 0.9rem;
        }
        .success-box {
            color: #6ee7b7; background: rgba(52, 211, 153, 0.08);
            border: 1px solid rgba(52, 211, 153, 0.3); border-radius: 12px;
            padding: 1rem 1.2rem; font-size: 0.9rem;
        }

        /* markdown output inside bordered containers */
        div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown ul { padding-left: 1.3rem; }
        div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown li { margin-bottom: 0.4rem; color: #dcdce8; }
        div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p { color: #dcdce8; line-height: 1.7; }
        div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown strong { color: #ffffff; }

        /* ---------- Auth pages ---------- */

        .auth-switch { text-align: center; color: #8b8ea3; font-size: 0.85rem; margin: 0.5rem 0 0.3rem 0; }

        /* ---------- Top bar (dashboard) ---------- */

        .topbar-user { display: flex; align-items: center; gap: 0.7rem; padding: 0.4rem 0; }
        .avatar-chip {
            width: 38px; height: 38px; border-radius: 50%;
            background: linear-gradient(135deg, #7c3aed, #2563eb);
            display: flex; align-items: center; justify-content: center;
            color: #fff; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.02em;
            box-shadow: 0 0 14px rgba(124, 58, 237, 0.35);
            flex-shrink: 0;
        }
        .topbar-email { color: #cbd5e1; font-size: 0.88rem; font-weight: 600; }

        </style>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# Hero
# ======================================================

def render_hero(badge: str, title: str, sub: str, desc: str):
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">{badge}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-sub">{sub}</div>
            <div class="hero-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# User avatar — initials from the email (no name column in DB yet)
# ======================================================

def get_initials(email: str) -> str:
    if not email:
        return "?"
    local_part = email.split("@")[0]
    tokens = [t for t in re.split(r"[._\-]+", local_part) if t]
    if len(tokens) >= 2:
        return (tokens[0][0] + tokens[1][0]).upper()
    if tokens:
        return tokens[0][:2].upper()
    return local_part[:2].upper()


def render_user_topbar(email: str) -> bool:
    """Renders the avatar + email on the left and a Logout button on the
    right. Returns True if Logout was clicked (caller handles the actual
    session clear + redirect, since that's page-flow logic, not styling)."""
    initials = get_initials(email)
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(
            f"""
            <div class="topbar-user">
                <div class="avatar-chip">{initials}</div>
                <span class="topbar-email">{email}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        return st.button("Logout", use_container_width=True)

# ======================================================
# Stats card (Model / Version / Response Time)
# ======================================================

def render_stats(result: dict):
    model_class = "live" if result.get("model") not in (None, "—") else ""
    st.markdown(
        f"""
        <div class="stat-row">
            <span class="stat-label">Model</span>
            <span class="stat-value {model_class}">{result.get("model", "—")}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Version</span>
            <span class="stat-value">{result.get("version", "v1.0.0")}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Response Time</span>
            <span class="stat-value">{result.get("response_time", "—")}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# Generative typewriter loader
# ======================================================

def run_generative_loader(placeholder, thread: threading.Thread):
    """
    Types each loading message out character by character, cycling
    through LOADING_MESSAGES until the background thread (the real
    network call) finishes. Python/threading equivalent of an
    async + setTimeout JS loader.
    """
    msg_index = 0
    while thread.is_alive():
        message = LOADING_MESSAGES[msg_index % len(LOADING_MESSAGES)]
        typed = ""
        for ch in message:
            if not thread.is_alive():
                break
            typed += ch
            placeholder.markdown(
                f'<div class="loader-box">{typed}<span class="loader-cursor">▍</span></div>',
                unsafe_allow_html=True
            )
            time.sleep(0.02)
        time.sleep(0.5)
        msg_index += 1

    placeholder.empty()


def clean_summary_text(text: str) -> str:
    """Normalizes model output so it renders as proper Markdown."""
    if not text:
        return ""
    text = text.replace("\\n", "\n")
    return text.strip()

# ======================================================
# Message Boxes (Error, Warning, Success)
# ======================================================

def render_message_box(msg_type: str, text: str):
    """Renders a styled message box based on the type provided."""
    if msg_type == "error":
        st.markdown(f'<div class="error-box">⚠️ {text}</div>', unsafe_allow_html=True)
    elif msg_type == "warning":
        st.markdown(f'<div class="warn-box">⚠️ {text}</div>', unsafe_allow_html=True)
    elif msg_type == "success":
        st.markdown(f'<div class="success-box">✅ {text}</div>', unsafe_allow_html=True)