import streamlit as st
from supabase import Client, create_client


@st.cache_resource
def get_supabase() -> Client:
    """Return the server-side Supabase client configured in Streamlit secrets."""
    try:
        url = st.secrets["supabase"]["url"]
        service_key = st.secrets["supabase"].get("service_role_key") or st.secrets["supabase"]["secret_key"]
    except (KeyError, FileNotFoundError) as error:
        raise RuntimeError(
            "Supabase is not configured. Add url and secret_key under "
            "[supabase] in .streamlit/secrets.toml."
        ) from error
    return create_client(url, service_key)
