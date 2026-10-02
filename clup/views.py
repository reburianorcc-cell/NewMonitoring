import pandas as pd
import streamlit as st

try:
    from portal_chart import render_plotly_chart
except ImportError:
    def render_plotly_chart(figure, **kwargs):
        return st.plotly_chart(figure, **kwargs)

try:
    from .charts import (
        application_status_chart, development_chart, land_use_pie,
        locational_timeline, processing_time_chart, reclassification_by_year,
        reclassification_date_applied_graph,
    )
    from .config import AVERAGE_HECTARE_BENCHMARK
except ImportError:
    from charts import (
        application_status_chart, development_chart, land_use_pie,
        locational_timeline, processing_time_chart, reclassification_by_year,
        reclassification_date_applied_graph,
    )
    from config import AVERAGE_HECTARE_BENCHMARK


def _title(title, note=""):
    st.markdown(f"<div class='section-title'>{title}</div><div class='section-note'>{note}</div>", unsafe_allow_html=True)


def overview(master, reclassification_records):
    total = master["Overall Total Area"].max() if "Overall Total Area" in master else master["Total Area"].sum()
    developed = master["Overall Developed Area"].max() if "Overall Developed Area" in master else master["Developed Area"].sum()
    remaining = master["Overall Still to Be Developed"].max() if "Overall Still to Be Developed" in master else master["Still to Be Developed"].sum()
    rate = developed / total * 100 if total else 0
    a, b, c, d = st.columns(4)
    developed_share = developed / total * 100 if total else 0
    remaining_share = remaining / total * 100 if total else 0
    a.metric("Total Area", f"{total:,.2f} ha", delta="Approved CLUP area", delta_color="off")
    b.metric("Developed Area", f"{developed:,.2f} ha", delta=f"{developed_share:.1f}% of total")
    c.metric("Still to Be Developed", f"{remaining:,.2f} ha", delta=f"{remaining_share:.1f}% remaining", delta_color="inverse")
    d.metric("Development Rate", f"{rate:.1f}%", delta=f"{rate:.1f}% completed")
    left, right = st.columns(2)
    with left, st.container(border=True):
        _title("Land-Use Distribution", "Settlement, production, infrastructure, protection and municipal water")
        render_plotly_chart(land_use_pie(master), use_container_width=True)
    with right, st.container(border=True):
        _title("Development Status", "Developed area compared with remaining development area")
        render_plotly_chart(development_chart(master), use_container_width=True)
    with st.container(border=True):
        _title(
            "Reclassification Applications",
            "Monthly applications by Date Applied, with the total applied area in hectares",
        )
        render_plotly_chart(
            reclassification_date_applied_graph(reclassification_records),
            use_container_width=True,
        )
    with st.container(border=True):
        _title("Area Breakdown", "Detailed totals from the approved zoning ordinance and zoning map")
        grouped = master.groupby("Category", as_index=False)[["Total Area", "Developed Area", "Still to Be Developed"]].sum()
        totals = pd.DataFrame([{
            "Category": "TOTAL",
            "Total Area": total,
            "Developed Area": developed,
            "Still to Be Developed": remaining,
        }])
        summary = pd.concat([grouped, totals], ignore_index=True)
        numeric_columns = ["Total Area", "Developed Area", "Still to Be Developed"]

        def shade_rows(row):
            if row["Category"] == "TOTAL":
                return ["background-color: #dbeafe; font-weight: 700"] * len(row)
            background = "#f8fafc" if row.name % 2 else "#ffffff"
            return [f"background-color: {background}"] * len(row)

        styled_summary = (
            summary.style
            .apply(shade_rows, axis=1)
            .format({column: "{:,.2f} ha" for column in numeric_columns})
            .set_properties(subset=numeric_columns, **{"text-align": "right"})
            .set_properties(subset=["Category"], **{"text-align": "left"})
            .set_table_styles([{"selector": "th", "props": [("font-weight", "700"), ("text-align", "center")]}])
        )
        st.dataframe(styled_summary, use_container_width=True, hide_index=True)


def locational_clearance(records):
    records = records.copy()
    records["Date Applied"] = pd.to_datetime(records.get("Date Applied"), errors="coerce")
    records["Date Issued"] = pd.to_datetime(records.get("Date Issued"), errors="coerce")
    records["Status"] = records["Date Issued"].notna().map({True: "Issued", False: "Pending"})
    records["Processing Days"] = (records["Date Issued"] - records["Date Applied"]).dt.days

    f1, f2, f3 = st.columns(3)
    zones = sorted(records["Zoning Classification"].dropna().astype(str).unique())
    zone = f1.selectbox("Zoning Classification", ["All"] + zones, key="lc_zone_filter")
    years = sorted(records["Date Applied"].dropna().dt.year.unique().astype(int))
    year = f2.selectbox("Application Year", ["All"] + years, key="lc_year_filter")
    status = f3.selectbox("Application Status", ["All", "Issued", "Pending"], key="lc_status_filter")
    if zone != "All": records = records[records["Zoning Classification"].astype(str) == zone]
    if year != "All": records = records[records["Date Applied"].dt.year == year]
    if status != "All": records = records[records["Status"] == status]

    total = records["Area (ha)"].sum() if "Area (ha)" in records else 0
    avg = records["Area (ha)"].mean() if len(records) else 0
    avg_days = records["Processing Days"].dropna().mean()
    a, b, c, d = st.columns(4)
    a.metric("Locational Clearances", f"{len(records):,}")
    b.metric("Total Clearance Area", f"{total:,.2f} ha")
    c.metric("Average per Record", f"{avg:,.2f} ha")
    d.metric("Average Processing", f"{avg_days:,.1f} days" if pd.notna(avg_days) else "—")
    with st.container(border=True):
        _title("Hectare Usage Timeline", f"Monthly actual usage compared with the {AVERAGE_HECTARE_BENCHMARK:,.0f}-hectare average benchmark")
        render_plotly_chart(locational_timeline(records), use_container_width=True)
    left, right = st.columns(2)
    with left, st.container(border=True):
        _title("Application Status", "Issued and pending locational clearances")
        render_plotly_chart(application_status_chart(records, "Date Issued"), use_container_width=True)
    with right, st.container(border=True):
        _title("Processing-Time Trend", "Average days from application to issuance")
        render_plotly_chart(processing_time_chart(records, "Date Issued"), use_container_width=True)
    with st.container(border=True):
        _title("Locational Clearance Records", "Zoning classification, area, remaining area and application date")
        table_records = records.copy()
        text_columns = ["Issued To", "Zoning Classification", "Status"]
        numeric_columns = ["Area (ha)", "Still to Be Developed (ha)", "Processing Days"]
        date_columns = ["Date Applied", "Date Issued"]
        for column in text_columns:
            table_records[column] = table_records[column].fillna("—").replace("", "—")
        for column in date_columns:
            table_records[column] = pd.to_datetime(table_records[column], errors="coerce").dt.strftime("%b %d, %Y").fillna("—")

        def style_clearance_rows(row):
            background = "#f8fafc" if row.name % 2 else "#ffffff"
            styles = [f"background-color: {background}"] * len(row)
            status_position = table_records.columns.get_loc("Status")
            if row["Status"] == "Issued":
                styles[status_position] += "; color: #166534; background-color: #dcfce7; font-weight: 700"
            elif row["Status"] == "Pending":
                styles[status_position] += "; color: #92400e; background-color: #fef3c7; font-weight: 700"
            return styles

        styled_records = (
            table_records.style
            .apply(style_clearance_rows, axis=1)
            .format({
                "Area (ha)": "{:,.3f}",
                "Still to Be Developed (ha)": "{:,.3f}",
                "Processing Days": lambda value: "—" if pd.isna(value) else f"{value:,.0f}",
            }, na_rep="—")
            .set_properties(subset=text_columns, **{"text-align": "left", "padding": "8px 12px"})
            .set_properties(subset=numeric_columns, **{"text-align": "right", "padding": "8px 12px"})
            .set_properties(subset=date_columns, **{"text-align": "center", "padding": "8px 12px"})
            .set_table_styles([{"selector": "th", "props": [("font-weight", "700"), ("text-align", "center"), ("padding", "10px 12px")]}])
        )
        st.dataframe(styled_records, use_container_width=True, hide_index=True, height=430)
        st.caption(f"Showing {len(table_records):,} locational-clearance record{'s' if len(table_records) != 1 else ''}.")


def reclassification(records, master):
    records = records.copy()
    records["Date Applied"] = pd.to_datetime(records.get("Date Applied"), errors="coerce")
    records["Date Approved"] = pd.to_datetime(records.get("Date Approved"), errors="coerce")
    records["Status"] = records["Date Approved"].notna().map({True: "Approved", False: "Pending"})
    records["Processing Days"] = (records["Date Approved"] - records["Date Applied"]).dt.days

    f1, f2, f3 = st.columns(3)
    classes = sorted(records["Reclassified To"].dropna().astype(str).unique())
    classification = f1.selectbox("Reclassified To", ["All"] + classes, key="rc_class_filter")
    available_years = sorted(records["Date Applied"].dropna().dt.year.unique().astype(int))
    selected_year = f2.selectbox("Application Year", ["All"] + available_years, key="rc_year_filter")
    selected_status = f3.selectbox("Application Status", ["All", "Approved", "Pending"], key="rc_status_filter")
    if classification != "All": records = records[records["Reclassified To"].astype(str) == classification]
    if selected_year != "All": records = records[records["Date Applied"].dt.year == selected_year]
    if selected_status != "All": records = records[records["Status"] == selected_status]

    total = records["Area (ha)"].sum() if "Area (ha)" in records else 0
    avg_days = records["Processing Days"].dropna().mean()
    planning_values = pd.to_numeric(
        records.get("Number of Planning Years", pd.Series(dtype=float)), errors="coerce"
    ).dropna()
    planning_values = planning_values[planning_values > 0]
    if planning_values.empty:
        planning_values = pd.to_numeric(
            master.get("Number of Planning Years", pd.Series(dtype=float)), errors="coerce"
        ).dropna()
    planning_years = int(planning_values.max()) if not planning_values.empty else 0
    a, b, c, d, e = st.columns(5)
    a.metric("Reclassification Records", f"{len(records):,}")
    b.metric("Total Reclassified Area", f"{total:,.2f} ha")
    years = pd.concat([records.get("Date Approved", pd.Series(dtype="datetime64[ns]")), records.get("Date Applied", pd.Series(dtype="datetime64[ns]"))]).dropna().dt.year
    c.metric("Years Covered", f"{years.min()}–{years.max()}" if not years.empty else "—")
    d.metric("Average Processing", f"{avg_days:,.1f} days" if pd.notna(avg_days) else "—")
    e.metric("Planning Years", f"{planning_years} years" if planning_years else "—")
    with st.container(border=True):
        _title("Reclassified Area vs. Planning Duration Over Time", "Active years with recorded land-use reclassification activity")
        render_plotly_chart(reclassification_by_year(records), use_container_width=True)
    left, right = st.columns(2)
    with left, st.container(border=True):
        _title("Application Status", "Approved and pending reclassification applications")
        render_plotly_chart(application_status_chart(records, "Date Approved"), use_container_width=True)
    with right, st.container(border=True):
        _title("Processing-Time Trend", "Average days from application to approval")
        render_plotly_chart(processing_time_chart(records, "Date Approved"), use_container_width=True)
    with st.container(border=True):
        _title("Land-Use Reclassification Records", "Applicant, new classification, area, dates and approving authority")
        st.dataframe(records, use_container_width=True, hide_index=True, column_config={"Area (ha)": st.column_config.NumberColumn(format="%.2f"), "Net Balance (ha)": st.column_config.NumberColumn(format="%.2f"), "Number of Planning Years": st.column_config.NumberColumn(format="%d years"), "Date Applied": st.column_config.DateColumn(format="MMM DD, YYYY"), "Date Approved": st.column_config.DateColumn(format="MMM DD, YYYY")})
