import pandas as pd
import json
import re
import streamlit as st
from pathlib import Path
from urllib.parse import quote_plus
from .charts import occupancy_chart, profile_chart, center_type_chart
from .config import GALLERY_DIR
from .dashboard_store import get_gallery_image_url
from .map_view import create_map
from .metrics import dashboard_metrics, profile_metrics


def overview(df):
    total, active, evacuees, available, critical = dashboard_metrics(df)
    cols = st.columns(5)
    for col, label, value, help_text in zip(cols,
        ["🏢 Total Centers", "✅ Active Centers", "👥 Total Evacuees", "🟦 Available Capacity", "⚠️ Critical Alerts"],
        [total, active, f"{evacuees:,}", f"{available:,}", critical],
        ["All registered centers", "Centers with evacuees", "Across all centers", "Unoccupied person slots", "At or over capacity"]):
        col.metric(label, value, help=help_text)
    st.write("")
    left, right = st.columns([1.05, 1])
    with left:
        st.subheader("Center Occupancy")
        st.plotly_chart(occupancy_chart(df), use_container_width=True)
    with right:
        st.subheader("Evacuation Centers Map")
        deck = create_map(df)
        if deck: st.pydeck_chart(deck, use_container_width=True, height=410)
        else: st.info("No valid coordinates are available.")
    left, right = st.columns([1, 1])
    with left:
        st.subheader("Evacuee Profile")
        st.plotly_chart(profile_chart(profile_metrics(df)), use_container_width=True)
    with right:
        st.subheader("Center Types")
        st.plotly_chart(center_type_chart(df), use_container_width=True)
    st.subheader("Centers Requiring Attention")
    attention = df[df["Occupancy Rate"] >= 80][["Name", "Address", "Actual No. of Evacuees", "Capacity", "Occupancy Rate", "Status"]].copy()
    attention["Occupancy Rate"] = attention["Occupancy Rate"].map(lambda x: f"{x:.1f}%")
    st.dataframe(attention, use_container_width=True, hide_index=True)


def centers_view(df):
    st.subheader("Evacuation Centers")
    status = st.multiselect("Status", sorted(df["Status"].astype(str).unique()), default=[])
    shown = df[df["Status"].astype(str).isin(status)] if status else df
    columns = ["Name", "Address", "Capacity", "Actual No. of Evacuees", "Available Capacity", "Occupancy Rate", "Status", "Contact Number"]
    table = shown[columns].copy()
    table["Occupancy Rate"] = table["Occupancy Rate"].map(lambda x: f"{x:.1f}%")
    def directions_url(row):
        latitude = pd.to_numeric(row.get("latitude"), errors="coerce")
        longitude = pd.to_numeric(row.get("longitude"), errors="coerce")
        if pd.notna(latitude) and pd.notna(longitude):
            destination = f"{latitude:.7f},{longitude:.7f}"
        else:
            destination = str(row.get("Address", "")).strip()
        if not destination or destination == "No address provided":
            return None
        return (
            "https://www.google.com/maps/dir/?api=1"
            f"&destination={quote_plus(destination)}"
            "&travelmode=driving&dir_action=navigate"
        )

    table["Directions"] = shown.apply(directions_url, axis=1)
    st.caption("Select Open Google Maps to get directions from your current location.")
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Directions": st.column_config.LinkColumn(
                "Directions",
                display_text="Open Google Maps",
                help="Open driving directions from your current location.",
            )
        },
    )
    st.download_button("⬇️ Download filtered CSV", shown.to_csv(index=False).encode(), "evacuation_centers_filtered.csv", "text/csv")


def evacuees_view(df):
    st.subheader("Evacuee Summary")
    st.plotly_chart(profile_chart(profile_metrics(df)), use_container_width=True)
    st.dataframe(df[["Name", "Actual No. of Evacuees", "No. of Male", "No. of Female", "Senior Citizens", "No. of PWD"]], use_container_width=True, hide_index=True)


def _image_sources(value):
    if pd.isna(value) or not str(value).strip():
        return []
    sources = re.split(r"\s*(?:\||\n|;)\s*", str(value).strip())
    resolved = []
    for source in filter(None, sources):
        if source.startswith("supabase://"):
            resolved.append(get_gallery_image_url(source))
        elif source.startswith(("http://", "https://", "data:image/")):
            resolved.append(source)
        else:
            safe_parts = [part for part in Path(source).parts if part not in ("..", ".")]
            local = GALLERY_DIR.joinpath(*safe_parts)
            if local.exists():
                resolved.append(str(local))
    return resolved


def gallery_view(df):
    st.subheader("Evacuation Center Gallery")
    st.caption("Photos are loaded from image links/file names in CSV or Excel, including embedded XLSX pictures.")
    search = st.text_input("Search center or address", placeholder="Type an evacuation center name...")
    records = df.copy()
    if search:
        mask = records["Name"].str.contains(search, case=False, na=False) | records["Address"].str.contains(search, case=False, na=False)
        records = records[mask]
    items = []
    for _, row in records.iterrows():
        metadata_by_file = {}
        raw_metadata = row.get("Gallery Metadata", "")
        if pd.notna(raw_metadata) and str(raw_metadata).strip():
            try:
                metadata_by_file = {item.get("filename"): item for item in json.loads(raw_metadata)}
            except (TypeError, json.JSONDecodeError):
                metadata_by_file = {}
        for source in _image_sources(row.get("Gallery Image", "")):
            items.append((row, source, metadata_by_file.get(Path(source).name, {})))
    if not items:
        st.info("No gallery photos were found. Add a Photo, Image, Gallery, or Gallery Album column containing an image URL/file name, or upload an XLSX file with embedded pictures.")
        return
    for start in range(0, len(items), 3):
        columns = st.columns(3)
        for column, (row, source, details) in zip(columns, items[start:start + 3]):
            with column:
                st.image(source, use_container_width=True)
                st.markdown(f"**{row['Name']}**")
                st.caption(row["Address"])
                st.write(f"Evacuees: {int(row['Actual No. of Evacuees']):,} · Capacity: {row['Capacity']}")
                if details.get("photo_no"):
                    st.caption(f"Photo No.: {details['photo_no']}")
                if details.get("title"):
                    st.write(f"**Photo details:** {details['title']}")
                if details.get("date"):
                    st.caption(f"Photo date: {details['date']}")


def placeholder_view(title):
    st.subheader(title)
    st.info(f"The uploaded sample has no {title.lower()} columns yet. Add those fields to a future CSV/Excel template to activate this module.")
