import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
    :root {--navy:#052e63;--blue:#0878e6;--cyan:#19b8c5;--ink:var(--text-color,#10213c);--muted:color-mix(in srgb,var(--text-color,#10213c) 62%,transparent);--line:color-mix(in srgb,var(--text-color,#10213c) 16%,transparent);--card:var(--secondary-background-color,#fff)}
    html, body, .stApp, input, button, textarea, select {font-family:"MS PGothic","ＭＳ Ｐゴシック","MS Gothic","Yu Gothic","Noto Sans JP",Arial,sans-serif}
    /* Hide Streamlit's hosting chrome throughout the unified portal. */
    [data-testid="stHeader"] {
        display:block !important;
        position:absolute !important;
        inset:0 0 auto 0 !important;
        height:64px !important;
        min-height:64px !important;
        background:transparent !important;
        box-shadow:none !important;
        overflow:visible !important;
        pointer-events:auto !important;
        z-index:1000000 !important;
    }
    /* Show Streamlit navigation after authentication. The login page adds a
       later override that hides the complete header until sign-in succeeds. */
    [data-testid="stToolbar"],
    [data-testid="stStatusWidget"],
    [data-testid="stDecoration"],
    [data-testid="stAppDeployButton"],
    #MainMenu {
        display:flex !important;
        visibility:visible !important;
        opacity:1 !important;
        pointer-events:auto !important;
    }
    footer {display:none !important}
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {display:flex !important}
    /* Keep the navigation controls reachable after the sidebar is collapsed.
       The regular Streamlit header is hidden, so the mobile opener must be
       taken out of the zero-height header and placed above the page. */
    [data-testid="stSidebarCollapsedControl"] {
        display:flex !important;
        visibility:visible !important;
        opacity:1 !important;
        position:fixed !important;
        top:12px !important;
        left:max(16px, calc((100vw - 1720px) / 2)) !important;
        z-index:1000002 !important;
        width:44px !important;
        height:44px !important;
        align-items:center !important;
        justify-content:center !important;
        pointer-events:auto !important;
    }
    [data-testid="stSidebarCollapsedControl"] button {
        width:44px !important;
        height:44px !important;
        min-height:44px !important;
        padding:0 !important;
        border:1px solid #d6e3f1 !important;
        border-radius:12px !important;
        background:#ffffff !important;
        color:#073b76 !important;
        box-shadow:0 8px 24px rgba(15,23,42,.18) !important;
    }
    [data-testid="stSidebarCollapsedControl"] button * {
        color:#073b76 !important;
        fill:#073b76 !important;
    }
    /* Replace Streamlit's small chevron with a clear menu icon while keeping
       the original button and its sidebar-opening click behavior. */
    [data-testid="stSidebarCollapsedControl"] button > * {
        display:none !important;
    }
    [data-testid="stSidebarCollapsedControl"] button::before {
        content:"☰";
        display:block;
        color:#ffffff;
        font-family:Arial,sans-serif;
        font-size:24px;
        font-weight:700;
        line-height:1;
    }
    [data-testid="stSidebarCollapsedControl"] button {
        background:linear-gradient(135deg,#108cf1,#0872d1) !important;
        border-color:#43a9ff !important;
    }
    [data-testid="stSidebarCollapseButton"] {
        position:absolute !important;
        top:25px !important;
        right:12px !important;
        left:auto !important;
        z-index:1000003 !important;
        visibility:visible !important;
        opacity:1 !important;
        pointer-events:auto !important;
    }
    [data-testid="stSidebarCollapseButton"] button {
        width:38px !important;
        height:38px !important;
        min-height:38px !important;
        padding:0 !important;
        background:#ffffff18 !important;
        border:1px solid #ffffff35 !important;
        border-radius:10px !important;
        box-shadow:0 6px 16px #001b3b45 !important;
    }
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
    .stApp {background:var(--background-color,#f6f8fc);color:var(--ink)}
    [data-testid="stSidebar"] {background:linear-gradient(165deg,#073d7b 0%,#032b5a 48%,#021d3d 100%);border-right:0;box-shadow:8px 0 30px #062b5514}
    [data-testid="stSidebar"] * {color:white}
    [data-testid="stSidebar"] [data-testid="stRadio"] label {background:#ffffff0b;border:1px solid transparent;border-radius:11px;padding:.58rem .7rem;margin:.12rem 0;transition:all .2s ease}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {background:#ffffff18;border-color:#ffffff18;transform:translateX(3px)}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {background:linear-gradient(90deg,#108cf1,#0872d1);border-color:#43a9ff55;box-shadow:0 7px 18px #001b3b55}
    [data-testid="stSidebar"] hr {border-color:#ffffff1f}
    [data-testid="stSidebar"] code {
        display:inline-block;
        max-width:100%;
        padding:.28rem .5rem;
        border:1px solid #ffffff20;
        border-radius:7px;
        background:#021f43 !important;
        color:#d9edff !important;
        font-size:.76rem;
        line-height:1.45;
        overflow-wrap:anywhere;
        white-space:normal;
    }
    [data-testid="stSidebar"] [class*="st-key-download_uploaded_"] button {
        min-height:44px;
        background:linear-gradient(90deg,#108cf1,#0872d1) !important;
        color:#fff !important;
        border:1px solid #43a9ff66 !important;
        box-shadow:0 7px 18px #001b3b55;
    }
    [data-testid="stSidebar"] [class*="st-key-download_uploaded_"] button:hover {
        background:linear-gradient(90deg,#249cf7,#0d7de0) !important;
        border-color:#7bc2ff !important;
        transform:translateY(-2px);
    }
    [data-testid="stSidebar"] [class*="st-key-download_uploaded_"] button * {
        color:#fff !important;
        fill:#fff !important;
    }
    [data-testid="stSidebar"] [class*="st-key-delete_uploaded_"] button {
        min-height:44px;
        background:#7f1d2d !important;
        color:#fff !important;
        border:1px solid #ff8b9a55 !important;
        box-shadow:0 7px 18px #19081355;
    }
    [data-testid="stSidebar"] [class*="st-key-delete_uploaded_"] button:hover {
        background:#a6283c !important;
        border-color:#ff9cab !important;
        transform:translateY(-2px);
    }
    [data-testid="stSidebar"] [class*="st-key-delete_uploaded_"] button * {
        color:#fff !important;
        fill:#fff !important;
    }
    .block-container {padding-top:.8rem;max-width:1540px;padding-bottom:3rem}
    div[data-testid="stMetric"] {background:var(--card);border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 8px 24px #0f172a0a;transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
    div[data-testid="stMetric"]:hover {transform:translateY(-5px);box-shadow:0 16px 35px #075aaa20;border-color:#b9dafb}
    div[data-testid="stMetricValue"] {color:var(--ink);font-weight:800}
    [data-testid="stPlotlyChart"], [data-testid="stPydeckChart"], [data-testid="stDataFrame"] {background:var(--card);border:1px solid var(--line);border-radius:18px;padding:8px;box-shadow:0 8px 24px #0f172a0a;transition:box-shadow .22s ease,transform .22s ease;overflow:hidden !important}
    [data-testid="stPlotlyChart"]:hover, [data-testid="stPydeckChart"]:hover {box-shadow:0 15px 35px #0f172a14;transform:translateY(-2px)}
    /* When a chart is already inside a bordered card, suppress its second box. */
    div[data-testid="stVerticalBlockBorderWrapper"] {background:var(--card);border:1px solid var(--line);border-radius:18px;box-shadow:0 8px 28px rgba(15,23,42,.04);overflow:hidden}
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPlotlyChart"],
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPydeckChart"],
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stDataFrame"] {background:transparent !important;border:0 !important;border-radius:0 !important;padding:0 !important;box-shadow:none !important;overflow:hidden !important}
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPlotlyChart"]:hover,
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPydeckChart"]:hover {transform:none !important;box-shadow:none !important}
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
    .panel {background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:0 8px 24px #0f172a0a}
    .section-title {margin:4px 0 2px;color:var(--ink);font-weight:750;font-size:1.15rem}
    .section-note {color:var(--muted);font-size:.88rem;margin-bottom:12px}
    .empty {padding:42px 20px;text-align:center;background:var(--card);border:1px dashed var(--line);border-radius:18px;color:var(--muted)}
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
    [data-testid="stSidebar"] [class*="st-key-sidebar_logout"] button,
    [data-testid="stSidebar"] .st-key-portal_logout button,
    [data-testid="stSidebar"] [class*="st-key-portal_logout"] button {justify-content:center !important;text-align:center !important;background:linear-gradient(90deg,#e84b5f,#c92e46) !important;color:#fff !important;border:1px solid #ff8b9a55 !important;box-shadow:0 8px 20px #19081355}
    [data-testid="stSidebar"] .st-key-sidebar_logout button:hover,
    [data-testid="stSidebar"] [class*="st-key-sidebar_logout"] button:hover,
    [data-testid="stSidebar"] .st-key-portal_logout button:hover,
    [data-testid="stSidebar"] [class*="st-key-portal_logout"] button:hover {background:linear-gradient(90deg,#f05a6d,#d43850) !important;color:#fff !important;transform:translateY(-2px)}
    [data-testid="stSidebar"] .st-key-sidebar_logout button *,
    [data-testid="stSidebar"] [class*="st-key-sidebar_logout"] button *,
    [data-testid="stSidebar"] .st-key-portal_logout button *,
    [data-testid="stSidebar"] [class*="st-key-portal_logout"] button * {color:#fff !important;fill:#fff !important}
    .page-heading .eyebrow {font-size:.7rem;font-weight:800;letter-spacing:.16em;color:#0878e6}
    .page-heading h1 {font-size:2rem;margin:.18rem 0 .25rem;color:var(--ink);letter-spacing:-.035em}
    .page-heading p {color:var(--muted);margin:0 0 1rem}
    .dataset-card {display:flex;align-items:center;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 16px;box-shadow:0 8px 24px #0f172a0b;margin-top:3px;transition:all .22s ease}
    .dataset-card:hover {transform:translateY(-3px);box-shadow:0 14px 30px #0878e61c;border-color:#bddcff}
    .dataset-card small {display:block;color:#7a8aa0;font-size:.66rem;font-weight:800;letter-spacing:.1em}
    .dataset-card strong {display:block;color:var(--ink);margin-top:3px;max-width:360px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
    .dataset-icon {display:grid;place-items:center;width:43px;height:43px;border-radius:12px;background:#eaf5ff;font-size:1.25rem}
    .live-dot {width:9px;height:9px;border-radius:50%;background:#20b26b;margin-left:auto;box-shadow:0 0 0 6px #20b26b18;animation:pulse 1.8s infinite}
    .idle-dot {width:9px;height:9px;border-radius:50%;background:#94a3b8;margin-left:auto;box-shadow:0 0 0 6px #94a3b818}
    .empty-state {background:var(--card);border:1px dashed var(--line);border-radius:22px;text-align:center;padding:70px 24px;margin-top:28px;box-shadow:0 12px 30px #0f172a08}
    .empty-state .empty-icon {display:grid;place-items:center;width:70px;height:70px;border-radius:22px;background:linear-gradient(135deg,#e7f5ff,#e8fbfa);margin:0 auto 18px;font-size:2rem}
    .empty-state h2 {color:var(--ink);margin:0 0 8px}.empty-state p {color:var(--muted);margin:0}
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
    @media (prefers-color-scheme: dark) {
        div[data-testid="stMetric"], div[data-testid="stVerticalBlockBorderWrapper"], .panel, .dataset-card {box-shadow:0 8px 28px rgba(0,0,0,.22)}
        [data-testid="stDataFrame"], [data-testid="stPlotlyChart"], [data-testid="stPydeckChart"] {color-scheme:dark}
    }
    /* One chart theme across Incident, Evacuation and CLUP. */
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
    @media(max-width:900px){
        .dataset-card{margin-bottom:12px}
        .page-heading h1{font-size:1.55rem}
        /* Streamlit mounts the collapsed-sidebar opener inside stHeader.
           Give that parent a real mobile hit area instead of clipping it. */
        [data-testid="stHeader"] {
            display:block !important;
            position:absolute !important;
            inset:0 0 auto 0 !important;
            height:64px !important;
            min-height:64px !important;
            background:transparent !important;
            box-shadow:none !important;
            overflow:visible !important;
            pointer-events:auto !important;
            z-index:1000000 !important;
        }
        [data-testid="stHeader"] [data-testid="stToolbar"],
        [data-testid="stHeader"] [data-testid="stAppDeployButton"],
        [data-testid="stHeader"] [data-testid="stStatusWidget"] {
            display:flex !important;
            visibility:visible !important;
            opacity:1 !important;
            pointer-events:auto !important;
        }
        [data-testid="stSidebarCollapsedControl"] {
            display:flex !important;
            visibility:visible !important;
            opacity:1 !important;
            position:fixed !important;
            top:10px !important;
            left:12px !important;
            pointer-events:auto !important;
        }
        [data-testid="stSidebarCollapsedControl"] button {background:#0878e6 !important;border-color:#38a7ff !important}
        [data-testid="stSidebarCollapsedControl"] button * {color:#fff !important;fill:#fff !important}
        [data-testid="stSidebar"] {
            display:block !important;
            z-index:1000001 !important;
        }
        [data-testid="stSidebarCollapseButton"] {
            display:flex !important;
            visibility:visible !important;
            opacity:1 !important;
            pointer-events:auto !important;
            position:absolute !important;
            top:25px !important;
            right:10px !important;
            left:auto !important;
        }
        [data-testid="stMain"] .block-container {padding-top:4.25rem !important}
    }
    </style>
    """, unsafe_allow_html=True)
