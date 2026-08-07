import streamlit as st
from theme import inject_theme_css, render_hero, render_message_box
from api_client import signup_request

inject_theme_css()

render_hero(
    badge="🧠 AI-Powered Note Intelligence",
    title="Dhvani",
    sub="Create your account.",
    desc="Sign up, verify your email, then start summarizing."
)

st.write("")

if "signup_done" not in st.session_state:
    st.session_state.signup_done = False

_, mid, _ = st.columns([1, 1.3, 1])

with mid:
    with st.container(border=True):

        if st.session_state.signup_done:
            st.markdown('<div class="section-label">Almost there</div>', unsafe_allow_html=True)
            render_message_box(
                "success",
                "Verification link sent to your email. Click it, then come back and log in."
            )
            st.write("")
            if st.button("Back to Login", use_container_width=True, type="primary"):
                st.session_state.signup_done = False
                st.switch_page("login.py")  # used to connect pages: signup -> login

        else:
            st.markdown('<div class="section-label">Sign Up</div>', unsafe_allow_html=True)

            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="At least 8 characters")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat your password")

            st.write("")
            signup_clicked = st.button("Sign Up", use_container_width=True, type="primary")

            if signup_clicked:
                if not email or not password or not confirm_password:
                    render_message_box("error", "Please fill in all fields.")
                elif password != confirm_password:
                    render_message_box("error", "Passwords don't match.")
                elif len(password) < 8:
                    render_message_box("error", "Password should be at least 8 characters.")
                else:
                    with st.spinner("Creating your account..."):
                        result = signup_request(email.strip(), password)

                    if result["success"]:
                        st.session_state.signup_done = True
                        st.rerun()
                    else:
                        render_message_box("error", result["error"])

            st.markdown(
                '<div class="auth-switch">Already have an account?</div>',
                unsafe_allow_html=True
            )
            if st.button("Log in →", use_container_width=True):
                st.switch_page("login.py")  # used to connect pages: signup -> login