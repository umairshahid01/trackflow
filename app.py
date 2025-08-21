import streamlit as st

# --- Inject CSS ---
def inject_branding_css():
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
        <style>
        :root {
            --bg1:#0a0f1f;  
            --bg2:#111827;  
            --bg3:#1a2235;
            --accent:#00f6ff; 
            --accent-glow:#00f6ff;
            --text:#e5e7eb;   
        }

        html, body {
            height: 100%;
            margin: 0;
            overflow-x: hidden;
            background: repeating-linear-gradient(
                -45deg,
                #0a0f1f 0px,
                #0a0f1f 4px,
                #111827 4px,
                #111827 8px
            );
            background-size: 200% 200%;
            animation: bgmove 20s linear infinite;
            color: var(--text);
        }

        @keyframes bgmove {
            0% { background-position: 0% 0%; }
            100% { background-position: 100% 100%; }
        }

        .block-container {
            padding-top: 1rem !important; /* moved everything up */
            max-width: 1200px;
        }

        .tf-stage {
            min-height: 92vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding-top: 10px;
        }

        .tf-title {
            font-family: 'Orbitron', ui-sans-serif, system-ui;
            font-weight: 900;
            font-size: clamp(36px, 5vw, 64px);
            text-align: center;
            margin-bottom: 40px;
            color: var(--accent);
            text-shadow: 0 0 8px rgba(0,246,255,0.8),
                         0 0 20px rgba(0,246,255,0.6),
                         0 0 36px rgba(0,246,255,0.3);
            animation: pulse-glow 3s ease-in-out infinite;
        }

        @keyframes pulse-glow {
            0%, 100% {
                text-shadow: 0 0 8px rgba(0,246,255,0.8),
                             0 0 20px rgba(0,246,255,0.6),
                             0 0 36px rgba(0,246,255,0.3);
                color: var(--accent);
            }
            50% {
                text-shadow: 0 0 16px rgba(0,246,255,1),
                             0 0 32px rgba(0,246,255,0.7),
                             0 0 52px rgba(0,246,255,0.5);
                color: #a5f3fc;
            }
        }

        .stButton>button {
            background: rgba(17, 24, 39, 0.85);
            border: 2px solid rgba(0,246,255,0.4);
            border-radius: 16px;
            padding: 24px 42px;
            font-family: 'Orbitron', ui-sans-serif, system-ui;
            font-weight: 700;
            font-size: 18px;
            color: var(--text);
            letter-spacing: 0.05em;
            cursor: pointer;
            transition: all 0.25s ease-in-out;
            box-shadow: 0 6px 14px rgba(0,0,0,0.6),
                        inset 0 0 12px rgba(0,246,255,0.15);
            width: 220px;
            height: 120px;
        }

        .stButton>button:hover {
            transform: translateY(-4px) scale(1.04);
            border-color: var(--accent-glow);
            box-shadow: 0 0 18px rgba(0,246,255,0.5),
                        0 0 36px rgba(0,246,255,0.35);
            color: var(--accent);
        }

        .tf-admin-wrap {
            position: fixed;
            right: 22px;
            bottom: 18px;
        }

        .tf-admin-btn {
            background: rgba(17, 24, 39, 0.9);
            border: 2px solid rgba(0,246,255,0.6);
            border-radius: 16px;
            padding: 16px 32px;
            font-family: 'Orbitron', ui-sans-serif, system-ui;
            font-weight: 700;
            font-size: 16px;
            color: var(--text);
            letter-spacing: 0.05em;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 6px 14px rgba(0,0,0,0.6),
                        inset 0 0 12px rgba(0,246,255,0.15);
        }

        .tf-admin-btn:hover {
            transform: translateY(-3px) scale(1.03);
            border-color: var(--accent);
            color: var(--accent);
            box-shadow: 0 0 18px rgba(0,246,255,0.5),
                        0 0 36px rgba(0,246,255,0.35);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --- Render Interface ---
def main():
    inject_branding_css()

    st.markdown("<div class='tf-stage'>", unsafe_allow_html=True)

    st.markdown("<div class='tf-title'>TrackFlow</div>", unsafe_allow_html=True)

    # Four slabs in one row
    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        if st.button("Dashboard"):
            st.session_state.page = "dashboard"
    with col2:
        if st.button("Analytics"):
            st.session_state.page = "analytics"
    with col3:
        if st.button("Reports"):
            st.session_state.page = "reports"
    with col4:
        if st.button("Settings"):
            st.session_state.page = "settings"

    st.markdown("</div>", unsafe_allow_html=True)

    # Admin button fixed bottom right
    st.markdown(
        """
        <div class="tf-admin-wrap">
            <button class="tf-admin-btn">Admin</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
