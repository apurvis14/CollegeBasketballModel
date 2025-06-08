import pandas as pd
import streamlit as st

# All Over Function (Regular Season) - All Seasons
def allover_count_win_loss(df, offense_value, defense_value):
    count = len(df[(df['All Formulas Over'] == 1) & 
                   (df['Offense Over 100'] == offense_value) & 
                   (df['Defense Over 100'] == defense_value) &
                   (df['RS/PS'] == 'RS')])
    
    win = len(df[(df['All Formulas Over'] == 1) & 
                 (df['Offense Over 100'] == offense_value) & 
                 (df['Defense Over 100'] == defense_value) & 
                 (df['Over Hit'] == 1) &
                 (df['RS/PS'] == 'RS')])
    
    loss = count - win
    
    return count, win, loss


# All Under Function (Regular Season) - All Seasons
def allunder_count_win_loss(df, offense_value, defense_value):
    count = len(df[(df['All Formulas Under'] == 1) & 
                   (df['Offense Under 100'] == offense_value) & 
                   (df['Defense Under 100'] == defense_value) &
                   (df['RS/PS'] == 'RS')])
    
    win = len(df[(df['All Formulas Under'] == 1) & 
                 (df['Offense Under 100'] == offense_value) & 
                 (df['Defense Under 100'] == defense_value) & 
                 (df['Under Hit'] == 1) &
                 (df['RS/PS'] == 'RS')])
    
    loss = count - win
    
    return count, win, loss

# EFF and PPG Over and Tempo Under Function (Regular Season) - All Seasons
def EPOver_TempoUnder_count_win_loss(df, offense_value, offense_value_1, defense_value, defense_value_1):
    count = len(df[(df['Efficiency/PPG over  (Tempo under)'] == 1) & 
                   (df['Count of OFF over 100'] == offense_value) & 
                   (df['Count of OFF over 110'] == offense_value_1) &
                   (df['Count of DEF under 100'] == defense_value) &
                   (df['Count of DEF under 95'] == defense_value_1)
                   & (df['RS/PS'] == 'RS')])
    
    win = len(df[(df['Efficiency/PPG over  (Tempo under)'] == 1) & 
                   (df['Count of OFF over 100'] == offense_value) & 
                   (df['Count of OFF over 110'] == offense_value_1) &
                   (df['Count of DEF under 100'] == defense_value) &
                   (df['Count of DEF under 95'] == defense_value_1) &
                   (df['Over Hit.1'] == 1)
                   & (df['RS/PS'] == 'RS')])
    
    loss = count - win
    
    return count, win, loss

# Tempo and EFF Over and PPG Under Function (Regular Season) - All Seasons
def TEOver_PPGUnder_count_win_loss(df, offense_value, offense_value_1, defense_value, defense_value_1):
    count = len(df[(df['Tempo and Efficiency over (PPG under)'] == 1) & 
                   (df['OFF Under 100'] == offense_value) & 
                   (df['OFF Under 95'] == offense_value_1) &
                   (df['DEF Under 100'] == defense_value) &
                   (df['DEF Under 95'] == defense_value_1) &
                   (df['RS/PS'] == 'RS')])
    
    win = len(df[(df['Tempo and Efficiency over (PPG under)'] == 1) & 
                   (df['OFF Under 100'] == offense_value) & 
                   (df['OFF Under 95'] == offense_value_1) &
                   (df['DEF Under 100'] == defense_value) &
                   (df['DEF Under 95'] == defense_value_1) &
                   (df['Over Hit.2'] == 1) &
                   (df['RS/PS'] == 'RS')])
    
    loss = count - win
    
    return count, win, loss

# Tempo and PPG Over and EFF Under Function (Regular Season) - All Seasons
def TPOver_EFFUnder_count_win_loss(df):
    count = len(df[(df['Tempo and PPG over (Efficiency Under)'] == 1) &
                (df['RS/PS'] == 'RS')])
    
    win = len(df[(df['Tempo and PPG over (Efficiency Under)'] == 1) &
                (df['Over Hit.3'] == 1) &
                (df['RS/PS'] == 'RS')])
    
    loss = count - win
    
    return count, win, loss

# Just Tempo Over Function (Regular Season) - All Seasons
def TempoOver_count_win_loss(df, eff_value):
    count = len(df[(df['Just Tempo Over'] == 1) & 
                   (df['Over 105 EFF'] == eff_value) &
                   (df['RS/PS'] == 'RS')])
    
    win = len(df[(df['Just Tempo Over'] == 1) & 
                   (df['Over 105 EFF'] == eff_value) &
                   (df['Over Hit.4'] == 1) &
                   (df['RS/PS'] == 'RS')])
    
    loss = count - win
    
    return count, win, loss

# Just PPG Over Function (Regular Season) - All Seasons
def PPGover_count_win_loss(df,eff_value):
    count = len(df[(df['Just PPG Over'] == 1) &
                   (df['Over 110 EFF'] == eff_value) &
                   (df['RS/PS'] == 'RS')])
    
    win = len(df[(df['Just PPG Over'] == 1) &
                   (df['Over 110 EFF'] == eff_value) &
                   (df['Over Hit.5'] == 1) &
                   (df['RS/PS'] == 'RS')])
    
    loss = count - win

    return count, win, loss

# Just EFF Over Function (Regular Season) - All Seasons
def EFFover_count_win_loss(df,offense_value, defense_value):
    count = len(df[(df['Just Efficiency Over'] == 1) &
                   (df['OFF Over 105'] == offense_value) &
                   (df['DEF Over 105'] == defense_value) &
                   (df['RS/PS'] == 'RS')])
    
    win = len(df[(df['Just Efficiency Over'] == 1) &
                   (df['OFF Over 105'] == offense_value) &
                   (df['DEF Over 105'] == defense_value) &
                   (df['Over Hit.6'] == 1) &
                   (df['RS/PS'] == 'RS')])
    
    loss = count - win

    return count, win, loss

#Display metrics for Over Rate
def display_metrics(percent, win, loss):
    if percent is None:
        percent_display = "N/A"
    elif percent >= 60:
        percent_display = f"<span style='color:darkgreen; font-weight:bold'><i>{percent}%</i></span>"
    elif percent >= 55:
        percent_display = f"<span style='color:lightgreen; font-weight:bold'><i>{percent}%</i></span>"
    elif 40 <= percent <= 46:
        percent_display = f"<span style='color:orange; font-weight:bold'><i>{percent}%</i></span>"
    elif percent < 40:
        percent_display = f"<span style='color:red; font-weight:bold'><i>{percent}%</i></span>"
    else:
        percent_display = f"<i>{percent}%</i>"

    units = round(win * 0.909 - loss, 2)
    if units >= 15:
        units_display = f"<span style='color:darkgreen; font-weight:bold'>{units}</span>"
    elif 10 <= units < 15:
        units_display = f"<span style='color:green; font-weight:bold'>{units}</span>"
    elif 0 <= units < 10:
        units_display = f"<span style='color:lightgreen; font-weight:bold'>{units}</span>"
    else:
        units_display = f"<span style='color:red; font-weight:bold'>{units}</span>"

    st.markdown(
        f"""
        <div style='text-align: center; font-size: 16px; margin-bottom: 1rem;'>
            <b>Over Hit Rate:</b> {percent_display}<br>
            <b>Wins:</b> <span style='color:gold; font-size:18px;'>{win}</span> &nbsp;&nbsp;&nbsp;
            <b>Losses:</b> <span style='color:gold; font-size:18px;'>{loss}</span><br>
            <b>Net Units:</b> {units_display}<br>
        </div>
        """,
        unsafe_allow_html=True
    )
    
# Display metrics for Under Rate
def display_metrics_under(percent, win, loss):
    if percent is None:
        percent_display = "N/A"
    elif percent >= 60:
        percent_display = f"<span style='color:darkgreen; font-weight:bold'><i>{percent}%</i></span>"
    elif percent >= 55:
        percent_display = f"<span style='color:lightgreen; font-weight:bold'><i>{percent}%</i></span>"
    elif 40 <= percent <= 46:
        percent_display = f"<span style='color:orange; font-weight:bold'><i>{percent}%</i></span>"
    elif percent < 40:
        percent_display = f"<span style='color:red; font-weight:bold'><i>{percent}%</i></span>"
    else:
        percent_display = f"<i>{percent}%</i>"

    st.markdown(
        f"""
        <div style='text-align: center; font-size: 16px; margin-bottom: 1rem;'>
            <b>Under Hit Rate:</b> {percent_display}<br>
            <b>Wins:</b> <span style='color:gold; font-size:18px;'>{win}</span> &nbsp;&nbsp;&nbsp;
            <b>Losses:</b> <span style='color:gold; font-size:18px;'>{loss}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# All Over Function (Regular Season) - Current Season
def allover_count_win_loss_current(df, offense_value, defense_value):
    count_cur = len(df[(df['All Formulas Over'] == 1) & 
                   (df['Offense Over 100'] == offense_value) & 
                   (df['Defense Over 100'] == defense_value) &
                   (df['RS/PS'] == 'RS') & 
                   (df['Year'] == 2024)])
    
    win_cur = len(df[(df['All Formulas Over'] == 1) & 
                 (df['Offense Over 100'] == offense_value) & 
                 (df['Defense Over 100'] == defense_value) & 
                 (df['Over Hit'] == 1) &
                 (df['RS/PS'] == 'RS') &
                 (df['Year'] == 2024)])
    
    loss_cur = count_cur - win_cur
    
    return count_cur, win_cur, loss_cur

# All Under Function (Regular Season) - Current Season
def allunder_count_win_loss_current(df, offense_value, defense_value):
    count_cur = len(df[(df['All Formulas Under'] == 1) &
                     (df['Offense Under 100'] == offense_value) &
                        (df['Defense Under 100'] == defense_value) &
                        (df['RS/PS'] == 'RS') &
                        (df['Year'] == 2024)])
    
    win_cur = len(df[(df['All Formulas Under'] == 1) &
                        (df['Offense Under 100'] == offense_value) &
                        (df['Defense Under 100'] == defense_value) &
                        (df['Under Hit'] == 1) &
                        (df['RS/PS'] == 'RS') &
                        (df['Year'] == 2024)])
    
    loss_cur = count_cur - win_cur

    return count_cur, win_cur, loss_cur

# EFF and PPG Over and Tempo Under Function (Regular Season) - Current Season
def EPOver_TempoUnder_count_win_loss_current(df, offense_value, offense_value_1, defense_value, defense_value_1):
    count_cur = len(df[(df['Efficiency/PPG over  (Tempo under)'] == 1) & 
                   (df['Count of OFF over 100'] == offense_value) & 
                   (df['Count of OFF over 110'] == offense_value_1) &
                   (df['Count of DEF under 100'] == defense_value) &
                   (df['Count of DEF under 95'] == defense_value_1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2024)])
    
    win_cur = len(df[(df['Efficiency/PPG over  (Tempo under)'] == 1) & 
                   (df['Count of OFF over 100'] == offense_value) & 
                   (df['Count of OFF over 110'] == offense_value_1) &
                   (df['Count of DEF under 100'] == defense_value) &
                   (df['Count of DEF under 95'] == defense_value_1) &
                   (df['Over Hit.1'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2024)])
    
    loss_cur = count_cur - win_cur
    
    return count_cur, win_cur, loss_cur

# Tempo and EFF Over and PPG Under Function (Regular Season) - Current Season
def TEOver_PPGUnder_count_win_loss_current(df, offense_value, offense_value_1, defense_value, defense_value_1):
    count_cur = len(df[(df['Tempo and Efficiency over (PPG under)'] == 1) & 
                   (df['OFF Under 100'] == offense_value) & 
                   (df['OFF Under 95'] == offense_value_1) &
                   (df['DEF Under 100'] == defense_value) &
                   (df['DEF Under 95'] == defense_value_1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2024)])
    
    win_cur = len(df[(df['Tempo and Efficiency over (PPG under)'] == 1) & 
                   (df['OFF Under 100'] == offense_value) & 
                   (df['OFF Under 95'] == offense_value_1) &
                   (df['DEF Under 100'] == defense_value) &
                   (df['DEF Under 95'] == defense_value_1) &
                   (df['Over Hit.2'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2024)])
    
    loss_cur = count_cur - win_cur
    
    return count_cur, win_cur, loss_cur

# Tempo and PPG Over and EFF Under Function (Regular Season) - Current Season
def TPOver_EFFUnder_count_win_loss_current(df):
    count_cur = len(df[(df['Tempo and PPG over (Efficiency Under)'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2024)])
    
    win_cur = len(df[(df['Tempo and PPG over (Efficiency Under)'] == 1) &
                (df['Over Hit.3'] == 1) &
                (df['RS/PS'] == 'RS') &
                (df['Year'] == 2024)])
    
    loss_cur = count_cur - win_cur
    
    return count_cur, win_cur, loss_cur

# Just Tempo Over Function (Regular Season) - Current Season
def TempoOver_count_win_loss_current(df, eff_value):
    count_cur = len(df[(df['Just Tempo Over'] == 1) & 
                   (df['Over 105 EFF'] == eff_value) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2024)])
    
    win_cur = len(df[(df['Just Tempo Over'] == 1) & 
                   (df['Over 105 EFF'] == eff_value) &
                   (df['Over Hit.4'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2024)])
    
    loss_cur = count_cur - win_cur
    
    return count_cur, win_cur, loss_cur

# Just PPG Over Function (Regular Season) - Current Season
def PPGover_count_win_loss_current(df, eff_value):
    count_cur = len(df[(df['Just PPG Over'] == 1) &
                   (df['Over 110 EFF'] == eff_value) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2024)])
    
    win_cur = len(df[(df['Just PPG Over'] == 1) &
                   (df['Over 110 EFF'] == eff_value) &
                   (df['Over Hit.5'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2024)])
    
    loss_cur = count_cur - win_cur

    return count_cur, win_cur, loss_cur

# Just EFF Over Function (Regular Season) - Current Season
def EFFover_count_win_loss_current(df, offense_value, defense_value):
    count_cur = len(df[(df['Just Efficiency Over'] == 1) &
                   (df['OFF Over 105'] == offense_value) &
                   (df['DEF Over 105'] == defense_value) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2024)])
    
    win_cur = len(df[(df['Just Efficiency Over'] == 1) &
                   (df['OFF Over 105'] == offense_value) &
                   (df['DEF Over 105'] == defense_value) &
                   (df['Over Hit.6'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2024)])
    
    loss_cur = count_cur - win_cur

    return count_cur, win_cur, loss_cur

# All Over Function (Regular Season) - Previous Season
def allover_count_win_loss_prev(df, offense_value, defense_value):
    count_prev = len(df[(df['All Formulas Over'] == 1) & 
                   (df['Offense Over 100'] == offense_value) & 
                   (df['Defense Over 100'] == defense_value) &
                   (df['RS/PS'] == 'RS') & 
                   (df['Year'] == 2023)])
    
    win_prev = len(df[(df['All Formulas Over'] == 1) & 
                 (df['Offense Over 100'] == offense_value) & 
                 (df['Defense Over 100'] == defense_value) & 
                 (df['Over Hit'] == 1) &
                 (df['RS/PS'] == 'RS') &
                 (df['Year'] == 2023)])
    
    loss_prev = count_prev - win_prev

    return count_prev, win_prev, loss_prev

# All Under Function (Regular Season) - Previous Season
def allunder_count_win_loss_prev(df, offense_value, defense_value):
    count_prev = len(df[(df['All Formulas Under'] == 1) & 
                   (df['Offense Under 100'] == offense_value) & 
                   (df['Defense Under 100'] == defense_value) &
                   (df['RS/PS'] == 'RS') & 
                   (df['Year'] == 2023)])
    
    win_prev = len(df[(df['All Formulas Under'] == 1) & 
                 (df['Offense Under 100'] == offense_value) & 
                 (df['Defense Under 100'] == defense_value) & 
                 (df['Under Hit'] == 1) &
                 (df['RS/PS'] == 'RS') &
                 (df['Year'] == 2023)])
    
    loss_prev = count_prev - win_prev

    return count_prev, win_prev, loss_prev

# EFF and PPG Over and Tempo Under Function (Regular Season) - Previous Season
def EPOver_TempoUnder_count_win_loss_prev(df, offense_value, offense_value_1, defense_value, defense_value_1):
    count_prev = len(df[(df['Efficiency/PPG over  (Tempo under)'] == 1) & 
                   (df['Count of OFF over 100'] == offense_value) & 
                   (df['Count of OFF over 110'] == offense_value_1) &
                   (df['Count of DEF under 100'] == defense_value) &
                   (df['Count of DEF under 95'] == defense_value_1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    win_prev = len(df[(df['Efficiency/PPG over  (Tempo under)'] == 1) & 
                   (df['Count of OFF over 100'] == offense_value) & 
                   (df['Count of OFF over 110'] == offense_value_1) &
                   (df['Count of DEF under 100'] == defense_value) &
                   (df['Count of DEF under 95'] == defense_value_1) &
                   (df['Over Hit.1'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    loss_prev = count_prev - win_prev

    return count_prev, win_prev, loss_prev

# Tempo and EFF Over and PPG Under Function (Regular Season) - Previous Season
def TEOver_PPGUnder_count_win_loss_prev(df, offense_value, offense_value_1, defense_value, defense_value_1):
    count_prev = len(df[(df['Tempo and Efficiency over (PPG under)'] == 1) & 
                   (df['OFF Under 100'] == offense_value) & 
                   (df['OFF Under 95'] == offense_value_1) &
                   (df['DEF Under 100'] == defense_value) &
                   (df['DEF Under 95'] == defense_value_1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    win_prev = len(df[(df['Tempo and Efficiency over (PPG under)'] == 1) & 
                   (df['OFF Under 100'] == offense_value) & 
                   (df['OFF Under 95'] == offense_value_1) &
                   (df['DEF Under 100'] == defense_value) &
                   (df['DEF Under 95'] == defense_value_1) &
                   (df['Over Hit.2'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    loss_prev = count_prev - win_prev

    return count_prev, win_prev, loss_prev

# Tempo and PPG Over and EFF Under Function (Regular Season) - Previous Season
def TPOver_EFFUnder_count_win_loss_prev(df):
    count_prev = len(df[(df['Tempo and PPG over (Efficiency Under)'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    win_prev = len(df[(df['Tempo and PPG over (Efficiency Under)'] == 1) &
                (df['Over Hit.3'] == 1) &
                (df['RS/PS'] == 'RS') &
                (df['Year'] == 2023)])
    
    loss_prev = count_prev - win_prev

    return count_prev, win_prev, loss_prev

# Just Tempo Over Function (Regular Season) - Previous Season
def TempoOver_count_win_loss_prev(df, eff_value):
    count_prev = len(df[(df['Just Tempo Over'] == 1) & 
                   (df['Over 105 EFF'] == eff_value) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    win_prev = len(df[(df['Just Tempo Over'] == 1) & 
                   (df['Over 105 EFF'] == eff_value) &
                   (df['Over Hit.4'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    loss_prev = count_prev - win_prev

    return count_prev, win_prev, loss_prev

# Just PPG Over Function (Regular Season) - Previous Season
def PPGover_count_win_loss_prev(df, eff_value):
    count_prev = len(df[(df['Just PPG Over'] == 1) &
                   (df['Over 110 EFF'] == eff_value) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    win_prev = len(df[(df['Just PPG Over'] == 1) &
                   (df['Over 110 EFF'] == eff_value) &
                   (df['Over Hit.5'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    loss_prev = count_prev - win_prev

    return count_prev, win_prev, loss_prev  

# Just EFF Over Function (Regular Season) - Previous Season
def EFFover_count_win_loss_prev(df, offense_value, defense_value):
    count_prev = len(df[(df['Just Efficiency Over'] == 1) &
                   (df['OFF Over 105'] == offense_value) &
                   (df['DEF Over 105'] == defense_value) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    win_prev = len(df[(df['Just Efficiency Over'] == 1) &
                   (df['OFF Over 105'] == offense_value) &
                   (df['DEF Over 105'] == defense_value) &
                   (df['Over Hit.6'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    loss_prev = count_prev - win_prev

    return count_prev, win_prev, loss_prev
