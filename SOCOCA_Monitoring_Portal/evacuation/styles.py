import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
    :root {--navy:#052e63;--blue:#0878e6;--cyan:#19b8c5;--ink:#10213c;--muted:#64748b;--line:#e5eaf1}
    html, body, .stApp, input, button, textarea, select {font-family:"MS PGothic","ＭＳ Ｐゴシック","MS Gothic","Yu Gothic","Noto Sans JP",Arial,sans-serif}
    /* Streamlit renders built-in icons as Material-symbol ligature text.
       Never allow the dashboard text font to override their icon font. */
    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    .material-symbols-outlined,
    span[class*="material-symbols"] {
        font-family:"Material Symbols Rounded","Material Symbols Outlined" !important;
        font-weight:normal !important;
        font-style:normal !important;
        font-size:inherit;
        line-height:1 !important;
        letter-spacing:normal !important;
        text-transform:none !important;
        white-space:nowrap !important;
        word-wrap:normal !important;
        direction:ltr !important;
        font-feature-settings:"liga" !important;
        -webkit-font-feature-settings:"liga" !important;
        -webkit-font-smoothing:antialiased !important;
    }
    [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"] {font-size:1.5rem !important;overflow:hidden;width:1.5rem}
    [data-testid="stSidebar"] [data-testid="stExpander"] summary [data-testid="stIconMaterial"] {font-size:1.25rem !important;flex:0 0 1.25rem;overflow:hidden;width:1.25rem}
    .stApp {background:radial-gradient(circle at 92% 2%,#e8f4ff 0,transparent 25%),#f6f8fc;color:var(--ink)}
    [data-testid="stSidebar"] {background:linear-gradient(165deg,#073d7b 0%,#032b5a 48%,#021d3d 100%);border-right:0;box-shadow:8px 0 30px #062b5514}
    [data-testid="stSidebar"] * {color:white}
    .block-container {padding-top:1.6rem;max-width:1540px;padding-bottom:3rem}
    div[data-testid="stMetric"] {background:linear-gradient(145deg,#fff,#fbfdff);border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 8px 24px #0f172a0a;transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
    div[data-testid="stMetric"]:hover {transform:translateY(-5px);box-shadow:0 16px 35px #075aaa20;border-color:#b9dafb}
    div[data-testid="stMetricValue"] {color:#073b76;font-weight:800}
    [data-testid="stPlotlyChart"], [data-testid="stPydeckChart"], [data-testid="stDataFrame"] {background:#fff;border:1px solid var(--line);border-radius:18px;padding:8px;box-shadow:0 8px 24px #0f172a0a;transition:box-shadow .22s ease,transform .22s ease}
    [data-testid="stPlotlyChart"]:hover, [data-testid="stPydeckChart"]:hover {box-shadow:0 15px 35px #0f172a14;transform:translateY(-2px)}
    .panel {background:white;border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:0 8px 24px #0f172a0a}
    .login-title {text-align:center;color:#073b76;font-size:2rem;font-weight:800;margin:12vh 0 2rem}
    .brand {display:flex;align-items:center;gap:12px;font-size:.96rem;font-weight:800;letter-spacing:.04em;padding:1rem 0 1.8rem}
    .brand small {display:block;font-size:.72rem;font-weight:500;letter-spacing:.08em;opacity:.72;margin-top:3px}
    .brand-icon {display:grid;place-items:center;width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,#22c6d3,#1388ef);font-size:1.3rem;box-shadow:0 8px 20px #001d4055}
    /* Sidebar navigation uses regular buttons, so no radio circles are rendered. */
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
    [data-testid="stSidebar"] [class*="st-key-open_login_dialog"] button {display:flex !important;align-items:center !important;justify-content:center !important;gap:.6rem !important;width:100% !important;min-height:45px;background:#ffffff12 !important;color:#fff !important;border:1px solid #ffffff24 !important;border-radius:11px !important;margin-bottom:.65rem !important}
    [data-testid="stSidebar"] [class*="st-key-open_login_dialog"] button:hover {background:#ffffff20 !important;border-color:#ffffff3d !important;transform:translateY(-2px)}
    [data-testid="stSidebar"] [class*="st-key-open_login_dialog"] button * {color:#fff !important}
    .stButton>button, .stDownloadButton>button {border-radius:11px;border:1px solid #cfe0f2;font-weight:700;transition:all .2s ease}
    .stButton>button:hover, .stDownloadButton>button:hover {transform:translateY(-2px);box-shadow:0 9px 20px #0878e62b;border-color:#0878e6}
    /* Dedicated logout style prevents white text on a white button. */
    [data-testid="stSidebar"] .st-key-sidebar_logout button,
    [data-testid="stSidebar"] [class*="st-key-sidebar_logout"] button {justify-content:center !important;text-align:center !important;background:linear-gradient(90deg,#e84b5f,#c92e46) !important;color:#fff !important;border:1px solid #ff8b9a55 !important;box-shadow:0 8px 20px #19081355}
    [data-testid="stSidebar"] .st-key-sidebar_logout button:hover,
    [data-testid="stSidebar"] [class*="st-key-sidebar_logout"] button:hover {background:linear-gradient(90deg,#f05a6d,#d43850) !important;color:#fff !important;transform:translateY(-2px)}
    [data-testid="stSidebar"] .st-key-sidebar_logout button *,
    [data-testid="stSidebar"] [class*="st-key-sidebar_logout"] button * {color:#fff !important}
    .page-heading .eyebrow {font-size:.7rem;font-weight:800;letter-spacing:.16em;color:#0878e6}
    .page-heading h1 {font-size:2rem;margin:.18rem 0 .25rem;color:#10213c;letter-spacing:-.035em}
    .page-heading p {color:var(--muted);margin:0 0 1rem}
    .dataset-card {display:flex;align-items:center;gap:12px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 16px;box-shadow:0 8px 24px #0f172a0b;margin-top:3px;transition:all .22s ease}
    .dataset-card:hover {transform:translateY(-3px);box-shadow:0 14px 30px #0878e61c;border-color:#bddcff}
    .dataset-card small {display:block;color:#7a8aa0;font-size:.66rem;font-weight:800;letter-spacing:.1em}
    .dataset-card strong {display:block;color:#173557;margin-top:3px;max-width:360px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
    .dataset-icon {display:grid;place-items:center;width:43px;height:43px;border-radius:12px;background:#eaf5ff;font-size:1.25rem}
    .live-dot {width:9px;height:9px;border-radius:50%;background:#20b26b;margin-left:auto;box-shadow:0 0 0 6px #20b26b18;animation:pulse 1.8s infinite}
    .idle-dot {width:9px;height:9px;border-radius:50%;background:#94a3b8;margin-left:auto;box-shadow:0 0 0 6px #94a3b818}
    .empty-state {background:#fff;border:1px dashed #bfd3e8;border-radius:22px;text-align:center;padding:70px 24px;margin-top:28px;box-shadow:0 12px 30px #0f172a08}
    .empty-state .empty-icon {display:grid;place-items:center;width:70px;height:70px;border-radius:22px;background:linear-gradient(135deg,#e7f5ff,#e8fbfa);margin:0 auto 18px;font-size:2rem}
    .empty-state h2 {color:#173557;margin:0 0 8px}.empty-state p {color:#6b7b90;margin:0}
    .user-chip {display:flex;align-items:center;gap:10px;background:#ffffff0c;border:1px solid #ffffff18;border-radius:12px;padding:10px 12px;margin-bottom:10px}
    .user-chip small {opacity:.62}
    /* Public sidebar staff-login panel: keep every control readable. */
    [data-testid="stSidebar"] [data-testid="stExpander"] {background:#ffffff0d;border:1px solid #ffffff1f;border-radius:13px;overflow:hidden;margin-bottom:.75rem}
    [data-testid="stSidebar"] [data-testid="stExpander"] details {background:transparent}
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {background:#ffffff12;color:#fff !important;font-weight:700;border-radius:12px;padding:.7rem .8rem;transition:background .2s ease}
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {background:#ffffff20}
    [data-testid="stSidebar"] [data-testid="stExpander"] summary * {color:#fff !important}
    [data-testid="stSidebar"] [data-testid="stTextInput"] label p {color:#fff !important;font-weight:600}
    [data-testid="stSidebar"] [data-testid="stTextInput"] input {background:#fff !important;color:#10213c !important;border:2px solid transparent !important;border-radius:10px}
    [data-testid="stSidebar"] [data-testid="stTextInput"] input:focus {border-color:#23b7ee !important;box-shadow:0 0 0 3px #23b7ee2b !important}
    [data-testid="stSidebar"] [data-testid="stForm"] {border:1px solid #ffffff14;border-radius:12px;padding:1rem}
    [data-testid="stSidebar"] [data-testid="stForm"] .stButton>button,
    [data-testid="stSidebar"] [data-testid="stFormSubmitButton"]>button {background:linear-gradient(90deg,#1297ed,#11b5c4) !important;color:#fff !important;border:0 !important;box-shadow:0 7px 18px #001b3b55}
    [data-testid="stSidebar"] [data-testid="stForm"] .stButton>button:hover,
    [data-testid="stSidebar"] [data-testid="stFormSubmitButton"]>button:hover {background:linear-gradient(90deg,#0c86db,#0ca3b2) !important;color:#fff !important;transform:translateY(-2px)}
    [data-testid="stSidebar"] [data-testid="stForm"] button * {color:#fff !important}
    [data-testid="stImage"] img {border-radius:16px;transition:transform .28s ease,box-shadow .28s ease}
    [data-testid="stImage"] img:hover {transform:scale(1.018);box-shadow:0 16px 30px #0f172a25}
    @keyframes pulse {0%,100%{box-shadow:0 0 0 5px #20b26b18}50%{box-shadow:0 0 0 10px #20b26b05}}
    @media(max-width:900px){.dataset-card{margin-bottom:12px}.page-heading h1{font-size:1.55rem}}
    </style>
    """, unsafe_allow_html=True)
