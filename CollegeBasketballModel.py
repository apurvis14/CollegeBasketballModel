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
    display_metrics
)
from datetime import datetime
from PIL import Image
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
    PPG, EFF, and tempo. Select a trend to see performance stats. <u>Scroll down to view games for today.<u>
    </p>
    """,
    unsafe_allow_html=True
)


## Trend Selection
trend_option = st.selectbox("Choose Trend Type", [
    "All Over", "All Under", "EFF/PPG Over & Tempo Under", "Tempo/EFF Over & PPG Under",
    "PPG/Tempo Over & EFF Under", "Tempo Over", "PPG Over", "EFF Over"
])


if trend_option == "All Over":
    # Filter the df for the 'All Formulas Over' condition
    subset = df[(df['All Formulas Over'] == 1)]  # Filter based on condition

    combinations = [(2, 2), (2, 1), (1, 2), (1, 1), (1, 0), (0, 1), (0, 0), (0, 2), (2, 0)]
    results = []
    
    for o, d in combinations:
        count, win, loss = allover_count_win_loss(df, o, d)
        if count != 0:
            percent = round((win / count) * 100, 2) if count != 0 else None
            results.append(((o, d), percent, win, loss))

    results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

    for (o, d), percent, win, loss in results:
        st.markdown(
        f"""
        <h3 style="text-align: left; font-size: 24px; text-decoration: underline;">
            {o} Offense over 100 / {d} Defense over 100
        </h3>
        """,
        unsafe_allow_html=True
        )
        display_metrics(percent, win, loss)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.subheader("Data for Today's Games with All Over Trends")

    # Convert the selected date to a datetime object
    today_date = datetime.today().date()
    
    # Filter the 'subset' DataFrame based on the specific date
    filtered_subset = subset[subset['Date'].dt.normalize() == today_date]
    
    # Reorder the columns as needed
    desired_order = ['Home Team', 'Away Team', 'Book Total'] + [col for col in subset.columns if col not in ['Home Team', 'Away Team', 'Book Total']]
    desired_df = filtered_subset[desired_order]

    if not desired_df.empty:
        st.dataframe(desired_df)  # Display the filtered subset DataFrame for the selected date
    else:
        st.write(f"No data available for {today_date}.")

elif trend_option == "All Under":
    combinations = [(2, 2), (2, 1), (1, 2), (1, 1), (1, 0), (0, 1), (0, 0), (0, 2), (2, 0)]
    results = []

    for o, d in combinations:
        count, win, loss = allunder_count_win_loss(df, o, d)
        percent = round((win / count) * 100, 2) if count != 0 else None
        results.append(((o, d), percent, win, loss))

    results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

    for (o, d), percent, win, loss in results:
        st.write(f"**{o} Offense under 100 / {d} Defense under 100**")
        display_metrics(percent, win, loss)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.subheader("Data for Today's Games with All Under Trends")

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
    combinations = [(0, 0, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1), (0, 0, 2, 0), (0, 0, 2, 1), (0, 0, 2, 2),
    
    (1, 0, 0, 0), (1, 0, 1, 0), (1, 0, 1, 1), (1, 0, 2, 0), (1, 0, 2, 1), (1, 0, 2, 2),
    (1, 1, 0, 0), (1, 1, 1, 0), (1, 1, 1, 1), (1, 1, 2, 0), (1, 1, 2, 1), (1, 1, 2, 2),
    
    (2, 0, 0, 0), (2, 0, 1, 0), (2, 0, 1, 1), (2, 0, 2, 0), (2, 0, 2, 1), (2, 0, 2, 2),
    (2, 1, 0, 0), (2, 1, 1, 0), (2, 1, 1, 1), (2, 1, 2, 0), (2, 1, 2, 1), (2, 1, 2, 2),
    (2, 2, 0, 0), (2, 2, 1, 0), (2, 2, 1, 1), (2, 2, 2, 0), (2, 2, 2, 1), (2, 2, 2, 2)]

    results = []

    for o1, o2, d1, d2 in combinations:
        count, win, loss = EPOver_TempoUnder_count_win_loss(df, o1, o2, d1, d2)
        if count != 0:
            percent = round((win / count) * 100, 2) if count != 0 else None
            results.append(((o1, o2, d1, d2), percent, win, loss))

    results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

    for (o1, o2, d1, d2), percent, win, loss in results:    
        st.write(f"**{o1} Offense Over 100 and {o2} 110 / {d1} Defense Under 100 and {d2} 95**")
        display_metrics(percent, win, loss)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.subheader("Today's Games for EFF/PPG Over & Tempo Under Trends")

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
    for o1, o2, d1, d2 in combinations:
        count, win, loss = TEOver_PPGUnder_count_win_loss(df, o1, o2, d1, d2)
        if count != 0:
            percent = round((win / count) * 100, 2) if count != 0 else None
            results.append(((o1, o2, d1, d2), percent, win, loss))

    results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

    for (o1, o2, d1, d2), percent, win, loss in results:
        st.write(f"**{o1} OFF Under 100 and {o2} 95 / {d1} DEF Under 100 and {d2} 95**")
        display_metrics(percent, win, loss)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.subheader("Today's Games for Tempo/EFF Over & PPG Under Trends")

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
        percent = round((win / count) * 100, 2) if count != 0 else None
        display_metrics(percent, win, loss)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.subheader("Today's Games for PPG/Tempo Over & EFF Under Trends")

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
    for val in [0,1,2]:
        count, win, loss = TempoOver_count_win_loss(df, val)
        if count != 0:
            percent = round((win / count) * 100, 2) if count != 0 else None
            results.append((val, percent, win, loss))

    results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

    for val, percent, win, loss in results:
        st.write(f"**{val} EFF Over 105**")
        display_metrics(percent, win, loss)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.subheader("Today's Games for Tempo Over Trends.")

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
    for val in [0,1,2,3]:
        count, win, loss = PPGover_count_win_loss(df, val)
        if count != 0:
            percent = round((win / count) * 100, 2) if count != 0 else None
            results.append((val, percent, win, loss))
    
    results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

    for val, percent, win, loss in results:
        st.write(f"**{val} PPG Over**")
        display_metrics(percent, win, loss)

    # **NEW** Section to Filter by Specific Date and Display Data
    st.subheader("Today's Games for PPG Over Trends")
    
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
    for o, d in combinations:
        count, win, loss = EFFover_count_win_loss(df, o, d)
        if count != 0:
            percent = round((win / count) * 100, 2) if count != 0 else None
            results.append(((o, d), percent, win, loss))

    results.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

    for (o, d), percent, win, loss in results:
        st.write(f"**{o} Offense Over 105 / {d} Defense Over 105**")
        display_metrics(percent, win, loss)
    
    # **NEW** Section to Filter by Specific Date and Display Data
    st.subheader("Today's Games for EFF Over Trends")

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

