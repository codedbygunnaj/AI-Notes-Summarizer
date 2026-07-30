import streamlit as st

st.set_page_config(
    page_title="Dhvani",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* page background */
    .stApp {
        background: radial-gradient(circle at 20% 0%, #1a1c2e 0%, #0d0e17 45%, #0a0b12 100%);
        color: #e8e8f0;
    }

    /* center + cap content width like a real product page */
    .block-container {
        max-width: 1100px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    /* hero wrapper — centered, with breathing room */
    .hero-wrap {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }

    /* small pill badge above the title */
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

    /* hero title with gradient text + soft glow */
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

    /* section labels */
    .section-label {
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: #a78bfa;
        margin-bottom: 0.6rem;
    }

    /* glassmorphism card wrapper — applied to containers with border=True */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.035);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    }

    /* text area styling */
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

    /* radio + selectbox labels */
    .stRadio label, .stSelectbox label {
        color: #cbd5e1 !important;
        font-weight: 600;
    }

    /* selectbox box */
    div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* glowing gradient button */
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

    /* divider */
    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }

    /* chatgpt-style response text inside summary card */
    .summary-empty {
        color: #7d8093;
        font-size: 0.95rem;
        text-align: center;
        padding: 1.5rem 0;
    }

    .summary-text {
        color: #e8e8f0;
        font-size: 1rem;
        line-height: 1.7;
    }

    </style>
    """,
    unsafe_allow_html=True
)

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

left, right = st.columns([3.7, 1.3], gap="large")

with left:

    st.markdown('<div class="section-label">Notes</div>', unsafe_allow_html=True)

    notes = st.text_area(
        "",
        height=430,
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

with right:

    st.markdown('<div class="section-label">Settings</div>', unsafe_allow_html=True)

    summary_type = st.radio(
        "Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    audience = st.selectbox(
        "Target Audience",
        ["Student", "Interview", "Research"]
    )

    st.write("")
    st.write("")

    generate = st.button(
        "Generate Summary",
        use_container_width=True,
        type="primary"
    )

st.write("")
st.divider()

st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)

summary_container = st.container(border=True)

with summary_container:

    if generate and notes.strip():
        # Placeholder — wire this up to your actual summarization call
        st.markdown(
            f"""<div class="summary-text">
            <b>({summary_type} summary for {audience})</b><br><br>
            This is where your generated summary will appear once the backend
            call is wired up. Swap this block out for the real model response.
            </div>""",
            unsafe_allow_html=True
        )
    elif generate and not notes.strip():
        st.markdown(
            '<div class="summary-empty">Please paste some notes before generating a summary.</div>',
            unsafe_allow_html=True
        )
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