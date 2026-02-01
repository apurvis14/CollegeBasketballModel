import pandas as pd
import streamlit as st
from functions import (
    # Win/Loss Record Functions
    allover_count_win_loss, allunder_count_win_loss,
    EPOver_TempoUnder_count_win_loss, TEOver_PPGUnder_count_win_loss,
    TPOver_EFFUnder_count_win_loss, TempoOver_count_win_loss,
    PPGover_count_win_loss, EFFover_count_win_loss,

    # Win/Loss Record by Period (Current vs. Previous)
    allover_count_win_loss_current, allover_count_win_loss_prev, allover_count_win_loss_conference, allover_count_win_loss_nonconference, allover_count_win_loss_conference_specific, allover_count_win_loss_total, allover_count_win_loss_dayweek,
    allunder_count_win_loss_current, allunder_count_win_loss_prev, allunder_count_win_loss_conference, allunder_count_win_loss_nonconference, allunder_count_win_loss_conference_specific, allunder_count_win_loss_total, allunder_count_win_loss_dayweek,
    EPOver_TempoUnder_count_win_loss_current, EPOver_TempoUnder_count_win_loss_prev, EPOver_TempoUnder_count_win_loss_conference, EPOver_TempoUnder_count_win_loss_nonconference, EPOver_TempoUnder_count_win_loss_conference_specific, EPOver_TempoUnder_count_win_loss_total, EPOver_TempoUnder_count_win_loss_dayweek,
    TEOver_PPGUnder_count_win_loss_current, TEOver_PPGUnder_count_win_loss_prev, TEOver_PPGUnder_count_win_loss_conference, TEOver_PPGUnder_count_win_loss_nonconference, TEOver_PPGUnder_count_win_loss_conference_specific, TEOver_PPGUnder_count_win_loss_total, TEOver_PPGUnder_count_win_loss_dayweek,
    TPOver_EFFUnder_count_win_loss_current, TPOver_EFFUnder_count_win_loss_prev, TPOver_EFFUnder_count_win_loss_conference, TPOver_EFFUnder_count_win_loss_nonconference, TPOver_EFFUnder_count_win_loss_conference_specific, TPOver_EFFUnder_count_win_loss_total, TPOver_EFFUnder_count_win_loss_dayweek,
    TempoOver_count_win_loss_current, TempoOver_count_win_loss_prev, TempoOver_count_win_loss_conference, TempoOver_count_win_loss_nonconference, TempoOver_count_win_loss_conference_specific, TempoOver_count_win_loss_total, TempoOver_count_win_loss_dayweek,
    PPGover_count_win_loss_current, PPGover_count_win_loss_prev, PPGover_count_win_loss_conference, PPGover_count_win_loss_nonconference, PPGover_count_win_loss_conference_specific, PPGover_count_win_loss_total, PPGover_count_win_loss_dayweek,
    EFFover_count_win_loss_current, EFFover_count_win_loss_prev, EFFover_count_win_loss_conference, EFFover_count_win_loss_nonconference, EFFover_count_win_loss_conference_specific, EFFover_count_win_loss_total, EFFover_count_win_loss_dayweek,


    # Display / Metrics Functions
    display_metrics_expand, win_loss_record_expand,

    # Home/Away Breakdown
    home_away_over_under_by_team, home_away_over_under_by_team_all,
    home_away_over_under_by_team_all_under, home_away_over_under_by_team_all_under_all,
    home_away_over_under_by_team_EP_over, home_away_over_under_by_team_EP_over_all,
    home_away_over_under_by_team_TE_over, home_away_over_under_by_team_TE_over_all,
    home_away_over_under_by_team_TP_over, home_away_over_under_by_team_TP_over_all,
    home_away_over_under_by_team_T_over, home_away_over_under_by_team_T_over_all,
    home_away_over_under_by_team_P_over, home_away_over_under_by_team_P_over_all,
    home_away_over_under_by_team_E_over, home_away_over_under_by_team_E_over_all,

    # Utilities
    get_base64, show_trend_html, details_html
)

from datetime import datetime
from PIL import Image
from streamlit.components.v1 import html as st_html
import base64
from zoneinfo import ZoneInfo

st.set_page_config(layout="centered", page_title="CBB Trends", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    /* Shrink top bar */
    header[data-testid="stHeader"] {
        height: 40px !important;
        padding: 0 !important;
        min-height: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True)

ENCODED_USERS = {
    "U2FtIERyZW5uYW46Y2hhcmxpZWtpcms2Nw==": "Sam Drennan",
    "Qmxha2UgUGFpbnRlcjpMdW5hQm9vdHk2OQ==": "Blake Painter",
    "R3JpZmY6MTIzNA==": "Griff",
    "QWRtaW46YWNjZXNz": "Admin",
    "SmFjb2IgUGVya2luczpXYXJyaW9yMTIzNDUh": "Jacob Perkins",
    "VGFubmVyIEdyYXZlczokU21pdGgxMjI=": "Tanner Graves",
    "QmVuOkxJR01BQkFMTFM=": "Ben",
}

# ---------- SESSION STATE INIT ----------
if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.username = None

def do_login():
    """Callback to validate and set session state."""
    combined = f"{st.session_state.u}:{st.session_state.p}"
    encoded = base64.b64encode(combined.encode()).decode()
    if encoded in ENCODED_USERS:
        st.session_state.auth = True
        st.session_state.username = st.session_state.u
    else:
        st.session_state.login_error = "Invalid username or password"

def do_logout():
    st.session_state.auth = False
    st.session_state.username = None

# ---------- UI ----------
if not st.session_state.auth:
    st.sidebar.header("Login")

    # Text inputs with keys so values persist across reruns
    st.sidebar.text_input("Username", key="u", on_change=None)
    st.sidebar.text_input("Password", type="password", key="p", on_change=None)

    # Single button triggers the callback once
    st.sidebar.button("Login", on_click=do_login)

    # Show any login error
    if st.session_state.get("login_error"):
        st.sidebar.error(st.session_state.login_error)

    st.stop()  # Nothing below runs until logged in

# ---------- PROTECTED CONTENT ----------
st.sidebar.success(f"Welcome **{st.session_state.username}**!")
st.sidebar.button("Logout", on_click=do_logout)

@st.cache_data(show_spinner=False)
def load_data(filename, sheet):
    df = pd.read_excel(filename, sheet_name=sheet, engine="openpyxl")
    df.columns = df.columns.astype(str).str.strip().str.replace('\n', ' ', regex=False)
    df = df.fillna(0)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    # Drop unnecessary columns
    columns_to_drop = [
    'Home Score', 'Away Score', 'Book Spread (Home Team)', 'Actual Spread', 'DIFF',
    'Sum of Formulas Over', 'Temp Over Book Value', 'PPG Over Book Value', 'EFF over Book Value',
    'Sum EFF from 100', '1', 'DIFF.1', 'Sum of Formulas Under', '2', 'DIFF.2',
    'Average to Book Value', 'Sum of EFF/PPG Over', 'Absolute Value Tempo to Book',
    'Possession to Tempo', 'AVG of 3 Over', '3', 'DIFF.3', 'Absolute Value PPG to Book',
    '4', 'DIFF.4', '5', 'DIFF.5', 'Difference Tempo to Book', 'DIFF.6',
    'Difference PPG to Book', 'DIFF.7', 'Difference EFF to Book']

    df = df.drop(columns=columns_to_drop, errors='ignore')

    return df

@st.cache_resource(show_spinner=False)
def load_logo(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    

# Preload all logos to cache
def preload_logos(df):
    logos = {}
    teams = set(df['Home Team'].unique()).union(set(df['Away Team'].unique()))
    for team in teams:
        try:
            logos[team] = load_logo(f"Team Logo/{team}.jpg")
        except FileNotFoundError:
            logos[team] = load_logo("Team Logo/Error.jpg")  # placeholder if missing
    return logos

df = load_data("data/College Basketball Model.xlsm", "All Seasons Data")
logos = preload_logos(df)

@st.cache_data(show_spinner=False)
def compute_game_metrics(game, df):
    """
    Compute win/loss counts, percentages for a given game.
    """
    if game['All Formulas Over'] == "True":
        o = game['Offense Over 100']
        d = game['Defense Over 100']
        conf = game['Conference']
        bucket = game['Book Total Bucket']
        day = game['Day of Week']

        count_prev, win_prev, loss_prev = allover_count_win_loss_prev(df, o, d)
        count, win, loss = allover_count_win_loss(df, o, d)
        count_cur, win_cur, loss_cur = allover_count_win_loss_current(df, o, d)
        count_nonconf, win_nonconf, loss_nonconf = allover_count_win_loss_nonconference(df, o, d)
        count_conf, win_conf, loss_conf = allover_count_win_loss_conference(df, o, d, conf)
        count_specific, win_specific, loss_specific = allover_count_win_loss_conference_specific(df, o, d, conf)
        count_book, win_book, loss_book = allover_count_win_loss_total(df, o, d, bucket)
        count_day, win_day, loss_day = allover_count_win_loss_dayweek(df, o, d, day)

    elif game['All Formulas Under'] == "Look":
        o = game['Offense Under 100']
        d = game['Defense Under 100']
        conf = game['Conference']
        bucket = game['Book Total Bucket']
        day = game['Day of Week']

        count_prev, win_prev, loss_prev = allunder_count_win_loss_prev(df, o, d)
        count, win, loss = allunder_count_win_loss(df, o, d)
        count_cur, win_cur, loss_cur = allunder_count_win_loss_current(df, o, d)
        count_nonconf, win_nonconf, loss_nonconf = allunder_count_win_loss_nonconference(df, o, d)
        count_conf, win_conf, loss_conf = allunder_count_win_loss_conference(df, o, d)
        count_specific, win_specific, loss_specific = allunder_count_win_loss_conference_specific(df, o, d, conf)
        count_book, win_book, loss_book = allunder_count_win_loss_total(df, o, d, bucket)
        count_day, win_day, loss_day = allunder_count_win_loss_dayweek(df, o, d,day)
    
    elif game['Efficiency/PPG over  (Tempo under)'] == "Invest":
        o1 = game['Count of OFF over 100']
        o2 = game['Count of OFF over 110']
        d1 = game['Count of DEF under 100']
        d2 = game['Count of DEF under 95']
        conf = game['Conference']
        bucket = game['Book Total Bucket']
        day = game['Day of Week']

        count_prev, win_prev, loss_prev = EPOver_TempoUnder_count_win_loss_prev(df, o1, o2, d1, d2)
        count, win, loss = EPOver_TempoUnder_count_win_loss(df, o1, o2, d1, d2)
        count_cur, win_cur, loss_cur = EPOver_TempoUnder_count_win_loss_current(df, o1, o2, d1, d2)
        count_nonconf, win_nonconf, loss_nonconf = EPOver_TempoUnder_count_win_loss_nonconference(df, o1, o2, d1, d2)
        count_conf, win_conf, loss_conf = EPOver_TempoUnder_count_win_loss_conference(df, o1, o2, d1, d2)
        count_specific, win_specific, loss_specific = EPOver_TempoUnder_count_win_loss_conference_specific(df, o1, o2, d1, d2, conf)
        count_book, win_book, loss_book = EPOver_TempoUnder_count_win_loss_total(df, o1, o2, d1, d2, bucket)
        count_day, win_day, loss_day = EPOver_TempoUnder_count_win_loss_dayweek(df, o1, o2, d1, d2, day)

    elif game['Tempo and Efficiency over (PPG under)'] == "Alert":
        o1 = game['OFF Under 100']
        o2 = game['OFF Under 95']
        d1 = game['DEF Under 100']
        d2 = game['DEF Under 95']
        conf = game['Conference']
        bucket = game['Book Total Bucket']
        day = game['Day of Week']

        count_prev, win_prev, loss_prev = TEOver_PPGUnder_count_win_loss_prev(df, o1, o2, d1, d2)
        count, win, loss = TEOver_PPGUnder_count_win_loss(df, o1, o2, d1, d2)
        count_cur, win_cur, loss_cur = TEOver_PPGUnder_count_win_loss_current(df, o1, o2, d1, d2)
        count_nonconf, win_nonconf, loss_nonconf = TEOver_PPGUnder_count_win_loss_nonconference(df, o1, o2, d1, d2)
        count_conf, win_conf, loss_conf = TEOver_PPGUnder_count_win_loss_conference(df, o1, o2, d1, d2)
        count_specific, win_specific, loss_specific = TEOver_PPGUnder_count_win_loss_conference_specific(df, o1, o2, d1, d2, conf)
        count_book, win_book, loss_book = TEOver_PPGUnder_count_win_loss_total(df, o1, o2, d1, d2, bucket)
        count_day, win_day, loss_day = TEOver_PPGUnder_count_win_loss_dayweek(df, o1, o2, d1, d2, day)
    
    elif game['Tempo and PPG over (Efficiency Under)'] == "Alive":
            conf = game['Conference']
            bucket = game['Book Total Bucket']
            day = game['Day of Week']

            count_prev, win_prev, loss_prev = TPOver_EFFUnder_count_win_loss_prev(df)
            count, win, loss = TPOver_EFFUnder_count_win_loss(df)
            count_cur, win_cur, loss_cur = TPOver_EFFUnder_count_win_loss_current(df)
            count_conf, win_conf, loss_conf = TPOver_EFFUnder_count_win_loss_conference(df)
            count_nonconf, win_nonconf, loss_nonconf = TPOver_EFFUnder_count_win_loss_nonconference(df)
            count_specific, win_specific, loss_specific = TPOver_EFFUnder_count_win_loss_conference_specific(df, conf)
            count_book, win_book, loss_book = TPOver_EFFUnder_count_win_loss_total(df, bucket)
            count_day, win_day, loss_day = TPOver_EFFUnder_count_win_loss_dayweek(df, day)

    elif game['Just Tempo Over'] == "Tempo":
            val = game['Over 105 EFF']
            conf = game['Conference']
            bucket = game['Book Total Bucket']
            day = game['Day of Week']

            count_prev, win_prev, loss_prev = TempoOver_count_win_loss_prev(df, val)
            count, win, loss = TempoOver_count_win_loss(df, val)
            count_cur, win_cur, loss_cur = TempoOver_count_win_loss_current(df, val)
            count_nonconf, win_nonconf, loss_nonconf = TempoOver_count_win_loss_nonconference(df, val)
            count_conf, win_conf, loss_conf = TempoOver_count_win_loss_conference(df, val)
            count_specific, win_specific, loss_specific = TempoOver_count_win_loss_conference_specific(df, val, conf)
            count_book, win_book, loss_book = TempoOver_count_win_loss_total(df, val, bucket)
            count_day, win_day, loss_day = TempoOver_count_win_loss_dayweek(df, val, day)

    elif game['Just PPG Over'] == "PPG":
            val = game['Over 110 EFF']
            conf = game['Conference']
            bucket = game['Book Total Bucket']
            day = game['Day of Week']

            count_prev, win_prev, loss_prev = PPGover_count_win_loss_prev(df, val)
            count, win, loss = PPGover_count_win_loss(df, val)
            count_cur, win_cur, loss_cur = PPGover_count_win_loss_current(df, val)
            count_nonconf, win_nonconf, loss_nonconf = PPGover_count_win_loss_nonconference(df, val)
            count_conf, win_conf, loss_conf = PPGover_count_win_loss_conference(df, val)
            count_specific, win_specific, loss_specific = PPGover_count_win_loss_conference_specific(df, val, conf)
            count_book, win_book, loss_book = PPGover_count_win_loss_total(df, val, bucket)
            count_day, win_day, loss_day = PPGover_count_win_loss_dayweek(df, val, day)

    elif game['Just Efficiency Over'] == "EFF":
            o = game['OFF Over 105']
            d = game['DEF Over 105']
            conf = game['Conference']
            bucket = game['Book Total Bucket']
            day = game['Day of Week'] 

            count_prev, win_prev, loss_prev = EFFover_count_win_loss_prev(df, o, d)
            count, win, loss = EFFover_count_win_loss(df, o, d)
            count_cur, win_cur, loss_cur = EFFover_count_win_loss_current(df, o, d)
            count_conf, win_conf, loss_conf = EFFover_count_win_loss_conference(df, o, d)
            count_nonconf, win_nonconf, loss_nonconf = EFFover_count_win_loss_nonconference(df, o, d)
            count_specific, win_specific, loss_specific = EFFover_count_win_loss_conference_specific(df, o, d, conf)
            count_book, win_book, loss_book = EFFover_count_win_loss_total(df, o, d, bucket)    
            count_day, win_day, loss_day = EFFover_count_win_loss_dayweek(df, o, d, day)
            
    else:
            percent_all = 'None'
            win, loss = 0, 0
            percent_prev = 'None'
            win_prev, loss_prev = 0, 0
            count, count_prev = 0, 0
            percent_cur = 'None'
            count_cur = 0
            percent_conf = 'None'
            count_conf, count_nonconf = 0, 0
            win_conf, win_nonconf = 0, 0
            loss_conf, loss_nonconf = 0, 0
            percent_specific = 'None'
            count_specific, win_specific, loss_specific = 0, 0, 0
            count_book = 0
            win_book, loss_book = 0, 0
            percent_book = 'None'
            win_day, loss_day = 0, 0
            percent_day = 'None'


    percent_all = round((win/count)*100,2) if count else 0
    percent_prev = round((win_prev/count_prev)*100,2) if count_prev else 0
    percent_cur = round((win_cur/count_cur)*100,2) if count_cur else 0
    percent_conf = round((win_conf/count_conf)*100,2) if count_conf else 0
    percent_nonconf = round((win_nonconf/count_nonconf)*100,2) if count_nonconf else 0 
    percent_specific = round((win_specific/count_specific)*100,2) if count_specific else 0
    percent_book = round((win_book/count_book)*100,2) if count_book else 0
    percent_day = round((win_day/count_day)*100,2) if count_day else 0

    return count, win, loss, percent_all, percent_prev, win_prev, loss_prev, percent_cur, count_cur, win_cur, loss_cur, percent_conf, percent_nonconf, count_conf, count_nonconf, win_conf, win_nonconf, loss_conf, loss_nonconf, count_specific, win_specific, loss_specific, percent_specific, win_book, loss_book, percent_book, count_day, win_day, loss_day, percent_day


# Remove padding at the top
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Logo For Top of Page
logo = Image.open("data/CBB Horizontal Logo.png")
st.image(logo, use_container_width=True)

# Tabs Using for Info
tab1, = st.tabs(["Today's Games with Trends"]) 

with tab1:
    st.markdown(
        """
        <style>
        /* Target the expander header using data-testid */
        [data-testid="stExpander"] > details > summary {
            background-color: #DAA520 !important;  /* gold */
            color: black !important;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }

        /* Optional: hover effect */
        [data-testid="stExpander"] > details > summary:hover {
            background-color: #DAA520 !important;  /* lighter gold */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    with st.expander("Explanation of Information"):
        # st.write("- Dropdown to Select Specific Conferences\n- Each Game has a Dropdown with Trend Info and Team's Season Record in that Active Trend \n- BLAH\n- BLAH")
        st.markdown("""
        <div class="mobile-adjust" style="font-size:12px; color:black; line-height:2.4;">
            <ol>
                <li>Below "Today's Games" use the Dropdown to Select Specific Conferences</li>
                <li>Each Game has a Dropdown with Trend Info and Team's Season Records for that Active Trend
                    <ul>
                        <li>There are 8 Trends based on 3 Model Formulas in Comparison to Book Total</li> 
                        <li>With Various Subcategories for Each of the 8 Trends using the Team's KenPom Efficiencies</li>
                        <li>All Records are Record Against the Book Total for the Active Trend (Ex: 92-11 = 92 Overs to 11 Unders)</li>
                    </ul>
                </li>
                <li>Each Game has a Suggestion, Use Your Analysis and Take Games at Your Own Risk</li>
            </ol>
        </div>

        <style>
            /* Mobile adjustments */
            @media (max-width: 600px) {
                .mobile-adjust {
                    font-size: 9px !important;
                    line-height: 1.6 !important;
                }
            }
        </style>
        """, unsafe_allow_html=True)


    st.markdown(
    "<hr style='border: 2px solid goldenrod; margin-top: 0rem; margin-bottom: 0.5rem;'>",
    unsafe_allow_html=True)

    st.markdown(
    """
    <div style="
        display: flex;
        justify-content: center;  /* centers horizontally */
        align-items: center;      /* centers vertically */
        width: 100%;">
        <div style="
            border: 4px solid goldenrod; 
            padding: 2px; 
            border-radius: 10px; 
            width: 375px;
            height: 80px;
            font-size: 48px;
            font-weight: bold;
            background-color: #545353ff;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;">
            Today's Games
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

    # Today Variable for Sorting
    today = datetime.now(ZoneInfo("America/Chicago")).date()

    # Names of Columns
    home_col = 'Home Conference'
    away_col = 'Away Conference'

    # Clean Sorted conference list
    conf_series = pd.concat([
        df[home_col].replace(0, pd.NA),
        df[away_col].replace(0, pd.NA)
    ]).dropna().astype(str).str.strip()


    # Put All Conferences into Variable
    all_confs = sorted(conf_series.unique(), key=lambda s: s.upper())
    st.markdown(
    """
    <style>
    /* --- Fix selectbox background & text color --- */
    div[data-baseweb="select"] > div {
        background-color: #DAA520 !important;   /* Gold dropdown background */
        color: #000000 !important!              /* black text */
        border: 2px solid #000000 !important
        border-radius: 8px !important
    }
    div[data-baseweb="select"] span {
        color: #000000 !important;              /* ensure label text is black */
    }
    </style>
    """,
    unsafe_allow_html=True)


    # Select Box for conference filter
    cola, colc = st.columns([3.25,10])
    with cola:
        selected_conf = st.selectbox("",
            options=["All Conferences"] + all_confs,
            label_visibility="collapsed"
        )

    # Mask to get only today's games
    date_mask = df['Date'].dt.date == today

    # Conference mask (only if a conference is selected) ---
    if selected_conf != "All Conferences":
        conf_mask = (
            (df[home_col].astype(str).str.strip() == selected_conf) |
            (df[away_col].astype(str).str.strip() == selected_conf)
        )
        mask = date_mask & conf_mask
    else:
        mask = date_mask

    # --- Filtered DataFrame ---
    today_games = df.loc[mask]

    with colc:
        st.markdown(
            f"""
            <div style="
                display: inline-block;
                float: right;
                border: 1px solid black; 
                padding: 6px; 
                border-radius: 10px; 
                margin-top: 18px;
                font-size: 16px;
                width: 250px;
                height: 40px;
                background-color: #DAA520;
                text-align: center;
                color: #000000">
                Number of Games for Today: {today_games.shape[0]}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown(
    "<hr style='border: 2px solid goldenrod; margin-top: 0.25rem; margin-bottom: 0rem;'>",
    unsafe_allow_html=True)

    for idx, game in today_games.iterrows():
        count, win, loss, percent_all, percent_prev, win_prev, loss_prev, percent_cur, count_cur, win_cur, loss_cur, percent_conf, percent_nonconf, count_conf, count_nonconf, win_conf, win_nonconf, loss_conf, loss_nonconf, count_specific, win_specific, loss_specific, percent_specific, win_book, loss_book, percent_book, count_day, win_day, loss_day, percent_day = compute_game_metrics(game, df)
        

        percent_cur1 = display_metrics_expand(percent_cur)
        percent_all1 = display_metrics_expand(percent_all)
        percent_prev1 = display_metrics_expand(percent_prev)
        percent_specific1 = display_metrics_expand(percent_specific)
        percent_book1 = display_metrics_expand(percent_book)
        percent_day1 = display_metrics_expand(percent_day)


        record_cur, units_cur, fade_cur = win_loss_record_expand(win_cur, loss_cur)
        record_all, units_all, fade_all = win_loss_record_expand(win, loss)
        record_prev, units_prev, fade_prev = win_loss_record_expand(win_prev, loss_prev)
        record_day, units_day, fade_day = win_loss_record_expand(win_day, loss_day)

        if game['Same Conference'] == 1:
            record_need, units_need, fade_need = win_loss_record_expand(win_conf, loss_conf)
            percent_need = display_metrics_expand(percent_conf)
            record_specific1, unit_specific, fade_specific = win_loss_record_expand(win_specific, loss_specific)
            
            need = "Conference"
            need1 = f"Conf. ({game['Conference']})"
            conf_need = game['Conference']
            book_bucket = game['Book Total Bucket']
            record_book, units_book, fade_book = win_loss_record_expand(win_book, loss_book)
            day = game['Day of Week']

            away_logo = get_base64(f"Team Logo/{game['Away Team']}.jpg")
            home_logo = get_base64(f"Team Logo/{game['Home Team']}.jpg")

            away_img = f'<img class="team-logo" src="data:image/jpeg;base64,{away_logo}">'
            home_img = f'<img class="team-logo" src="data:image/jpeg;base64,{home_logo}">'

            matchup_header = (
            f"{away_img}{game['Away Team']} @&nbsp;{home_img}{game['Home Team']}"
            f"&nbsp;|&nbsp;Total: {game['Book Total']} | {need1}||"
            f"'25-'26 Trend Record: {record_cur} {percent_cur1} <br>"
            f"All Time Trend Record: {record_all} {percent_all1} - When {book_bucket}: {record_book} {percent_book1}<br>"
            f"Last Season Trend Record: {record_prev} {percent_prev1} - On {day}. {record_day} {percent_day1} <br>"
            f"{need} Trend Record: {record_need} {percent_need} - {conf_need}: {record_specific1} {percent_specific1}")

        elif game['Same Conference'] == 0:
            record_need, units_need, fade_need = win_loss_record_expand(win_nonconf, loss_nonconf)
            percent_need = display_metrics_expand(percent_nonconf)
            need = "Non-Conference"
            need1 = "Non-Conf."
            record_specific = ""
            book_bucket = game['Book Total Bucket']
            day = game['Day of Week']
            record_book, units_book, fade_book = win_loss_record_expand(win_book, loss_book)

            away_logo = get_base64(f"Team Logo/{game['Away Team']}.jpg")
            home_logo = get_base64(f"Team Logo/{game['Home Team']}.jpg")

            away_img = f'<img class="team-logo" src="data:image/jpeg;base64,{away_logo}">'
            home_img = f'<img class="team-logo" src="data:image/jpeg;base64,{home_logo}">'

            matchup_header = (
                f"{away_img}{game['Away Team']} @&nbsp;{home_img}{game['Home Team']}"
                f"&nbsp;|&nbsp;Total: {game['Book Total']} | {need1}||"
                f"'25-'26 Trend Record: {record_cur} {percent_cur1} <br>"
                f"All Time Trend Record: {record_all} {percent_all1} - When{book_bucket}: {record_book} {percent_book1}<br>"
                f"Last Season Trend Record: {record_prev} {percent_prev1} - On {day}. {record_day} {percent_day1}<br>"
                f"{need} Trend Record: {record_need} {percent_need}")

        with st.container(border=False):
            height = 325
            if game['All Formulas Over'] == "True":
                trend_html = show_trend_html(
                    allover_count_win_loss,
                    allover_count_win_loss_current,
                    allover_count_win_loss_prev,
                    home_away_over_under_by_team,
                    home_away_over_under_by_team_all,
                    df,
                    game,
                    game['Offense Over 100'],
                    game['Defense Over 100']
                )

                # Adjust height to fit (or compute dynamically). Use scrolling if content is larger.
                # height = int(estimate_height(trend_html))
                # trend_html_safe = trend_html.replace("{", "{{").replace("}", "}}")
                # st.markdown(details_html(matchup_header, trend_html), unsafe_allow_html=True) 
                st_html(details_html(matchup_header, trend_html), height=height, scrolling=True)

            
            elif game['All Formulas Under'] == "Look":
                trend_html = show_trend_html(
                    allunder_count_win_loss,
                    allunder_count_win_loss_current,
                    allunder_count_win_loss_prev,
                    home_away_over_under_by_team_all_under,
                    home_away_over_under_by_team_all_under_all,
                    df,
                    game,
                    game['Offense Under 100'],
                    game['Defense Under 100']
                )

                # Adjust height to fit (or compute dynamically). Use scrolling if content is larger.
                # height = int(estimate_height(trend_html))
                st_html(details_html(matchup_header, trend_html), height=height, scrolling=True)
            
            elif game['Efficiency/PPG over  (Tempo under)'] == "Invest":
                trend_html = show_trend_html(
                    EPOver_TempoUnder_count_win_loss,
                    EPOver_TempoUnder_count_win_loss_current,
                    EPOver_TempoUnder_count_win_loss_prev,
                    home_away_over_under_by_team_EP_over,
                    home_away_over_under_by_team_EP_over_all,
                    df,
                    game,
                    game['Count of OFF over 100'],
                    game['Count of OFF over 110'],
                    game['Count of DEF under 100'],
                    game['Count of DEF under 95']
                )

                # Adjust height to fit (or compute dynamically). Use scrolling if content is larger.
                st_html(details_html(matchup_header, trend_html), height=height, scrolling=True)

            elif game['Tempo and Efficiency over (PPG under)'] == "Alert":
                trend_html = show_trend_html(
                    TEOver_PPGUnder_count_win_loss,
                    TEOver_PPGUnder_count_win_loss_current,
                    TEOver_PPGUnder_count_win_loss_prev,
                    home_away_over_under_by_team_TE_over,
                    home_away_over_under_by_team_TE_over_all,
                    df,
                    game,
                    game['OFF Under 100'],
                    game['OFF Under 95'],
                    game['DEF Under 100'],
                    game['DEF Under 95']
                )

                # Adjust height to fit (or compute dynamically). Use scrolling if content is larger.
                st_html(details_html(matchup_header, trend_html), height=height, scrolling=True)
            
            elif game['Tempo and PPG over (Efficiency Under)'] == "Alive":
                trend_html = show_trend_html(
                    TPOver_EFFUnder_count_win_loss,
                    TPOver_EFFUnder_count_win_loss_current,
                    TPOver_EFFUnder_count_win_loss_prev,
                    home_away_over_under_by_team_TP_over,
                    home_away_over_under_by_team_TP_over_all,
                    df,
                    game,
                    game["Arg"]
                )

                # Adjust height to fit (or compute dynamically). Use scrolling if content is larger.
                st_html(details_html(matchup_header, trend_html), height=height, scrolling=True)

            elif game['Just Tempo Over'] == "Tempo":
                trend_html = show_trend_html(
                        TempoOver_count_win_loss,
                        TempoOver_count_win_loss_current,
                        TempoOver_count_win_loss_prev,
                        home_away_over_under_by_team_T_over,
                        home_away_over_under_by_team_T_over_all,
                        df,
                        game,
                        game['Over 105 EFF']
                    )

                # Adjust height to fit (or compute dynamically). Use scrolling if content is larger.
                st_html(details_html(matchup_header, trend_html), height=height, scrolling=True)
            
            elif game['Just PPG Over'] == "PPG":
                trend_html = show_trend_html(
                        PPGover_count_win_loss,
                        PPGover_count_win_loss_current,
                        PPGover_count_win_loss_prev,
                        home_away_over_under_by_team_P_over,
                        home_away_over_under_by_team_P_over_all,
                        df,
                        game,
                        game['Over 110 EFF']
                    )

                # Adjust height to fit (or compute dynamically). Use scrolling if content is larger.
                st_html(details_html(matchup_header, trend_html), height=height, scrolling=True)

            elif game['Just Efficiency Over'] == "EFF":
                trend_html = show_trend_html(
                        EFFover_count_win_loss,
                        EFFover_count_win_loss_current,
                        EFFover_count_win_loss_prev,
                        home_away_over_under_by_team_E_over,
                        home_away_over_under_by_team_E_over_all,
                        df,
                        game,
                        game['OFF Over 105'],
                        game['DEF Over 105']
                    )
                
                # Adjust height to fit (or compute dynamically). Use scrolling if content is larger.
                st_html(details_html(matchup_header, trend_html), height=height, scrolling=True)
