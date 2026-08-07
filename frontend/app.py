import streamlit as st

st.set_page_config(
    page_title="Dhvani",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# Auth session state — lives here so it survives page switches
# ======================================================

if "jwt_token" not in st.session_state:
    st.session_state.jwt_token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ======================================================
# Pages
# ======================================================

login_page = st.Page("login.py", title="Login", url_path="login")
signup_page = st.Page("signup.py", title="Sign Up", url_path="signup")
dashboard_page = st.Page("dashboard.py", title="Dashboard", url_path="dashboard")

if st.session_state.jwt_token:
    pg = st.navigation([dashboard_page], position="hidden")
else:
    pg = st.navigation([login_page, signup_page], position="hidden")

pg.run()