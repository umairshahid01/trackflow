import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path
import base64

# ===============================
# --------- CONFIG --------------
# ===============================
APP_TITLE = "TrackFlow"
DATA_DIR = Path("data")
SECRETS_DIR = Path("secrets")
ADMIN_PASS_FILE = SECRETS_DIR / "admin_password.txt"
INTERNAL_DB_PATH = DATA_DIR / "mw_sites_database.xlsx"  # Admin can update this later

# Create folders if running locally the first time
DATA_DIR.mkdir(parents=True, exist_ok=True)
SECRETS_DIR.mkdir(parents=True, exist_ok=True)

# ===============================
# ----- HELPER FUNCTIONS --------
# ===============================
def load_admin_password(default: str = "admin123") -> str:
    """Read admin password from a simple text file."""
    try:
        txt = ADMIN_PASS_FILE.read_text(encoding="utf-8").strip()
        return txt if txt else default
    except FileNotFoundError:
        return default

def set_page():
    st.set_page_config(page_title=APP_TITLE, layout="wide", page_icon="📡")

def inject_branding_css():
    # Google Font (tech/futuristic): Orbitron
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )
    # Styling
    st.markdown(
        f"""
        <style>
        :root {{
            --bg1:#0f172a;  
            --bg2:#111827;  
            --bg3:#0b1220;
            --accent:#22d3ee; 
            --muted:#94a3b8;  
            --text:#e5e7eb;   
            --card:#0b1220cc; 
        }}

        .block-container {{
            padding-top: 0rem;
            padding-bottom: 1.5rem;
            max-width: 1200px;
        }}

        html, body {{
            height: 100%;
            background: linear-gradient(135deg, var(--bg1), var(--bg2), var(--bg3));
            background-size: 400% 400%;
            animation: gradientShift 18s ease infinite;
            color: var(--text);
        }}
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        .tf-stage {{
            position: relative;
            min-height: 92vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}

        .tf-logo-wrap {{
            position: fixed;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%) scale(0.5);
            opacity: 0;
            animation: tfLogoIn 1.2s ease-out forwards, tfLogoDock 1.1s ease-in-out 1.4s forwards;
            z-index: 10;
        }}
        @keyframes tfLogoIn {{
            0% {{ opacity: 0; transform: translate(-50%, -50%) scale(0.5); }}
            100% {{ opacity: 1; transform: translate(-50%, -50%) scale(1); }}
        }}
        @keyframes tfLogoDock {{
            0% {{ left:50%; top:50%; transform: translate(-50%, -50%) scale(1); }}
            100% {{ left: 26px; top: 20px; transform: translate(0, 0) scale(0.85); }}
        }}
        .tf-logo {{
            width: 86px; height: 86px; border-radius: 16px;
            box-shadow: 0 12px 40px rgba(0,0,0,0.35);
            object-fit: contain;
            background: #0b1220;
            border: 1px solid rgba(255,255,255,0.08);
        }}

        .tf-title {{
            font-family: 'Orbitron', ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
            font-weight: 900;
            font-size: clamp(42px, 6vw, 72px);
            letter-spacing: 0.04em;
            text-align: center;
            margin-top: 28px;
            text-shadow: 0 8px 26px rgba(0,0,0,0.35);
        }}

        .tf-slabs {{
            display: grid;
            grid-template-columns: repeat(4, minmax(180px, 1fr));
            gap: 16px;
            margin-top: 26px;
            width: min(1100px, 92vw);
        }}
        .tf-slab {{
            background: var(--card);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 22px 18px;
            text-align: center;
            cursor: pointer;
            transition: transform .15s ease, box-shadow .2s ease, border-color .2s ease;
            user-select: none;
        }}
        .tf-slab:hover {{
            transform: translateY(-3px);
            border-color: rgba(34, 211, 238, 0.55);
            box-shadow: 0 18px 45px rgba(0,0,0,0.35);
        }}
        .tf-slab-title {{
            font-family: 'Orbitron', ui-sans-serif, system-ui;
            font-weight: 700;
            font-size: clamp(14px, 1.7vw, 18px);
            letter-spacing: 0.06em;
            color: white; /* ✅ Ensures slab text is white */
        }}

        .tf-admin-wrap {{
            position: fixed;
            right: 22px;
            bottom: 18px;
            z-index: 20;
        }}
        .tf-admin-btn {{
            background: var(--accent);
            color: #062329;
            border: none;
            border-radius: 12px;
            padding: 10px 14px;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 10px 28px rgba(0,0,0,0.25);
        }}
        .tf-admin-btn:hover {{ filter: brightness(0.95); }}

        .tf-modal-overlay {{
            position: fixed; inset: 0;
            background: rgba(0,0,0,0.45);
            backdrop-filter: blur(1px);
            display: flex; align-items: center; justify-content: center;
            z-index: 50;
        }}
        .tf-modal {{
            width: min(420px, 92vw);
            background: var(--card);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 30px 70px rgba(0,0,0,0.5);
        }}
        .tf-modal h3 {{
            font-family: 'Orbitron', ui-sans-serif, system-ui;
            margin-top: 0; margin-bottom: 10px;
        }}
        .tf-hint {{ color: var(--muted); font-size: 13px; }}

        .tf-card {{
            background: var(--card);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 16px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def read_image_as_base64(path: Path) -> str:
    if not path.exists():
        return ""
    data = path.read_bytes()
    return base64.b64encode(data).decode("utf-8")

def show_logo():
    # ✅ Load from "assets/logo.png"
    logo_b64 = read_image_as_base64(Path("assets/logo.png"))
    if logo_b64:
        st.markdown(
            f"""
            <div class="tf-logo-wrap">
              <img class="tf-logo" src="data:image/png;base64,{logo_b64}" alt="TrackFlow Logo"/>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="tf-logo-wrap">
              <div class="tf-logo" style="display:flex;align-items:center;justify-content:center;font-weight:900;">TF</div>
            </div>
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

# ===============================
# --------- VIEWS ----------------
# ===============================
def view_home():
    show_logo()
    st.markdown('<div class="tf-stage">', unsafe_allow_html=True)
    st.markdown(f'<div class="tf-title">{APP_TITLE}</div>', unsafe_allow_html=True)

    st.markdown('<div class="tf-slabs">', unsafe_allow_html=True)
    cols = st.columns(4, gap="small")
    labels = ["TXN_User", "OFN_User", "NDTO_User", "BSD_User"]
    for i, c in enumerate(cols):
        with c:
            clicked = st.button(label=labels[i], key=f"slab_{labels[i]}", use_container_width=True)
            st.markdown(
                f"""<div class="tf-slab"><div class="tf-slab-title">{labels[i]}</div></div>""",
                unsafe_allow_html=True,
            )
            if clicked:
                switch_view(labels[i])
                st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="tf-admin-wrap">
          <button class="tf-admin-btn" onclick="window.location.hash='#admin'">Admin</button>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Admin", key="admin_fallback"):
        st.session_state.show_admin_login = True

    if st.session_state.show_admin_login or st.experimental_get_query_params().get('', [''])[0] == 'admin':
        with st.container():
            st.markdown(
                """
                <div class="tf-modal-overlay">
                  <div class="tf-modal">
                    <h3>Administrator Login</h3>
                    <div class="tf-hint">Enter the admin password to continue.</div>
                """,
                unsafe_allow_html=True,
            )
            with st.form("admin_login_form", clear_on_submit=False):
                pw = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                if submit:
                    if admin_login(pw):
                        st.session_state.is_admin = True
                        st.session_state.show_admin_login = False
                        st.session_state.admin_error = ""
                        switch_view("admin")
                        st.experimental_rerun()
                    else:
                        st.session_state.admin_error = "Incorrect password."
            if st.session_state.admin_error:
                st.error(st.session_state.admin_error)
            if st.button("Cancel", key="admin_cancel"):
                st.session_state.show_admin_login = False
                st.session_state.admin_error = ""
                st.experimental_rerun()
            st.markdown("</div></div>", unsafe_allow_html=True)

def view_role_placeholder(role_name: str):
    show_logo()
    st.markdown(f"### {role_name} — Coming Soon")
    st.markdown(
        """
        <div class="tf-card">
            This area will host the full workflow for the selected user role.
            <br/><br/>
            ✅ Upload BSD Input (for that role), validate fields, run analysis, and allow export to <b>TXN Feasibility Response.xlsx</b> in the exact required format.
            <br/>
            ✅ Business checks & error messages will appear here before analysis starts.
            <br/>
            ✅ Interactive tables & charts (Plotly) can be added here as needed.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    if st.button("⬅ Back to Home"):
        switch_view("home")
        st.experimental_rerun()

def view_admin():
    show_logo()
    st.markdown("## Admin Panel")
    if not st.session_state.get("is_admin", False):
        st.warning("You are not logged in as Admin.")
        if st.button("Back to Home"):
            switch_view("home")
            st.experimental_rerun()
        return

    with st.expander("🔐 Password Management (for you)"):
        st.write(f"Admin password is read from: `{ADMIN_PASS_FILE.as_posix()}`")
        st.caption("Change it by editing that file (or move to Streamlit Secrets later for better security).")

    st.markdown("### 📂 Update Internal Reference Database")
    st.write("Upload the latest **MW Sites Database** Excel. This will replace the current internal file used by the platform.")

    uploaded_db = st.file_uploader("Upload MW Sites Database (.xlsx)", type=["xlsx"], key="upload_db")

    if uploaded_db and st.button("Update Database"):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        bytes_data = uploaded_db.read()
        INTERNAL_DB_PATH.write_bytes(bytes_data)
        st.success(f"Database updated successfully → `{INTERNAL_DB_PATH.as_posix()}`")

    st.divider()
    if st.button("⬅ Back to Home"):
        switch_view("home")
        st.experimental_rerun()

# ===============================
# -------- MAIN ROUTER ----------
# ===============================
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
