import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

try:
    from .config import AVERAGE_HECTARE_BENCHMARK, COLORS, LAND_USE_ORDER
except ImportError:
    from config import AVERAGE_HECTARE_BENCHMARK, COLORS, LAND_USE_ORDER


def land_use_pie(master):
    grouped = master.groupby("Category", as_index=False)["Total Area"].sum()
    grouped["Category"] = pd.Categorical(grouped["Category"], LAND_USE_ORDER, ordered=True)
    grouped = grouped.sort_values("Category")
    fig = px.pie(
        grouped,
        names="Category",
        values="Total Area",
        hole=.60,
        color="Category",
        color_discrete_map=COLORS,
    )
    fig.update_traces(
        textinfo="percent",
        textposition="inside",
        insidetextorientation="horizontal",
        hovertemplate="%{label}<br>%{percent}<br>%{value:,.2f} ha<extra></extra>",
    )
    fig.update_layout(height=390, margin=dict(l=10, r=10, t=20, b=35), legend=dict(orientation="h", y=-.08))
    fig.update_layout(
        height=410,
        margin=dict(l=10, r=185, t=20, b=20),
        legend=dict(orientation="v", x=1.02, y=.5, xanchor="left", yanchor="middle"),
    )
    return fig


def development_chart(master):
    developed = master["Overall Developed Area"].max() if "Overall Developed Area" in master else master["Developed Area"].sum()
    remaining = master["Overall Still to Be Developed"].max() if "Overall Still to Be Developed" in master else master["Still to Be Developed"].sum()
    totals = pd.DataFrame({
        "Status": ["Developed", "Still to Be Developed"],
        "Area": [developed, remaining],
    })
    fig = px.pie(
        totals, names="Status", values="Area", hole=.60, color="Status",
        color_discrete_map={"Developed": "#2563eb", "Still to Be Developed": "#f59e0b"},
    )
    fig.update_traces(
        textinfo="percent",
        textposition="inside",
        hovertemplate="%{label}<br>%{percent}<br>%{value:,.2f} ha<extra></extra>",
    )
    fig.update_layout(
        height=410,
        margin=dict(l=10, r=185, t=20, b=20),
        legend=dict(orientation="v", x=1.02, y=.5, xanchor="left", yanchor="middle"),
    )
    return fig


def locational_timeline(records):
    data = records.dropna(subset=["Date Applied"]).copy()
    if data.empty:
        return go.Figure().update_layout(title="No dated locational-clearance records")
    data["Month"] = data["Date Applied"].dt.to_period("M").astype(str)
    monthly = data.groupby("Month", as_index=False)["Area (ha)"].sum().rename(columns={"Area (ha)": "Actual Usage"})
    monthly["Average Benchmark"] = AVERAGE_HECTARE_BENCHMARK
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Average Benchmark"], name="Average Benchmark",
        mode="lines", line=dict(color="#f97316", width=3, dash="dash"),
        hovertemplate="%{x}<br>Average benchmark: %{y:,.2f} ha<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Actual Usage"], name="Actual Usage",
        mode="lines+markers", line=dict(color="#1d4ed8", width=3.5, shape="spline"),
        marker=dict(size=9, color="#ffffff", line=dict(color="#1d4ed8", width=3)),
        fill="tozeroy", fillcolor="rgba(37,99,235,.28)",
        hovertemplate="%{x}<br>Actual usage: %{y:,.2f} ha<extra></extra>",
    ))
    fig.update_layout(
        height=380, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Month", yaxis_title="Area used (ha)", hovermode="x unified",
        legend=dict(orientation="h", y=1.12),
    )
    return fig


def reclassification_by_year(records):
    start_year = 2025
    end_year = 2035
    data = records.copy()

    if data.empty:
        return go.Figure().update_layout(height=500, title="No reclassification records available")
    else:
        approved = pd.to_datetime(
            data.get("Date Approved", pd.Series(pd.NaT, index=data.index)),
            errors="coerce",
        )
        applied = pd.to_datetime(
            data.get("Date Applied", pd.Series(pd.NaT, index=data.index)),
            errors="coerce",
        )
        data["Reference Date"] = approved.fillna(applied)
        data["Area (ha)"] = pd.to_numeric(data["Area (ha)"], errors="coerce").fillna(0)
        data["Number of Planning Years"] = pd.to_numeric(
            data.get("Number of Planning Years", pd.Series(0, index=data.index)),
            errors="coerce",
        ).fillna(0)
        data = data.dropna(subset=["Reference Date"])
        data["Year"] = data["Reference Date"].dt.year
        data = data[data["Year"].between(start_year, end_year)]
        if data.empty:
            return go.Figure().update_layout(height=500, title="No active reclassification years")
        yearly = (
            data.groupby("Year")
            .agg(
                **{
                    "Area (ha)": ("Area (ha)", "sum"),
                    "Average Planning Duration": (
                        "Number of Planning Years",
                        lambda values: values[values > 0].mean() if (values > 0).any() else 0,
                    ),
                }
            )
            .rename_axis("Year")
            .reset_index()
            .sort_values("Year")
        )

    duration_data = yearly[yearly["Average Planning Duration"] > 0]
    planning_duration = (
        float(duration_data["Average Planning Duration"].max()) if not duration_data.empty else 0
    )

    yearly["Label"] = yearly["Area (ha)"].apply(
        lambda value: f"{value:,.2f} ha" if value > 0 else ""
    )

    active_years = yearly["Year"].astype(int).tolist()
    fig = go.Figure()
    fig.add_bar(
        x=yearly["Year"],
        y=yearly["Area (ha)"],
        name="Reclassified Area (ha)",
        text=yearly["Label"],
        textposition="outside",
        width=.55,
        marker=dict(color="#1e3a8a", line=dict(color="#172554", width=1.2)),
        hovertemplate="Year: %{x}<br>Reclassified area: %{y:,.2f} ha<extra></extra>",
    )
    if planning_duration:
        fig.add_trace(go.Scatter(
            x=duration_data["Year"],
            y=duration_data["Average Planning Duration"],
            name="Average Planning Duration",
            mode="lines+markers+text",
            yaxis="y2",
            line=dict(color="#f97316", width=3.5),
            marker=dict(size=10, color="#ffffff", line=dict(color="#f97316", width=3)),
            text=duration_data["Average Planning Duration"].map(lambda value: f"{value:.1f} years"),
            textposition="top center",
            hovertemplate="Application year: %{x}<br>Average duration: %{y:.1f} years<extra></extra>",
        ))
    fig.update_layout(
        height=520,
        margin=dict(l=20, r=25, t=65, b=25),
        showlegend=bool(planning_duration),
        barmode="group",
        bargap=.32,
        hovermode="x unified",
        font=dict(size=14),
        xaxis=dict(title="Year", tickmode="array", tickvals=active_years),
        yaxis=dict(title="Reclassified Area (hectares)", rangemode="tozero"),
        yaxis2=dict(
            title="Average Planning Duration (years)",
            rangemode="tozero",
            overlaying="y",
            side="right",
            showgrid=False,
            range=[0, max(12, planning_duration * 1.25)] if planning_duration else None,
        ),
        legend=dict(orientation="h", y=1.10, x=.5, xanchor="center"),
    )
    return fig


def reclassification_date_applied_graph(records):
    """Show monthly application count and applied hectares in one chart."""
    data = records.copy()
    if "Date Applied" not in data.columns:
        return go.Figure().update_layout(height=480, title="No Date Applied column found")

    data["Date Applied"] = pd.to_datetime(data["Date Applied"], errors="coerce")
    data["Area (ha)"] = pd.to_numeric(
        data.get("Area (ha)", pd.Series(0, index=data.index)), errors="coerce"
    ).fillna(0)
    data = data.dropna(subset=["Date Applied"])
    if data.empty:
        return go.Figure().update_layout(height=480, title="No dated reclassification applications")

    data["Month"] = data["Date Applied"].dt.to_period("M")
    monthly = (
        data.groupby("Month")
        .agg(Applications=("Date Applied", "size"), **{"Applied Area (ha)": ("Area (ha)", "sum")})
        .reset_index()
        .sort_values("Month")
    )
    monthly["Month Label"] = monthly["Month"].astype(str).map(
        lambda value: pd.Period(value, freq="M").strftime("%b %Y")
    )

    fig = go.Figure()
    fig.add_bar(
        x=monthly["Month Label"], y=monthly["Applications"], name="Applications Count",
        marker=dict(color="#22a9df", line=dict(color="#1588b5", width=1)),
        text=monthly["Applications"], textposition="outside",
        hovertemplate="Active month: %{x}<br>Applications: %{y:,.0f}<extra></extra>",
    )
    fig.add_trace(go.Scatter(
        x=monthly["Month Label"], y=monthly["Applied Area (ha)"], name="Applied Area (ha)",
        mode="lines+markers+text", yaxis="y2",
        line=dict(color="#ef6b67", width=3),
        marker=dict(size=10, color="#ffffff", line=dict(color="#ef6b67", width=3)),
        text=monthly["Applied Area (ha)"].map(lambda value: f"{value:,.2f} ha"),
        textposition="top center",
        hovertemplate="Active month: %{x}<br>Applied area: %{y:,.2f} ha<extra></extra>",
    ))
    fig.update_layout(
        height=520, margin=dict(l=20, r=20, t=60, b=30), bargap=.22,
        hovermode="x unified", font=dict(size=14),
        xaxis=dict(title="Active Application Month", type="category", categoryorder="array", categoryarray=monthly["Month Label"].tolist()),
        yaxis=dict(title="Number of Applications", rangemode="tozero", dtick=1),
        yaxis2=dict(title="Applied Area (hectares)", rangemode="tozero", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h", y=1.10, x=.5, xanchor="center"),
    )
    return fig


def application_status_chart(records, approved_column):
    data = records.copy()
    approved = pd.to_datetime(
        data.get(approved_column, pd.Series(pd.NaT, index=data.index)), errors="coerce"
    )
    completed_label = "Issued" if approved_column == "Date Issued" else "Approved"
    data["Status"] = approved.notna().map({True: completed_label, False: "Pending"})
    summary = data["Status"].value_counts().rename_axis("Status").reset_index(name="Applications")
    fig = px.bar(
        summary, x="Status", y="Applications", color="Status", text="Applications",
        color_discrete_map={"Issued": "#16a34a", "Approved": "#16a34a", "Pending": "#f59e0b"},
    )
    fig.update_traces(textposition="outside", hovertemplate="%{x}<br>%{y} applications<extra></extra>")
    fig.update_layout(height=360, margin=dict(l=15, r=15, t=25, b=15), showlegend=False)
    return fig


def processing_time_chart(records, completed_column):
    data = records.copy()
    data["Date Applied"] = pd.to_datetime(data.get("Date Applied"), errors="coerce")
    data[completed_column] = pd.to_datetime(data.get(completed_column), errors="coerce")
    data = data.dropna(subset=["Date Applied", completed_column])
    if data.empty:
        return go.Figure().update_layout(height=380, title="No completed applications with valid dates")
    data["Processing Days"] = (data[completed_column] - data["Date Applied"]).dt.days.clip(lower=0)
    data["Application Month"] = data["Date Applied"].dt.to_period("M").astype(str)
    monthly = data.groupby("Application Month", as_index=False)["Processing Days"].mean()
    monthly["Smoothed Days"] = monthly["Processing Days"].rolling(
        window=3, min_periods=1, center=True
    ).median()
    fig = go.Figure(go.Scatter(
        x=monthly["Application Month"],
        y=monthly["Smoothed Days"],
        customdata=monthly[["Processing Days"]],
        mode="lines+markers+text",
        text=monthly["Smoothed Days"].map(lambda value: f"{value:.1f}"),
        textposition="top center",
        name="Smoothed Processing Trend",
        line=dict(color="#0f766e", width=3.5, shape="spline"),
        marker=dict(size=9, color="#ffffff", line=dict(color="#0f766e", width=3)),
        hovertemplate=(
            "%{x}<br>Smoothed trend: %{y:.1f} days"
            "<br>Raw monthly average: %{customdata[0]:.1f} days<extra></extra>"
        ),
    ))
    fig.update_layout(
        height=380, margin=dict(l=15, r=15, t=25, b=15),
        xaxis_title="Application Month",
        yaxis=dict(title="Days", side="right", rangemode="tozero"),
        showlegend=False,
    )
    return fig
