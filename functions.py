import pandas as pd
import streamlit as st

# All Over Function
def allover_count_win_loss(df, offense_value, defense_value):
    count = len(df[(df['All Formulas Over'] == 1) & 
                   (df['Offense Over 100'] == offense_value) & 
                   (df['Defense Over 100'] == defense_value)])
    
    win = len(df[(df['All Formulas Over'] == 1) & 
                 (df['Offense Over 100'] == offense_value) & 
                 (df['Defense Over 100'] == defense_value) & 
                 (df['Over Hit'] == 1)])
    
    loss = count - win
    
    return count, win, loss

# All Under Function
def allunder_count_win_loss(df, offense_value, defense_value):
    count = len(df[(df['All Formulas Under'] == 1) & 
                   (df['Offense Under 100'] == offense_value) & 
                   (df['Defense Under 100'] == defense_value)])
    
    win = len(df[(df['All Formulas Under'] == 1) & 
                 (df['Offense Under 100'] == offense_value) & 
                 (df['Defense Under 100'] == defense_value) & 
                 (df['Under Hit'] == 1)])
    
    loss = count - win
    
    return count, win, loss

# EFF and PPG Over and Tempo Under Function
def EPOver_TempoUnder_count_win_loss(df, offense_value, offense_value_1, defense_value, defense_value_1):
    count = len(df[(df['Efficiency/PPG over  (Tempo under)'] == 1) & 
                   (df['Count of OFF over 100'] == offense_value) & 
                   (df['Count of OFF over 110'] == offense_value_1) &
                   (df['Count of DEF under 100'] == defense_value) &
                   (df['Count of DEF under 95'] == defense_value_1)])
    
    win = len(df[(df['Efficiency/PPG over  (Tempo under)'] == 1) & 
                   (df['Count of OFF over 100'] == offense_value) & 
                   (df['Count of OFF over 110'] == offense_value_1) &
                   (df['Count of DEF under 100'] == defense_value) &
                   (df['Count of DEF under 95'] == defense_value_1) &
                   (df['Over Hit.1'] == 1)])
    
    loss = count - win
    
    return count, win, loss

# Tempo and EFF Over and PPG Under
def TEOver_PPGUnder_count_win_loss(df, offense_value, offense_value_1, defense_value, defense_value_1):
    count = len(df[(df['Tempo and Efficiency over (PPG under)'] == 1) & 
                   (df['OFF Under 100'] == offense_value) & 
                   (df['OFF Under 95'] == offense_value_1) &
                   (df['DEF Under 100'] == defense_value) &
                   (df['DEF Under 95'] == defense_value_1)])
    
    win = len(df[(df['Tempo and Efficiency over (PPG under)'] == 1) & 
                   (df['OFF Under 100'] == offense_value) & 
                   (df['OFF Under 95'] == offense_value_1) &
                   (df['DEF Under 100'] == defense_value) &
                   (df['DEF Under 95'] == defense_value_1) &
                   (df['Over Hit.2'] == 1)])
    
    loss = count - win
    
    return count, win, loss

# Tempo and PPG Over and EFF Under
def TPOver_EFFUnder_count_win_loss(df):
    count = len(df[df['Tempo and PPG over (Efficiency Under)'] == 1])
    
    win = len(df[(df['Tempo and PPG over (Efficiency Under)'] == 1) &
                (df['Over Hit.3'] == 1)])
    
    loss = count - win
    
    return count, win, loss

# Just Tempo Over
def TempoOver_count_win_loss(df, eff_value):
    count = len(df[(df['Just Tempo Over'] == 1) & 
                   (df['Over 105 EFF'] == eff_value)])
    
    win = len(df[(df['Just Tempo Over'] == 1) & 
                   (df['Over 105 EFF'] == eff_value) &
                   (df['Over Hit.4'] == 1)])
    
    loss = count - win
    
    return count, win, loss

# Just PPG Over
def PPGover_count_win_loss(df,eff_value):
    count = len(df[(df['Just PPG Over'] == 1) &
                   (df['Over 110 EFF'] == eff_value)])
    
    win = len(df[(df['Just PPG Over'] == 1) &
                   (df['Over 110 EFF'] == eff_value) &
                   (df['Over Hit.5'] == 1)])
    
    loss = count - win

    return count, win, loss

# Just EFF Over
def EFFover_count_win_loss(df,offense_value, defense_value):
    count = len(df[(df['Just Efficiency Over'] == 1) &
                   (df['OFF Over 105'] == offense_value) &
                   (df['DEF Over 105'] == defense_value)])
    
    win = len(df[(df['Just Efficiency Over'] == 1) &
                   (df['OFF Over 105'] == offense_value) &
                   (df['DEF Over 105'] == defense_value) &
                   (df['Over Hit.6'] == 1)])
    
    loss = count - win

    return count, win, loss

#Display
def display_metrics(percent, win, loss):
    if percent is None:
        percent_display = "N/A"
    elif percent > 60:
        percent_display = f"<span style='color:darkgreen; font-weight:bold'>{percent}%</span>"
    elif percent > 55:
        percent_display = f"<span style='color:lightgreen; font-weight:bold'>{percent}%</span>"
    elif percent > 40 and percent < 46:
        percent_display = f"<span style='color:orange; font-weight:bold'>{percent}%</span>"
    elif percent < 40:
        percent_display = f"<span style='color:red; font-weight:bold'>{percent}%</span>"
    else:
        percent_display = f"{percent}%"

    st.markdown(f"**Percentage:** {percent_display}", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    # Display Wins with gold color
    col1.metric(f"<h4 style='color: gold;'> Wins: {win}</h4>", unsafe_allow_html=True)
    
    # Display Losses with gold color
    col2.metric(f"<h4 style='color: gold;'> Losses: {loss}</h4>", unsafe_allow_html=True)
