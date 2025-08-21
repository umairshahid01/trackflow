import streamlit as st
import time

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="TrackFlow", layout="wide")

# -------------------------------
# CUSTOM CSS (Background + Animations + Styling)
# -------------------------------
page_bg = """
<style>
/* Telecom themed background */
body {
    background-image: url("https://images.unsplash.com/photo-1518770660439-4636190af475"); 
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    font-family: 'Arial', sans-serif;
    overflow: hidden;
    margin: 0;
}

/* Overlay for blur + darkening */
.bg-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    backdrop-filter: blur(0px);
    background: rgba(0,0,0,0);
    animation: blurFade 5s forwards;
    z-index: 1;
}

@keyframes blurFade {
    0% { backdrop-filter: blur(0px); background: rgba(0,0,0,0); }
    100% { backdrop-filter: blur(10px); background: rgba(0,0,0,0.7); }
}

/* Jazz Logo Animation */
@keyframes logoZoomCenter {
    0% {
        transform: translate(-50%, -50%) scale(1);
        top: 50%;
        left: 50%;
    }
    50% {
        transform: translate(-50%, -50%) scale(50);
        top: 50%;
        left: 50%;
    }
    80% {
        transform: translate(-50%, -50%) scale(1.2);
        top: 50%;
        left: 50%;
    }
    100% {
        transform: translate(0, 0) scale(1);
        top: 20px;
        left: 20px;
    }
}

.logo-container {
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%) scale(1);
    animation: logoZoomCenter 5s ease-in-out forwards;
    z-index: 2;
}

/* Title */
h1 {
    text-align: center;
    font-size: 60px;
    color: #f5f5f5;
    text-shadow: 2px 2px 5px #000000;
}

/* Buttons */
.stButton>button {
    background-color: #2c2f38;
    color: white;
    font-size: 20px;
    border-radius: 15px;
    padding: 15px 40px;
    margin: 20px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    z-index: 3;
}

.stButton>button:hover {
    background-color: #444857;
    color: #ffcc00;
    transition: 0.3s;
}

/* Admin button */
.admin-button {
    position: fixed;
    bottom: 20px;
    right: 30px;
    background-color: #d32f2f !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 12px 25px !important;
    font-size: 18px !important;
    font-weight: bold;
    z-index: 3;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -------------------------------
# BACKGROUND OVERLAY
# -------------------------------
st.markdown('<div class="bg-overlay"></div>', unsafe_allow_html=True)

# -------------------------------
# JAZZ LOGO
# -------------------------------
st.markdown(
    """
    <div class="logo-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/8/88/Jazz_%28Mobilink%29_Logo.png" width="120">
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# DELAY FOR ANIMATION
# -------------------------------
time.sleep(5)

# -------------------------------
# TITLE
# -------------------------------
st.markdown("<h1>TrackFlow</h1>", unsafe_allow_html=True)

# -------------------------------
# FOUR BUTTONS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("TXN_User"):
        st.success("TXN_User Window Opened")
with col2:
    if st.button("OFN_User"):
        st.success("OFN_User Window Opened")
with col3:
    if st.button("NOTO_User"):
        st.success("NOTO_User Window Opened")
with col4:
    if st.button("BSD_User"):
        st.success("BSD_User Window Opened")

# -------------------------------
# ADMIN BUTTON
# -------------------------------
st.markdown(
    """
    <div style="position: fixed; bottom: 20px; right: 30px;">
        <form action="#" method="get">
            <button class="admin-button">Admin</button>
        </form>
    </div>
    """,
    unsafe_allow_html=True
)
