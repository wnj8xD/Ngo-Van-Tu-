import streamlit as st
from modules.auth import login_user, create_user
from modules.db import init_db
from modules.home import show_home
from modules.feedback import save_feedback
from modules.history import show_user_history, show_area_statistics

# Custom CSS for green leaf background and readable content
st.markdown(
    """
    <style>
    /* Background image */
    .stApp {
        background: url('https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1950&q=80') no-repeat center center fixed;
        background-size: cover;
    }
    /* Semi-transparent container for contrast */
    .css-1d391kg .css-1d391kg, .block-container {
        background-color: rgba(255, 255, 255, 0.85) !important;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    /* Headings */
    h1, h2, h3, h4 {
        color: #1B3A02 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    /* Paragraph and label text */
    p, label, div, span, li {
        color: #1e2f1b !important;
        font-weight: 500;
    }
    /* Buttons */
    .stButton > button {
        background-color: #388E3C !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }
    .stButton > button:hover {
        background-color: #2E7D32 !important;
        transform: scale(1.02);
    }
    /* Input fields */
    input[type="text"], input[type="password"] {
        background-color: rgba(255, 255, 255, 0.9);
        color: #1e2f1b;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Cấu hình ứng dụng
st.set_page_config(page_title="Leaf Disease Detection App", layout="centered")
init_db()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "registered" not in st.session_state:
    st.session_state.registered = False

# Tabs giao diện chính
tabs = st.tabs(["🌿 Main Page", "📝 Sign Up", "🔐 Sign In", "📊 History"])

# -------- Tab 0: Main Page --------
with tabs[0]:
    st.write("Hello ", st.session_state.username)
    st.title("🌿 Plant Disease Checker 🌳")
    st.header("With just one photo, we can identify diseases on your plants! 🤩")

    if not st.session_state.logged_in:
        st.warning("Please log in to use the application")
        st.info("Switch to '🔐 Sign In' tab or '📝 Sign Up' tab above.")
    else:
        show_home(st.session_state.username)

# -------- Tab 1: Sign Up --------
with tabs[1]:
    st.title("Register Account")
    username = st.text_input("Username", key="signup_user")
    password = st.text_input("Password", type="password", key="signup_pass")
    confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

    if st.button("Register"):
        if not username or not password:
            st.warning("Please enter all information")
        elif password != confirm:
            st.error("Passwords do not match")
        else:
            success, msg = create_user(username, password)
            if success:
                st.success(msg)
                st.session_state.registered = True
            else:
                st.error(msg)

# -------- Tab 2: Sign In --------
with tabs[2]:
    st.title("Sign In")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Sign In"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Login successful! Welcome {username}.")
        else:
            st.error("Incorrect username or password")

# -------- Tab 3: History --------
with tabs[3]:
    st.title("📊 History")
    if not st.session_state.logged_in:
        st.warning("Please log in to view your history.")
    else:
        show_user_history(st.session_state.username)
        show_area_statistics()
