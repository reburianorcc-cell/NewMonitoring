from html import escape
import pandas as pd
import streamlit as st

from .auth import current_user, logout
from .config import APP_TITLE
from .dashboard_store import delete_dashboard, list_dashboards, load_dashboard, save_dashboard
from .data_loader import empty_dashboard_data, parse_upload
from .styles import apply_styles
from .views import centers_view, evacuees_view, gallery_view, overview

apply_styles()

authenticated = bool(st.session_state.get("authenticated"))
username, user = current_user() if authenticated else (None, {})
role = user.get("role", "public")
try:
    dashboards = list_dashboards()
except Exception as error:
    st.error("Supabase connection failed. Confirm your Streamlit secrets and run supabase_setup.sql in the Supabase SQL Editor.")
    st.caption(str(error))
    st.stop()
all_names = sorted(dashboards)
if role == "operator":
    assigned = user.get("dashboard")
    visible_names = [assigned] if assigned in dashboards else []
else:
    visible_names = all_names


def select_page(page_name):
    st.session_state.current_page = page_name

with st.sidebar:
    navigation = [
        ("Overview", ":material/home:"),
        ("Evacuation Centers", ":material/apartment:"),
        ("Evacuees", ":material/groups:"),
        ("Gallery", ":material/photo_library:"),
    ]
    if authenticated:
        navigation.append(("Data Upload", ":material/cloud_upload:"))
    allowed_pages = [item[0] for item in navigation]
    if st.session_state.get("current_page") not in allowed_pages:
        st.session_state.current_page = "Overview"
    for page_name, page_icon in navigation:
        st.button(
            page_name,
            icon=page_icon,
            key=f"nav_{page_name.casefold().replace(' ', '_')}",
            type="primary" if st.session_state.current_page == page_name else "secondary",
            use_container_width=True,
            on_click=select_page,
            args=(page_name,),
        )
    page = st.session_state.current_page
    st.divider()

title_col, selector_col = st.columns([1.7, 1])
with title_col:
    st.markdown(f"<div class='page-heading'><span class='eyebrow'>COMMAND CENTER</span><h1>{APP_TITLE}</h1><p>Public operational overview of registered evacuation centers</p></div>", unsafe_allow_html=True)
with selector_col:
    if visible_names:
        previous = st.session_state.get("selected_dashboard")
        default_index = visible_names.index(previous) if previous in visible_names else 0
        selected_dashboard = st.selectbox("📊 Selected dashboard", visible_names, index=default_index)
        st.session_state.selected_dashboard = selected_dashboard
    else:
        selected_dashboard = None
        st.markdown("<div class='dataset-card'><div class='dataset-icon'>📊</div><div><small>SELECTED DASHBOARD</small><strong>No dashboard available</strong></div><span class='idle-dot'></span></div>", unsafe_allow_html=True)

# Keep the upload result visible after st.rerun clears the uploader form.
upload_success = st.session_state.pop("upload_success", None)
if upload_success:
    st.success(upload_success, icon="✅")
    st.toast(upload_success, icon="✅")

df = load_dashboard(selected_dashboard) if selected_dashboard else empty_dashboard_data()
view_pages = ("Overview", "Evacuation Centers", "Evacuees", "Gallery")
if not df.empty and page in view_pages:
    selected_centers = st.multiselect("🏢 Filter evacuation centers", sorted(df["Name"].dropna().unique()), placeholder="All evacuation centers")
    filtered_df = df[df["Name"].isin(selected_centers)].copy() if selected_centers else df
    st.caption(f"Showing {len(filtered_df):,} of {len(df):,} evacuation centers")
else:
    filtered_df = df

if page in view_pages and df.empty:
    st.markdown("<div class='empty-state'><div class='empty-icon'>☁️</div><h2>No dashboard data available</h2><p>Dashboard data will appear here after an authorized user uploads it.</p></div>", unsafe_allow_html=True)
elif page == "Overview": overview(filtered_df)
elif page == "Evacuation Centers": centers_view(filtered_df)
elif page == "Evacuees": evacuees_view(filtered_df)
elif page == "Gallery": gallery_view(filtered_df)
elif page == "Data Upload":
    st.subheader("Upload Evacuation Center Data")
    st.info("Select an existing dashboard to update it, or create a new dashboard if your role allows it.")
    if role == "operator":
        target_name = user.get("dashboard") or ""
        st.text_input("Assigned dashboard", value=target_name, disabled=True)
    else:
        target_choice = st.selectbox("Dashboard action", ["Create new dashboard"] + all_names)
        if target_choice == "Create new dashboard":
            target_name = st.text_input("New dashboard name", placeholder="Example: Bohol", max_chars=80).strip()
        else:
            target_name = target_choice
            st.caption(f"Uploading will update **{target_name}**.")
    uploaded = st.file_uploader("CSV or Excel file", type=["csv", "xlsx", "xls"])
    if uploaded:
        try:
            preview, gallery_assets = parse_upload(uploaded)
            st.success(f"Validated {len(preview)} evacuation centers.")
            st.dataframe(preview.head(10), use_container_width=True, hide_index=True)
            confirm = st.checkbox("I confirm that I want to create or update this dashboard.")
            if st.button("☁️ Save dashboard", type="primary", disabled=not (confirm and target_name)):
                action = save_dashboard(target_name, preview, gallery_assets, username, uploaded.name)
                st.session_state.selected_dashboard = target_name
                if action == "Created":
                    st.session_state.upload_success = f"New CSV/Excel file added successfully to {target_name}."
                else:
                    st.session_state.upload_success = f"CSV/Excel file updated successfully for {target_name}."
                st.rerun()
        except Exception as error: st.error(str(error))
