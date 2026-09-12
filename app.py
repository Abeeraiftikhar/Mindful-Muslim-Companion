import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Mindful Muslim Companion",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --green: #0F4D3A;
        --green-2: #1E6B57;
        --green-3: #2B7D66;
        --mint: #F4F9F6;
        --mint-2: #EAF5F0;
        --white: #FFFFFF;
        --border: #D9E7E1;
        --gold: #F4B942;
        --gold-soft: #FFF4D6;
        --text: #1F2937;
        --muted: #6B7280;
        --muted-green: #54756A;
        --success: #2F8F6B;
        --shadow: 0 5px 22px rgba(15,77,58,.055);
    }

    .stApp { background: var(--mint); color: var(--text); }
    .block-container {
        max-width: 1200px;
        padding: 4.6rem 2.2rem 3rem;
    }

    /* Streamlit sidebar: native control is intentionally retained so
       desktop starts expanded and mobile can open/close it naturally. */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F4D3A 0%, #0C4535 100%);
        border-right: 1px solid rgba(255,255,255,.08);
    }
    [data-testid="stSidebar"] > div:first-child { background: transparent; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { color: #F7FFFB; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.12); }
    [data-testid="stSidebar"] .stCaption { color: #CFE0D9 !important; }

    .brand-wrap { padding: 4px 2px 0; }
    .brand-mark {
        width: 42px; height: 42px; border-radius: 13px;
        display: inline-flex; align-items: center; justify-content: center;
        background: rgba(255,255,255,.08);
        border: 1px solid rgba(255,255,255,.12);
        font-size: 25px; margin-bottom: 12px;
    }
    .brand-name { font-size: 22px; line-height: 1.16; font-weight: 800; color: white; }
    .brand-sub { margin-top: 10px; color: #CFE0D9; font-size: 12px; line-height: 1.55; }

    /* Sidebar buttons become the icon navigation instead of radio circles. */
    [data-testid="stSidebar"] .stButton { margin: 0 0 5px 0; }
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        min-height: 40px;
        justify-content: flex-start;
        text-align: left;
        padding: 8px 12px;
        border: 1px solid transparent;
        border-radius: 10px;
        background: transparent;
        color: #F7FFFB;
        font-size: 13px;
        font-weight: 600;
        box-shadow: none;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(30,107,87,.9);
        color: white;
        border-color: rgba(255,255,255,.06);
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #1E6B57;
        color: white;
        border-color: rgba(255,255,255,.08);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.025);
    }

    .sidebar-quote {
        margin-top: 28px; padding: 16px 13px;
        border-radius: 13px; text-align: center;
        background: rgba(255,255,255,.055);
        border: 1px solid rgba(255,255,255,.07);
        color: #E6F0EC; font-size: 11px; line-height: 1.65;
    }
    .sidebar-quote .dot { color: var(--gold); margin-top: 6px; }

    /* Top bar */
    .topbar {
        display:flex;
        min-height: 20px;
        position: relative;
        z-index: 5; align-items:center; justify-content:space-between;
        margin-bottom: 16px;
    }
    .eyebrow { color: var(--green); font-size: 12px;
        white-space: nowrap; font-weight: 800; letter-spacing: .08em; }
    .top-note { color: var(--muted); font-size: 12px; white-space: nowrap; }

    /* Hero */
    .hero {
        position: relative; overflow: hidden; min-height: 178px;
        border: 1px solid var(--border); border-radius: 20px;
        background: linear-gradient(135deg, #FBFDFC 0%, #EAF5F0 72%, #F8F1D8 100%);
        padding: 29px 30px 24px; margin-bottom: 24px;
        box-shadow: var(--shadow);
    }
    .hero-copy { position: relative; z-index: 3; max-width: 67%; }
    .hero-moon { font-size: 39px; line-height: 1; color: var(--gold); margin-bottom: 9px; }
    .hero-title { color: var(--green); font-size: 29px; line-height: 1.18; font-weight: 800; letter-spacing: -.45px; }
    .hero-text { color: #4C6D62; font-size: 14px; line-height: 1.55; margin-top: 8px; }
    .skyline {
        position:absolute; right: 2%; bottom: 0; width: 43%; height: 92%; opacity: .19;
        color: var(--green); z-index: 1;
    }
    .skyline svg { width:100%; height:100%; }

    .greeting { color: var(--text); font-size: 24px; font-weight: 800; margin-top: 4px; }
    .date-line { color: var(--muted); font-size: 14px; margin-top: 3px; }
    .divider { height:1px; background: var(--border); margin: 24px 0 18px; }

    /* Metric cards */
    .metric-card {
        background: var(--white); border: 1px solid var(--border); border-radius: 14px;
        padding: 16px 16px 15px; min-height: 115px; box-shadow: var(--shadow);
    }
    .metric-top { display:flex; align-items:center; gap:9px; color:var(--muted); font-size:12px; }
    .metric-icon { width:36px; height:36px; border-radius:50%; background:#F7F4D9; display:inline-flex; align-items:center; justify-content:center; font-size:19px; }
    .metric-value { color:var(--text); font-size:28px; line-height:1.05; font-weight:500; margin-top:11px; }
    .metric-badge { display:inline-block; margin-top:9px; padding:3px 8px; border-radius:999px; background:#E8F6EE; color:#27825F; font-size:11px; }

    .section-heading { color: var(--text); font-size: 22px; font-weight: 800; margin: 28px 0 13px; }

    /* Focus cards */
    .focus-card {
        display:flex; align-items:center; gap:14px; min-height:94px;
        background: var(--white); border:1px solid var(--border); border-radius:14px;
        padding:15px 16px; box-shadow:var(--shadow); margin-bottom:13px;
    }
    .focus-icon { flex:0 0 48px; width:48px; height:48px; border-radius:50%; background:#F7F4D9; display:flex; align-items:center; justify-content:center; font-size:24px; }
    .focus-content { flex:1; }
    .focus-title { color:var(--green); font-size:15px; font-weight:800; }
    .focus-text { color:var(--muted); font-size:12px; line-height:1.45; margin-top:4px; }
    .arrow-pill { width:34px; height:34px; border-radius:50%; background:#EEF6F2; color:var(--green); display:flex; align-items:center; justify-content:center; font-size:18px; }

    .quick-card {
        background:var(--white); border:1px solid var(--border); border-radius:14px; padding:18px;
        box-shadow:var(--shadow); margin-bottom:14px;
    }
    .quick-title { color:var(--green); font-weight:800; font-size:14px; }
    .quick-text { color:var(--muted); font-size:12px; margin-top:4px; }

    .primary-action > button, .stButton > button[kind="primary"] {
        background:var(--green); color:white; border-color:var(--green);
        border-radius:10px; font-weight:750;
    }
    .primary-action > button:hover, .stButton > button[kind="primary"]:hover { background:var(--green-2); color:white; }

    .stButton > button {
        border-radius:10px; border:1px solid var(--border); background:white; color:var(--green);
        font-weight:700; min-height:40px;
    }
    .stButton > button:hover { border-color:#BBD8CC; background:#EEF6F2; color:var(--green); }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, textarea, input { border-radius:9px !important; border-color:var(--border) !important; }
    div[data-testid="stMetric"] { background:white; border:1px solid var(--border); border-radius:14px; }
    .stProgress > div > div > div { background:var(--green); }

    .notice, .success, .gentle {
        border-radius:11px; padding:14px 16px; margin:13px 0; font-size:13px; line-height:1.5;
    }
    .notice { background:#EDF5F2; border-left:4px solid var(--green-2); color:#315C4F; }
    .success { background:#E8F6EE; border-left:4px solid var(--success); color:#245F48; }
    .gentle { background:#FFF8E8; border-left:4px solid var(--gold); color:#6E5623; }

    .page-hero {
        background:linear-gradient(135deg,#FBFDFC,#EAF5F0); border:1px solid var(--border);
        border-radius:17px; padding:22px 24px; margin-bottom:22px;
    }
    .page-title { color:var(--green); font-size:29px; font-weight:800; line-height:1.2; }
    .page-subtitle { color:var(--muted); font-size:13px; line-height:1.55; margin-top:6px; }

    .mini-stat { background:white; border:1px solid var(--border); border-radius:12px; padding:14px; text-align:center; box-shadow:var(--shadow); }
    .mini-stat-value { color:var(--green); font-size:24px; font-weight:800; }
    .mini-stat-label { color:var(--muted); font-size:11px; margin-top:3px; }

    .footer {
        margin-top:34px; padding:18px 20px; border-radius:14px;
        background:var(--green); color:#E8F3EE; font-size:11px;
        display:flex; justify-content:space-between; gap:10px; align-items:center;
    }
    .footer strong { color:white; }

    @media (max-width: 768px) {
        .block-container { padding: 4.1rem .85rem 2rem; }
        .hero { padding:22px 18px; min-height:165px; }
        .hero-copy { max-width:83%; }
        .hero-title { font-size:24px; }
        .hero-text { font-size:12px; }
        .skyline { width:52%; opacity:.14; }
        .greeting { font-size:21px; }
        .section-heading { font-size:20px; }
        .metric-card { min-height:102px; padding:13px; }
        .metric-value { font-size:24px; }
        .footer { flex-direction:column; text-align:center; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# STATE
# ============================================================

def initialize_state():
    defaults = {
        "profile": {"name": "", "goal": "Build overall consistency", "daily_time": "10–20 minutes", "reminder_style": "Gentle"},
        "salah": {"Fajr": False, "Dhuhr": False, "Asr": False, "Maghrib": False, "Isha": False},
        "quran_sessions": [],
        "reflections": [],
        "habits": [
            {"name": "Quran Reading", "frequency": "Daily", "completed": False},
            {"name": "Reflection", "frequency": "Daily", "completed": False},
        ],
        "notifications": {"enabled": True, "morning": True, "evening": True},
        "page": "Today",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_state()


def salah_completion():
    total = len(st.session_state.salah)
    completed = sum(1 for value in st.session_state.salah.values() if value)
    percentage = int((completed / total) * 100) if total else 0
    return completed, total, percentage


def habit_completion():
    habits = st.session_state.habits
    if not habits:
        return 0
    completed = sum(1 for habit in habits if habit["completed"])
    return int((completed / len(habits)) * 100)


def adaptive_guidance():
    completed, _, percentage = salah_completion()
    quran_count = len(st.session_state.quran_sessions)
    reflection_count = len(st.session_state.reflections)
    if percentage == 100:
        return "Your Salah tracking is complete for today. If this routine feels sustainable, continue with the same approach."
    if percentage >= 60:
        return "You have made progress today. Consider keeping your next step small and realistic."
    if completed > 0:
        return "You have started today's routine. Focus on continuing rather than trying to make everything perfect."
    if quran_count == 0 and reflection_count == 0:
        return "A simple restart can be useful. Choose one small activity that fits naturally into your day."
    return "Your routine does not need to be perfect. Choose one manageable action and continue from there."


def go_to(page):
    st.session_state.page = page
    st.rerun()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

nav_items = [
    ("🏠", "Today"),
    ("☾", "Salah"),
    ("📖", "Quran"),
    ("🌿", "Habits"),
    ("♡", "Reflection"),
    ("📈", "Progress"),
    ("⚙", "Settings"),
    ("ⓘ", "About"),
]

with st.sidebar:
    st.markdown(
        """
        <div class="brand-wrap">
            <div class="brand-mark">🌙</div>
            <div class="brand-name">Mindful Muslim<br>Companion</div>
            <div class="brand-sub">Personalized Islamic habit-building &amp; reflection</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown('<div style="font-size:12px;font-weight:800;color:#DDECE6;margin-bottom:8px;">Navigation</div>', unsafe_allow_html=True)
    for icon, label in nav_items:
        selected = st.session_state.page == label
        if st.button(f"{icon}   {label}", key=f"nav_{label}", use_container_width=True, type="primary" if selected else "secondary"):
            go_to(label)
    st.markdown(
        """
        <div class="sidebar-quote">
            “Small steps in faith<br>lead to big changes.”
            <div class="dot">• ─ ◆ ─ •</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# SHARED UI
# ============================================================

def page_header(title, subtitle, icon="🌿"):
    st.markdown(
        f"""
        <div class="page-hero">
            <div class="page-title">{icon} {title}</div>
            <div class="page-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        """
        <div class="footer">
            <div><strong>🌙 Mindful Muslim Companion</strong></div>
            <div>Build better habits &nbsp;•&nbsp; Stay connected &nbsp;•&nbsp; Grow spiritually</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# TODAY
# ============================================================

if st.session_state.page == "Today":
    st.markdown(
        """
        <div class="topbar">
            <div class="eyebrow">MINDFUL MUSLIM COMPANION</div>
            <div class="top-note">Support • Reflect • Continue</div>
        </div>
        <div class="hero">
            <div class="hero-copy">
                <div class="hero-moon">☾</div>
                <div class="hero-title">A calmer way to build consistency</div>
                <div class="hero-text">A calm space for building consistency, reflection, and meaningful daily routines.</div>
            </div>
            <div class="skyline" aria-hidden="true">
                <svg viewBox="0 0 600 220" preserveAspectRatio="none">
                    <path fill="currentColor" d="M0 220V185h32v-35h10v35h22v-65h9v65h22v-27h18v27h27v-91h10v-25h8v25h10v91h20v-46h22v46h29v-82h10v-27h9v27h10v82h27v-42h18v42h30v-63h10v-35h9v35h10v63h25v-50h22v50h26v-88h11v-28h8v28h11v88h28v-41h16v41h29v-69h10v-25h8v25h10v69h31v-52h18v52h34v35z"/>
                    <circle cx="475" cy="54" r="31" fill="#F4B942" opacity=".55"/>
                </svg>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    name = st.session_state.profile.get("name", "")
    greeting = f"Assalamu Alaikum, {name}" if name else "Assalamu Alaikum"
    st.markdown(f'<div class="greeting">{greeting}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-line">Today is <strong>{date.today().strftime("%A, %d %B %Y")}</strong>.</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    completed, total, salah_percent = salah_completion()
    habit_percent = habit_completion()
    quran_count = len(st.session_state.quran_sessions)
    reflection_count = len(st.session_state.reflections)

    cols = st.columns(4)
    metrics = [
        ("🧎", "Salah today", f"{completed}/{total}", f"↑ {salah_percent}%"),
        ("📖", "Quran sessions", str(quran_count), "Today"),
        ("🌿", "Habits", f"{habit_percent}%", "On track"),
        ("♡", "Reflections", str(reflection_count), "Today"),
    ]
    for col, (icon, label, value, badge) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-top"><span class="metric-icon">{icon}</span><span>{label}</span></div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-badge">{badge}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-heading">Today\'s Focus</div>', unsafe_allow_html=True)
    focus = [
        ("🧎", "Salah", "Keep your prayers on time", "Salah"),
        ("📖", "Quran", "Read and reflect", "Quran"),
        ("🌿", "Habits", "Build good habits", "Habits"),
        ("♡", "Reflection", "Be closer to Allah", "Reflection"),
    ]
    c1, c2 = st.columns(2)
    for idx, (icon, title, text, page) in enumerate(focus):
        with (c1 if idx % 2 == 0 else c2):
            st.markdown(
                f"""
                <div class="focus-card">
                    <div class="focus-icon">{icon}</div>
                    <div class="focus-content"><div class="focus-title">{title}</div><div class="focus-text">{text}</div></div>
                    <div class="arrow-pill">→</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open {title}", key=f"focus_{title}", use_container_width=True):
                go_to(page)

    st.markdown('<div class="section-heading">Quick Actions</div>', unsafe_allow_html=True)
    qa1, qa2, qa3, qa4 = st.columns(4)
    quick = [(qa1, "＋", "Add Habit", "Habits"), (qa2, "📖", "View Quran", "Quran"), (qa3, "♡", "New Reflection", "Reflection"), (qa4, "📈", "View Progress", "Progress")]
    for col, icon, title, page in quick:
        with col:
            st.markdown(f'<div class="quick-card"><div style="font-size:25px;color:#0F4D3A">{icon}</div><div class="quick-title">{title}</div></div>', unsafe_allow_html=True)
            if st.button(title, key=f"quick_{title}", use_container_width=True):
                go_to(page)

    st.markdown('<div class="section-heading">A gentle suggestion</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="gentle">{adaptive_guidance()}</div>', unsafe_allow_html=True)
    footer()

# ============================================================
# SALAH
# ============================================================

elif st.session_state.page == "Salah":
    page_header("Salah", "Track today's prayer routine as behavioral information — not as a measure of religious worth.", "☾")
    completed, total, percentage = salah_completion()
    st.progress(percentage / 100, text=f"Today's tracked progress: {completed}/{total}")
    st.markdown('<div class="section-heading">Today\'s Salah</div>', unsafe_allow_html=True)
    for prayer in st.session_state.salah:
        current = st.session_state.salah[prayer]
        checked = st.checkbox(prayer, value=current, key=f"salah_{prayer}")
        st.session_state.salah[prayer] = checked
    completed, total, percentage = salah_completion()
    if percentage == 100:
        st.markdown('<div class="success"><strong>Today\'s tracking is complete.</strong><br>Continue with a sustainable routine that works for you.</div>', unsafe_allow_html=True)
    elif completed > 0:
        st.markdown(f'<div class="notice">You have recorded {completed} of {total} prayers today. Keep your next step manageable.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="gentle">No Salah activity has been recorded yet today. Start whenever you are ready.</div>', unsafe_allow_html=True)
    if st.button("Reset today's tracker"):
        for prayer in st.session_state.salah:
            st.session_state.salah[prayer] = False
        st.rerun()
    footer()

# ============================================================
# QURAN
# ============================================================

elif st.session_state.page == "Quran":
    page_header("Quran", "Record meaningful Quran engagement rather than focusing only on quantity.", "📖")
    st.markdown('<div class="section-heading">Record a Quran Session</div>', unsafe_allow_html=True)
    with st.form("quran_form"):
        reference = st.text_input("Reading reference", placeholder="Example: Surah / Juz / personal reading reference")
        duration = st.number_input("Approximate minutes", min_value=1, max_value=300, value=10)
        takeaway = st.text_area("What stood out to you?", placeholder="Write an optional personal takeaway...")
        submitted = st.form_submit_button("Save Quran Session", use_container_width=True)
        if submitted:
            st.session_state.quran_sessions.append({"date": str(date.today()), "reference": reference or "Personal reading", "minutes": duration, "takeaway": takeaway})
            st.success("Quran session recorded.")
            st.rerun()
    st.markdown('<div class="section-heading">Reading History</div>', unsafe_allow_html=True)
    if st.session_state.quran_sessions:
        st.dataframe(pd.DataFrame(st.session_state.quran_sessions), use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="notice">No Quran sessions recorded yet. Your first entry can be small.</div>', unsafe_allow_html=True)
    footer()

# ============================================================
# HABITS
# ============================================================

elif st.session_state.page == "Habits":
    page_header("Islamic Habit Builder", "Create flexible habits that fit naturally into your routine.", "🌿")
    st.markdown('<div class="section-heading">Your Habits</div>', unsafe_allow_html=True)
    if not st.session_state.habits:
        st.markdown('<div class="notice">No habits created yet.</div>', unsafe_allow_html=True)
    else:
        for index, habit in enumerate(st.session_state.habits):
            col1, col2, col3 = st.columns([5, 2, 1])
            with col1:
                checked = st.checkbox(habit["name"], value=habit["completed"], key=f"habit_{index}")
                st.session_state.habits[index]["completed"] = checked
            with col2:
                st.caption(habit["frequency"])
            with col3:
                if st.button("✕", key=f"delete_{index}"):
                    st.session_state.habits.pop(index)
                    st.rerun()
    st.markdown('<div class="section-heading">Add a Habit</div>', unsafe_allow_html=True)
    with st.form("habit_form"):
        habit_name = st.text_input("Habit name", placeholder="Example: Evening Dhikr")
        frequency = st.selectbox("Frequency", ["Daily", "3 times per week", "Weekly", "Flexible"])
        add_habit = st.form_submit_button("Add Habit", use_container_width=True)
        if add_habit:
            if habit_name.strip():
                st.session_state.habits.append({"name": habit_name.strip(), "frequency": frequency, "completed": False})
                st.success(f"{habit_name} added.")
                st.rerun()
            else:
                st.warning("Please enter a habit name.")
    if st.button("Reset today's habit progress"):
        for habit in st.session_state.habits:
            habit["completed"] = False
        st.rerun()
    footer()

# ============================================================
# REFLECTION
# ============================================================

elif st.session_state.page == "Reflection":
    page_header("Reflection", "A private space for thoughtful self-reflection and gratitude.", "♡")
    prompts = [
        "What am I grateful for today?",
        "What did I learn today?",
        "What challenged me today?",
        "What would I like to improve tomorrow?",
        "Which reminder or verse stayed with me?",
    ]
    prompt = st.selectbox("Choose a reflection prompt", prompts)
    entry = st.text_area("Your reflection", height=180, placeholder="Write your thoughts here...")
    if st.button("Save Reflection", use_container_width=True):
        if entry.strip():
            st.session_state.reflections.append({"date": str(date.today()), "prompt": prompt, "entry": entry.strip()})
            st.success("Reflection saved.")
            st.rerun()
        else:
            st.warning("Please write something before saving.")
    st.markdown('<div class="section-heading">Previous Reflections</div>', unsafe_allow_html=True)
    if st.session_state.reflections:
        for item in reversed(st.session_state.reflections):
            st.markdown(f'<div class="quick-card"><div class="quick-title">{item["date"]} · {item["prompt"]}</div><div class="quick-text" style="font-size:13px;color:#3F514B;margin-top:9px">{item["entry"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="notice">No reflections recorded yet.</div>', unsafe_allow_html=True)
    footer()

# ============================================================
# PROGRESS
# ============================================================

elif st.session_state.page == "Progress":
    page_header("Progress", "Review your tracked routines with a gentle, non-judgmental view.", "📈")
    completed, total, salah_percent = salah_completion()
    habit_percent = habit_completion()
    stats = [(f"{salah_percent}%", "Salah today"), (f"{habit_percent}%", "Habit completion"), (str(len(st.session_state.quran_sessions)), "Quran sessions"), (str(len(st.session_state.reflections)), "Reflections")]
    cols = st.columns(4)
    for col, (value, label) in zip(cols, stats):
        with col:
            st.markdown(f'<div class="mini-stat"><div class="mini-stat-value">{value}</div><div class="mini-stat-label">{label}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Today at a glance</div>', unsafe_allow_html=True)
    progress_df = pd.DataFrame({"Area": ["Salah", "Habits"], "Completion": [salah_percent, habit_percent]})
    st.bar_chart(progress_df.set_index("Area"))
    st.markdown('<div class="notice">Progress is intended as a reflection tool. A lower number is not a measure of personal or spiritual worth.</div>', unsafe_allow_html=True)
    footer()

# ============================================================
# SETTINGS
# ============================================================

elif st.session_state.page == "Settings":
    page_header("Settings", "Adjust your companion experience and personal routine preferences.", "⚙")
    st.markdown('<div class="section-heading">Profile</div>', unsafe_allow_html=True)
    with st.form("settings_form"):
        name = st.text_input("Name", value=st.session_state.profile.get("name", ""))
        goal = st.selectbox("Main goal", ["Build overall consistency", "Improve Salah consistency", "Build Quran routine", "Develop reflection habits", "Build several small habits"], index=["Build overall consistency", "Improve Salah consistency", "Build Quran routine", "Develop reflection habits", "Build several small habits"].index(st.session_state.profile.get("goal", "Build overall consistency")) if st.session_state.profile.get("goal") in ["Build overall consistency", "Improve Salah consistency", "Build Quran routine", "Develop reflection habits", "Build several small habits"] else 0)
        daily_time = st.selectbox("Typical daily time", ["5–10 minutes", "10–20 minutes", "20–30 minutes", "30+ minutes"], index=["5–10 minutes", "10–20 minutes", "20–30 minutes", "30+ minutes"].index(st.session_state.profile.get("daily_time", "10–20 minutes")) if st.session_state.profile.get("daily_time") in ["5–10 minutes", "10–20 minutes", "20–30 minutes", "30+ minutes"] else 1)
        reminder_style = st.selectbox("Reminder style", ["Gentle", "Direct", "Minimal"], index=["Gentle", "Direct", "Minimal"].index(st.session_state.profile.get("reminder_style", "Gentle")) if st.session_state.profile.get("reminder_style") in ["Gentle", "Direct", "Minimal"] else 0)
        saved = st.form_submit_button("Save Settings", use_container_width=True)
        if saved:
            st.session_state.profile.update({"name": name, "goal": goal, "daily_time": daily_time, "reminder_style": reminder_style})
            st.success("Settings saved.")
            st.rerun()
    st.markdown('<div class="section-heading">Notifications</div>', unsafe_allow_html=True)
    st.session_state.notifications["enabled"] = st.checkbox("Enable reminders", value=st.session_state.notifications["enabled"])
    st.session_state.notifications["morning"] = st.checkbox("Morning reminder", value=st.session_state.notifications["morning"])
    st.session_state.notifications["evening"] = st.checkbox("Evening reminder", value=st.session_state.notifications["evening"])
    st.markdown('<div class="notice">Reminder settings are stored for this local session. A deployed multi-user version would need persistent user storage for account-level settings.</div>', unsafe_allow_html=True)
    footer()

# ============================================================
# ABOUT
# ============================================================

elif st.session_state.page == "About":
    page_header("About Mindful Muslim Companion", "A calm digital space designed around consistency, reflection, and meaningful routines.", "🌙")
    st.markdown(
        """
        <div class="quick-card">
            <div class="quick-title">Purpose</div>
            <div class="quick-text" style="font-size:14px;line-height:1.65;color:#3F514B;">
            The companion brings Salah tracking, Quran engagement, habit building, reflection, and progress awareness into one simple workspace.
            </div>
        </div>
        <div class="quick-card">
            <div class="quick-title">Design principles</div>
            <div class="quick-text" style="font-size:14px;line-height:1.65;color:#3F514B;">
            Gentle guidance • Simple routines • Clear progress • Low-friction interaction • Calm visual design
            </div>
        </div>
        <div class="notice"><strong>Important:</strong> This application is a habit-building and reflection tool. It does not issue fatwas or authoritative Islamic rulings.</div>
        """,
        unsafe_allow_html=True,
    )
    footer()
