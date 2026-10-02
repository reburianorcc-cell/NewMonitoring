"""One fixed, readable Plotly renderer shared by every portal module."""
import streamlit as st


CHART_TEXT = "#172033"
CHART_GRID = "rgba(23,32,51,0.14)"
CHART_ZERO = "rgba(23,32,51,0.22)"


def render_plotly_chart(figure, **kwargs):
    """Render a light chart even when the surrounding Streamlit UI is dark."""
    figure.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color=CHART_TEXT, size=12),
        title_font=dict(color=CHART_TEXT),
        legend=dict(font=dict(color=CHART_TEXT), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(color=CHART_TEXT, gridcolor=CHART_GRID, zerolinecolor=CHART_ZERO),
        yaxis=dict(color=CHART_TEXT, gridcolor=CHART_GRID, zerolinecolor=CHART_ZERO),
    )
    kwargs["theme"] = None
    config = dict(kwargs.pop("config", {}) or {})
    config.update({"displayModeBar": False, "displaylogo": False})
    return st.plotly_chart(figure, config=config, **kwargs)
