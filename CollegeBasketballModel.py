import pandas as pd
import numpy as np
import streamlit as st
from functions import (
    allover_count_win_loss,
    allunder_count_win_loss,
    EPOver_TempoUnder_count_win_loss,
    TEOver_PPGUnder_count_win_loss,
    TPOver_EFFUnder_count_win_loss,
    TempoOver_count_win_loss,
    PPGover_count_win_loss,
    EFFover_count_win_loss,
    display_metrics,
    display_metrics_under,
    allover_count_win_loss_current,
    allover_count_win_loss_prev,
    allunder_count_win_loss_current,
    allunder_count_win_loss_prev,
    EPOver_TempoUnder_count_win_loss_current,
    EPOver_TempoUnder_count_win_loss_prev,
    TEOver_PPGUnder_count_win_loss_current,
    TEOver_PPGUnder_count_win_loss_prev,
    TPOver_EFFUnder_count_win_loss_current,
    TPOver_EFFUnder_count_win_loss_prev,
    TempoOver_count_win_loss_current,
    TempoOver_count_win_loss_prev,
    PPGover_count_win_loss_current,
    PPGover_count_win_loss_prev,
    EFFover_count_win_loss_current,
    EFFover_count_win_loss_prev
)
from datetime import datetime
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

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
    'Difference PPG to Book', 'DIFF.7', 'Difference EFF to Book'
]
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

logo = Image.open("data/CBB Horizontal Logo.png")
st.image(logo, use_container_width=True)


st.markdown(
    """
    <h1 style='text-align: center;'>College Basketball Trends Dashboard</h1>
    <p style='text-align: center;'>
    This dashboard explores win/loss for various trends across multiple calculations using offensive/defensive ratings, 
    PPG, EFF, and tempo. Select a trend to see performance stats.<br> 
    <u>Scroll down to view games for today.</u><br>
    </p>
    """,
    unsafe_allow_html=True
)


## Trend Selection
trend_option = st.selectbox("Choose Trend Type", [
    "All Over", "All Under", "EFF/PPG Over & Tempo Under", "Tempo/EFF Over & PPG Under",
    "PPG/Tempo Over & EFF Under", "Tempo Over", "PPG Over", "EFF Over"
])

st.markdown("""
    <p style='text-align: center;'>
    **Over Net Units means how many units won by betting on the Over** <br>
    **Under Net Units means how many units won by betting on the Under** <br>
    """,
    unsafe_allow_html=True
)

# with st.expander("View Explanation of these Trends"):
#     st.markdown("""
#                 - All Over means all 3 of my formulas predictions were over the book total.
#                 - The All Over trends are divided into subcategories based on the offensive and defensive efficiency ratings.

#                 - Example: 2 OFF EFF over 100 / 2 DEF EFF over 100 means All Formulas Predicted Over the Book Total while both teams' Offensive Efficiency and Defensive Efficiency over 100. 
#                 """,
#                 unsafe_allow_html=True)

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

        # Plot histogram
        plot_df = subset[
            (subset['Offense Over 100'] == o) & 
            (subset['Defense Over 100'] == d)
        ]

        if not plot_df.empty:
            fig, ax = plt.subplots(figsize=(4, 2.5))
            sns.histplot(plot_df['Total Difference'], bins=20, kde=True, ax=ax, color='mediumseagreen')
            ax.axvline(x=0, color='red', linestyle='--', label='Even Line')
            ax.set_title('Distribution of Difference from Book Total', fontsize=10)
            ax.set_xlabel('Total Difference (Actual - Book)', fontsize=9)
            ax.set_ylabel('Frequency', fontsize=9)
            ax.tick_params(axis='both', labelsize=8)
            ax.legend(fontsize=8)
            ax.grid(True)

            st.columns([1, 2, 1])[1].pyplot(fig)


    # **NEW** Section to Filter by Specific Date and Display Data
    st.markdown(
        "<h3 style='text-align: center;'>Today's Games for All Over Trends</h3>", 
        unsafe_allow_html=True
    )

    # Convert the selected date to a datetime object
    today_date = datetime.today().date()
    
    # Filter the 'subset' DataFrame based on the specific date
    filtered_subset = subset[subset['Date'].dt.normalize() == "2/15/2025"]
    
    # Reorder the columns as needed
    desired_order = ['Date','Home Team', 'Away Team', 'Book Total', 'Tempo Formula Prediction', 'PPG Prediction', 'Efficiency Prediction', 'All Formulas Over', 'Offense Over 100', 'Defense Over 100'] 
    desired_df = filtered_subset[desired_order]
    desired_df['Date'] = desired_df['Date'].dt.strftime('%Y-%m-%d')  # Format date for display

    if not desired_df.empty:
        st.dataframe(desired_df)  # Display the filtered subset DataFrame for the selected date
    else:
        st.write(f"No data available for {today_date}.")

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

                # Plot below metrics, centered with Streamlit's default centering
        plot_df = subset1[
            (subset1['Offense Under 100'] == o) & 
            (subset1['Defense Under 100'] == d)
        ]

        if not plot_df.empty:
            fig, ax = plt.subplots(figsize=(4, 2.5))  # Smaller figure size
            sns.histplot(plot_df['Total Difference'], bins=20, kde=True, ax=ax, color='mediumseagreen')
            ax.axvline(x=0, color='red', linestyle='--', label='Even Line')
            ax.set_title('Distribution of Difference from Book Total', fontsize=10)
            ax.set_xlabel('Total Difference (Actual - Book)', fontsize=9)
            ax.set_ylabel('Frequency', fontsize=9)
            ax.tick_params(axis='both', labelsize=8)
            ax.legend(fontsize=8)
            ax.grid(True)

            # Display in a narrower column
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.pyplot(fig)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.markdown(
        "<h3 style='text-align: center;'>Today's Games for All Formulas Under Trends</h3>", 
        unsafe_allow_html=True
    )

    # Convert the selected date to a datetime object
    today_date = datetime.today().date()

    # Filter data based on the 'All Formulas Under' condition
    subset = df[(df['All Formulas Under'] == 1)]
    filtered_subset = subset[subset['Date'].dt.normalize() == today_date]

    # Reorder and display
    desired_order = ['Home Team', 'Away Team', 'Book Total'] + [col for col in subset.columns if col not in ['Home Team', 'Away Team', 'Book Total']]
    desired_df = filtered_subset[desired_order]

    if not desired_df.empty:
        st.dataframe(desired_df)
    else:
        st.write(f"No data available for {today_date}.")

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

        # Plot below metrics, centered with Streamlit's default centering
        plot_df = df[
            (df['Efficiency/PPG over  (Tempo under)'] == 1) &
            (df['Count of OFF over 100'] == o1) &
            (df['Count of OFF over 110'] == o2) &
            (df['Count of DEF under 100'] == d1) &
            (df['Count of DEF under 95'] == d2)
        ]
        if not plot_df.empty:
            fig, ax = plt.subplots(figsize=(4, 2.5))
            sns.histplot(plot_df['Total Difference'], bins=20, kde=True, ax=ax, color='mediumseagreen')
            ax.axvline(x=0, color='red', linestyle='--', label='Even Line')
            ax.set_title('Distribution of Difference from Book Total', fontsize=10)
            ax.set_xlabel('Total Difference (Actual - Book)', fontsize=9)
            ax.set_ylabel('Frequency', fontsize=9)
            ax.tick_params(axis='both', labelsize=8)
            ax.legend(fontsize=8)
            ax.grid(True)

            # Display in a narrower column
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.pyplot(fig)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.markdown(
        "<h3 style='text-align: center;'>Today's Games for EFF/PPG Over & Tempo Under Trends</h3>", 
        unsafe_allow_html=True
    )

    # Today's date
    today_date = datetime.today().date()

    # Filter data based on the EFF/PPG Over & Tempo Under trend
    subset = df[(df['Efficiency/PPG over  (Tempo under)'] == 1)]
    filtered_subset = subset[subset['Date'].dt.normalize() == today_date]

    # Reorder and display
    desired_order = ['Home Team', 'Away Team', 'Book Total'] + [col for col in subset.columns if col not in ['Home Team', 'Away Team', 'Book Total']]
    desired_df = filtered_subset[desired_order]

    if not desired_df.empty:
        st.dataframe(desired_df)
    else:
        st.write(f"No data available for {today_date}.")

elif trend_option == "Tempo/EFF Over & PPG Under":
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

        # Plot below metrics, centered with Streamlit's default centering
        plot_df = df[
            (df['Tempo and Efficiency over (PPG under)'] == 1) &
            (df['OFF Under 100'] == o1) &
            (df['OFF Under 95'] == o2) &
            (df['DEF Under 100'] == d1) &
            (df['DEF Under 95'] == d2)
        ]
        if not plot_df.empty:
            fig, ax = plt.subplots(figsize=(4, 2.5))
            sns.histplot(plot_df['Total Difference'], bins=20, kde=True, ax=ax, color='mediumseagreen')
            ax.axvline(x=0, color='red', linestyle='--', label='Even Line')
            ax.set_title('Distribution of Difference from Book Total', fontsize=10)
            ax.set_xlabel('Total Difference (Actual - Book)', fontsize=9)
            ax.set_ylabel('Frequency', fontsize=9)
            ax.tick_params(axis='both', labelsize=8)
            ax.legend(fontsize=8)
            ax.grid(True)

            # Display in a narrower column
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.pyplot(fig)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.markdown(
        "<h3 style='text-align: center;'>Today's Games for Tempo/EFF Over & PPG Under Trends</h3>", 
        unsafe_allow_html=True
    )

    # Today's date
    today_date = datetime.today().date()

    # Filter data based on the Tempo/EFF Over & PPG Under trend
    subset = df[(df['Tempo and Efficiency over (PPG under)'] == 1)]
    filtered_subset = subset[subset['Date'].dt.normalize() == today_date]

    # Reorder and display
    desired_order = ['Home Team', 'Away Team', 'Book Total'] + [col for col in subset.columns if col not in ['Home Team', 'Away Team', 'Book Total']]
    desired_df = filtered_subset[desired_order]

    if not desired_df.empty:
        st.dataframe(desired_df)
    else:
        st.write(f"No data available for {today_date}.")

elif trend_option == "PPG/Tempo Over & EFF Under":
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


    # Plot below metrics, centered with Streamlit's default centering
    plot_df = df[df['Tempo and PPG over (Efficiency Under)'] == 1]
    if not plot_df.empty:
        fig, ax = plt.subplots(figsize=(4, 2.5))
        sns.histplot(plot_df['Total Difference'], bins=20, kde=True, ax=ax, color='mediumseagreen')
        ax.axvline(x=0, color='red', linestyle='--', label='Even Line')
        ax.set_title('Distribution of Difference from Book Total', fontsize=10)
        ax.set_xlabel('Total Difference (Actual - Book)', fontsize=9)
        ax.set_ylabel('Frequency', fontsize=9)
        ax.tick_params(axis='both', labelsize=8)
        ax.legend(fontsize=8)
        ax.grid(True)
        # Display in a narrower column
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.pyplot(fig)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.markdown(
        "<h3 style='text-align: center;'>Today's Games for PPG/Tempo Over & EFF Under Trends</h3>", 
        unsafe_allow_html=True
    )

    # Today's date
    today_date = datetime.today().date()

    # Filter data based on the PPG/Tempo Over & EFF Under trend
    subset = df[(df['Tempo and PPG over (Efficiency Under)'] == 1)]
    filtered_subset = subset[subset['Date'].dt.normalize() == today_date]

    # Reorder and display
    desired_order = ['Home Team', 'Away Team', 'Book Total'] + [col for col in subset.columns if col not in ['Home Team', 'Away Team', 'Book Total']]
    desired_df = filtered_subset[desired_order]

    if not desired_df.empty:
        st.dataframe(desired_df)
    else:
        st.write(f"No data available for {today_date}.")

elif trend_option == "Tempo Over":
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

        # Plot below metrics, centered with Streamlit's default centering
        plot_df = df[(df['Just Tempo Over'] == 1) &
                     (df['Over 105 EFF'] == val)]
        if not plot_df.empty:
            fig, ax = plt.subplots(figsize=(4, 2.5))
            sns.histplot(plot_df['Total Difference'], bins=20, kde=True, ax=ax, color='mediumseagreen')
            ax.axvline(x=0, color='red', linestyle='--', label='Even Line')
            ax.set_title('Distribution of Difference from Book Total', fontsize=10)
            ax.set_xlabel('Total Difference (Actual - Book)', fontsize=9)
            ax.set_ylabel('Frequency', fontsize=9)
            ax.tick_params(axis='both', labelsize=8)
            ax.legend(fontsize=8)
            ax.grid(True)
            # Display in a narrower column
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.pyplot(fig)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.markdown(
        "<h3 style='text-align: center;'>Today's Games for Tempo Over Trends</h3>", 
        unsafe_allow_html=True
    )

    # Today's date
    today_date = datetime.today().date()

    # Filter data based on the Tempo Over trend
    subset = df[(df['Just Tempo Over'] == 1)]
    filtered_subset = subset[subset['Date'].dt.normalize() == today_date]

    # Reorder and display
    desired_order = ['Home Team', 'Away Team', 'Book Total'] + [col for col in subset.columns if col not in ['Home Team', 'Away Team', 'Book Total']]
    desired_df = filtered_subset[desired_order]

    if not desired_df.empty:
        st.dataframe(desired_df)
    else:
        st.write(f"No data available for {today_date}.")

elif trend_option == "PPG Over":
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

        # Plot below metrics, centered with Streamlit's default centering
        plot_df = df[(df['Just PPG Over'] == 1) &
                     (df['Over 110 EFF'] == val)]
        if not plot_df.empty:
            fig, ax = plt.subplots(figsize=(4, 2.5))
            sns.histplot(plot_df['Total Difference'], bins=20, kde=True, ax=ax, color='mediumseagreen')
            ax.axvline(x=0, color='red', linestyle='--', label='Even Line')
            ax.set_title('Distribution of Difference from Book Total', fontsize=10)
            ax.set_xlabel('Total Difference (Actual - Book)', fontsize=9)
            ax.set_ylabel('Frequency', fontsize=9)
            ax.tick_params(axis='both', labelsize=8)
            ax.legend(fontsize=8)
            ax.grid(True)

            # Display in a narrower column
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.pyplot(fig)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.markdown(
        "<h3 style='text-align: center;'>Today's Games for PPG Over Trends</h3>", 
        unsafe_allow_html=True
    )
    
    today_date = datetime.today().date()

    # Filter data based on the PPG Over trend
    subset = df[(df['Just PPG Over'] == 1)]
    filtered_subset = subset[subset['Date'].dt.normalize() == today_date]

    # Reorder and display
    desired_order = ['Home Team', 'Away Team', 'Book Total'] + [col for col in subset.columns if col not in ['Home Team', 'Away Team', 'Book Total']]
    desired_df = filtered_subset[desired_order]

    if not desired_df.empty:
        st.dataframe(desired_df)
    else:
        st.write(f"No data available for {today_date}.")

elif trend_option == "EFF Over":
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

        # Plot below metrics, centered with Streamlit's default centering
        plot_df = df[
            (df['Just Efficiency Over'] == 1) &
            (df['OFF Over 105'] == o) &
            (df['DEF Over 105'] == d)
        ]

        if not plot_df.empty:
            fig, ax = plt.subplots(figsize=(4, 2.5))
            sns.histplot(plot_df['Total Difference'], bins=20, kde=True, ax=ax, color='mediumseagreen')
            ax.axvline(x=0, color='red', linestyle='--', label='Even Line')
            ax.set_title('Distribution of Difference from Book Total', fontsize=10)
            ax.set_xlabel('Total Difference (Actual - Book)', fontsize=9)
            ax.set_ylabel('Frequency', fontsize=9)
            ax.tick_params(axis='both', labelsize=8)
            ax.legend(fontsize=8)
            ax.grid(True)

            # Display in a narrower column
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.pyplot(fig)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.markdown(
        "<h3 style='text-align: center;'>Today's Games for EFF Over Trends</h3>", 
        unsafe_allow_html=True
    )

    today_date = datetime.today().date()

    # Filter data based on the EFF Over trend
    subset = df[(df['Just Efficiency Over'] == 1)]
    filtered_subset = subset[subset['Date'].dt.normalize() == today_date]

    # Reorder and display
    desired_order = ['Home Team', 'Away Team', 'Book Total'] + [col for col in subset.columns if col not in ['Home Team', 'Away Team', 'Book Total']]
    desired_df = filtered_subset[desired_order]

    if not desired_df.empty:
        st.dataframe(desired_df)
    else:
        st.write(f"No data available for {today_date}.")

