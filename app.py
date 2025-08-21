import streamlit as st
import time

# Set page config
st.set_page_config(page_title="TrackFlow", layout="wide")

# Custom CSS for background, animations, and slabs
st.markdown(
    """
    <style>
    /* Telecom themed background */
    body {
        margin: 0;
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        height: 100vh;
        overflow: hidden;
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
            top: 10px;
            left: 10px;
        }
    }

    .logo-container {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(1);
        animation: logoZoomCenter 5s ease-in-out forwards;
        z-index: 9999;
    }

    /* TrackFlow title */
    .trackflow-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px;
        text-align: center;
        margin-top: 120px;
        color: white;
    }

    /* Slabs styling */
    .slabs-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 50px;
    }

    .slab {
        background: #1e3c72;
        background: linear-gradient(to right, #2a5298, #1e3c72);
        padding: 50px 80px;
        border-radius: 20px;
        box-shadow: 0 8px 15px rgba(0,0,0,0.3);
        font-family: 'Orbitron', sans-serif;
        font-size: 22px;
        color: white;
        text-align: center;
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .slab:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 25px rgba(0,0,0,0.5);
    }

    /* Admin button */
    .admin-btn {
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ff4b2b;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        font-family: 'Orbitron', sans-serif;
        cursor: pointer;
        z-index: 10000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo
st.markdown(
    """
    <div class="logo-container">
        <img src="assets/logo.png" width="120">
    </div>
    """,
    unsafe_allow_html=True
)

# Delay before showing rest of UI
time.sleep(5)

# TrackFlow Title
st.markdown('<div class="trackflow-title">TrackFlow</div>', unsafe_allow_html=True)

# Slabs
st.markdown(
    """
    <div class="slabs-container">
        <div class="slab" onclick="window.location.href='TXN_User'">TXN_User</div>
        <div class="slab" onclick="window.location.href='OFN_User'">OFN_User</div>
        <div class="slab" onclick="window.location.href='NDTO_User'">NDTO_User</div>
        <div class="slab" onclick="window.location.href='BSD_User'">BSD_User</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Admin Button
st.markdown('<div class="admin-btn">Admin</div>', unsafe_allow_html=True)
