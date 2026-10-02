import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
    :root {--navy:#052e63;--blue:#0878e6;--cyan:#19b8c5;--ink:var(--text-color,#10213c);--muted:color-mix(in srgb,var(--text-color,#10213c) 62%,transparent);--line:color-mix(in srgb,var(--text-color,#10213c) 16%,transparent);--card:var(--secondary-background-color,#fff)}
    html, body, .stApp, input, button, textarea, select {font-family:"MS PGothic","Yu Gothic","Noto Sans JP",Arial,sans-serif}
    [data-testid="stIconMaterial"], .material-symbols-rounded, .material-symbols-outlined, span[class*="material-symbols"] {font-family:"Material Symbols Rounded","Material Symbols Outlined" !important;font-weight:normal !important;font-style:normal !important;line-height:1 !important;font-feature-settings:"liga" !important;-webkit-font-feature-settings:"liga" !important}
    .stApp {background:var(--background-color,#f6f8fc);color:var(--ink)}
    [data-testid="stSidebar"] {background:linear-gradient(165deg,#073d7b 0%,#032b5a 48%,#021d3d 100%);border-right:0;box-shadow:8px 0 30px #062b5514}
    [data-testid="stSidebar"] * { color:#fff; }
    .block-container {padding-top:1.6rem;max-width:1540px;padding-bottom:3rem}
    .brand {display:flex;align-items:center;gap:12px;font-size:.96rem;font-weight:800;letter-spacing:.04em;padding:1rem 0 1.8rem}
    .brand small {display:block;font-size:.72rem;font-weight:500;letter-spacing:.08em;opacity:.72;margin-top:3px}
    .brand-icon {display:grid;place-items:center;width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,#22c6d3,#1388ef);font-size:1.3rem;box-shadow:0 8px 20px #001d4055}
    .brand-copy {padding-top:1px}
    [data-testid="stSidebarUserContent"] > [data-testid="stVerticalBlock"] {gap:.45rem !important}
    [data-testid="stSidebar"] [class*="st-key-nav_"] {width:100% !important;margin:0 !important}
    [data-testid="stSidebar"] [class*="st-key-nav_"] .stButton {width:100% !important;margin:0 !important}
    [data-testid="stSidebar"] [class*="st-key-nav_"] button {display:flex !important;align-items:center !important;justify-content:flex-start !important;gap:.75rem !important;text-align:left !important;width:100% !important;min-height:46px;border-radius:11px !important;padding:10px 16px !important;margin:0 !important;font-weight:700;transition:all .2s ease}
    [data-testid="stSidebar"] [class*="st-key-nav_"] button > div {display:flex !important;align-items:center !important;justify-content:flex-start !important;width:100% !important;text-align:left !important}
    [data-testid="stSidebar"] [class*="st-key-nav_"] button p {width:100% !important;margin:0 !important;text-align:left !important;white-space:nowrap !important}
    [data-testid="stSidebar"] [class*="st-key-nav_"] button [data-testid="stIconMaterial"] {width:1.35rem !important;min-width:1.35rem !important;font-size:1.25rem !important;text-align:center !important}
    [data-testid="stSidebar"] [class*="st-key-nav_"] button[kind="secondary"] {background:transparent !important;border:1px solid transparent !important;color:#fff !important;box-shadow:none !important}
    [data-testid="stSidebar"] [class*="st-key-nav_"] button[kind="secondary"]:hover {background:#ffffff18 !important;transform:translateX(5px);border-color:#ffffff12 !important}
    [data-testid="stSidebar"] [class*="st-key-nav_"] button[kind="primary"] {background:linear-gradient(90deg,#108cf1,#0872d1) !important;color:#fff !important;border:1px solid #43a9ff55 !important;box-shadow:0 7px 18px #001b3b55;transform:none !important}
    [data-testid="stSidebar"] [class*="st-key-nav_"] button * {color:#fff !important}
    [data-testid="stSidebar"] .st-key-logout_button button {background:#ffffff14 !important;border:1px solid #ffffff30 !important;color:#fff !important;font-weight:700 !important}
    [data-testid="stSidebar"] .st-key-logout_button button * {color:#fff !important}
    [data-testid="stSidebar"] .st-key-logout_button button:hover {background:#dc2626 !important;border-color:#ef4444 !important}
    .page-heading .eyebrow {font-size:.7rem;font-weight:800;letter-spacing:.16em;color:#0878e6}
    .page-heading h1 {font-size:2rem;margin:.18rem 0 .25rem;color:var(--ink);letter-spacing:-.035em}
    .page-heading p {color:var(--muted);margin:0 0 1rem}
    div[data-testid="stMetric"] {background:var(--card);border:1px solid var(--line);border-left:4px solid #2563eb;border-radius:18px;padding:20px;box-shadow:0 8px 24px #0f172a0a;transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
    div[data-testid="stMetric"]:hover {transform:translateY(-5px);box-shadow:0 16px 35px #075aaa20;border-color:#b9dafb}
    div[data-testid="stMetricValue"] {color:var(--ink);font-weight:800}
    div[data-testid="stVerticalBlockBorderWrapper"] {background:var(--card);border:1px solid var(--line);border-radius:18px;box-shadow:0 8px 28px rgba(15,23,42,.04);overflow:hidden}
    /* A bordered container is already the chart card; remove Plotly's second box. */
    [data-testid="stPlotlyChart"] {overflow:hidden !important}
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPlotlyChart"] {background:transparent !important;border:0 !important;border-radius:0 !important;padding:0 !important;box-shadow:none !important;overflow:hidden !important}
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPlotlyChart"]:hover {transform:none !important;box-shadow:none !important}
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPlotlyChart"] > div {overflow:hidden !important}
    .js-plotly-plot .plotly .legendtext,
    .js-plotly-plot .plotly .legendtitletext,
    .js-plotly-plot .plotly .gtitle,
    .js-plotly-plot .plotly .xtitle,
    .js-plotly-plot .plotly .ytitle,
    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text,
    .js-plotly-plot .plotly .annotation-text,
    .js-plotly-plot .plotly .cbtitle text,
    .js-plotly-plot .plotly .colorbar text {fill:var(--text-color) !important;color:var(--text-color) !important}
    .section-title {margin:4px 0 2px;color:var(--ink);font-weight:750;font-size:1.15rem}
    .section-note { color:var(--muted); font-size:.88rem; margin-bottom:12px; }
    .empty {padding:42px 20px;text-align:center;background:var(--card);border:1px dashed var(--line);border-radius:18px;color:var(--muted)}
    .login-title {max-width:460px;margin:9vh auto 1rem;text-align:center;font-size:1.35rem;font-weight:850;letter-spacing:.08em;color:#073b76}
    [data-testid="stForm"] {max-width:460px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px;box-shadow:0 18px 50px #0f172a14}
    [class*="st-key-create_account_form"] [data-testid="stForm"],
    [class*="st-key-edit_account_form"] [data-testid="stForm"] {max-width:980px;margin:1.25rem auto;padding:30px 34px;border-top:4px solid #0878e6;box-shadow:0 14px 40px #0f172a12}
    [class*="st-key-create_account_form"] [data-testid="stForm"] h4,
    [class*="st-key-edit_account_form"] [data-testid="stForm"] h4 {color:#073b76;margin-bottom:.15rem}
    [class*="st-key-create_account_form"] [data-testid="stFormSubmitButton"],
    [class*="st-key-edit_account_form"] [data-testid="stFormSubmitButton"] {margin-top:.65rem}
    [class*="st-key-create_account_form"] [data-testid="stFormSubmitButton"] button,
    [class*="st-key-edit_account_form"] [data-testid="stFormSubmitButton"] button {min-width:210px;border-radius:10px;font-weight:750}
    @media (max-width: 700px) {
        .page-heading h1 {font-size:1.55rem;}
        [class*="st-key-create_account_form"] [data-testid="stForm"],
        [class*="st-key-edit_account_form"] [data-testid="stForm"] {padding:22px 18px;margin-top:.8rem}
        [class*="st-key-create_account_form"] [data-testid="stFormSubmitButton"] button,
        [class*="st-key-edit_account_form"] [data-testid="stFormSubmitButton"] button {width:100%;min-width:0}
    }
    @media (prefers-color-scheme: dark) {
        div[data-testid="stMetric"], div[data-testid="stVerticalBlockBorderWrapper"] {box-shadow:0 8px 28px rgba(0,0,0,.22)}
        [data-testid="stDataFrame"], [data-testid="stPlotlyChart"] {color-scheme:dark}
    }
    /* Match the fixed light Plotly theme used by Incident and Evacuation. */
    [data-testid="stPlotlyChart"] {background:#fff !important;border:0 !important;box-shadow:none !important;padding:0 !important;border-radius:18px !important;overflow:hidden !important;color-scheme:light}
    [data-testid="stPlotlyChart"] .modebar {display:none !important}
    [data-testid="stPlotlyChart"]:hover {box-shadow:none !important;transform:none !important}
    div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stPlotlyChart"]) {background:transparent !important;border:0 !important;box-shadow:none !important;overflow:hidden !important}
    .js-plotly-plot .plotly .legendtext,
    .js-plotly-plot .plotly .legendtitletext,
    .js-plotly-plot .plotly .gtitle,
    .js-plotly-plot .plotly .xtitle,
    .js-plotly-plot .plotly .ytitle,
    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text,
    .js-plotly-plot .plotly .annotation-text,
    .js-plotly-plot .plotly .cbtitle text,
    .js-plotly-plot .plotly .colorbar text {fill:#172033 !important;color:#172033 !important}
    </style>
    """, unsafe_allow_html=True)
