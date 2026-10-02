import bcrypt
import streamlit as st

from .config import ACCOUNTS_TABLE
from .supabase_client import get_supabase

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "Admin@123"


def _default_credentials():
    try:
        return st.secrets["admin"]["username"], st.secrets["admin"]["password"]
    except (KeyError, FileNotFoundError):
        return DEFAULT_USERNAME, DEFAULT_PASSWORD


def ensure_user_store():
    response = get_supabase().table(ACCOUNTS_TABLE).select("username").limit(1).execute()
    if response.data:
        return
    username, password = _default_credentials()
    get_supabase().table(ACCOUNTS_TABLE).insert({
        "username": username,
        "password_hash": bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
        "role": "super_admin",
        "active": True,
        "dashboard": None,
    }).execute()


def load_users():
    ensure_user_store()
    response = (
        get_supabase()
        .table(ACCOUNTS_TABLE)
        .select("username,password_hash,role,active,dashboard")
        .order("username")
        .execute()
    )
    return {item["username"]: item for item in (response.data or [])}


def authenticate(username, password):
    ensure_user_store()
    response = (
        get_supabase()
        .table(ACCOUNTS_TABLE)
        .select("username,password_hash,role,active,dashboard")
        .eq("username", username)
        .limit(1)
        .execute()
    )
    if not response.data:
        return False
    user = response.data[0]
    return bool(
        user.get("active", True)
        and bcrypt.checkpw(password.encode(), user["password_hash"].encode())
    )


def current_user():
    username = st.session_state.get("admin_username")
    if not username:
        return None, {}
    return username, {
        "username": username,
        "role": st.session_state.get("admin_role", "viewer"),
        "active": bool(st.session_state.get("admin_authenticated")),
        "dashboard": st.session_state.get("assigned_dashboard"),
    }


def create_user(username, password, role, dashboard=None):
    if username in load_users():
        raise ValueError("Username already exists.")
    get_supabase().table(ACCOUNTS_TABLE).insert({
        "username": username,
        "password_hash": bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
        "role": role,
        "active": True,
        "dashboard": dashboard if role == "operator" else None,
    }).execute()
    from .dashboard_store import add_history
    add_history(st.session_state.get("username", "system"), f"Created {role} account", dashboard or "", username)


def update_user(username, role, active, dashboard=None):
    if username not in load_users():
        raise ValueError("User not found.")
    get_supabase().table(ACCOUNTS_TABLE).update({
        "role": role,
        "active": active,
        "dashboard": dashboard if role == "operator" else None,
    }).eq("username", username).execute()
    from .dashboard_store import add_history
    add_history(st.session_state.get("username", "system"), f"Updated {role} account", dashboard or "", username)


def change_password(username, current_password, new_password):
    if not authenticate(username, current_password):
        raise ValueError("The current password is incorrect.")
    if len(new_password) < 8:
        raise ValueError("The new password must contain at least 8 characters.")
    if current_password == new_password:
        raise ValueError("The new password must be different from the current password.")
    password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    get_supabase().table(ACCOUNTS_TABLE).update({
        "password_hash": password_hash,
    }).eq("username", username).execute()
    from .dashboard_store import add_history
    add_history(username, "Changed account password", "", username)


def login_screen():
    st.markdown("<div class='login-title'>Evacuation Center<br>Management System</div>", unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", use_container_width=True)
    if submitted:
        if authenticate(username.strip(), password):
            st.session_state.authenticated = True
            st.session_state.username = username.strip()
            st.rerun()
        st.error("Incorrect username or password.")


def require_login():
    if not st.session_state.get("authenticated"):
        login_screen()
        st.stop()


@st.dialog("Staff Sign In")
def login_dialog():
    st.caption("Enter your authorized dashboard account.")
    with st.form("modal_login", clear_on_submit=False):
        username = st.text_input("Username", key="modal_username")
        password = st.text_input("Password", type="password", key="modal_password")
        submitted = st.form_submit_button(
            "Sign In", icon=":material/lock_open:", use_container_width=True, type="primary"
        )
    if submitted:
        if authenticate(username.strip(), password):
            st.session_state.authenticated = True
            st.session_state.username = username.strip()
            st.rerun()
        st.error("Incorrect username or password.")


def logout():
    st.session_state.clear()
    st.rerun()
