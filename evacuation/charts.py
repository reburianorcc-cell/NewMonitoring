import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

NAVY = "#073b76"
TEAL = "#12a4ae"


def occupancy_chart(df):
    data = df.nlargest(12, "Capacity Numeric").sort_values("Capacity Numeric")
    fig = go.Figure()
    fig.add_bar(y=data["Name"], x=data["Actual No. of Evacuees"], name="Occupied", orientation="h", marker_color=NAVY)
    fig.add_bar(y=data["Name"], x=data["Available Capacity"], name="Available", orientation="h", marker_color="#dce3ec")
    fig.update_layout(barmode="stack", height=410, margin=dict(l=10, r=10, t=25, b=10), legend=dict(orientation="h", y=1.08), xaxis_title="Number of persons", yaxis_title="")
    return fig


def profile_chart(profile):
    data = pd.DataFrame({"Group": profile.keys(), "People": profile.values()})
    fig = px.pie(data, names="Group", values="People", hole=.62, color_discrete_sequence=[NAVY, TEAL, "#8567c7", "#68a6db", "#d95682"])
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=20, b=10), legend=dict(orientation="h", y=-.12))
    return fig


def center_type_chart(df):
    col = "Type of Evacuation Center"
    values = df[col].fillna("Not specified").replace("", "Not specified").value_counts().reset_index()
    values.columns = ["Type", "Centers"]
    fig = px.bar(values, x="Type", y="Centers", color="Type", color_discrete_sequence=[NAVY, TEAL, "#f59e0b"])
    fig.update_layout(height=330, showlegend=False, margin=dict(l=10, r=10, t=20, b=10))
    return fig

