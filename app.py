import streamlit as st
from streamlit_lottie import st_lottie
import json
import os

# -------------------------
# PAGE CONFIGURATION
# -------------------------
st.set_page_config(
    page_title="TrackFlow",
    page_icon="assets/logo.png",
    layout="wide"
)

# -------------------------
# CUSTOM CSS
# -------------------------
st.markdown(
    """
    <style>
        /* Move logo lower and animate zoom-in */
        .app-logo {
            position: absolute;
            top: 40px;  /* adjust so it's not hidden under top bar */
            left: 40px;
            width: 100px;
            animation: zoomMove 2s ease-in-out forwards;
        }

        @keyframes zoomMove {
            0% {
                transform: scale(10) translateY(100px); /* Big zoom */
                opacity: 0.8;
            }
            100% {
                transform: scale(1) translateY(0); /* Final small logo */
                opacity: 1;
            }
        }

        /* Centered title styling */
        .main-title {
            font-size: 60px;
            font-weight: bold;
            text-align: center;
            margin-top: 180px;
            margin-bottom: 40px;
        }

        /* User buttons as slabs */
        .user-button {
            display: inline-block;
            padding: 20px 40px;
            margin: 10px;
            background-color: #333;
            color: white;
            font-size: 20px;
            font-family: 'Helvetica', sans-serif;
            font-weight: bold;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: background 0.3s ease-in-out;
        }
        .user-button:hover {
            background-color: #555;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# LOGO
# -------------------------
st.image("assets/logo.png", width=100, caption=None, output_format="PNG")

# -------------------------
# MAIN TITLE
# -------------------------
st.markdown("<h1 class='main-title'>TrackFlow</h1>", unsafe_allow_html=True)

# -------------------------
# USER BUTTONS
# -------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='user-button'>TXN_User</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='user-button'>OFN_User</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='user-button'>NDTO_User</div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='user-button'>BSD_User</div>", unsafe_allow_html=True)

# -------------------------
# ADMIN BUTTON
# -------------------------
st.button("Admin")
