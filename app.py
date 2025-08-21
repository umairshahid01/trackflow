import streamlit as st
import streamlit.components.v1 as components

# Set page config
st.set_page_config(page_title="TrackFlow", layout="wide")

# Custom CSS + JS animation
st.markdown(
    """
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #533483);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            height: 100vh;
        }

        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        .logo-container {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0.1);
            animation: zoomInOut 4s ease forwards, moveToCorner 2s ease 4s forwards;
            z-index: 1000;
        }

        @keyframes zoomInOut {
            0% { transform: translate(-50%, -50%) scale(0.1); opacity: 0; }
            40% { transform: translate(-50%, -50%) scale(50); opacity: 1; }
            60% { transform: translate(-50%, -50%) scale(1.2); }
            100% { transform: translate(-50%, -50%) scale(1); }
        }

        @keyframes moveToCorner {
            0% { top: 50%; left: 50%; transform: translate(-50%, -50%) scale(1); }
            100% { top: 40px; left: 40px; transform: translate(0, 0) scale(1); }
        }

        .title {
            font-family: 'Orbitron', sans-serif;
            font-size: 64px;
            font-weight: bold;
            color: white;
            text-align: center;
            margin-top: 200px;
            opacity: 0;
            animation: fadeIn 2s ease 5s forwards;
        }

        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }

        .slabs {
            display: flex;
            justify-content: center;
            margin-top: 50px;
            gap: 40px;
            opacity: 0;
            animation: fadeIn 2s ease 6s forwards;
        }

        .slab {
            width: 200px;
            height: 120px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Orbitron', sans-serif;
            font-size: 20px;
            color: white;
            cursor: pointer;
            transition: transform 0.3s, background 0.3s;
        }

        .slab:hover {
            transform: scale(1.05);
            background: rgba(255, 255, 255, 0.2);
        }

        .admin-btn {
            position: absolute;
            bottom: 30px;
            right: 40px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 10px 20px;
            color: white;
            font-family: 'Orbitron', sans-serif;
            cursor: pointer;
            transition: background 0.3s;
            opacity: 0;
            animation: fadeIn 2s ease 7s forwards;
        }

        .admin-btn:hover {
            background: rgba(255, 255, 255, 0.3);
        }
    </style>

    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">

    <div class="logo-container">
        <img src="assets/logo_placeholder.png" width="100" />
    </div>

    <div class="title">TrackFlow</div>

    <div class="slabs">
        <div class="slab" onclick="window.location.href='?page=TXN_User'">TXN_User</div>
        <div class="slab" onclick="window.location.href='?page=OFN_User'">OFN_User</div>
        <div class="slab" onclick="window.location.href='?page=NDTO_User'">NDTO_User</div>
        <div class="slab" onclick="window.location.href='?page=BSD_User'">BSD_User</div>
    </div>

    <div class="admin-btn" onclick="window.location.href='?page=Admin'">Admin</div>
    """,
    unsafe_allow_html=True,
)

# Routing logic
query_params = st.query_params

if "page" in query_params:
    page = query_params["page"]
    if page == "Admin":
        st.title("🔑 Admin Login")
        pwd = st.text_input("Enter Admin Password", type="password")
        if pwd == "1234":  # change later
            st.success("Access Granted ✅")
        elif pwd:
            st.error("Wrong Password ❌")
    else:
        st.title(f"🚧 Coming Soon: {page}")
