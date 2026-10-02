"""CLUP module embedded in the authenticated SOCOCA Monitoring Portal."""
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

try:
    # Package mode: imported by the SOCOCA Monitoring Portal.
    from .config import APP_TITLE
    from .dashboard_store import delete_dashboard, list_dashboards, load_history, save_dashboard, supabase_configured
    from .data_loader import load_all, load_sococa_exports, parse_table_upload
    from .views import locational_clearance, overview, reclassification
    from .shapefile_map import boundary_names, municipality_barangay_map, parse_shapefile_files
except ImportError:
    # Standalone mode: streamlit run app.py
    from config import APP_TITLE
    from dashboard_store import delete_dashboard, list_dashboards, load_history, save_dashboard, supabase_configured
    from data_loader import load_all, load_sococa_exports, parse_table_upload
    from views import locational_clearance, overview, reclassification
    from shapefile_map import boundary_names, municipality_barangay_map, parse_shapefile_files

try:
    from evacuation.styles import apply_styles
except ImportError:
    try:
        from .styles import apply_styles
    except ImportError:
        from styles import apply_styles

apply_styles()

LAND_DISPUTE_COLUMNS = [
    "Case ID", "Municipality", "Barangay", "Dispute Type", "Area (ha)",
    "Date Filed", "Status", "Complainant", "Respondent", "Notes",
]


def empty_land_disputes():
    return pd.DataFrame(columns=LAND_DISPUTE_COLUMNS)


def parse_land_disputes(uploaded_file):
    uploaded_file.seek(0)
    frame = pd.read_csv(uploaded_file) if Path(uploaded_file.name).suffix.lower() == ".csv" else pd.read_excel(uploaded_file, engine="openpyxl")
    aliases = {column.casefold().strip(): column for column in LAND_DISPUTE_COLUMNS}
    frame = frame.rename(columns={column: aliases.get(str(column).casefold().strip(), str(column).strip()) for column in frame.columns})
    for column in LAND_DISPUTE_COLUMNS:
        if column not in frame:
            frame[column] = pd.NA
    frame = frame[LAND_DISPUTE_COLUMNS].copy()
    frame["Area (ha)"] = pd.to_numeric(frame["Area (ha)"], errors="coerce").fillna(0)
    frame["Date Filed"] = pd.to_datetime(frame["Date Filed"], errors="coerce")
    frame["Status"] = frame["Status"].fillna("Unspecified").astype(str).replace("", "Unspecified")
    return frame

if not st.session_state.get("admin_authenticated"):
    st.error("Please sign in through the SOCOCA Monitoring Portal.")
    st.stop()
if not supabase_configured():
    st.error("Supabase is not configured for CLUP Monitoring.")
    st.info("Use the same [supabase] URL and secret/service key configured for the Incident Dashboard.")
    st.stop()

username = st.session_state.get("admin_username") or "unknown"
role = st.session_state.get("admin_role") or "operator"
assigned_dashboard = st.session_state.get("assigned_dashboard")

try:
    dashboards = list_dashboards(username, role, assigned_dashboard)
except Exception as error:
    st.error(f"Unable to load CLUP dashboard data: {error}")
    st.stop()

def go(page_name):
    st.session_state.clup_page = page_name

with st.sidebar:
    pages = [
        ("Overview", ":material/home:"),
        ("Locational Clearance", ":material/location_on:"),
        ("Land-Use Reclassification", ":material/swap_horiz:"),
        ("Boundary Disputes", ":material/gavel:"),
        ("Municipality Map", ":material/map:"),
        ("Documents", ":material/picture_as_pdf:"),
        ("Data Upload", ":material/cloud_upload:"),
    ]
    if st.session_state.get("clup_page") not in [item[0] for item in pages]:
        st.session_state.clup_page = "Overview"
    for name, icon in pages:
        st.button(name, icon=icon, use_container_width=True, type="primary" if st.session_state.clup_page == name else "secondary", on_click=go, args=(name,), key=f"nav_clup_{name.casefold().replace(' ', '_').replace('-', '_')}")

page = st.session_state.clup_page
title_col, selector_col = st.columns([1.7, 1])
selected_dashboard = None
if dashboards:
    names = sorted(dashboards)
    current = st.session_state.get("clup_selected_dashboard")
    with selector_col:
        selected_dashboard = st.selectbox("📊 Selected dashboard", names, index=names.index(current) if current in names else 0, key="clup_dashboard_selector")
        st.session_state.clup_selected_dashboard = selected_dashboard
        st.caption(f"Source: {dashboards[selected_dashboard]['source_name']}")
elif role == "operator":
    st.warning("Your assigned dashboard has no CLUP data yet. Open Data Upload to add it.")

display_location = "CLUP"
display_region = "PLANNING & DEVELOPMENT"
if selected_dashboard:
    selected_master = dashboards[selected_dashboard].get("master")
    if selected_master is not None and not selected_master.empty:
        if "Province" in selected_master:
            provinces = selected_master["Province"].dropna().astype(str).str.strip()
            provinces = provinces[provinces.ne("")]
            if not provinces.empty:
                display_location = provinces.iloc[0]
        if display_location == "CLUP" and "Municipality" in selected_master:
            municipalities = selected_master["Municipality"].dropna().astype(str).str.strip()
            municipalities = municipalities[municipalities.ne("")]
            if not municipalities.empty:
                display_location = municipalities.iloc[0]
        if "Region" in selected_master:
            regions = selected_master["Region"].dropna().astype(str).str.strip()
            regions = regions[regions.ne("")]
            if not regions.empty:
                display_region = f"{regions.iloc[0]} · PLANNING & DEVELOPMENT"

with title_col:
    heading = f"{display_location} CLUP Monitoring Dashboard" if display_location != "CLUP" else APP_TITLE
    st.markdown(
        f"<div class='page-heading'><span class='eyebrow'>{display_region}</span>"
        f"<h1>{heading}</h1><p>Monitor approved land-use areas, locational clearances "
        f"and land-use reclassification activity for {display_location}.</p></div>",
        unsafe_allow_html=True,
    )

def require_dashboard():
    if not selected_dashboard:
        st.info("No CLUP dashboard data is stored yet. Open **Data Upload** to add the first workbook.")
        st.stop()
    return dashboards[selected_dashboard]

if page == "Overview":
    dashboard = require_dashboard()
    master = dashboard["master"]
    municipalities = sorted(master["Municipality"].dropna().astype(str).unique()) if "Municipality" in master else []
    municipality = st.selectbox("🏛️ Municipality", ["All Municipalities"] + municipalities, key="clup_municipality")
    filtered = master if municipality == "All Municipalities" else master[master["Municipality"] == municipality]
    overview(filtered, dashboard["reclassification"])
elif page == "Locational Clearance":
    locational_clearance(require_dashboard()["locational"])
elif page == "Land-Use Reclassification":
    dashboard = require_dashboard()
    reclassification(dashboard["reclassification"], dashboard["master"])
elif page == "Boundary Disputes":
    dashboard = require_dashboard()
    disputes = dashboard.get("land_disputes", empty_land_disputes()).copy()
    st.subheader("Boundary Disputes")
    st.caption("Monitor reported boundary disputes by municipality, barangay, type and status.")
    if disputes.empty:
        st.info("No boundary-dispute records are available. Upload records from Data Upload.")
    else:
        municipality_options = sorted(disputes["Municipality"].dropna().astype(str).unique())
        selected_municipality = st.selectbox("Municipality", ["All Municipalities"] + municipality_options, key="clup_dispute_municipality")
        filtered = disputes if selected_municipality == "All Municipalities" else disputes[disputes["Municipality"] == selected_municipality]
        barangay_options = sorted(filtered["Barangay"].dropna().astype(str).unique())
        selected_barangay = st.selectbox("Barangay", ["All Barangays"] + barangay_options, key="clup_dispute_barangay")
        if selected_barangay != "All Barangays":
            filtered = filtered[filtered["Barangay"] == selected_barangay]
        metric_left, metric_middle, metric_right = st.columns(3)
        metric_left.metric("Total Cases", len(filtered))
        metric_middle.metric("Disputed Area", f"{pd.to_numeric(filtered['Area (ha)'], errors='coerce').fillna(0).sum():,.2f} ha")
        metric_right.metric("Municipalities", filtered["Municipality"].nunique())
        counts = filtered["Status"].fillna("Unspecified").value_counts().sort_values()
        figure = go.Figure(go.Bar(x=counts.values, y=counts.index, orientation="h", text=counts.values, textposition="outside", marker_color="#2563eb"))
        figure.update_layout(title="Dispute Cases by Status", showlegend=False, plot_bgcolor="white", xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        st.plotly_chart(figure, use_container_width=True, config={"displaylogo": False})
        st.dataframe(filtered, use_container_width=True, hide_index=True)
elif page == "Municipality Map":
    dashboard = require_dashboard()
    st.subheader("CLUP Municipality and Barangay Map")
    map_geojson = dashboard.get("map_geojson")
    municipality_field = dashboard.get("municipality_field")
    barangay_field = dashboard.get("barangay_field")
    if not map_geojson or not municipality_field or not barangay_field:
        st.info("No Shapefile is attached yet. Upload one from Data Upload.")
    else:
        municipalities = boundary_names(map_geojson, municipality_field)
        map_municipality = st.selectbox("Municipality", ["All Municipalities"] + municipalities, key="clup_map_municipality")
        features = map_geojson.get("features", [])
        scoped = features if map_municipality == "All Municipalities" else [feature for feature in features if str(feature.get("properties", {}).get(municipality_field, "")).strip() == map_municipality]
        barangays = sorted({str(feature.get("properties", {}).get(barangay_field, "")).strip() for feature in scoped if str(feature.get("properties", {}).get(barangay_field, "")).strip()})
        map_barangay = st.selectbox("Barangay", ["All Barangays"] + barangays, key="clup_map_barangay")
        st.plotly_chart(
            municipality_barangay_map(map_geojson, municipality_field, barangay_field, map_municipality, map_barangay, dashboard.get("map_legend_field")),
            use_container_width=True,
            config={"displaylogo": False, "scrollZoom": True},
        )
elif page == "Documents":
    dashboard = require_dashboard()
    documents = list(dashboard.get("documents", []))
    st.subheader("CLUP Document Library")
    if not documents:
        st.info("No PDF documents are available. Upload a PDF from Data Upload.")
    else:
        municipalities = sorted({document.get("municipality", "Unassigned") for document in documents})
        municipality = st.selectbox("Municipality", ["All Municipalities"] + municipalities, key="clup_document_municipality")
        filtered_documents = documents if municipality == "All Municipalities" else [document for document in documents if document.get("municipality") == municipality]
        labels = {f"{document.get('title')} — {document.get('municipality')}": document for document in filtered_documents}
        selected_document = labels[st.selectbox("PDF document", list(labels), key="clup_pdf_view_selection")]
        if selected_document.get("data"):
            pdf_viewer(input=selected_document["data"], width="100%", height=840, zoom_level="auto")
        else:
            st.info("The PDF content is unavailable.")
else:
    st.subheader("Upload CLUP Monitoring Data")
    st.caption("Operators can add or update only their assigned dashboard. Admins can manage all CLUP dashboards.")
    can_create = role in ("super_admin", "admin")
    export_tab, complete_tab, lc_tab, reclass_tab, dispute_tab, pdf_tab, map_tab, history_tab = st.tabs([
        "SOCOCA Export Files",
        "Combined CLUP Template",
        "Locational Clearance Records",
        "Land-Use Reclassification Records",
        "Boundary Dispute Records",
        "PDF Documents",
        "Municipality Shapefile",
        "Upload History",
    ])
    with export_tab:
        st.caption(
            "Upload the Spot CLUP XLSX, Zone Areas CSV, Locational Clearance CSV, "
            "and Land-Use Reclassification CSV from the same SOCOCA export."
        )
        export_dashboard_name = st.text_input(
            "Dashboard name",
            value=assigned_dashboard or "",
            disabled=role == "operator",
            max_chars=80,
            key="clup_exports_name",
        ).strip()
        spot_upload = st.file_uploader(
            "1. Spot CLUP Monitoring file",
            type=["xlsx", "csv"],
            key="clup_spot_export",
        )
        zone_upload = st.file_uploader(
            "2. Zone Areas Based from Approved",
            type=["csv", "xlsx"],
            key="clup_zone_export",
        )
        locational_upload = st.file_uploader(
            "3. Locational Clearance Records",
            type=["csv", "xlsx"],
            key="clup_locational_export",
        )
        reclassification_upload = st.file_uploader(
            "4. Land-Use Reclassification",
            type=["csv", "xlsx"],
            key="clup_reclassification_export",
        )
        export_files = [spot_upload, zone_upload, locational_upload, reclassification_upload]
        if all(export_files):
            try:
                master, locational, reclass = load_sococa_exports(*export_files)
                total = master["Overall Total Area"].max()
                developed = master["Overall Developed Area"].max()
                remaining = master["Overall Still to Be Developed"].max()
                st.success(
                    f"Validated {len(master)} zoning categories, {len(locational)} clearance "
                    f"records and {len(reclass)} reclassification records. Overall land: "
                    f"{total:,.2f} ha ({developed:,.2f} ha developed; {remaining:,.2f} ha remaining)."
                )
                export_allowed = can_create or bool(
                    assigned_dashboard
                    and export_dashboard_name.casefold() == assigned_dashboard.casefold()
                )
                confirm_exports = st.checkbox(
                    "I confirm that these four files belong to the same CLUP dashboard.",
                    key="clup_confirm_exports",
                )
                if st.button(
                    "Save SOCOCA CLUP exports",
                    type="primary",
                    disabled=not (confirm_exports and export_dashboard_name and export_allowed),
                    key="clup_save_exports",
                ):
                    source_names = ", ".join(file.name for file in export_files)
                    save_dashboard(
                        export_dashboard_name,
                        {
                            "master": master,
                            "locational": locational,
                            "reclassification": reclass,
                            "source_name": source_names,
                        },
                        username,
                        "SOCOCA CLUP Exports",
                    )
                    st.session_state.clup_selected_dashboard = export_dashboard_name
                    st.success(f"Dashboard '{export_dashboard_name}' saved successfully.")
                    st.rerun()
            except Exception as error:
                st.error(f"Unable to read the SOCOCA export files: {error}")
        elif any(export_files):
            st.info("Select all four SOCOCA export files to validate and save the CLUP dashboard.")
    with complete_tab:
        dashboard_name = st.text_input("Dashboard name", value=assigned_dashboard or "", disabled=role == "operator", max_chars=80, key="clup_complete_name").strip()
        complete = st.file_uploader(
            "Complete CLUP Excel or CSV file",
            type=["xlsx", "csv"],
            key="clup_complete_upload",
        )
        if complete:
            try:
                master, locational, reclass = load_all(complete)
                if master.empty:
                    raise ValueError(
                        "No valid CLUP zoning rows were found. Upload the complete CLUP template "
                        "as an XLSX file or as a CSV exported without removing its original columns."
                    )
                st.success(f"Validated {len(master)} zoning rows, {len(locational)} clearance records and {len(reclass)} reclassification records.")
                allowed = can_create or bool(assigned_dashboard and dashboard_name.casefold() == assigned_dashboard.casefold())
                confirm = st.checkbox("I confirm that I want to save this complete CLUP workbook.", key="clup_confirm_complete")
                if st.button("Save complete CLUP data", type="primary", disabled=not (confirm and dashboard_name and allowed), key="clup_save_complete"):
                    save_dashboard(dashboard_name, {"master": master, "locational": locational, "reclassification": reclass, "source_name": complete.name}, username, "Complete CLUP")
                    st.session_state.clup_selected_dashboard = dashboard_name
                    st.success(f"Dashboard '{dashboard_name}' saved successfully.")
                    st.rerun()
            except Exception as error:
                st.error(f"Unable to read the workbook: {error}")
    targets = sorted(dashboards)
    with lc_tab:
        if not targets:
            st.info("Upload a complete CLUP workbook first.")
        else:
            target = st.selectbox("Upload to dashboard", targets, key="clup_lc_target")
            upload = st.file_uploader(
                "Locational Clearance Records (Excel or CSV)",
                type=["xlsx", "csv"],
                key="clup_lc_upload",
            )
            if upload:
                try:
                    preview = parse_table_upload(upload, "locational")
                    if preview.empty:
                        raise ValueError("No valid locational-clearance records were found in the uploaded file.")
                    confirm = st.checkbox("I confirm replacement of the locational-clearance records.", key="clup_confirm_lc")
                    if st.button("Save locational-clearance records", type="primary", disabled=not confirm, key="clup_save_lc"):
                        updated = dict(dashboards[target]); updated["locational"] = preview; updated["source_name"] = upload.name
                        save_dashboard(target, updated, username, "Locational Clearance")
                        st.success("Locational-clearance records saved."); st.rerun()
                except Exception as error:
                    st.error(f"Unable to read the file: {error}")
    with reclass_tab:
        if not targets:
            st.info("Upload a complete CLUP workbook first.")
        else:
            target = st.selectbox("Upload to dashboard", targets, key="clup_reclass_target")
            upload = st.file_uploader(
                "Land-Use Reclassification Records (Excel or CSV)",
                type=["xlsx", "csv"],
                key="clup_reclass_upload",
            )
            if upload:
                try:
                    preview = parse_table_upload(upload, "reclassification")
                    if preview.empty:
                        raise ValueError("No valid land-use reclassification records were found in the uploaded file.")
                    confirm = st.checkbox("I confirm replacement of the reclassification records.", key="clup_confirm_reclass")
                    if st.button("Save reclassification records", type="primary", disabled=not confirm, key="clup_save_reclass"):
                        updated = dict(dashboards[target]); updated["reclassification"] = preview; updated["source_name"] = upload.name
                        save_dashboard(target, updated, username, "Land-Use Reclassification")
                        st.success("Reclassification records saved."); st.rerun()
                except Exception as error:
                    st.error(f"Unable to read the file: {error}")
    with dispute_tab:
        if not targets:
            st.info("Upload a complete CLUP dashboard first.")
        else:
            dispute_target = st.selectbox("Upload disputes to dashboard", targets, key="clup_dispute_target")
            dispute_template = pd.DataFrame(columns=LAND_DISPUTE_COLUMNS).to_csv(index=False).encode("utf-8")
            st.download_button("Download boundary-dispute CSV template", dispute_template, "Boundary_Dispute_Records_Template.csv", "text/csv")
            dispute_file = st.file_uploader("Boundary Dispute Records", type=["xlsx", "csv"], key="clup_dispute_upload")
            if dispute_file:
                try:
                    dispute_preview = parse_land_disputes(dispute_file)
                    st.dataframe(dispute_preview.head(15), use_container_width=True, hide_index=True)
                    confirm_dispute = st.checkbox("Confirm replacement of boundary-dispute records", key="clup_confirm_dispute")
                    if st.button("Save boundary-dispute records", type="primary", disabled=not confirm_dispute, key="clup_save_dispute"):
                        updated = dict(dashboards[dispute_target])
                        updated["land_disputes"] = dispute_preview
                        updated["source_name"] = dispute_file.name
                        save_dashboard(dispute_target, updated, username, "Boundary Disputes")
                        st.success("Boundary-dispute records saved successfully.")
                        st.rerun()
                except Exception as error:
                    st.error(f"Unable to read the boundary-dispute file: {error}")
            if role in ("super_admin", "admin") and not dashboards[dispute_target].get("land_disputes", empty_land_disputes()).empty:
                confirm_dispute_delete = st.checkbox("Delete all boundary-dispute records", key="clup_confirm_dispute_delete")
                if st.button("Delete boundary-dispute records", disabled=not confirm_dispute_delete, key="clup_delete_disputes"):
                    updated = dict(dashboards[dispute_target])
                    updated["land_disputes"] = empty_land_disputes()
                    save_dashboard(dispute_target, updated, username, "Deleted Boundary Disputes")
                    st.success("Boundary-dispute records deleted.")
                    st.rerun()
    with pdf_tab:
        if not targets:
            st.info("Upload a complete CLUP dashboard first.")
        else:
            pdf_target = st.selectbox("Upload documents to dashboard", targets, key="clup_pdf_target")
            pdf_dashboard = dashboards[pdf_target]
            documents = list(pdf_dashboard.get("documents", []))
            municipality_options = sorted(pdf_dashboard.get("master", pd.DataFrame()).get("Municipality", pd.Series(dtype=str)).dropna().astype(str).unique())
            document_municipality = st.selectbox("Municipality", ["Unassigned"] + municipality_options, key="clup_pdf_municipality")
            document_title = st.text_input("PDF title", key="clup_pdf_title").strip()
            pdf_files = st.file_uploader("Select PDF files", type=["pdf"], accept_multiple_files=True, key="clup_pdf_upload")
            if st.button("Upload PDF documents", type="primary", disabled=not pdf_files, key="clup_save_pdfs"):
                added = 0
                for pdf_file in pdf_files or []:
                    file_bytes = pdf_file.getvalue()
                    if not file_bytes.startswith(b"%PDF"):
                        continue
                    documents.append({
                        "id": uuid4().hex,
                        "title": document_title or Path(pdf_file.name).stem,
                        "file_name": pdf_file.name,
                        "municipality": document_municipality,
                        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "data": file_bytes,
                    })
                    added += 1
                updated = dict(pdf_dashboard)
                updated["documents"] = documents
                save_dashboard(pdf_target, updated, username, "PDF Documents")
                st.success(f"{added} PDF document(s) uploaded successfully.")
                st.rerun()
            if documents and role in ("super_admin", "admin"):
                document_labels = {f"{item['title']} — {item['file_name']}": item for item in documents}
                delete_label = st.selectbox("PDF to delete", list(document_labels), key="clup_pdf_delete")
                confirm_pdf_delete = st.checkbox("Confirm PDF deletion", key="clup_confirm_pdf_delete")
                if st.button("Delete selected PDF", disabled=not confirm_pdf_delete, key="clup_delete_pdf"):
                    selected_id = document_labels[delete_label]["id"]
                    updated = dict(pdf_dashboard)
                    updated["documents"] = [item for item in documents if item["id"] != selected_id]
                    save_dashboard(pdf_target, updated, username, "Deleted PDF")
                    st.success("PDF deleted successfully.")
                    st.rerun()
    with map_tab:
        if not targets:
            st.info("Upload a complete CLUP dashboard first.")
        else:
            map_target = st.selectbox("Upload map to dashboard", targets, key="clup_map_target")
            st.caption("Select matching .shp, .shx and .dbf files together. Include .prj and .cpg when available.")
            shape_files = st.file_uploader("Municipality and barangay Shapefile", type=["shp", "shx", "dbf", "prj", "cpg"], accept_multiple_files=True, key="clup_shape_upload")
            if shape_files:
                suffixes = {Path(item.name).suffix.lower() for item in shape_files}
                missing = {".shp", ".shx", ".dbf"} - suffixes
                if missing:
                    st.warning(f"Missing required files: {', '.join(sorted(missing))}")
                elif st.button("Upload and validate Shapefile", type="primary", key="clup_validate_shape"):
                    try:
                        geojson, fields, detected_municipality, detected_barangay, source_name = parse_shapefile_files(shape_files)
                        st.session_state.clup_shape_preview = (geojson, fields, detected_municipality, detected_barangay, source_name)
                        st.success("Shapefile validated successfully. Save the municipality map to add it to Upload History.")
                    except Exception as error:
                        st.error(f"Unable to upload Shapefile: {error}")
            preview = st.session_state.get("clup_shape_preview")
            if preview:
                geojson, fields, detected_municipality, detected_barangay, source_name = preview
                municipality_index = fields.index(detected_municipality) if detected_municipality in fields else 0
                municipality_field = st.selectbox("Municipality attribute", fields, index=municipality_index, key="clup_shape_municipality_field")
                barangay_options = [field for field in fields if field != municipality_field]
                barangay_index = barangay_options.index(detected_barangay) if detected_barangay in barangay_options else 0
                barangay_field = st.selectbox("Barangay attribute", barangay_options, index=barangay_index, key="clup_shape_barangay_field")
                legend_options = ["Automatic"] + fields
                legend_selection = st.selectbox("Legend/color attribute", legend_options, key="clup_shape_legend_field")
                legend_field = None if legend_selection == "Automatic" else legend_selection
                st.plotly_chart(municipality_barangay_map(geojson, municipality_field, barangay_field, legend_field=legend_field), use_container_width=True, config={"displaylogo": False})
                confirm_map = st.checkbox("Attach this Shapefile to the dashboard", key="clup_confirm_map")
                if st.button("Save municipality map", type="primary", disabled=not confirm_map, key="clup_save_map"):
                    updated = dict(dashboards[map_target])
                    updated.update({
                        "map_geojson": geojson,
                        "map_source": source_name,
                        "municipality_field": municipality_field,
                        "barangay_field": barangay_field,
                        "map_legend_field": legend_field,
                    })
                    save_dashboard(
                        map_target,
                        updated,
                        username,
                        "Municipality Map",
                        history_source_name=source_name,
                    )
                    st.session_state.pop("clup_shape_preview", None)
                    st.success(f"Municipality map '{source_name}' was saved and added to Upload History.")
                    st.rerun()
    with history_tab:
        if role not in ("super_admin", "admin"):
            st.info("Upload history and dashboard deletion are available to administrators.")
        else:
            history = load_history()
            st.dataframe(history, use_container_width=True, hide_index=True) if not history.empty else st.info("No upload history yet.")
            st.divider()
            st.subheader("Delete Dashboard Data")
            if targets:
                delete_target = st.selectbox("Dashboard to delete", targets, key="clup_delete_target")
                confirm_delete = st.checkbox(f"I confirm permanent deletion of '{delete_target}'.", key="clup_confirm_delete")
                if st.button("Delete selected dashboard", type="primary", icon=":material/delete_forever:", disabled=not confirm_delete, key="clup_delete"):
                    delete_dashboard(delete_target, username)
                    st.session_state.pop("clup_selected_dashboard", None)
                    st.success(f"Dashboard '{delete_target}' was deleted.")
                    st.rerun()
            else:
                st.info("There are no dashboards available to delete.")
