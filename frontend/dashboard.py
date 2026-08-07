import threading

import streamlit as st
from pypdf import PdfReader

from theme import (
    inject_theme_css,
    render_hero,
    render_user_topbar,
    render_stats,
    run_generative_loader,
    clean_summary_text,
    render_message_box,
)
from api_client import call_summarize_threaded

CHAR_LIMIT = 24000  # backend limit is 25K; trimming a bit short to stay safely under

# ======================================================
# Auth guard — defensive; app.py's navigation already gates this page,
# but this keeps dashboard.py safe to run/refresh directly.
# ======================================================

if not st.session_state.get("jwt_token"):
    st.switch_page("login.py")

inject_theme_css()

# ======================================================
# Session State (per-run summary result)
# ======================================================

if "last_result" not in st.session_state:
    st.session_state.last_result = {
        "summary": None,
        "model": "—",
        "version": "v1.0.0",
        "response_time": "—",
        "warning": None,
        "error": None,
    }

# ======================================================
# PDF text extraction
# ======================================================

def extract_pdf_text(uploaded_pdf) -> str:
    """Extracts text from an uploaded PDF using pypdf. Skips pages that fail
    to extract (e.g. scanned/image-only pages) instead of crashing the app."""
    reader = PdfReader(uploaded_pdf)
    chunks = []
    for page in reader.pages:
        try:
            page_text = page.extract_text() or ""
        except Exception:
            page_text = ""
        if page_text.strip():
            chunks.append(page_text.strip())
    return "\n\n".join(chunks).strip()

# ======================================================
# Top bar — avatar/email left, Logout right
# ======================================================

logout_clicked = render_user_topbar(st.session_state.get("user_email", ""))

if logout_clicked:
    st.session_state.jwt_token = None
    st.session_state.user_email = None
    st.session_state.pop("last_result", None)
    st.rerun()  # app.py re-evaluates nav -> back to login

# ======================================================
# Hero
# ======================================================

render_hero(
    badge="🧠 AI-Powered Note Intelligence",
    title="Dhvani",
    sub="Your thoughts already know where to go.",
    desc="Transform lengthy notes into concise, structured knowledge."
)

st.write("")
st.divider()

# ======================================================
# Main Layout — Notes + Settings + PDF | Custom Instructions + Stats
# ======================================================

left, right = st.columns([3.7, 1.3], gap="large")

with left:

    st.markdown('<div class="section-label">Notes</div>', unsafe_allow_html=True)

    notes = st.text_area(
        "",
        height=340,
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

    set_col1, set_col2 = st.columns(2)

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

    st.markdown('<div class="section-label-sm">Reference PDF (optional)</div>', unsafe_allow_html=True)

    # note: dropped the old `max_upload_size` kwarg from the previous version —
    # st.file_uploader doesn't support it, it was throwing a TypeError on load
    reference_pdf = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )

    pdf_text = ""

    if reference_pdf is not None:
        pdf_text = extract_pdf_text(reference_pdf)

        if pdf_text:
            st.caption(f"📄 Extracted **{len(pdf_text):,}** characters from **{reference_pdf.name}**")
        else:
            st.caption("⚠️ Couldn't extract any text from this PDF — it may be scanned/image-only.")

        with st.expander("Preview PDF"):
            st.pdf(reference_pdf, height=320)

with right:

    st.markdown('<div class="section-label">Custom Instructions</div>', unsafe_allow_html=True)

    additional_instructions = st.text_area(
        "",
        height=160,
        placeholder="""Examples

• Explain like I'm 10
• Use Hinglish
• Keep examples
• Focus on interview questions
• Don't use bullet points""",
        label_visibility="collapsed"
    )

    st.write("")

    generate = st.button(
        "Generate Summary",
        use_container_width=True,
        type="primary"
    )

    st.markdown('<div class="section-label-sm">Status</div>', unsafe_allow_html=True)

    stats_placeholder = st.empty()
    with stats_placeholder.container():
        render_stats(st.session_state.last_result)

# ======================================================
# Generate flow — merge sources, guard char limit, call backend with JWT
# ======================================================

if generate:

    combined_parts = []
    if notes.strip():
        combined_parts.append(notes.strip())
    if pdf_text.strip():
        combined_parts.append(pdf_text.strip())

    combined_text = "\n\n".join(combined_parts).strip()

    if not combined_text:
        st.session_state.last_result = {
            "summary": None,
            "model": st.session_state.last_result.get("model", "—"),
            "version": "v1.0.0",
            "response_time": st.session_state.last_result.get("response_time", "—"),
            "warning": None,
            "error": "Please paste some notes or upload a PDF before generating a summary.",
        }

    else:
        warning = None
        if len(combined_text) > CHAR_LIMIT:
            combined_text = combined_text[:CHAR_LIMIT]
            warning = (
                f"⚠️ Limit exceeded — your notes/PDF were trimmed to the first "
                f"{CHAR_LIMIT:,} characters to stay within the backend's limit."
            )

        payload = {
            "text": combined_text,
            "summary_type": summary_type.lower(),
            "audience": audience.lower(),
            "additional_instructions": additional_instructions.strip(),
        }

        result_box = {"done": False}
        thread = threading.Thread(
            target=call_summarize_threaded,
            args=(payload, st.session_state.jwt_token, result_box)
        )
        thread.start()

        loader_placeholder = st.empty()
        run_generative_loader(loader_placeholder, thread)
        thread.join()

        if result_box.get("auth_error"):
            # token expired/invalid — clear it and give the user a clean
            # way back instead of showing an error they can't act on
            st.session_state.jwt_token = None
            st.session_state.user_email = None
            render_message_box("error", result_box.get("error", "Session expired. Please log in again."))
            if st.button("Back to Login"):
                st.rerun()
            st.stop()

        if result_box.get("success"):
            st.session_state.last_result = {
                "summary": clean_summary_text(result_box.get("summary", "")),
                "model": result_box.get("model", "—"),
                "version": "v1.0.0",
                "response_time": result_box.get("response_time", "—"),
                "warning": warning,
                "error": None,
            }
        else:
            st.session_state.last_result = {
                "summary": None,
                "model": st.session_state.last_result.get("model", "—"),
                "version": "v1.0.0",
                "response_time": st.session_state.last_result.get("response_time", "—"),
                "warning": warning,
                "error": result_box.get("error", "Something went wrong."),
            }

        # refresh the stats card with the new run's data
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

    if result.get("warning"):
        render_message_box("warning", result["warning"])

    if result.get("error"):
        render_message_box("error", result["error"])

    elif result.get("summary"):
        st.markdown(result["summary"])

    else:
        st.markdown(
            """
            <div class="summary-empty">
            No summary generated yet.<br>
            Paste your notes, upload a PDF, or both — then click <b>Generate Summary</b>.
            </div>
            """,
            unsafe_allow_html=True
        )