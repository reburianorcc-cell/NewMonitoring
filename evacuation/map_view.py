import pydeck as pdk

COLORS = {"Operational": [25, 160, 90], "Near Capacity": [245, 158, 11], "Over Capacity": [220, 38, 38], "Inactive": [107, 114, 128]}


def create_map(df):
    points = df.dropna(subset=["latitude", "longitude"]).copy()
    points["color"] = points["Status"].astype(str).map(COLORS).apply(lambda x: x or COLORS["Inactive"])
    if points.empty:
        return None
    view = pdk.ViewState(latitude=points.latitude.mean(), longitude=points.longitude.mean(), zoom=8.2, pitch=0)
    layer = pdk.Layer("ScatterplotLayer", points, get_position="[longitude, latitude]", get_fill_color="color", get_radius=550, pickable=True, stroked=True, get_line_color=[255, 255, 255])
    tooltip = {"html": "<b>{Name}</b><br>{Address}<br>Occupied: {Actual No. of Evacuees}<br>Capacity: {Capacity}<br>Status: {Status}"}
    return pdk.Deck(layers=[layer], initial_view_state=view, tooltip=tooltip, map_style="light")

