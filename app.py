import streamlit as st
from pathlib import Path

APP_TITLE = "TrackFlow"
DATA_DIR = Path("data")
SECRETS_DIR = Path("secrets")
ADMIN_PASS_FILE = SECRETS_DIR / "admin_password.txt"

DATA_DIR.mkdir(parents=True, exist_ok=True)
SECRETS_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------
# Helpers
# -------------------------
def load_admin_password(default: str = "admin123") -> str:
    try:
        txt = ADMIN_PASS_FILE.read_text(encoding="utf-8").strip()
        return txt if txt else default
    except FileNotFoundError:
        return default


def set_page():
    st.set_page_config(page_title=APP_TITLE, layout="wide")


def inject_branding_css():
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
        <style>
        :root {
            --bg:#0a0f1c;  /* solid futuristic deep navy */
            --accent:#22d3ee; 
            --text:#e5e7eb;   
        }
        html, body, .stApp {
            height: 100%;
            background: var(--bg) !important;  /* enforce solid fill */
            color: var(--text);
        }
        .block-container {
            padding-top: 1rem !important;   /* moved everything up */
            max-width: 1200px;
        }
        .tf-stage {
            min-height: 92vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding-top: 10px;  /* reduced from 40px */
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
        /* Rectangular slabs (user role buttons) now same style as Admin */
        .stButton>button {
            background: linear-gradient(145deg, #111827, #1e293b);
            border: 2px solid rgba(34,211,238,0.6); /* match admin */
            border-radius: 16px;
            padding: 16px 32px;  /* match admin */
            font-family: 'Orbitron', ui-sans-serif, system-ui;
            font-weight: 700;
            font-size: 16px;  /* same as admin */
            color: white;
            letter-spacing: 0.05em;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 6px 14px rgba(0,0,0,0.4);
            width: 220px;
            height: 120px;
        }
        .stButton>button:hover {
            transform: translateY(-3px) scale(1.02); /* match admin */
            border-color: var(--accent);
            color: var(--accent);
            box-shadow: 0 12px 24px rgba(34,211,238,0.35);
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
        unsafe_allow_html=True,
    )


def init_state():
    if "current_view" not in st.session_state:
        st.session_state.current_view = "home"
    if "show_admin_login" not in st.session_state:
        st.session_state.show_admin_login = False
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False
    if "admin_error" not in st.session_state:
        st.session_state.admin_error = ""


def switch_view(view: str):
    st.session_state.current_view = view


def admin_login(password_input: str) -> bool:
    return password_input == load_admin_password()


# -------------------------
# Views
# -------------------------
def view_home():
    st.markdown('<div class="tf-stage">', unsafe_allow_html=True)
    st.markdown(f'<div class="tf-title">{APP_TITLE}</div>', unsafe_allow_html=True)

    # All four slabs in one row
    cols = st.columns(4, gap="large")
    labels = ["TXN_User", "OFN_User", "NDTO_User", "BSD_User"]
    for i, col in enumerate(cols):
        with col:
            if st.button(labels[i], key=f"slab_{labels[i]}", use_container_width=True):
                switch_view(labels[i])
                st.experimental_rerun()

    # Floating admin button only
    st.markdown(
        """
        <div class="tf-admin-wrap">
          <button class="tf-admin-btn" onclick="window.location.hash='#admin'">Admin</button>
        </div>
        """,
        unsafe_allow_html=True,
    )


def view_role_placeholder(role_name: str):
    st.markdown(f"### {role_name} — Coming Soon")
    st.write("This area will hold workflow for the selected user role.")
    if st.button("⬅ Back to Home"):
        switch_view("home")
        st.experimental_rerun()


def view_admin():
    st.markdown("## Admin Panel")
    if not st.session_state.get("is_admin", False):
        st.warning("You are not logged in as Admin.")
        if st.button("Back to Home"):
            switch_view("home")
            st.experimental_rerun()
        return
    st.write("Admin functionality goes here.")


# -------------------------
# Main app
# -------------------------
def main():
    set_page()
    inject_branding_css()
    init_state()

    view = st.session_state.current_view
    if view == "home":
        view_home()
    elif view in ["TXN_User", "OFN_User", "NDTO_User", "BSD_User"]:
        view_role_placeholder(view)
    elif view == "admin":
        view_admin()
    else:
        switch_view("home")
        view_home()


if __name__ == "__main__":
    main()
