import streamlit as st
import requests
import threading
import time

# ======================================================
# Configuration
# ======================================================

APP_NAME = "Dhvani"
APP_ICON = "🧠"

# FastAPI backend URL
# Default: uvicorn backend:app --reload  
BACKEND_URL = "http://127.0.0.1:8000/summarize"
REQUEST_TIMEOUT = 60  # seconds

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# Session State
# ======================================================

if "last_result" not in st.session_state:
    st.session_state.last_result = {
        "summary": None,
        "model": "—",
        "version": "v1.0.0",
        "response_time": "—",
        "error": None,
    }

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
# Custom Styling (CSS)
# ======================================================

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

    .hero-wrap {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(167, 139, 250, 0.1);
        border: 1px solid rgba(167, 139, 250, 0.3);
        color: #c4b5fd;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.05;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 0 30px rgba(124, 58, 237, 0.35));
        margin-bottom: 0.9rem;
    }

    .hero-sub {
        font-size: 1.3rem;
        color: #e2e4ee;
        font-weight: 600;
        margin-bottom: 0.5rem;
        letter-spacing: -0.01em;
    }

    .hero-desc {
        font-size: 1.02rem;
        color: #8b8ea3;
        font-weight: 400;
        max-width: 560px;
        margin: 0 auto;
    }

    /* ---------- Section labels ---------- */

    .section-label {
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: #a78bfa;
        margin-bottom: 0.6rem;
    }

    .section-label-sm {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #6b6e85;
        margin: 1.1rem 0 0.6rem 0;
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
        border-radius: 14px;
        color: #e8e8f0;
        font-size: 0.95rem;
        padding: 1rem;
    }
    .stTextArea textarea:focus {
        border: 1px solid #a78bfa;
        box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15);
    }

    .stRadio label, .stSelectbox label {
        color: #cbd5e1 !important;
        font-weight: 600;
    }

    div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* horizontal radio -> segmented-control look */
    div[role="radiogroup"] {
        gap: 0.4rem;
    }

    /* ---------- Button ---------- */

    .stButton button {
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1rem;
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.45);
        transition: all 0.2s ease-in-out;
    }
    .stButton button:hover {
        box-shadow: 0 0 30px rgba(124, 58, 237, 0.75);
        transform: translateY(-1px);
    }

    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }

    /* ---------- Stats card (Model / Version / Time) ---------- */

    .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.6rem 0.9rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }

    .stat-label {
        color: #8b8ea3;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .stat-value {
        color: #e8e8f0;
        font-size: 0.88rem;
        font-weight: 700;
        text-align: right;
        max-width: 60%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .stat-value.live {
        color: #34d399;
    }

    /* ---------- Loader ---------- */

    .loader-box {
        text-align: center;
        color: #c4b5fd;
        font-size: 1.05rem;
        font-weight: 600;
        padding: 2.2rem 0;
        min-height: 60px;
    }

    .loader-cursor {
        animation: blink 0.9s steps(1) infinite;
    }

    @keyframes blink {
        50% { opacity: 0; }
    }

    /* ---------- Summary output ---------- */

    .summary-empty {
        color: #7d8093;
        font-size: 0.95rem;
        text-align: center;
        padding: 1.5rem 0;
    }

    .error-box {
        color: #fca5a5;
        background: rgba(248, 113, 113, 0.08);
        border: 1px solid rgba(248, 113, 113, 0.3);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        font-size: 0.9rem;
    }

    /* markdown output styling inside summary card */
    div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown ul {
        padding-left: 1.3rem;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown li {
        margin-bottom: 0.4rem;
        color: #dcdce8;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p {
        color: #dcdce8;
        line-height: 1.7;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown strong {
        color: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# Helper — call the FastAPI backend
# ======================================================

def call_backend(payload: dict, result_box: dict):
    """
        Runs in a background thread so the main thread is free
        to animate the loader while we wait on the network call.
        Writes into result_box (mutable dict) instead of returning,
        since threads can't return values directly.
    """
    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        result_box["success"] = True
        result_box["summary"] = data.get("summary", "")
        result_box["model"] = data.get("model", "—")
        result_box["response_time"] = f'{data.get("response_time_seconds", "—")} sec'

    except requests.exceptions.ConnectionError:
        result_box["success"] = False
        result_box["error"] = (
            f"Error: 500 (Couldn't reach the backend)"
            "Is your FastAPI server running (uvicorn backend:app --reload)?"
        )
    except requests.exceptions.Timeout:
        result_box["success"] = False
        result_box["error"] = "The backend took too long to respond. Try again."
    except requests.exceptions.HTTPError as e:
        result_box["success"] = False
        result_box["error"] = f"Backend returned an error: {e}"
    except Exception as e:
        result_box["success"] = False
        result_box["error"] = f"Unexpected error: {e}"

    result_box["done"] = True


def clean_summary_text(text: str) -> str:
    """
    Normalizes model output so it renders properly as Markdown
    instead of showing raw '\\n' / stray whitespace.
    """
    if not text:
        return ""
    text = text.replace("\\n", "\n")   # literal backslash-n -> real newline
    text = text.strip()
    return text


def run_generative_loader(placeholder, thread: threading.Thread):
    """
    Typewriter-style rotating loader. Types each message out
    character by character (like a generative response streaming
    in), cycling through LOADING_MESSAGES until the background
    thread finishes. This is the Python/threading equivalent of
    the async + setTimeout loader pattern from JS.
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
# Hero Section
# ======================================================

st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-badge">🧠 AI-Powered Note Intelligence</div>
        <div class="hero-title">Dhvani</div>
        <div class="hero-sub">Your thoughts already know where to go.</div>
        <div class="hero-desc">Transform lengthy notes into concise, structured knowledge.</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")
st.divider()

# ======================================================
# Main Layout — Notes (+ Settings) | Custom Instructions (+ Stats)
# ======================================================

left, right = st.columns([3.7, 1.3], gap="large")

with left:

    st.markdown('<div class="section-label">Notes</div>', unsafe_allow_html=True)

    notes = st.text_area(
        "",
        height=380,
        placeholder="""Paste your notes here...

Examples

• Class Notes
• Documentation
• Research Papers
• Meeting Notes
• Articles
• Technical Blogs""",
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label-sm">Settings</div>', unsafe_allow_html=True)

    set_col1, set_col2, set_col3 = st.columns(3)

    with set_col1:
        summary_type = st.radio(
            "Summary Length",
            ["Short", "Medium", "Detailed"],
            horizontal=True
        )

    with set_col2:
        audience = st.selectbox(
            "Target Audience",
            ["Student", "Interview", "Research"]
        )

    with set_col3:
        generate = st.button(
            "Generate Summary",
            use_container_width=True,
            type="primary"
        )
    
with right:

    st.markdown('<div class="section-label">Custom Instructions</div>', unsafe_allow_html=True)

    additional_instructions = st.text_area(
        "",
        height=160,
        placeholder="""Examples

• Use Analogies
• Keep examples
• Focus on interview questions
• Don't use bullet points""",
        label_visibility="collapsed"
    )

    st.write("")

    st.markdown('<div class="section-label-sm">Status</div>', unsafe_allow_html=True)

    stats_placeholder = st.empty()
    with stats_placeholder.container():
        render_stats(st.session_state.last_result)

# ======================================================
# Generate flow — validate, animate loader, call backend
# ======================================================

if generate:

    if not notes.strip():
        st.session_state.last_result = {
            "summary": None,
            "model": st.session_state.last_result.get("model", "—"),
            "version": "v1.0.0",
            "response_time": st.session_state.last_result.get("response_time", "—"),
            "error": "Please paste some notes before generating a summary.",
        }

    else:
        payload = {
            "text": notes,
            "summary_type": summary_type.lower(),
            "audience": audience.lower(),
            "additional_instructions": additional_instructions.strip(),
        }

        result_box = {"done": False}
        thread = threading.Thread(target=call_backend, args=(payload, result_box))
        thread.start()

        loader_placeholder = st.empty()
        run_generative_loader(loader_placeholder, thread)
        thread.join()

        if result_box.get("success"):
            st.session_state.last_result = {
                "summary": clean_summary_text(result_box.get("summary", "")),
                "model": result_box.get("model", "—"),
                "version": "v1.0.0",
                "response_time": result_box.get("response_time", "—"),
                "error": None,
            }
        else:
            st.session_state.last_result = {
                "summary": None,
                "model": st.session_state.last_result.get("model", "—"),
                "version": "v1.0.0",
                "response_time": st.session_state.last_result.get("response_time", "—"),
                "error": result_box.get("error", "Something went wrong."),
            }

        # refresh the stats card in the right column with the new run's data
        with stats_placeholder.container():
            render_stats(st.session_state.last_result)

# ======================================================
# Summary Section
# ======================================================

st.write("")
st.divider()

st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)

summary_container = st.container(border=True)

with summary_container:

    result = st.session_state.last_result

    if result.get("error"):
        st.markdown(
            f'<div class="error-box">{result["error"]}</div>',
            unsafe_allow_html=True
        )

    elif result.get("summary"):
        st.markdown(result["summary"])

    else:
        st.markdown(
            """
            <div class="summary-empty">
            No summary generated yet.<br>
            Paste your notes and click <b>Generate Summary</b>.
            </div>
            """,
            unsafe_allow_html=True
        )