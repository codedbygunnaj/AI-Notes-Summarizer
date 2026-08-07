import streamlit as st
from theme import inject_theme_css, render_hero, render_message_box
from api_client import login_request

inject_theme_css()

render_hero(
    badge="🧠 AI-Powered Note Intelligence",
    title="Dhvani",
    sub="Welcome back.",
    desc="Log in to keep summarizing your notes."
)

st.write("")

_, mid, _ = st.columns([1, 1.3, 1])

with mid:
    with st.container(border=True):

        st.markdown('<div class="section-label">Login</div>', unsafe_allow_html=True)

        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        st.write("")
        login_clicked = st.button("Login", use_container_width=True, type="primary")

        if login_clicked:
            if not email or not password:
                render_message_box("error", "Please enter both email and password.")
            else:
                with st.spinner("Logging in..."):
                    result = login_request(email.strip(), password)

                if result["success"]:
                    st.session_state.jwt_token = result["token"]
                    st.session_state.user_email = email.strip()
                    st.rerun()  # app.py re-evaluates nav -> dashboard
                else:
                    render_message_box("error", result["error"])

        st.markdown(
            '<div class="auth-switch">Don\'t have an account?</div>',
            unsafe_allow_html=True
        )
        if st.button("Create one →", use_container_width=True):
            st.switch_page("signup.py")  # used to connect pages: login -> signup