import streamlit as st

# ---- Custom CSS with Futuristic Nebula Background ----
st.markdown(
    """
    <style>
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
        padding-top: 10px; /* reduced from 40px */
    }

    /* Futuristic Nebula Background */
    html, body, .stApp {
        background: radial-gradient(circle at 20% 30%, rgba(34,211,238,0.08) 0%, transparent 60%),
                    radial-gradient(circle at 80% 70%, rgba(168,85,247,0.08) 0%, transparent 60%),
                    radial-gradient(circle at 50% 50%, rgba(59,130,246,0.06) 0%, transparent 70%),
                    #0a0f1c;  /* deep navy base */
        background-size: 200% 200%;
        animation: nebula-move 20s ease-in-out infinite;
    }

    @keyframes nebula-move {
        0%   { background-position: 0% 0%; }
        50%  { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    .tf-title {
        font-family: 'Orbitron', ui-sans-serif, system-ui;
        font-weight: 900;
        font-size: clamp(36px, 5vw, 64px);
        text-align: center;
        margin-bottom: 40px;
        color: var(--accent);
        text-shadow: 0 0 8px rgba(34,211,238,0.7),
                     0 0 20px rgba(34,211,238,0.4),
                     0 0 36px rgba(34,211,238,0.25);
        animation: pulse-glow 3s ease-in-out infinite;
    }

    @keyframes pulse-glow {
        0%, 100% {
            text-shadow: 0 0 8px rgba(34,211,238,0.7),
                         0 0 20px rgba(34,211,238,0.4),
                         0 0 36px rgba(34,211,238,0.25);
            color: var(--accent);
        }
        50% {
            text-shadow: 0 0 12px rgba(34,211,238,1),
                         0 0 28px rgba(34,211,238,0.6),
                         0 0 48px rgba(34,211,238,0.35);
            color: #a5f3fc; /* lighter cyan */
        }
    }

    .stButton>button {
        background: linear-gradient(145deg, #111827, #1e293b);
        border: 2px solid rgba(34,211,238,0.4);
        border-radius: 16px;
        padding: 24px 42px;
        font-family: 'Orbitron', ui-sans-serif, system-ui;
        font-weight: 700;
        font-size: 18px;
        color: white;
        letter-spacing: 0.05em;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 6px 14px rgba(0,0,0,0.4);
        width: 220px;
        height: 120px;
    }

    .stButton>button:hover {
        transform: translateY(-4px) scale(1.03);
        border-color: var(--accent);
        box-shadow: 0 12px 26px rgba(34,211,238,0.35);
        color: var(--accent);
    }

    .tf-admin-wrap {
        position: fixed;
        right: 22px;
        bottom: 18px;
    }

    .tf-admin-btn {
        background: linear-gradient(145deg, #111827, #1e293b);
        border: 2px solid rgba(34,211,238,0.6);
        border-radius: 16px;
        padding: 16px 32px;
        font-family: 'Orbitron', ui-sans-serif, system-ui;
        font-weight: 700;
        font-size: 16px;
        color: white;
        letter-spacing: 0.05em;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 6px 14px rgba(0,0,0,0.4);
    }

    .tf-admin-btn:hover {
        transform: translateY(-3px) scale(1.02);
        border-color: var(--accent);
        color: var(--accent);
        box-shadow: 0 12px 24px rgba(34,211,238,0.35);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Title ----
st.markdown("<div class='tf-title'>TrackFlow</div>", unsafe_allow_html=True)

# ---- Four Slabs in One Row ----
col1, col2, col3, col4 = st.columns(4, gap="large")

with col1:
    if st.button("Tab 1"):
        st.write("Tab 1 clicked!")

with col2:
    if st.button("Tab 2"):
        st.write("Tab 2 clicked!")

with col3:
    if st.button("Tab 3"):
        st.write("Tab 3 clicked!")

with col4:
    if st.button("Tab 4"):
        st.write("Tab 4 clicked!")

# ---- Admin Button (Bottom Right) ----
st.markdown(
    """
    <div class="tf-admin-wrap">
        <button class="tf-admin-btn">Admin</button>
    </div>
    """,
    unsafe_allow_html=True
)
