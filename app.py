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
    # Use your logo for page icon as requested earlier
    st.set_page_config(page_title=APP_TITLE, layout="wide", page_icon="assets/logo.png")

def inject_branding_css():
    # Google Font (tech/futuristic): Orbitron
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )
    # Styling + Telecom splash + logo animation + delayed UI reveal
    st.markdown(
        f"""
        <style>
        :root {{
            --bg1:#0b0f1a;  
            --bg2:#0f172a;  
            --bg3:#111827;
            --accent:#22d3ee; 
            --muted:#94a3b8;  
            --text:#e5e7eb;   
            --card:#0b1220cc; 
        }}

        /* Keep Streamlit container tight and centered, avoid scroll */
        .block-container {{
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            max-width: 1200px;
        }}

        html, body {{
            height: 100%;
            color: var(--text);
            margin: 0;
            overflow-x: hidden;
            /* Telecom animated background: dark gradient + moving subtle beams */
            background:
              radial-gradient(1200px 500px at 10% 10%, rgba(34,211,238,0.06), rgba(0,0,0,0) 60%),
              radial-gradient(1200px 500px at 90% 20%, rgba(99,102,241,0.06), rgba(0,0,0,0) 60%),
              linear-gradient(135deg, var(--bg1), var(--bg2), var(--bg3));
            background-size: 120% 120%, 120% 120%, 400% 400%;
            animation: bgDrift1 22s ease-in-out infinite, bgDrift2 28s ease-in-out infinite, gradientShift 18s ease infinite;
        }}
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        @keyframes bgDrift1 {{
            0% {{ background-position: 0% 0%, 0% 0%, 0% 50%; }}
            50% {{ background-position: 10% 10%, 0% 0%, 100% 50%; }}
            100% {{ background-position: 0% 0%, 0% 0%, 0% 50%; }}
        }}
        @keyframes bgDrift2 {{
            0% {{ background-position: 0% 0%, 0% 0%, 0% 50%; }}
            50% {{ background-position: 0% 0%, 90% 20%, 100% 50%; }}
            100% {{ background-position: 0% 0%, 0% 0%, 0% 50%; }}
        }}

        /* Stage ensures content is vertically centered and visible without scrolling */
        .tf-stage {{
            position: relative;
            min-height: 100vh;              /* full viewport height */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;         /* center everything */
        }}

        /* Splash overlay: blur + darken during logo animation, then fade away */
        .tf-splash-dim {{
            position: fixed; inset: 0;
            pointer-events: none;
            backdrop-filter: blur(0px);
            background: rgba(0,0,0,0);
            z-index: 6;
            animation: tfDim 5.5s ease-in-out forwards;
        }}
        @keyframes tfDim {{
            0%   {{ backdrop-filter: blur(0px);  background: rgba(0,0,0,0.0); }}
            20%  {{ backdrop-filter: blur(6px);  background: rgba(0,0,0,0.45); }}
            55%  {{ backdrop-filter: blur(8px);  background: rgba(0,0,0,0.6);  }}
            85%  {{ backdrop-filter: blur(6px);  background: rgba(0,0,0,0.35); }}
            100% {{ backdrop-filter: blur(0px);  background: rgba(0,0,0,0.0); }}
        }}

        /* Centered logo: zoom to 50x, pulsate, then dock to top-left */
        .tf-logo-wrap {{
            position: fixed;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%) scale(1);
            opacity: 0;
            z-index: 10;
            /* 1) appear+zoom+pulse for 4.2s, 2) dock after that for 1.1s */
            animation: tfLogoZoomPulse 4.2s ease-out forwards, tfLogoDock 1.1s ease-in-out 4.25s forwards;
        }}
        @keyframes tfLogoZoomPulse {{
            0%   {{ opacity: 0; transform: translate(-50%, -50%) scale(0.4); }}
            10%  {{ opacity: 1; }}
            40%  {{ transform: translate(-50%, -50%) scale(50); }}
            60%  {{ transform: translate(-50%, -50%) scale(1.15); }}
            80%  {{ transform: translate(-50%, -50%) scale(0.92); }}
            100% {{ transform: translate(-50%, -50%) scale(1.00); }}
        }}
        @keyframes tfLogoDock {{
            0%   {{ left:50%; top:50%; transform: translate(-50%, -50%) scale(1.00); }}
            100% {{ left: 26px; top: 24px;  transform: translate(0, 0) scale(0.85); }}
        }}
        .tf-logo {{
            width: 86px; height: 86px; border-radius: 16px;
            box-shadow: 0 12px 40px rgba(0,0,0,0.35);
            object-fit: contain;
            background: #0b1220;
            border: 1px solid rgba(255,255,255,0.08);
        }}

        /* Title */
        .tf-title {{
            font-family: 'Orbitron', ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
            font-weight: 900;
            font-size: clamp(42px, 6vw, 72px);
            letter-spacing: 0.04em;
            text-align: center;
            margin-top: 8px;                 /* small margin so no scroll */
            text-shadow: 0 8px 26px rgba(0,0,0,0.35);
            opacity: 0;
            animation: tfUIIn 0.8s ease forwards;
            animation-delay: 5.5s;           /* delay until logo finishes docking */
        }}

        /* Slabs grid */
        .tf-slabs {{
            display: grid;
            grid-template-columns: repeat(4, minmax(180px, 1fr));
            gap: 16px;
            margin-top: 24px;
            width: min(1100px, 92vw);
            opacity: 0;
            animation: tfUIIn 0.8s ease forwards;
            animation-delay: 5.6s;           /* appear right after title */
        }}
        @keyframes tfUIIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to   {{ opacity: 1; transform: translateY(0px); }}
        }}
        .tf-slab {{
            background: var(--card);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 28px 18px;
            text-align: center;
            cursor: pointer;
            transition: transform .15s ease, box-shadow .2s ease, border-color .2s ease, background .2s ease;
            user-select: none;
        }}
        .tf-slab:hover {{
            transform: translateY(-4px);
            border-color: rgba(34, 211, 238, 0.55);
            box-shadow: 0 18px 45px rgba(0,0,0,0.35);
            background: rgba(34,211,238,0.06);
        }}
        .tf-slab-title {{
            font-family: 'Orbitron', ui-sans-serif, system-ui;
            font-weight: 700;
            font-size: clamp(14px, 1.7vw, 18px);
            letter-spacing: 0.06em;
            color: white; /* white text as requested */
        }}
        .tf-slab a {{ text-decoration: none; color: inherit; display:block; }}

        /* Floating Admin visual button */
        .tf-admin-wrap {{
            position: fixed;
            right: 22px;
            bottom: 18px;
            z-index: 20;
            opacity: 0;
            animation: tfUIIn 0.8s ease forwards;
            animation-delay: 5.7s;           /* after slabs */
        }}
        .tf-admin-btn {{
            background: var(--accent);
            color: #062329 !important;
            border: none;
            border-radius: 12px;
            padding: 10px 14px;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 10px 28px rgba(0,0,0,0.25);
        }}
        .tf-admin-btn:hover {{ filter: brightness(0.95); }}

        /* Modal */
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
            <div class="tf-splash-dim"></div>
            <div class="tf-logo-wrap">
              <img class="tf-logo" src="data:image/png;base64,{logo_b64}" alt="TrackFlow Logo"/>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="tf-splash-dim"></div>
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
    # Handle clickable slabs via query parameter (?nav=...)
    params = st.experimental_get_query_params()
    nav = params.get("nav", [None])[0]
    if nav:
        if nav in ["TXN_User", "OFN_User", "NDTO_User", "BSD_User"]:
            switch_view(nav)
            # Clear params to avoid stale URL
            st.experimental_set_query_params()
            st.experimental_rerun()
        elif nav == "admin":
            st.session_state.show_admin_login = True
            # Clear params and stay on home to show modal
            st.experimental_set_query_params()

    show_logo()

    st.markdown('<div class="tf-stage">', unsafe_allow_html=True)
    st.markdown(f'<div class="tf-title">{APP_TITLE}</div>', unsafe_allow_html=True)

    # Clickable slabs (names inside, white font). Uses query params for routing.
    labels = ["TXN_User", "OFN_User", "NDTO_User", "BSD_User"]
    slab_html = '<div class="tf-slabs">'
    for label in labels:
        slab_html += f"""
        <div class="tf-slab">
            <a href="?nav={label}">
              <div class="tf-slab-title">{label}</div>
            </a>
        </div>
        """
    slab_html += "</div>"
    st.markdown(slab_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close tf-stage

    # Floating visual Admin button (visual + link)
    st.markdown(
        """
        <div class="tf-admin-wrap">
          <a class="tf-admin-btn" href="?nav=admin">Admin</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Reliable fallback Admin button (always works)
    if st.button("Admin", key="admin_fallback"):
        st.session_state.show_admin_login = True

    # Existing admin modal logic preserved
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

    # Handle nav param globally (in case someone hits a direct deep link)
    params = st.experimental_get_query_params()
    nav = params.get("nav", [None])[0]
    if nav:
        if nav in ["TXN_User", "OFN_User", "NDTO_User", "BSD_User"]:
            switch_view(nav)
            st.experimental_set_query_params()
        elif nav == "admin":
            st.session_state.show_admin_login = True
            st.experimental_set_query_params()

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
