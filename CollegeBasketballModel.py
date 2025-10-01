import pandas as pd
import streamlit as st
from functions import (
    # Win/Loss Record Functions
    allover_count_win_loss, allunder_count_win_loss,
    EPOver_TempoUnder_count_win_loss, TEOver_PPGUnder_count_win_loss,
    TPOver_EFFUnder_count_win_loss, TempoOver_count_win_loss,
    PPGover_count_win_loss, EFFover_count_win_loss,

    # Win/Loss Record by Period (Current vs. Previous)
    allover_count_win_loss_current, allover_count_win_loss_prev,
    allunder_count_win_loss_current, allunder_count_win_loss_prev,
    EPOver_TempoUnder_count_win_loss_current, EPOver_TempoUnder_count_win_loss_prev,
    TEOver_PPGUnder_count_win_loss_current, TEOver_PPGUnder_count_win_loss_prev,
    TPOver_EFFUnder_count_win_loss_current, TPOver_EFFUnder_count_win_loss_prev,
    TempoOver_count_win_loss_current, TempoOver_count_win_loss_prev,
    PPGover_count_win_loss_current, PPGover_count_win_loss_prev,
    EFFover_count_win_loss_current, EFFover_count_win_loss_prev,

    # Display / Metrics Functions
    display_metrics, display_metrics_under,
    display_total_difference_histogram,
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
    "U2FtIERyZW5uYW46MTIzNDU=": "Sam Drennan",
    "QW5kcmV3IEdyaWZmaW46NTY3ODk=": "Andrew Griffin",
    "SGFtcCBIdWRuYWxsOjEzNTc5": "Hamp Hudnall"
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

# Load Data
filename = "data/College Basketball Model.xlsm"
sheet = "All Seasons Data"
df = pd.read_excel(filename, sheet_name=sheet, engine="openpyxl")
df.columns = df.columns.astype(str).str.strip().str.replace('\n', ' ', regex=False)
df = df.fillna(0)

# Drop Unnecessary Columns
columns_to_drop = [
    'Home Score', 'Away Score', 'Book Spread (Home Team)', 'Actual Spread', 'DIFF',
    'Sum of Formulas Over', 'Temp Over Book Value', 'PPG Over Book Value', 'EFF over Book Value',
    'Sum EFF from 100', '1', 'DIFF.1', 'Sum of Formulas Under', '2', 'DIFF.2',
    'Average to Book Value', 'Sum of EFF/PPG Over', 'Absolute Value Tempo to Book',
    'Possession to Tempo', 'AVG of 3 Over', '3', 'DIFF.3', 'Absolute Value PPG to Book',
    '4', 'DIFF.4', '5', 'DIFF.5', 'Difference Tempo to Book', 'DIFF.6',
    'Difference PPG to Book', 'DIFF.7', 'Difference EFF to Book']

df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

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
tab9, tab1 = st.tabs(["Today's Games with Trends", 'Extra Info: All Trend Info']) 

with tab9:
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
        # st.markdown("""
        #     - Below "Today's Games" use the Dropdown to Select Specific Conferences
        #     - Each Game has a Dropdown with Trend Info and Team's Season Record in that Active Trend
        #         - There are 8 Trends with Various Subcategories based on KenPom Efficiencies for Each Trend
        #         - All Records are Record Against the Total (2-1 = 2 Overs to 1 Under)
        #     - Each Game has a Suggestion, Use Your Analysis and Take Games at Your Own Risk
        #     """)

    st.markdown(
    "<hr style='border: 2px solid goldenrod; margin-top: 0rem; margin-bottom: 0.5rem;'>",
    unsafe_allow_html=True)

    st.markdown(
            """
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0 auto; 
                border: 4px solid goldenrod; 
                padding: 2px; 
                border-radius: 10px; 
                width: 350px;
                height: 80px;
                font-size: 48px;
                font-weight: bold;
                background-color: #545353ff;
                color: #ffffff;
                text-align: center;">
                Today's Games
            </div>
            """,
            unsafe_allow_html=True
        )

    # Today Variable for Sorting
    today = datetime(2025, 1, 11).date()

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
        if game['All Formulas Over'] == 1:
            o = game['Offense Over 100']
            d = game['Defense Over 100']

            count_cur, win_cur, loss_cur = allover_count_win_loss_current(df, o, d)
            percent_cur = round((win_cur/count_cur)*100,2) if count_cur else 0
            count, win, loss = allover_count_win_loss(df, o, d)
            percent_all = round((win/count)*100,2) if count else 0

        elif game['All Formulas Under'] == 1:
            o = game['Offense Under 100']
            d = game['Defense Under 100']

            count_cur, win_cur, loss_cur = allunder_count_win_loss_current(df, o, d)
            percent_cur = round((win_cur/count_cur)*100,2) if count_cur else 0
            count, win, loss = allunder_count_win_loss(df, o, d)
            percent_all = round((win/count)*100,2) if count else 0

        elif game['Efficiency/PPG over  (Tempo under)'] == 1:
            o1 = game['Count of OFF over 100']
            o2 = game['Count of OFF over 110']
            d1 = game['Count of DEF under 100']
            d2 = game['Count of DEF under 95']

            count_cur, win_cur, loss_cur = EPOver_TempoUnder_count_win_loss_current(df, o1, o2, d1, d2)
            percent_cur = round((win_cur/count_cur)*100,2) if count_cur else 0
            count, win, loss = EPOver_TempoUnder_count_win_loss(df, o1, o2, d1, d2)
            percent_all = round((win/count)*100,2) if count else 0

        elif game['Tempo and Efficiency over (PPG under)'] == 1:
            o1 = game['OFF Under 100']
            o2 = game['OFF Under 95']
            d1 = game['DEF Under 100']
            d2 = game['DEF Under 95']

            count_cur, win_cur, loss_cur = TEOver_PPGUnder_count_win_loss_current(df, o1, o2, d1, d2)
            percent_cur = round((win_cur/count_cur)*100,2) if count_cur else 0
            count, win, loss = TEOver_PPGUnder_count_win_loss(df, o1, o2, d1, d2)
            percent_all = round((win/count)*100,2) if count else 0

        elif game['Tempo and PPG over (Efficiency Under)'] == 1:
            count_cur, win_cur, loss_cur = TPOver_EFFUnder_count_win_loss_current(df)
            percent_cur = round((win_cur/count_cur)*100,2) if count_cur else 0
            count, win, loss = TPOver_EFFUnder_count_win_loss(df)
            percent_all = round((win/count)*100,2) if count else 0

        elif game['Just Tempo Over'] == 1:
            val = game['Over 105 EFF']

            count_cur, win_cur, loss_cur = TempoOver_count_win_loss_current(df, val)
            percent_cur = round((win_cur/count_cur)*100,2) if count_cur else 0
            count, win, loss = TempoOver_count_win_loss(df, val)
            percent_all = round((win/count)*100,2) if count else 0

        elif game['Just PPG Over'] == 1:
            val = game['Over 110 EFF']

            count_cur, win_cur, loss_cur = PPGover_count_win_loss_current(df, val)
            percent_cur = round((win_cur/count_cur)*100,2) if count_cur else 0
            count, win, loss = PPGover_count_win_loss(df, val)
            percent_all = round((win/count)*100,2) if count else 0

        elif game['Just Efficiency Over'] == 1:
            o = game['OFF Over 105']
            d = game['DEF Over 105']

            count_cur, win_cur, loss_cur = EFFover_count_win_loss_current(df, o, d)
            percent_cur = round((win_cur/count_cur)*100,2) if count_cur else 0
            count, win, loss = EFFover_count_win_loss(df, o, d)
            percent_all = round((win/count)*100,2) if count else 0
            
        else:
            percent_cur = 'None'
            win_cur, loss_cur = 0
            count_cur = 0
            percent_all = 'None'
            win, loss = 0


        percent_cur1 = display_metrics_expand(percent_cur)
        percent_all1 = display_metrics_expand(percent_all)

        if percent_cur >= 60 and percent_all >= 55:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Strong Over"
        elif percent_cur >= 60 and 53 <= percent_all < 55:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Over"
        elif percent_cur >= 60 and 50 <= percent_all < 53:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Over / Avoid"
        elif percent_cur >= 60 and percent_all < 50:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Avoid"

        elif percent_cur >= 55 and percent_all >= 60:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Strong Over"
        elif percent_cur >= 55 and percent_all >= 55:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Over"
        elif percent_cur >= 55 and 52 <= percent_all < 55:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Over / Avoid"
        elif percent_cur >= 55 and percent_all < 52:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Avoid"

        elif 52 <= percent_cur < 55 and percent_all >= 60:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Strong Over"
        elif 52 <= percent_cur < 55 and percent_all >= 55:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Over"
        elif 52 <= percent_cur < 55 and 52 <= percent_all < 55:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Over / Avoid"
        elif 52 <= percent_cur < 55 and percent_all < 52:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Avoid"

        elif 48 < percent_cur < 52 and percent_all >= 60:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Over / Avoid"
        elif 48 < percent_cur < 52 and percent_all >= 55:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Over / Avoid"
        elif 48 < percent_cur < 52 and 46 <= percent_all < 55:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Avoid"
        elif 48 < percent_cur < 52 and 42 < percent_all < 46:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Under / Avoid"
        elif 48 < percent_cur < 52 and percent_all <= 42:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Under"

        elif 46 < percent_cur <=48 and percent_all >= 60:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Avoid"
        elif 46 < percent_cur <=48 and percent_all >= 55:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Avoid"
        elif 46 < percent_cur <=48 and 48 < percent_all < 55:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Avoid"
        elif 46 < percent_cur <=48 and 46 < percent_all <= 48:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Under / Avoid"
        elif 46 < percent_cur <=48 and 42 < percent_all <= 46:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Under"
        elif 46 < percent_cur <=48 and percent_all <= 42:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Moderate Under"

        
        elif 40 <= percent_cur <= 46 and percent_all >= 50:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Avoid"
        elif 40 <= percent_cur <= 46 and 46 <= percent_all < 50:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Under / Avoid"
        elif 40 <= percent_cur <= 46 and 40 <= percent_all <= 46:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Under"
        elif 40 <= percent_cur <= 46 and percent_all < 40:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Strong Under"

        elif percent_cur < 40 and percent_all >= 50:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Avoid"
        elif percent_cur < 40 and 48 <= percent_all < 50:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Under / Avoid"
        elif percent_cur < 40 and 40 <= percent_all < 48:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Under"
        elif percent_cur < 40 and percent_all < 40:
            pick = "<span style='color:black; font-weight:bold'>Suggestion: Strong Under"


        record_cur, units_cur, fade_cur = win_loss_record_expand(win_cur, loss_cur)
        record_all, units_all, fade_all = win_loss_record_expand(win, loss)
        
        away_logo = get_base64(f"Team Logo/{game['Away Team']}.jpg")
        home_logo = get_base64(f"Team Logo/{game['Home Team']}.jpg")

        away_img = f'<img class="team-logo" src="data:image/jpeg;base64,{away_logo}">'
        home_img = f'<img class="team-logo" src="data:image/jpeg;base64,{home_logo}">'
        
        # matchup_header = f"""
        #         <div style="line-height:1.3;">
        #             <span style="font-size:22px; font-weight:bold;">
        #                 {away_img} {game['Away Team']} @ {home_img} {game['Home Team']} &nbsp;|&nbsp; Total: {game['Book Total']}
        #             </span><br>
        #             <span style="font-size:14px;">
        #                 '25-'26 Over Win Record: {record_cur} ({percent_cur1}) <br>
        #                 All Time Trend Over Record: {record_all} ({percent_all1})
        #             </span>
        #         </div>
        #         """

        matchup_header = (
            f"{away_img} {game['Away Team']} @ &nbsp;{home_img} {game['Home Team']} "
            f"&nbsp;|&nbsp; Total: {game['Book Total']}||"
            f"'25-'26 Trend Over Record: {record_cur} {percent_cur1} &nbsp;&nbsp;|&nbsp;&nbsp; {pick}<br>"
            f"All Time Trend Over Record: {record_all} {percent_all1}"
)

                #  &nbsp;|&nbsp; Over Units: {units_cur} &nbsp;|&nbsp; Under Units: {fade_cur}
                #  &nbsp;|&nbsp; Over Units: {units_all} &nbsp;|&nbsp; Under Units: {fade_all}

        with st.container(border=False):
            if game['All Formulas Over'] == 1:
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
                st_html(details_html(matchup_header, trend_html), height=290, scrolling=True)

            
            elif game['All Formulas Under'] == 1:
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
                st_html(details_html(matchup_header, trend_html), height=290, scrolling=True)
            
            elif game['Efficiency/PPG over  (Tempo under)'] == 1:
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
                st_html(details_html(matchup_header, trend_html), height=290, scrolling=True)

            elif game['Tempo and Efficiency over (PPG under)'] == 1:
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
                st_html(details_html(matchup_header, trend_html), height=290, scrolling=True)
            
            elif game['Tempo and PPG over (Efficiency Under)'] == 1:
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
                st_html(details_html(matchup_header, trend_html), height=290, scrolling=True)

            elif game['Just Tempo Over'] == 1:
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
                st_html(details_html(matchup_header, trend_html), height=290, scrolling=True)
            
            elif game['Just PPG Over'] == 1:
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
                st_html(details_html(matchup_header, trend_html), height=290, scrolling=True)

            elif game['Just Efficiency Over'] == 1:
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
                st_html(details_html(matchup_header, trend_html), height=290, scrolling=True)

with tab1: 
    ## Trend Selection
    trend_option = st.selectbox("Choose Trend Type", [
        "All Over", "All Under", "EFF/PPG Over & Tempo Under", "Tempo/EFF Over & PPG Under",
        "PPG/Tempo Over & EFF Under", "Tempo Over", "PPG Over", "EFF Over"
    ])

    st.markdown("""
        <p style='text-align: center;'>
        **Over Net Units means how many units won by betting on the Over on every game in that trend** <br>
        **Under Net Units means how many units won by betting on the Under on every game in that trend** <br>
        """,
        unsafe_allow_html=True
    )

    if trend_option == "All Over":

        with st.expander("View Explanation of these Trends"):
            st.markdown("""
                        - All Over means all 3 of my predictive formulas were over the book total.
                        - The All Over trends are divided into subcategories based on the offensive and defensive efficiency ratings.

                        - Example: 2 OFF EFF over 100 / 2 DEF EFF over 100 means All Formulas Predicted Over the Book Total while both teams' Offensive Efficiency and Defensive Efficiency over 100. 
                        """,
                        unsafe_allow_html=True)

        subset = df[(df['All Formulas Over'] == 1)]
        combinations = [(2, 2), (2, 1), (1, 2), (1, 1), (1, 0), (0, 1), (0, 0), (0, 2), (2, 0)]

        results_all = {}
        results_cur = {}
        results_prev = {}


        for o, d in combinations:
            key = (o, d)

            count, win, loss = allover_count_win_loss(df, o, d)
            if count != 0:
                percent = round((win / count) * 100, 2)
                results_all[key] = (percent, win, loss)

            count_cur, win_cur, loss_cur = allover_count_win_loss_current(df, o, d)
            if count_cur != 0:
                percent_cur = round((win_cur / count_cur) * 100, 2)
                results_cur[key] = (percent_cur, win_cur, loss_cur)

            count_prev, win_prev, loss_prev = allover_count_win_loss_prev(df, o, d)
            if count_prev != 0:
                percent_prev = round((win_prev / count_prev) * 100, 2)
                results_prev[key] = (percent_prev, win_prev, loss_prev)

        # Sort by All Seasons win %
        sorted_combos = sorted(
            results_all.items(), 
            key=lambda x: (x[1][0] is None, -x[1][0] if x[1][0] is not None else 0)
        )

        for (o, d), (percent, win, loss) in sorted_combos:
            st.markdown(
                f"""
                <h3 style="text-align: center; font-size: 32px; text-decoration: underline; margin-bottom: 0.2rem;">
                    {o} Offense EFF over 100 / {d} Defense EFF over 100
                </h3>
                """,
                unsafe_allow_html=True
            )

            percent_cur, win_cur, loss_cur = results_cur.get((o, d), (None, 0, 0))
            percent_prev, win_prev, loss_prev = results_prev.get((o, d), (None, 0, 0))

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
                display_metrics(percent, win, loss)

            with col2:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
                display_metrics(percent_cur, win_cur, loss_cur)

            with col3:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
                display_metrics(percent_prev, win_prev, loss_prev)

            today = datetime.strptime("2/15/2025", "%m/%d/%Y").date()
            today_games = df[
            (df['Date'].dt.date == today) &
            (df['All Formulas Over'] == 1) &
            (df['Offense Over 100'] == o) &
            (df['Defense Over 100'] == d)
    ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

            # Step 1: Run your function to get records_df
            records_df = home_away_over_under_by_team(df, o, d).reset_index().rename(columns={'index': 'Team'})

            # Step 2: Prepare mapping dictionaries for quick lookup
            home_record_map = records_df.set_index('Team')['Home Record'].to_dict()
            away_record_map = records_df.set_index('Team')['Away Record'].to_dict()
            total_record_map = records_df.set_index('Team')['Total Record'].to_dict()

            # Step 3: Add new columns to today_games by mapping from the dictionaries
            today_games['Home Team Record'] = (
            "Home: " + today_games['Home Team'].map(home_record_map).fillna("N/A") +
            " | Total: " + today_games['Home Team'].map(total_record_map).fillna("N/A")
            )

            today_games['Away Team Record'] = (
            "Away: " + today_games['Away Team'].map(away_record_map).fillna("N/A") +
            " | Total: " + today_games['Away Team'].map(total_record_map).fillna("N/A")
            )

            def move_cols_after(df, cols_to_move, target_col):
                # Extract columns
                for col in cols_to_move:
                    series = df.pop(col)
                    target_idx = df.columns.get_loc(target_col) + 1
                    # Insert col after target_col
                    df.insert(target_idx, col, series)
                    # Increment target_idx for next insert so columns keep order
                    target_col = col  # So next col inserts after the last inserted

            move_cols_after(today_games, ['Home Team Record'], 'Home Team')
            move_cols_after(today_games, ['Away Team Record'], 'Away Team')

            if not today_games.empty:
                today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
                with st.expander(f"📅 Games Today for Subcategory Trend -- {o} Offense over 100 EFF / {d} Defense over 100 EFF"):
                    st.dataframe(today_games)
                    st.markdown("***This Record represents (Overs - Unders), so (4-1) would say that team has 4 overs and 1 under.***")
            else:
                st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

            # Plot histogram
            plot_df = subset[
                (subset['Offense Over 100'] == o) & 
                (subset['Defense Over 100'] == d)
            ]

            display_total_difference_histogram(plot_df)

    elif trend_option == "All Under":
        with st.expander("View Explanation of these Trends"):
            st.markdown("""
                        - All Under means all 3 of my predictive formulas were under the book total.
                        - The All Under trends are divided into subcategories based on the offensive and defensive efficiency ratings.

                        - Example: 0 OFF EFF under 100 / 0 DEF EFF under 100 means All Formulas Predicted Under the Book Total while neither teams' Offensive Efficiency and Defensive Efficiency under 100. 
                        """,
                        unsafe_allow_html=True)

        subset1 = df[(df['All Formulas Under'] == 1)]  # Filter based on condition
        combinations = [(2, 2), (2, 1), (1, 2), (1, 1), (1, 0), (0, 1), (0, 0), (0, 2), (2, 0)]
        results = []
        results_cur = []
        results_prev = []

        for o, d in combinations:
            count, win, loss = allunder_count_win_loss(df, o, d)
            if count != 0:
                percent = round((win / count) * 100, 2) if count != 0 else None
                results.append(((o, d), percent, win, loss))

            count_cur, win_cur, loss_cur = allunder_count_win_loss_current(df, o, d)
            if count_cur != 0:
                percent_cur = round((win_cur / count_cur) * 100, 2)
                results_cur.append(((o, d), percent_cur, win_cur, loss_cur))
            else:
                results_cur.append(((o, d), None, 0, 0))

            count_prev, win_prev, loss_prev = allunder_count_win_loss_prev(df, o, d)
            if count_prev != 0:
                percent_prev = round((win_prev / count_prev) * 100, 2)
                results_prev.append(((o, d), percent_prev, win_prev, loss_prev))
            else:
                results_prev.append(((o, d), None, 0, 0))

        results_cur_dict = {k: v for k, *v in results_cur}
        results_prev_dict = {k: v for k, *v in results_prev}

        # Sort by All Seasons win %
        results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

        for (o, d), percent, win, loss in results:
            st.markdown(
            f"""
            <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
                {o} Offense EFF Under 100 / {d} Defense EFF Under 100
            </h3>
            """,
            unsafe_allow_html=True
            )

            percent_cur, win_cur, loss_cur = results_cur_dict.get((o, d), (None, 0, 0))
            percent_prev, win_prev, loss_prev = results_prev_dict.get((o, d), (None, 0, 0))

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
                display_metrics_under(percent, win, loss)

            with col2:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
                display_metrics_under(percent_cur, win_cur, loss_cur)

            with col3:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
                display_metrics_under(percent_prev, win_prev, loss_prev)

            # Today's Games
            today = datetime.strptime("2/15/2025", "%m/%d/%Y").date()
            today_games = df[
            (df['Date'].dt.date == today) &
            (df['All Formulas Under'] == 1) &
            (df['Offense Under 100'] == o) &
            (df['Defense Under 100'] == d)
    ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

            # Step 1: Run your function to get records_df
            records_df = home_away_over_under_by_team_all_under(df, o, d).reset_index().rename(columns={'index': 'Team'})

            # Step 2: Prepare mapping dictionaries for quick lookup
            home_record_map = records_df.set_index('Team')['Home Record'].to_dict()
            away_record_map = records_df.set_index('Team')['Away Record'].to_dict()
            total_record_map = records_df.set_index('Team')['Total Record'].to_dict()

            # Step 3: Add new columns to today_games by mapping from the dictionaries
            today_games['Home Team Record'] = (
            "Home: " + today_games['Home Team'].map(home_record_map).fillna("N/A") +
            " | Total: " + today_games['Home Team'].map(total_record_map).fillna("N/A")
            )

            today_games['Away Team Record'] = (
            "Away: " + today_games['Away Team'].map(away_record_map).fillna("N/A") +
            " | Total: " + today_games['Away Team'].map(total_record_map).fillna("N/A")
            )

            def move_cols_after(df, cols_to_move, target_col):
                # Extract columns
                for col in cols_to_move:
                    series = df.pop(col)
                    target_idx = df.columns.get_loc(target_col) + 1
                    # Insert col after target_col
                    df.insert(target_idx, col, series)
                    # Increment target_idx for next insert so columns keep order
                    target_col = col  # So next col inserts after the last inserted

            move_cols_after(today_games, ['Home Team Record'], 'Home Team')
            move_cols_after(today_games, ['Away Team Record'], 'Away Team')

            if not today_games.empty:
                today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
                with st.expander(f"📅 Games Today for Subcategory Trend -- {o} Offense under 100 EFF / {d} Defense under 100 EFF"):
                    st.dataframe(today_games)
                    st.markdown("***This Record represents (Unders - Overs), so (4-1) would say that team has 4 unders and 1 over.***")
            else:
                st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

            plot_df = subset1[
                (subset1['Offense Under 100'] == o) & 
                (subset1['Defense Under 100'] == d)
            ]

            display_total_difference_histogram(plot_df)

    elif trend_option == "EFF/PPG Over & Tempo Under":
        with st.expander("View Explanation of these Trends"):
            st.markdown("""
                        - EFF/PPG Over & Tempo Under means Efficiency and PPG predictive formulas were over the Book Total while Tempo predictive formula was under the Book Total.
                        - The EFF/PPG Over & Tempo Under trends are divided into subcategories based on the offensive and defensive efficiency ratings.
                        - To provide better insights, offensive and defensive efficiency used two numbers each to create subcategories.

                        - Example: 2 OFF EFF over 100 and 0 Over 110 / 2 DEF EFF under 100 and 0 under 95 Subcategory Trend means EFF and PPG Formulas Predicted over the Book Total and Tempo under the Book Total while both teams' Offensive Efficiency were over 100 but below 110 and both teams' Defensive Efficiency were under 100 but over 95. 
                        """,
                        unsafe_allow_html=True)

        combinations = [(0, 0, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1), (0, 0, 2, 0), (0, 0, 2, 1), (0, 0, 2, 2),

        (1, 0, 0, 0), (1, 0, 1, 0), (1, 0, 1, 1), (1, 0, 2, 0), (1, 0, 2, 1), (1, 0, 2, 2),
        (1, 1, 0, 0), (1, 1, 1, 0), (1, 1, 1, 1), (1, 1, 2, 0), (1, 1, 2, 1), (1, 1, 2, 2),

        (2, 0, 0, 0), (2, 0, 1, 0), (2, 0, 1, 1), (2, 0, 2, 0), (2, 0, 2, 1), (2, 0, 2, 2),
        (2, 1, 0, 0), (2, 1, 1, 0), (2, 1, 1, 1), (2, 1, 2, 0), (2, 1, 2, 1), (2, 1, 2, 2),
        (2, 2, 0, 0), (2, 2, 1, 0), (2, 2, 1, 1), (2, 2, 2, 0), (2, 2, 2, 1), (2, 2, 2, 2)]

        results = []
        results_cur = []
        results_prev = []

        for o1, o2, d1, d2 in combinations:
            count, win, loss = EPOver_TempoUnder_count_win_loss(df, o1, o2, d1, d2)
            if count != 0:
                percent = round((win / count) * 100, 2) if count != 0 else None
                results.append(((o1, o2, d1, d2), percent, win, loss))

            count_cur, win_cur, loss_cur = EPOver_TempoUnder_count_win_loss_current(df, o1, o2, d1, d2)
            if count_cur != 0:
                percent_cur = round((win_cur / count_cur) * 100, 2)
                results_cur.append(((o1, o2, d1, d2), percent_cur, win_cur, loss_cur))
            else:
                results_cur.append(((o1, o2, d1, d2), None, 0, 0))

            count_prev, win_prev, loss_prev = EPOver_TempoUnder_count_win_loss_prev(df, o1, o2, d1, d2)
            if count_prev != 0:
                percent_prev = round((win_prev / count_prev) * 100, 2)
                results_prev.append(((o1, o2, d1, d2), percent_prev, win_prev, loss_prev))

            else:
                results_prev.append(((o1, o2, d1, d2), None, 0, 0))

        results_cur_dict = {k: v for k, *v in results_cur}
        results_prev_dict = {k: v for k, *v in results_prev}

        results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

        for (o1, o2, d1, d2), percent, win, loss in results:    
            st.markdown(
                f"""
                <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
                    {o1} Offense EFF Over 100 and {o2} Over 110 / {d1} Defense EFF Under 100 and {d2} Under 95
                    </h3>
                    """, unsafe_allow_html=True)

            percent_cur, win_cur, loss_cur = results_cur_dict.get((o1, o2, d1, d2), (None, 0, 0))
            percent_prev, win_prev, loss_prev = results_prev_dict.get((o1, o2, d1, d2), (None, 0, 0))

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
                display_metrics(percent, win, loss)

            with col2:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
                display_metrics(percent_cur, win_cur, loss_cur)

            with col3:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
                display_metrics(percent_prev, win_prev, loss_prev)

            # Today's Games
            today = datetime.today().date()
            today_games = df[
            (df['Date'].dt.date == today) &
                (df['Efficiency/PPG over  (Tempo under)'] == 1) &
                (df['Count of OFF over 100'] == o1) &
                (df['Count of OFF over 110'] == o2) &
                (df['Count of DEF under 100'] == d1) &
                (df['Count of DEF under 95'] == d2)
    ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

            if not today_games.empty:
                today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
                with st.expander(f"📅 Games Today for Subcategory Trend -- {o1} Offense over 100 EFF and {o2} over 110 / {d1} Defense under 100 EFF and {d2} under 95"):
                    st.dataframe(today_games)
            else:
                st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

            # Plot below metrics, centered with Streamlit's default centering
            plot_df = df[
                (df['Efficiency/PPG over  (Tempo under)'] == 1) &
                (df['Count of OFF over 100'] == o1) &
                (df['Count of OFF over 110'] == o2) &
                (df['Count of DEF under 100'] == d1) &
                (df['Count of DEF under 95'] == d2)
            ]
            display_total_difference_histogram(plot_df)

    elif trend_option == "Tempo/EFF Over & PPG Under":
        with st.expander("View Explanation of these Trends"):
            st.markdown("""
                        - Tempo/EFF Over & PPG Under means Tempo and Efficiency predictive formulas were over the Book Total while PPG predictive formula was under the Book Total.
                        - The Tempo/EFF Over & PPG Under trends are divided into subcategories based on the offensive and defensive efficiency ratings.
                        - To provide better insights, offensive and defensive efficiency used two numbers each to create subcategories.

                        - Example: 1 OFF EFF under 100 and 0 under 95 / 1 DEF EFF under 100 and 1 under 95 Subcategory Trend means EFF and Tempo Formulas Predicted over the Book Total and PPG under the Book Total while only one team's Offensive Efficiency was under 100 but above 95 and neither teams' Defensive Efficiency were under 100 or 95. 
                        """,
                        unsafe_allow_html=True)

        combinations = [(0,0,0,0), (1,0,0,0), (1,1,0,0), (1,1,1,0), (1,0,1,1), (1,0,1,0), (2,0,0,0),(2,1,0,0),(2,1,1,0)]
        results = []
        results_cur = []
        results_prev = []

        for o1, o2, d1, d2 in combinations:
            count, win, loss = TEOver_PPGUnder_count_win_loss(df, o1, o2, d1, d2)
            if count != 0:
                percent = round((win / count) * 100, 2) if count != 0 else None
                results.append(((o1, o2, d1, d2), percent, win, loss))

            count_cur, win_cur, loss_cur = TEOver_PPGUnder_count_win_loss_current(df, o1, o2, d1, d2)
            if count_cur != 0:
                percent_cur = round((win_cur / count_cur) * 100, 2)
                results_cur.append(((o1, o2, d1, d2), percent_cur, win_cur, loss_cur))
            else:
                results_cur.append(((o1, o2, d1, d2), None, 0, 0))

            count_prev, win_prev, loss_prev = TEOver_PPGUnder_count_win_loss_prev(df, o1, o2, d1, d2)
            if count_prev != 0:
                percent_prev = round((win_prev / count_prev) * 100, 2)
                results_prev.append(((o1, o2, d1, d2), percent_prev, win_prev, loss_prev))
            else:
                results_prev.append(((o1, o2, d1, d2), None, 0, 0))

        results_cur_dict = {k: v for k, *v in results_cur}
        results_prev_dict = {k: v for k, *v in results_prev}

        results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

        for (o1, o2, d1, d2), percent, win, loss in results:
            st.markdown(
                f"""
                <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
                    {o1} OFF EFF Under 100 and {o2} Under 95 / {d1} DEF EFF Under 100 and {d2} Under 95
                    </h3>
                    """, unsafe_allow_html=True)

            percent_cur, win_cur, loss_cur = results_cur_dict.get((o1, o2, d1, d2), (None, 0, 0))
            percent_prev, win_prev, loss_prev = results_prev_dict.get((o1, o2, d1, d2), (None, 0, 0))

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
                display_metrics(percent, win, loss)

            with col2:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
                display_metrics(percent_cur, win_cur, loss_cur)

            with col3:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
                display_metrics(percent_prev, win_prev, loss_prev)

            # Today's Game
            today = datetime.today().date()
            today_games = df[
            (df['Date'].dt.date == today) &
                (df['Tempo and Efficiency over (PPG under)'] == 1) &
                (df['OFF Under 100'] == o1) &
                (df['OFF Under 95'] == o2) &
                (df['DEF Under 100'] == d1) &
                (df['DEF Under 95'] == d2)
    ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

            if not today_games.empty:
                today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
                with st.expander(f"📅 Games Today for Subcategory Trend -- {o1} Offense under 100 EFF and {o2} under 95 / {d1} Defense under 100 EFF and {d2} under 95"):
                    st.dataframe(today_games)
            else:
                st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

            # Plot below metrics, centered with Streamlit's default centering
            plot_df = df[
                (df['Tempo and Efficiency over (PPG under)'] == 1) &
                (df['OFF Under 100'] == o1) &
                (df['OFF Under 95'] == o2) &
                (df['DEF Under 100'] == d1) &
                (df['DEF Under 95'] == d2)
            ]

            display_total_difference_histogram(plot_df)

    elif trend_option == "PPG/Tempo Over & EFF Under":
        with st.expander("View Explanation of these Trends"):
            st.markdown("""
                        - PPG/Tempo Over & EFF Under means PPG and Tempo predictive formulas were over the Book Total while Efficiency predictive formula was under the Book Total.
                        - The Tempo/EFF Over & PPG Under trends do not have subcategories based on the offensive and defensive efficiency ratings due to low quantity of games.
                        - 

                        - Example: Trend means EFF and Tempo Formulas Predicted over the Book Total and PPG under the Book Total with no other constraints. 
                        """,
                        unsafe_allow_html=True)

        count, win, loss = TPOver_EFFUnder_count_win_loss(df)
        if count != 0:
            percent = round((win / count) * 100, 2)
        else:
            percent, win, loss = None, 0, 0

        count_cur, win_cur, loss_cur = TPOver_EFFUnder_count_win_loss_current(df)
        if count_cur != 0:
            percent_cur = round((win_cur / count_cur) * 100, 2)
            results_cur = (percent_cur, win_cur, loss_cur)
        else:
            results_cur = (None, 0, 0)

        count_prev, win_prev, loss_prev = TPOver_EFFUnder_count_win_loss_prev(df)
        if count_prev != 0:
            percent_prev = round((win_prev / count_prev) * 100, 2)
            results_prev = (percent_prev, win_prev, loss_prev)
        else:
            results_prev = (None, 0, 0)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
            display_metrics(percent, win, loss)
        with col2:
            st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
            display_metrics(percent_cur, win_cur, loss_cur)
        with col3:
            st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
            display_metrics(percent_prev, win_prev, loss_prev)

        # Today's Game
        today = datetime.today().date()
        today_games = df[
        (df['Date'].dt.date == today) &
        (df['Tempo and PPG over (Efficiency Under)'] == 1)

    ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

        if not today_games.empty:
            today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
            with st.expander("📅 Games Today for This Trend"):
                st.dataframe(today_games)
        else:
            st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)


        # Plot below metrics, centered with Streamlit's default centering
        plot_df = df[df['Tempo and PPG over (Efficiency Under)'] == 1]

        display_total_difference_histogram(plot_df)

    elif trend_option == "Tempo Over":
        with st.expander("View Explanation of these Trends"):
            st.markdown("""
                        - Tempo Over means Tempo predictive formulas were over the Book Total while Efficiency and PPG predictive formula was under the Book Total.
                        - The Tempo Over trends are divided into subcategories based on the efficiency ratings, not specific to offensive or defensive.

                        - Example: 2 EFF over 105 Subcategory Trend means Tempo Formula Predicted over the Book Total and EFF & PPG Formulas Predicted under the Book Total while 2 of the 4 team's efficiency ratings are over 105.
                        """,
                        unsafe_allow_html=True)

        results = []
        results_cur = []
        results_prev = []

        for val in [0,1,2]:
            count, win, loss = TempoOver_count_win_loss(df, val)
            if count != 0:
                percent = round((win / count) * 100, 2) if count != 0 else None
                results.append((val, percent, win, loss))

            count_cur, win_cur, loss_cur = TempoOver_count_win_loss_current(df, val)
            if count_cur != 0:
                percent_cur = round((win_cur / count_cur) * 100, 2)
                results_cur.append((val, percent_cur, win_cur, loss_cur))
            else:
                results_cur.append((val, None, 0, 0))

            count_prev, win_prev, loss_prev = TempoOver_count_win_loss_prev(df, val)
            if count_prev != 0:
                percent_prev = round((win_prev / count_prev) * 100, 2)
                results_prev.append((val, percent_prev, win_prev, loss_prev))
            else:
                results_prev.append((val, None, 0, 0))

        results_cur_dict = {k: v for k, *v in results_cur}
        results_prev_dict = {k: v for k, *v in results_prev}

        results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

        for val, percent, win, loss in results:
            st.markdown(
                f"""
                <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
                    {val} EFF Over 105
                </h3>
                """,unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
                display_metrics(percent, win, loss)
            with col2:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
                percent_cur, win_cur, loss_cur = results_cur_dict.get(val, (None, 0, 0))
                display_metrics(percent_cur, win_cur, loss_cur)
            with col3:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
                percent_prev, win_prev, loss_prev = results_prev_dict.get(val, (None, 0, 0))
                display_metrics(percent_prev, win_prev, loss_prev)

            # Today's Game
            today = datetime.today().date()
            today_games = df[
            (df['Date'].dt.date == today) &
                (df['Just Tempo Over'] == 1) &
                        (df['Over 105 EFF'] == val)
    ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

            if not today_games.empty:
                today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
                with st.expander(f"📅 Games Today for Subcategory Trend -- {val} Over 105 EFF"):
                    st.dataframe(today_games)
            else:
                st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)        

            # Plot below metrics, centered with Streamlit's default centering
            plot_df = df[(df['Just Tempo Over'] == 1) &
                        (df['Over 105 EFF'] == val)]

            display_total_difference_histogram(plot_df)

    elif trend_option == "PPG Over":
        with st.expander("View Explanation of these Trends"):
            st.markdown("""
                        - PPG Over means PPG predictive formulas were over the Book Total while Efficiency and Tempo predictive formula was under the Book Total.
                        - The PPG Over trends are divided into subcategories based on the efficiency ratings, not specific to offensive or defensive.

                        - Example: 3 EFF over 110 Subcategory Trend means PPG Formula Predicted over the Book Total and EFF & Tempo Formulas Predicted under the Book Total while 3 of the 4 team's efficiency ratings are over 110.
                        """,
                        unsafe_allow_html=True)

        results = []
        results_cur = []
        results_prev = []

        for val in [0,1,2,3]:
            count, win, loss = PPGover_count_win_loss(df, val)
            if count != 0:
                percent = round((win / count) * 100, 2) if count != 0 else None
                results.append((val, percent, win, loss))
            count_cur, win_cur, loss_cur = PPGover_count_win_loss_current(df, val)
            if count_cur != 0:
                percent_cur = round((win_cur / count_cur) * 100, 2)
                results_cur.append((val, percent_cur, win_cur, loss_cur))
            else:
                results_cur.append((val, None, 0, 0))
            count_prev, win_prev, loss_prev = PPGover_count_win_loss_prev(df, val)
            if count_prev != 0:
                percent_prev = round((win_prev / count_prev) * 100, 2)
                results_prev.append((val, percent_prev, win_prev, loss_prev))
            else:
                results_prev.append((val, None, 0, 0))

        results_cur_dict = {k: v for k, *v in results_cur}
        results_prev_dict = {k: v for k, *v in results_prev}

        results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

        for val, percent, win, loss in results:
            st.markdown(
                f"""
                <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
                    {val} EFF Over 110
                </h3>
                """,unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
                display_metrics(percent, win, loss)
            with col2:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
                percent_cur, win_cur, loss_cur = results_cur_dict.get(val, (None, 0, 0))
                display_metrics(percent_cur, win_cur, loss_cur)
            with col3:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
                percent_prev, win_prev, loss_prev = results_prev_dict.get(val, (None, 0, 0))
                display_metrics(percent_prev, win_prev, loss_prev)

            # Today's Game
            today = datetime.today().date()
            today_games = df[
            (df['Date'].dt.date == today) &
                (df['Just PPG Over'] == 1) &
                (df['Over 110 EFF'] == val)
    ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

            if not today_games.empty:
                today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
                with st.expander(f"📅 Games Today for Subcategory Trend -- {val} Over 110 EFF"):
                    st.dataframe(today_games)
            else:
                st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

            # Plot below metrics, centered with Streamlit's default centering
            plot_df = df[(df['Just PPG Over'] == 1) &
                        (df['Over 110 EFF'] == val)]

            display_total_difference_histogram(plot_df)

    elif trend_option == "EFF Over":
        with st.expander("View Explanation of these Trends"):
            st.markdown("""
                        - EFF Over means Efficiency predictive formulas were over the Book Total while PPG and Tempo predictive formula was under the Book Total.
                        - The EFF Over trends are divided into subcategories based on the offensive and defensive efficiency ratings.

                        - Example: 0 OFF EFF over 105 and 0 DEF EFF over 105 Subcategory Trend means EFF Formula Predicted over the Book Total and PPG & Tempo Formulas Predicted under the Book Total while neither teams' offensive or defensive ratings were over 105.
                        """,
                        unsafe_allow_html=True)

        combinations = [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1),(2,2)]
        results = []
        results_cur = []
        results_prev = []

        for o, d in combinations:
            count, win, loss = EFFover_count_win_loss(df, o, d)
            if count != 0:
                percent = round((win / count) * 100, 2) if count != 0 else None
                results.append(((o, d), percent, win, loss))

            count_cur, win_cur, loss_cur = EFFover_count_win_loss_current(df, o, d)
            if count_cur != 0:
                percent_cur = round((win_cur / count_cur) * 100, 2)
                results_cur.append(((o, d), percent_cur, win_cur, loss_cur))
            else:
                results_cur.append(((o, d), None, 0, 0))

            count_prev, win_prev, loss_prev = EFFover_count_win_loss_prev(df, o, d)
            if count_prev != 0:
                percent_prev = round((win_prev / count_prev) * 100, 2)
                results_prev.append(((o, d), percent_prev, win_prev, loss_prev))
            else:
                results_prev.append(((o, d), None, 0, 0))

        results_cur_dict = {k: v for k, *v in results_cur}
        results_prev_dict = {k: v for k, *v in results_prev}

        results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

        for (o, d), percent, win, loss in results:
            st.markdown(
                f"""
                <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
                    {o} Offense EFF Over 105 / {d} Defense EFF Over 105
                </h3>
                """,unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
                display_metrics(percent, win, loss)
            with col2:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
                percent_cur, win_cur, loss_cur = results_cur_dict.get((o, d), (None, 0, 0))
                display_metrics(percent_cur, win_cur, loss_cur)
            with col3:
                st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
                percent_prev, win_prev, loss_prev = results_prev_dict.get((o, d), (None, 0, 0))
                display_metrics(percent_prev, win_prev, loss_prev)

            # Today's Game
            today = datetime.today().date()
            today_games = df[
            (df['Date'].dt.date == today) &
                (df['Just Efficiency Over'] == 1) &
                (df['OFF Over 105'] == o) &
                (df['DEF Over 105'] == d)
    ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

            if not today_games.empty:
                today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
                with st.expander(f"📅 Games Today for Subcategory Trend -- {o} OFF Over 105 EFF and {d} DEF Over 105 EFF"):
                    st.dataframe(today_games)
            else:
                st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

            # Plot below metrics, centered with Streamlit's default centering
            plot_df = df[
                (df['Just Efficiency Over'] == 1) &
                (df['OFF Over 105'] == o) &
                (df['DEF Over 105'] == d)
            ]

            display_total_difference_histogram(plot_df)

#     with st.expander("View Explanation of these Trends"):
#         st.markdown("""
#                     - All Over means all 3 of my predictive formulas were over the book total.
#                     - The All Over trends are divided into subcategories based on the offensive and defensive efficiency ratings.

#                     - Example: 2 OFF EFF over 100 / 2 DEF EFF over 100 means All Formulas Predicted Over the Book Total while both teams' Offensive Efficiency and Defensive Efficiency over 100. 
#                     """,
#                     unsafe_allow_html=True)
    
#     subset = df[(df['All Formulas Over'] == 1)]
#     combinations = [(2, 2), (2, 1), (1, 2), (1, 1), (1, 0), (0, 1), (0, 0), (0, 2), (2, 0)]

#     results_all = {}
#     results_cur = {}
#     results_prev = {}

#     for o, d in combinations:
#         key = (o, d)

#         count, win, loss = allover_count_win_loss(df, o, d)
#         if count != 0:
#             percent = round((win / count) * 100, 2)
#             results_all[key] = (percent, win, loss)

#         count_cur, win_cur, loss_cur = allover_count_win_loss_current(df, o, d)
#         if count_cur != 0:
#             percent_cur = round((win_cur / count_cur) * 100, 2)
#             results_cur[key] = (percent_cur, win_cur, loss_cur)

#         count_prev, win_prev, loss_prev = allover_count_win_loss_prev(df, o, d)
#         if count_prev != 0:
#             percent_prev = round((win_prev / count_prev) * 100, 2)
#             results_prev[key] = (percent_prev, win_prev, loss_prev)

#     # Sort by All Seasons win %
#     sorted_combos = sorted(
#         results_all.items(), 
#         key=lambda x: (x[1][0] is None, -x[1][0] if x[1][0] is not None else 0)
#     )

#     for (o, d), (percent, win, loss) in sorted_combos:
#         st.markdown(
#             f"""
#             <h3 style="text-align: center; font-size: 32px; text-decoration: underline; margin-bottom: 0.2rem;">
#                 {o} Offense EFF over 100 / {d} Defense EFF over 100
#             </h3>
#             """,
#             unsafe_allow_html=True
#         )

#         percent_cur, win_cur, loss_cur = results_cur.get((o, d), (None, 0, 0))
#         percent_prev, win_prev, loss_prev = results_prev.get((o, d), (None, 0, 0))

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
#             display_metrics(percent, win, loss)

#         with col2:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
#             display_metrics(percent_cur, win_cur, loss_cur)

#         with col3:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
#             display_metrics(percent_prev, win_prev, loss_prev)

#         today = datetime.strptime("2/15/2025", "%m/%d/%Y").date()
#         today_games = df[
#         (df['Date'].dt.date == today) &
#         (df['All Formulas Over'] == 1) &
#         (df['Offense Over 100'] == o) &
#         (df['Defense Over 100'] == d)
# ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

#         # Step 1: Run your function to get records_df
#         records_df = home_away_over_under_by_team(df, o, d).reset_index().rename(columns={'index': 'Team'})

#         # Step 2: Prepare mapping dictionaries for quick lookup
#         home_record_map = records_df.set_index('Team')['Home Record'].to_dict()
#         away_record_map = records_df.set_index('Team')['Away Record'].to_dict()
#         total_record_map = records_df.set_index('Team')['Total Record'].to_dict()

#         # Step 3: Add new columns to today_games by mapping from the dictionaries
#         today_games['Home Team Record'] = (
#         "Home: " + today_games['Home Team'].map(home_record_map).fillna("N/A") +
#         " | Total: " + today_games['Home Team'].map(total_record_map).fillna("N/A")
#         )

#         today_games['Away Team Record'] = (
#         "Away: " + today_games['Away Team'].map(away_record_map).fillna("N/A") +
#         " | Total: " + today_games['Away Team'].map(total_record_map).fillna("N/A")
#         )

#         def move_cols_after(df, cols_to_move, target_col):
#             # Extract columns
#             for col in cols_to_move:
#                 series = df.pop(col)
#                 target_idx = df.columns.get_loc(target_col) + 1
#                 # Insert col after target_col
#                 df.insert(target_idx, col, series)
#                 # Increment target_idx for next insert so columns keep order
#                 target_col = col  # So next col inserts after the last inserted

#         move_cols_after(today_games, ['Home Team Record'], 'Home Team')
#         move_cols_after(today_games, ['Away Team Record'], 'Away Team')

#         if not today_games.empty:
#             today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
#             with st.expander(f"📅 Games Today for Subcategory Trend -- {o} Offense over 100 EFF / {d} Defense over 100 EFF"):
#                 st.dataframe(today_games)
#                 st.markdown("***This Record represents (Overs - Unders), so (4-1) would say that team has 4 overs and 1 under.***")
#         else:
#             st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

#         # Plot histogram
#         plot_df = subset[
#             (subset['Offense Over 100'] == o) & 
#             (subset['Defense Over 100'] == d)
#         ]

#         display_total_difference_histogram(plot_df)

# with tab2:
#     with st.expander("View Explanation of these Trends"):
#         st.markdown("""
#                     - All Under means all 3 of my predictive formulas were under the book total.
#                     - The All Under trends are divided into subcategories based on the offensive and defensive efficiency ratings.

#                     - Example: 0 OFF EFF under 100 / 0 DEF EFF under 100 means All Formulas Predicted Under the Book Total while neither teams' Offensive Efficiency and Defensive Efficiency under 100. 
#                     """,
#                     unsafe_allow_html=True)

#     subset1 = df[(df['All Formulas Under'] == 1)]  # Filter based on condition
#     combinations = [(2, 2), (2, 1), (1, 2), (1, 1), (1, 0), (0, 1), (0, 0), (0, 2), (2, 0)]
#     results = []
#     results_cur = []
#     results_prev = []

#     for o, d in combinations:
#         count, win, loss = allunder_count_win_loss(df, o, d)
#         if count != 0:
#             percent = round((win / count) * 100, 2) if count != 0 else None
#             results.append(((o, d), percent, win, loss))

#         count_cur, win_cur, loss_cur = allunder_count_win_loss_current(df, o, d)
#         if count_cur != 0:
#             percent_cur = round((win_cur / count_cur) * 100, 2)
#             results_cur.append(((o, d), percent_cur, win_cur, loss_cur))
#         else:
#             results_cur.append(((o, d), None, 0, 0))

#         count_prev, win_prev, loss_prev = allunder_count_win_loss_prev(df, o, d)
#         if count_prev != 0:
#             percent_prev = round((win_prev / count_prev) * 100, 2)
#             results_prev.append(((o, d), percent_prev, win_prev, loss_prev))
#         else:
#             results_prev.append(((o, d), None, 0, 0))

#     results_cur_dict = {k: v for k, *v in results_cur}
#     results_prev_dict = {k: v for k, *v in results_prev}

#     # Sort by All Seasons win %
#     results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

#     for (o, d), percent, win, loss in results:
#         st.markdown(
#         f"""
#         <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
#             {o} Offense EFF Under 100 / {d} Defense EFF Under 100
#         </h3>
#         """,
#         unsafe_allow_html=True
#         )

#         percent_cur, win_cur, loss_cur = results_cur_dict.get((o, d), (None, 0, 0))
#         percent_prev, win_prev, loss_prev = results_prev_dict.get((o, d), (None, 0, 0))

#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
#             display_metrics_under(percent, win, loss)

#         with col2:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
#             display_metrics_under(percent_cur, win_cur, loss_cur)

#         with col3:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
#             display_metrics_under(percent_prev, win_prev, loss_prev)

#         # Today's Games
#         today = datetime.strptime("2/15/2025", "%m/%d/%Y").date()
#         today_games = df[
#         (df['Date'].dt.date == today) &
#         (df['All Formulas Under'] == 1) &
#         (df['Offense Under 100'] == o) &
#         (df['Defense Under 100'] == d)
# ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]
        
#         # Step 1: Run your function to get records_df
#         records_df = home_away_over_under_by_team_all_under(df, o, d).reset_index().rename(columns={'index': 'Team'})

#         # Step 2: Prepare mapping dictionaries for quick lookup
#         home_record_map = records_df.set_index('Team')['Home Record'].to_dict()
#         away_record_map = records_df.set_index('Team')['Away Record'].to_dict()
#         total_record_map = records_df.set_index('Team')['Total Record'].to_dict()

#         # Step 3: Add new columns to today_games by mapping from the dictionaries
#         today_games['Home Team Record'] = (
#         "Home: " + today_games['Home Team'].map(home_record_map).fillna("N/A") +
#         " | Total: " + today_games['Home Team'].map(total_record_map).fillna("N/A")
#         )

#         today_games['Away Team Record'] = (
#         "Away: " + today_games['Away Team'].map(away_record_map).fillna("N/A") +
#         " | Total: " + today_games['Away Team'].map(total_record_map).fillna("N/A")
#         )

#         def move_cols_after(df, cols_to_move, target_col):
#             # Extract columns
#             for col in cols_to_move:
#                 series = df.pop(col)
#                 target_idx = df.columns.get_loc(target_col) + 1
#                 # Insert col after target_col
#                 df.insert(target_idx, col, series)
#                 # Increment target_idx for next insert so columns keep order
#                 target_col = col  # So next col inserts after the last inserted

#         move_cols_after(today_games, ['Home Team Record'], 'Home Team')
#         move_cols_after(today_games, ['Away Team Record'], 'Away Team')

#         if not today_games.empty:
#             today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
#             with st.expander(f"📅 Games Today for Subcategory Trend -- {o} Offense under 100 EFF / {d} Defense under 100 EFF"):
#                 st.dataframe(today_games)
#                 st.markdown("***This Record represents (Unders - Overs), so (4-1) would say that team has 4 unders and 1 over.***")
#         else:
#             st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

#         plot_df = subset1[
#             (subset1['Offense Under 100'] == o) & 
#             (subset1['Defense Under 100'] == d)
#         ]

#         display_total_difference_histogram(plot_df)

# with tab3:
#     with st.expander("View Explanation of these Trends"):
#         st.markdown("""
#                     - EFF/PPG Over & Tempo Under means Efficiency and PPG predictive formulas were over the Book Total while Tempo predictive formula was under the Book Total.
#                     - The EFF/PPG Over & Tempo Under trends are divided into subcategories based on the offensive and defensive efficiency ratings.
#                     - To provide better insights, offensive and defensive efficiency used two numbers each to create subcategories.

#                     - Example: 2 OFF EFF over 100 and 0 Over 110 / 2 DEF EFF under 100 and 0 under 95 Subcategory Trend means EFF and PPG Formulas Predicted over the Book Total and Tempo under the Book Total while both teams' Offensive Efficiency were over 100 but below 110 and both teams' Defensive Efficiency were under 100 but over 95. 
#                     """,
#                     unsafe_allow_html=True)

#     combinations = [(0, 0, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1), (0, 0, 2, 0), (0, 0, 2, 1), (0, 0, 2, 2),
    
#     (1, 0, 0, 0), (1, 0, 1, 0), (1, 0, 1, 1), (1, 0, 2, 0), (1, 0, 2, 1), (1, 0, 2, 2),
#     (1, 1, 0, 0), (1, 1, 1, 0), (1, 1, 1, 1), (1, 1, 2, 0), (1, 1, 2, 1), (1, 1, 2, 2),
    
#     (2, 0, 0, 0), (2, 0, 1, 0), (2, 0, 1, 1), (2, 0, 2, 0), (2, 0, 2, 1), (2, 0, 2, 2),
#     (2, 1, 0, 0), (2, 1, 1, 0), (2, 1, 1, 1), (2, 1, 2, 0), (2, 1, 2, 1), (2, 1, 2, 2),
#     (2, 2, 0, 0), (2, 2, 1, 0), (2, 2, 1, 1), (2, 2, 2, 0), (2, 2, 2, 1), (2, 2, 2, 2)]

#     results = []
#     results_cur = []
#     results_prev = []

#     for o1, o2, d1, d2 in combinations:
#         count, win, loss = EPOver_TempoUnder_count_win_loss(df, o1, o2, d1, d2)
#         if count != 0:
#             percent = round((win / count) * 100, 2) if count != 0 else None
#             results.append(((o1, o2, d1, d2), percent, win, loss))

#         count_cur, win_cur, loss_cur = EPOver_TempoUnder_count_win_loss_current(df, o1, o2, d1, d2)
#         if count_cur != 0:
#             percent_cur = round((win_cur / count_cur) * 100, 2)
#             results_cur.append(((o1, o2, d1, d2), percent_cur, win_cur, loss_cur))
#         else:
#             results_cur.append(((o1, o2, d1, d2), None, 0, 0))

#         count_prev, win_prev, loss_prev = EPOver_TempoUnder_count_win_loss_prev(df, o1, o2, d1, d2)
#         if count_prev != 0:
#             percent_prev = round((win_prev / count_prev) * 100, 2)
#             results_prev.append(((o1, o2, d1, d2), percent_prev, win_prev, loss_prev))

#         else:
#             results_prev.append(((o1, o2, d1, d2), None, 0, 0))

#     results_cur_dict = {k: v for k, *v in results_cur}
#     results_prev_dict = {k: v for k, *v in results_prev}

#     results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

#     for (o1, o2, d1, d2), percent, win, loss in results:    
#         st.markdown(
#             f"""
#             <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
#                 {o1} Offense EFF Over 100 and {o2} Over 110 / {d1} Defense EFF Under 100 and {d2} Under 95
#                 </h3>
#                 """, unsafe_allow_html=True)
        
#         percent_cur, win_cur, loss_cur = results_cur_dict.get((o1, o2, d1, d2), (None, 0, 0))
#         percent_prev, win_prev, loss_prev = results_prev_dict.get((o1, o2, d1, d2), (None, 0, 0))

#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
#             display_metrics(percent, win, loss)
        
#         with col2:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
#             display_metrics(percent_cur, win_cur, loss_cur)
        
#         with col3:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
#             display_metrics(percent_prev, win_prev, loss_prev)

#         # Today's Games
#         today = datetime.today().date()
#         today_games = df[
#         (df['Date'].dt.date == today) &
#             (df['Efficiency/PPG over  (Tempo under)'] == 1) &
#             (df['Count of OFF over 100'] == o1) &
#             (df['Count of OFF over 110'] == o2) &
#             (df['Count of DEF under 100'] == d1) &
#             (df['Count of DEF under 95'] == d2)
# ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

#         if not today_games.empty:
#             today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
#             with st.expander(f"📅 Games Today for Subcategory Trend -- {o1} Offense over 100 EFF and {o2} over 110 / {d1} Defense under 100 EFF and {d2} under 95"):
#                 st.dataframe(today_games)
#         else:
#             st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

#         # Plot below metrics, centered with Streamlit's default centering
#         plot_df = df[
#             (df['Efficiency/PPG over  (Tempo under)'] == 1) &
#             (df['Count of OFF over 100'] == o1) &
#             (df['Count of OFF over 110'] == o2) &
#             (df['Count of DEF under 100'] == d1) &
#             (df['Count of DEF under 95'] == d2)
#         ]
#         display_total_difference_histogram(plot_df)

# with tab4:
#     with st.expander("View Explanation of these Trends"):
#         st.markdown("""
#                     - Tempo/EFF Over & PPG Under means Tempo and Efficiency predictive formulas were over the Book Total while PPG predictive formula was under the Book Total.
#                     - The Tempo/EFF Over & PPG Under trends are divided into subcategories based on the offensive and defensive efficiency ratings.
#                     - To provide better insights, offensive and defensive efficiency used two numbers each to create subcategories.

#                     - Example: 1 OFF EFF under 100 and 0 under 95 / 1 DEF EFF under 100 and 1 under 95 Subcategory Trend means EFF and Tempo Formulas Predicted over the Book Total and PPG under the Book Total while only one team's Offensive Efficiency was under 100 but above 95 and neither teams' Defensive Efficiency were under 100 or 95. 
#                     """,
#                     unsafe_allow_html=True)

#     combinations = [(0,0,0,0), (1,0,0,0), (1,1,0,0), (1,1,1,0), (1,0,1,1), (1,0,1,0), (2,0,0,0),(2,1,0,0),(2,1,1,0)]
#     results = []
#     results_cur = []
#     results_prev = []

#     for o1, o2, d1, d2 in combinations:
#         count, win, loss = TEOver_PPGUnder_count_win_loss(df, o1, o2, d1, d2)
#         if count != 0:
#             percent = round((win / count) * 100, 2) if count != 0 else None
#             results.append(((o1, o2, d1, d2), percent, win, loss))

#         count_cur, win_cur, loss_cur = TEOver_PPGUnder_count_win_loss_current(df, o1, o2, d1, d2)
#         if count_cur != 0:
#             percent_cur = round((win_cur / count_cur) * 100, 2)
#             results_cur.append(((o1, o2, d1, d2), percent_cur, win_cur, loss_cur))
#         else:
#             results_cur.append(((o1, o2, d1, d2), None, 0, 0))

#         count_prev, win_prev, loss_prev = TEOver_PPGUnder_count_win_loss_prev(df, o1, o2, d1, d2)
#         if count_prev != 0:
#             percent_prev = round((win_prev / count_prev) * 100, 2)
#             results_prev.append(((o1, o2, d1, d2), percent_prev, win_prev, loss_prev))
#         else:
#             results_prev.append(((o1, o2, d1, d2), None, 0, 0))

#     results_cur_dict = {k: v for k, *v in results_cur}
#     results_prev_dict = {k: v for k, *v in results_prev}

#     results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

#     for (o1, o2, d1, d2), percent, win, loss in results:
#         st.markdown(
#             f"""
#             <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
#                 {o1} OFF EFF Under 100 and {o2} Under 95 / {d1} DEF EFF Under 100 and {d2} Under 95
#                 </h3>
#                 """, unsafe_allow_html=True)
        
#         percent_cur, win_cur, loss_cur = results_cur_dict.get((o1, o2, d1, d2), (None, 0, 0))
#         percent_prev, win_prev, loss_prev = results_prev_dict.get((o1, o2, d1, d2), (None, 0, 0))

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
#             display_metrics(percent, win, loss)

#         with col2:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
#             display_metrics(percent_cur, win_cur, loss_cur)

#         with col3:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
#             display_metrics(percent_prev, win_prev, loss_prev)

#         # Today's Game
#         today = datetime.today().date()
#         today_games = df[
#         (df['Date'].dt.date == today) &
#             (df['Tempo and Efficiency over (PPG under)'] == 1) &
#             (df['OFF Under 100'] == o1) &
#             (df['OFF Under 95'] == o2) &
#             (df['DEF Under 100'] == d1) &
#             (df['DEF Under 95'] == d2)
# ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

#         if not today_games.empty:
#             today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
#             with st.expander(f"📅 Games Today for Subcategory Trend -- {o1} Offense under 100 EFF and {o2} under 95 / {d1} Defense under 100 EFF and {d2} under 95"):
#                 st.dataframe(today_games)
#         else:
#             st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

#         # Plot below metrics, centered with Streamlit's default centering
#         plot_df = df[
#             (df['Tempo and Efficiency over (PPG under)'] == 1) &
#             (df['OFF Under 100'] == o1) &
#             (df['OFF Under 95'] == o2) &
#             (df['DEF Under 100'] == d1) &
#             (df['DEF Under 95'] == d2)
#         ]
        
#         display_total_difference_histogram(plot_df)

# with tab5:
#     with st.expander("View Explanation of these Trends"):
#         st.markdown("""
#                     - PPG/Tempo Over & EFF Under means PPG and Tempo predictive formulas were over the Book Total while Efficiency predictive formula was under the Book Total.
#                     - The Tempo/EFF Over & PPG Under trends do not have subcategories based on the offensive and defensive efficiency ratings due to low quantity of games.
#                     - 

#                     - Example: Trend means EFF and Tempo Formulas Predicted over the Book Total and PPG under the Book Total with no other constraints. 
#                     """,
#                     unsafe_allow_html=True)

#     count, win, loss = TPOver_EFFUnder_count_win_loss(df)
#     if count != 0:
#         percent = round((win / count) * 100, 2)
#     else:
#         percent, win, loss = None, 0, 0

#     count_cur, win_cur, loss_cur = TPOver_EFFUnder_count_win_loss_current(df)
#     if count_cur != 0:
#         percent_cur = round((win_cur / count_cur) * 100, 2)
#         results_cur = (percent_cur, win_cur, loss_cur)
#     else:
#         results_cur = (None, 0, 0)

#     count_prev, win_prev, loss_prev = TPOver_EFFUnder_count_win_loss_prev(df)
#     if count_prev != 0:
#         percent_prev = round((win_prev / count_prev) * 100, 2)
#         results_prev = (percent_prev, win_prev, loss_prev)
#     else:
#         results_prev = (None, 0, 0)
    
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
#         display_metrics(percent, win, loss)
#     with col2:
#         st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
#         display_metrics(percent_cur, win_cur, loss_cur)
#     with col3:
#         st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
#         display_metrics(percent_prev, win_prev, loss_prev)

#     # Today's Game
#     today = datetime.today().date()
#     today_games = df[
#     (df['Date'].dt.date == today) &
#     (df['Tempo and PPG over (Efficiency Under)'] == 1)

# ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

#     if not today_games.empty:
#         today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
#         with st.expander("📅 Games Today for This Trend"):
#             st.dataframe(today_games)
#     else:
#         st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)


#     # Plot below metrics, centered with Streamlit's default centering
#     plot_df = df[df['Tempo and PPG over (Efficiency Under)'] == 1]

#     display_total_difference_histogram(plot_df)

# with tab6:
#     with st.expander("View Explanation of these Trends"):
#         st.markdown("""
#                     - Tempo Over means Tempo predictive formulas were over the Book Total while Efficiency and PPG predictive formula was under the Book Total.
#                     - The Tempo Over trends are divided into subcategories based on the efficiency ratings, not specific to offensive or defensive.

#                     - Example: 2 EFF over 105 Subcategory Trend means Tempo Formula Predicted over the Book Total and EFF & PPG Formulas Predicted under the Book Total while 2 of the 4 team's efficiency ratings are over 105.
#                     """,
#                     unsafe_allow_html=True)

#     results = []
#     results_cur = []
#     results_prev = []

#     for val in [0,1,2]:
#         count, win, loss = TempoOver_count_win_loss(df, val)
#         if count != 0:
#             percent = round((win / count) * 100, 2) if count != 0 else None
#             results.append((val, percent, win, loss))

#         count_cur, win_cur, loss_cur = TempoOver_count_win_loss_current(df, val)
#         if count_cur != 0:
#             percent_cur = round((win_cur / count_cur) * 100, 2)
#             results_cur.append((val, percent_cur, win_cur, loss_cur))
#         else:
#             results_cur.append((val, None, 0, 0))
        
#         count_prev, win_prev, loss_prev = TempoOver_count_win_loss_prev(df, val)
#         if count_prev != 0:
#             percent_prev = round((win_prev / count_prev) * 100, 2)
#             results_prev.append((val, percent_prev, win_prev, loss_prev))
#         else:
#             results_prev.append((val, None, 0, 0))

#     results_cur_dict = {k: v for k, *v in results_cur}
#     results_prev_dict = {k: v for k, *v in results_prev}

#     results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

#     for val, percent, win, loss in results:
#         st.markdown(
#             f"""
#             <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
#                 {val} EFF Over 105
#             </h3>
#             """,unsafe_allow_html=True
#         )
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
#             display_metrics(percent, win, loss)
#         with col2:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
#             percent_cur, win_cur, loss_cur = results_cur_dict.get(val, (None, 0, 0))
#             display_metrics(percent_cur, win_cur, loss_cur)
#         with col3:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
#             percent_prev, win_prev, loss_prev = results_prev_dict.get(val, (None, 0, 0))
#             display_metrics(percent_prev, win_prev, loss_prev)
        
#         # Today's Game
#         today = datetime.today().date()
#         today_games = df[
#         (df['Date'].dt.date == today) &
#             (df['Just Tempo Over'] == 1) &
#                      (df['Over 105 EFF'] == val)
# ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

#         if not today_games.empty:
#             today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
#             with st.expander(f"📅 Games Today for Subcategory Trend -- {val} Over 105 EFF"):
#                 st.dataframe(today_games)
#         else:
#             st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)        

#         # Plot below metrics, centered with Streamlit's default centering
#         plot_df = df[(df['Just Tempo Over'] == 1) &
#                      (df['Over 105 EFF'] == val)]
        
#         display_total_difference_histogram(plot_df)

# with tab7:
#     with st.expander("View Explanation of these Trends"):
#         st.markdown("""
#                     - PPG Over means PPG predictive formulas were over the Book Total while Efficiency and Tempo predictive formula was under the Book Total.
#                     - The PPG Over trends are divided into subcategories based on the efficiency ratings, not specific to offensive or defensive.

#                     - Example: 3 EFF over 110 Subcategory Trend means PPG Formula Predicted over the Book Total and EFF & Tempo Formulas Predicted under the Book Total while 3 of the 4 team's efficiency ratings are over 110.
#                     """,
#                     unsafe_allow_html=True)

#     results = []
#     results_cur = []
#     results_prev = []

#     for val in [0,1,2,3]:
#         count, win, loss = PPGover_count_win_loss(df, val)
#         if count != 0:
#             percent = round((win / count) * 100, 2) if count != 0 else None
#             results.append((val, percent, win, loss))
#         count_cur, win_cur, loss_cur = PPGover_count_win_loss_current(df, val)
#         if count_cur != 0:
#             percent_cur = round((win_cur / count_cur) * 100, 2)
#             results_cur.append((val, percent_cur, win_cur, loss_cur))
#         else:
#             results_cur.append((val, None, 0, 0))
#         count_prev, win_prev, loss_prev = PPGover_count_win_loss_prev(df, val)
#         if count_prev != 0:
#             percent_prev = round((win_prev / count_prev) * 100, 2)
#             results_prev.append((val, percent_prev, win_prev, loss_prev))
#         else:
#             results_prev.append((val, None, 0, 0))
    
#     results_cur_dict = {k: v for k, *v in results_cur}
#     results_prev_dict = {k: v for k, *v in results_prev}
    
#     results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

#     for val, percent, win, loss in results:
#         st.markdown(
#             f"""
#             <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
#                 {val} EFF Over 110
#             </h3>
#             """,unsafe_allow_html=True
#         )
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
#             display_metrics(percent, win, loss)
#         with col2:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
#             percent_cur, win_cur, loss_cur = results_cur_dict.get(val, (None, 0, 0))
#             display_metrics(percent_cur, win_cur, loss_cur)
#         with col3:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
#             percent_prev, win_prev, loss_prev = results_prev_dict.get(val, (None, 0, 0))
#             display_metrics(percent_prev, win_prev, loss_prev)
        
#         # Today's Game
#         today = datetime.today().date()
#         today_games = df[
#         (df['Date'].dt.date == today) &
#             (df['Just PPG Over'] == 1) &
#             (df['Over 110 EFF'] == val)
# ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

#         if not today_games.empty:
#             today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
#             with st.expander(f"📅 Games Today for Subcategory Trend -- {val} Over 110 EFF"):
#                 st.dataframe(today_games)
#         else:
#             st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

#         # Plot below metrics, centered with Streamlit's default centering
#         plot_df = df[(df['Just PPG Over'] == 1) &
#                      (df['Over 110 EFF'] == val)]
        
#         display_total_difference_histogram(plot_df)

# with tab8:
#     with st.expander("View Explanation of these Trends"):
#         st.markdown("""
#                     - EFF Over means Efficiency predictive formulas were over the Book Total while PPG and Tempo predictive formula was under the Book Total.
#                     - The EFF Over trends are divided into subcategories based on the offensive and defensive efficiency ratings.

#                     - Example: 0 OFF EFF over 105 and 0 DEF EFF over 105 Subcategory Trend means EFF Formula Predicted over the Book Total and PPG & Tempo Formulas Predicted under the Book Total while neither teams' offensive or defensive ratings were over 105.
#                     """,
#                     unsafe_allow_html=True)

#     combinations = [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1),(2,2)]
#     results = []
#     results_cur = []
#     results_prev = []

#     for o, d in combinations:
#         count, win, loss = EFFover_count_win_loss(df, o, d)
#         if count != 0:
#             percent = round((win / count) * 100, 2) if count != 0 else None
#             results.append(((o, d), percent, win, loss))

#         count_cur, win_cur, loss_cur = EFFover_count_win_loss_current(df, o, d)
#         if count_cur != 0:
#             percent_cur = round((win_cur / count_cur) * 100, 2)
#             results_cur.append(((o, d), percent_cur, win_cur, loss_cur))
#         else:
#             results_cur.append(((o, d), None, 0, 0))
        
#         count_prev, win_prev, loss_prev = EFFover_count_win_loss_prev(df, o, d)
#         if count_prev != 0:
#             percent_prev = round((win_prev / count_prev) * 100, 2)
#             results_prev.append(((o, d), percent_prev, win_prev, loss_prev))
#         else:
#             results_prev.append(((o, d), None, 0, 0))
        
#     results_cur_dict = {k: v for k, *v in results_cur}
#     results_prev_dict = {k: v for k, *v in results_prev}

#     results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

#     for (o, d), percent, win, loss in results:
#         st.markdown(
#             f"""
#             <h3 style="text-align: center; font-size: 32px; text-decoration: underline;">
#                 {o} Offense EFF Over 105 / {d} Defense EFF Over 105
#             </h3>
#             """,unsafe_allow_html=True
#         )
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>All Seasons</h4>", unsafe_allow_html=True)
#             display_metrics(percent, win, loss)
#         with col2:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Current Season</h4>", unsafe_allow_html=True)
#             percent_cur, win_cur, loss_cur = results_cur_dict.get((o, d), (None, 0, 0))
#             display_metrics(percent_cur, win_cur, loss_cur)
#         with col3:
#             st.markdown("<h4 style='text-align:center; text-decoration: underline;'>Previous Season</h4>", unsafe_allow_html=True)
#             percent_prev, win_prev, loss_prev = results_prev_dict.get((o, d), (None, 0, 0))
#             display_metrics(percent_prev, win_prev, loss_prev)
        
#         # Today's Game
#         today = datetime.today().date()
#         today_games = df[
#         (df['Date'].dt.date == today) &
#             (df['Just Efficiency Over'] == 1) &
#             (df['OFF Over 105'] == o) &
#             (df['DEF Over 105'] == d)
# ][['Date', 'Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction']]

#         if not today_games.empty:
#             today_games['Date'] = today_games['Date'].dt.strftime('%Y-%m-%d')  # Optional formatting
#             with st.expander(f"📅 Games Today for Subcategory Trend -- {o} OFF Over 105 EFF and {d} DEF Over 105 EFF"):
#                 st.dataframe(today_games)
#         else:
#             st.markdown("<p style='text-align:center; color:gray;'>No games today for this combination.</p>", unsafe_allow_html=True)

#         # Plot below metrics, centered with Streamlit's default centering
#         plot_df = df[
#             (df['Just Efficiency Over'] == 1) &
#             (df['OFF Over 105'] == o) &
#             (df['DEF Over 105'] == d)
#         ]

#         display_total_difference_histogram(plot_df)
