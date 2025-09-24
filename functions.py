import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import base64

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
                 (df['Over Hit.1'] == 1) &
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
                   (df['Over Hit.2'] == 1)
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
                   (df['Over Hit.3'] == 1) &
                   (df['RS/PS'] == 'RS')])
    
    loss = count - win
    
    return count, win, loss

# Tempo and PPG Over and EFF Under Function (Regular Season) - All Seasons
def TPOver_EFFUnder_count_win_loss(df):
    count = len(df[(df['Tempo and PPG over (Efficiency Under)'] == 1) &
                (df['RS/PS'] == 'RS')])
    
    win = len(df[(df['Tempo and PPG over (Efficiency Under)'] == 1) &
                (df['Over Hit.4'] == 1) &
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
                   (df['Over Hit.5'] == 1) &
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
                   (df['Over Hit.6'] == 1) &
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
                   (df['Over Hit.7'] == 1) &
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
    elif 46 < percent < 55:
        percent_display = f"<span style='color:black; font-weight:bold'><i>{percent}%</i></span>"
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

    fade_units = round(loss*0.909 - win, 2)
    if fade_units >= 15:
        fade_display = f" <span style='color:darkgreen; font-weight:bold'>({fade_units})</span>"
    elif 10 <= fade_units < 15:
        fade_display = f" <span style='color:green; font-weight:bold'>({fade_units})</span>"
    elif 0 <= fade_units < 10:
        fade_display = f" <span style='color:lightgreen; font-weight:bold'>({fade_units})</span>"
    else:
        fade_display = f" <span style='color:red; font-weight:bold'>({fade_units})</span>"

    st.markdown(
        f"""
        <div style='text-align: center; font-size: 16px; margin-bottom: 1rem;'>
            <b>Record:</b>
            <span style='color:goldenrod; font-size:16px; font-weight:bold'>{win} - {loss}</span>
            <span style='font-size:16px;'><b>(<b>{percent_display}<b>)<b></span>
            &nbsp;&nbsp;&nbsp;
            <div style='font-size: 16px; margin-top: 4px;'>
                <b>Over<b>: {units_display} <b>units<b> <br>
                <b>Under<b>: {fade_display} <b>units<b>
            </div>
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

    units = round(win * 0.909 - loss, 2)
    if units >= 15:
        units_display = f"<span style='color:darkgreen; font-weight:bold'>{units}</span>"
    elif 10 <= units < 15:
        units_display = f"<span style='color:green; font-weight:bold'>{units}</span>"
    elif 0 <= units < 10:
        units_display = f"<span style='color:lightgreen; font-weight:bold'>{units}</span>"
    else:
        units_display = f"<span style='color:red; font-weight:bold'>{units}</span>"
    
    fade_units = round(loss*0.909 - win, 2)
    if fade_units >= 15:
        fade_display = f" <span style='color:darkgreen; font-weight:bold'>({fade_units})</span>"
    elif 10 <= fade_units < 15:
        fade_display = f" <span style='color:green; font-weight:bold'>({fade_units})</span>"
    elif 0 <= fade_units < 10:
        fade_display = f" <span style='color:lightgreen; font-weight:bold'>({fade_units})</span>"
    else:
        fade_display = f" <span style='color:red; font-weight:bold'>({fade_units})</span>"

    st.markdown(
        f"""
        <div style='text-align: center; font-size: 16px; margin-bottom: 1rem;'>
            <b>Under Hit Rate:</b> {percent_display}<br>
            <b>Wins:</b> <span style='color:goldenrod; font-size:16px;'>{win}</span> &nbsp;&nbsp;&nbsp;
            <b>Losses:</b> <span style='color:goldenrod; font-size:16px;'>{loss}</span><br>
            <div style='font-size: 14px; margin-top: 4px;'>
            <u>Under Net Units:</u> {units_display}<br>
            <u>Over Net Units:</u> {fade_display}
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
                        (df['Over Hit.1'] == 1) &
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
                   (df['Over Hit.2'] == 1) &
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
                   (df['Over Hit.3'] == 1) &
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
                (df['Over Hit.4'] == 1) &
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
                   (df['Over Hit.5'] == 1) &
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
                   (df['Over Hit.6'] == 1) &
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
                   (df['Over Hit.7'] == 1) &
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
                 (df['Over Hit.1'] == 1) &
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
                   (df['Over Hit.2'] == 1) &
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
                   (df['Over Hit.3'] == 1) &
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
                (df['Over Hit.4'] == 1) &
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
                   (df['Over Hit.5'] == 1) &
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
                   (df['Over Hit.6'] == 1) &
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
                   (df['Over Hit.7'] == 1) &
                   (df['RS/PS'] == 'RS') &
                   (df['Year'] == 2023)])
    
    loss_prev = count_prev - win_prev

    return count_prev, win_prev, loss_prev

def display_total_difference_histogram(plot_df):
    """
    Plots the histogram of 'Total Difference' from book total for the provided filtered DataFrame.
    The plot is centered and styled for Streamlit.
    """
    if not plot_df.empty:
        DARK_GOLD = '#B8860B'

        fig, ax = plt.subplots(figsize=(4, 2.5))
        sns.histplot(plot_df['Total Difference'], bins=20, kde=True, ax=ax, color=DARK_GOLD)
        ax.axvline(x=0, color='red', linestyle='--', label='Even Line')
        ax.set_title('Distribution of Difference from Book Total', fontsize=10)
        ax.set_xlabel('Total Difference (Actual - Book)', fontsize=9)
        ax.set_ylabel('Frequency', fontsize=9)
        ax.tick_params(axis='both', labelsize=8)
        ax.legend(fontsize=8)
        ax.grid(True)
        
        st.columns([1, 2, 1])[1].pyplot(fig)

def home_away_over_under_by_team(df, offense_value, defense_value):
    # Filter dataframe by offense, defense, and RS/PS criteria first
    filtered_df = df[(df['Offense Over 100'] == offense_value) & 
                     (df['Defense Over 100'] == defense_value) & 
                     (df['RS/PS'] == 'RS')]
    
    teams = pd.unique(filtered_df[['Home Team', 'Away Team']].values.ravel())
    
    records = {}
    for team in teams:
        year = 2024
        # Home games for team
        home_games = filtered_df[filtered_df['Home Team'] == team]
        home_overs = ((home_games['All Formulas Over'] == 1) & (home_games['Over Hit'] == 1) & (home_games['Year'] == year)).sum()
        home_unders = ((home_games['All Formulas Over'] == 1) & (home_games['Over Hit'] == " ") & (home_games['Year'] == year)).sum()

        # Away games for team
        away_games = filtered_df[filtered_df['Away Team'] == team]
        away_overs = ((away_games['All Formulas Over'] == 1) & (away_games['Over Hit'] == 1) & (away_games['Year'] == year)).sum()
        away_unders = ((away_games['All Formulas Over'] == 1) & (away_games['Over Hit'] == " ") & (away_games['Year'] == year)).sum()
        
        # Total overs/unders
        total_overs = home_overs + away_overs
        total_unders = home_unders + away_unders
        
        records[team] = {
            'Home Record': f"{home_overs} - {home_unders}",
            'Away Record': f"{away_overs} - {away_unders}",
            'Total Record': f"{total_overs} - {total_unders}"
        }
    
    return pd.DataFrame.from_dict(records, orient='index')

def home_away_over_under_by_team_all_under(df, o, d):
    # Filter dataframe by offense, defense, and RS/PS criteria first
    filtered_df = df[(df['Offense Under 100'] == o) & 
                     (df['Defense Under 100'] == d) & 
                     (df['RS/PS'] == 'RS')]
    
    teams = pd.unique(filtered_df[['Home Team', 'Away Team']].values.ravel())
    
    records = {}
    for team in teams:
        year = 2024
        # Home games for team
        home_games = filtered_df[filtered_df['Home Team'] == team]
        home_overs = ((home_games['All Formulas Under'] == 1) & (home_games['Over Hit.1'] == 1) & (home_games['Year'] == year)).sum()
        home_unders = ((home_games['All Formulas Under'] == 1) & (home_games['Over Hit.1'] == " ") & (home_games['Year'] == year)).sum()

        # Away games for team
        away_games = filtered_df[filtered_df['Away Team'] == team]
        away_overs = ((away_games['All Formulas Under'] == 1) & (away_games['Over Hit.1'] == 1) & (away_games['Year'] == year)).sum()
        away_unders = ((away_games['All Formulas Under'] == 1) & (away_games['Over Hit.1'] == " ") & (away_games['Year'] == year)).sum()
        
        # Total overs/unders
        total_overs = home_overs + away_overs
        total_unders = home_unders + away_unders
        
        records[team] = {
            'Home Record': f"{home_overs} - {home_unders}",
            'Away Record': f"{away_overs} - {away_unders}",
            'Total Record': f"{total_overs} - {total_unders}"
        }
    
    return pd.DataFrame.from_dict(records, orient='index')

def home_away_over_under_by_team_EP_over(df, offense_value1, offense_value2, defense_value, defense_value1):
    # Filter dataframe by offense, defense, and RS/PS criteria first
    filtered_df = df[(df['Count of OFF over 100'] == offense_value1) &
                     (df['Count of OFF over 110'] == offense_value2) &
                     (df['Count of DEF under 100'] == defense_value) &
                     (df['Count of DEF under 95'] == defense_value1) &
                     (df['RS/PS'] == 'RS')]
    
    teams = pd.unique(filtered_df[['Home Team', 'Away Team']].values.ravel())
    
    records = {}
    for team in teams:
        year = 2024
        # Home games for team
        home_games = filtered_df[filtered_df['Home Team'] == team]
        home_overs = ((home_games['Efficiency/PPG over  (Tempo under)'] == 1) & (home_games['Over Hit.2'] == 1) & (home_games['Year'] == year)).sum()
        home_unders = ((home_games['Efficiency/PPG over  (Tempo under)'] == 1) & (home_games['Over Hit.2'] == " ") & (home_games['Year'] == year)).sum()

        # Away games for team
        away_games = filtered_df[filtered_df['Away Team'] == team]
        away_overs = ((away_games['Efficiency/PPG over  (Tempo under)'] == 1) & (away_games['Over Hit.2'] == 1) & (away_games['Year'] == year)).sum()
        away_unders = ((away_games['Efficiency/PPG over  (Tempo under)'] == 1) & (away_games['Over Hit.2'] == " ") & (away_games['Year'] == year)).sum()
        
        # Total overs/unders
        total_overs = home_overs + away_overs
        total_unders = home_unders + away_unders
        
        records[team] = {
            'Home Record': f"{home_overs} - {home_unders}",
            'Away Record': f"{away_overs} - {away_unders}",
            'Total Record': f"{total_overs} - {total_unders}"
        }
    
    return pd.DataFrame.from_dict(records, orient='index')

def home_away_over_under_by_team_TE_over(df, offense_value1, offense_value2, defense_value, defense_value1):
    # Filter dataframe by offense, defense, and RS/PS criteria first
    filtered_df = df[(df['OFF Under 100'] == offense_value1) &
                     (df['OFF Under 95'] == offense_value2) &
                     (df['DEF Under 100'] == defense_value) &
                     (df['DEF Under 95'] == defense_value1) &
                     (df['RS/PS'] == 'RS')]
    
    teams = pd.unique(filtered_df[['Home Team', 'Away Team']].values.ravel())
    
    records = {}
    for team in teams:
        year = 2024
        # Home games for team
        home_games = filtered_df[filtered_df['Home Team'] == team]
        home_overs = ((home_games['Tempo and Efficiency over (PPG under)'] == 1) & (home_games['Over Hit.3'] == 1) & (home_games['Year'] == year)).sum()
        home_unders = ((home_games['Tempo and Efficiency over (PPG under)'] == 1) & (home_games['Over Hit.3'] == " ") & (home_games['Year'] == year)).sum()

        # Away games for team
        away_games = filtered_df[filtered_df['Away Team'] == team]
        away_overs = ((away_games['Tempo and Efficiency over (PPG under)'] == 1) & (away_games['Over Hit.3'] == 1) & (away_games['Year'] == year)).sum()
        away_unders = ((away_games['Tempo and Efficiency over (PPG under)'] == 1) & (away_games['Over Hit.3'] == " ") & (away_games['Year'] == year)).sum()
        
        # Total overs/unders
        total_overs = home_overs + away_overs
        total_unders = home_unders + away_unders
        
        records[team] = {
            'Home Record': f"{home_overs} - {home_unders}",
            'Away Record': f"{away_overs} - {away_unders}",
            'Total Record': f"{total_overs} - {total_unders}"
        }
    
    return pd.DataFrame.from_dict(records, orient='index')

def home_away_over_under_by_team_TP_over(df):
    # Filter dataframe by offense, defense, and RS/PS criteria first
    filtered_df = df[(df['RS/PS'] == 'RS')]
    
    teams = pd.unique(filtered_df[['Home Team', 'Away Team']].values.ravel())
    
    records = {}
    for team in teams:
        year = 2024
        # Home games for team
        home_games = filtered_df[filtered_df['Home Team'] == team]
        home_overs = ((home_games['Tempo and PPG Over (Efficiency Under)'] == 1) & (home_games['Over Hit.4'] == 1) & (home_games['Year'] == year)).sum()
        home_unders = ((home_games['Efficiency/PPG over  (Efficiency Under)'] == 1) & (home_games['Over Hit.4'] == " ") & (home_games['Year'] == year)).sum()

        # Away games for team
        away_games = filtered_df[filtered_df['Away Team'] == team]
        away_overs = ((away_games['Efficiency/PPG over  (Tempo under)'] == 1) & (away_games['Over Hit.4'] == 1) & (away_games['Year'] == year)).sum()
        away_unders = ((away_games['Efficiency/PPG over  (Tempo under)'] == 1) & (away_games['Over Hit.4'] == " ") & (away_games['Year'] == year)).sum()
        
        # Total overs/unders
        total_overs = home_overs + away_overs
        total_unders = home_unders + away_unders
        
        records[team] = {
            'Home Record': f"{home_overs} - {home_unders}",
            'Away Record': f"{away_overs} - {away_unders}",
            'Total Record': f"{total_overs} - {total_unders}"
        }
    
    return pd.DataFrame.from_dict(records, orient='index')

def home_away_over_under_by_team_T_over(df, val):
    # Filter dataframe by offense, defense, and RS/PS criteria first
    filtered_df = df[(df['Over 105 EFF'] == val) &
                     (df['RS/PS'] == 'RS')]
    
    teams = pd.unique(filtered_df[['Home Team', 'Away Team']].values.ravel())
    
    records = {}
    for team in teams:
        year = 2024
        # Home games for team
        home_games = filtered_df[filtered_df['Home Team'] == team]
        home_overs = ((home_games['Just Tempo Over'] == 1) & (home_games['Over Hit.5'] == 1) & (home_games['Year'] == year)).sum()
        home_unders = ((home_games['Just Tempo Over'] == 1) & (home_games['Over Hit.5'] == " ") & (home_games['Year'] == year)).sum()

        # Away games for team
        away_games = filtered_df[filtered_df['Away Team'] == team]
        away_overs = ((away_games['Just Tempo Over'] == 1) & (away_games['Over Hit.5'] == 1) & (away_games['Year'] == year)).sum()
        away_unders = ((away_games['Just Tempo Over'] == 1) & (away_games['Over Hit.5'] == " ") & (away_games['Year'] == year)).sum()
        
        # Total overs/unders
        total_overs = home_overs + away_overs
        total_unders = home_unders + away_unders
        
        records[team] = {
            'Home Record': f"{home_overs} - {home_unders}",
            'Away Record': f"{away_overs} - {away_unders}",
            'Total Record': f"{total_overs} - {total_unders}"
        }
    
    return pd.DataFrame.from_dict(records, orient='index')

def home_away_over_under_by_team_P_over(df, val):
    # Filter dataframe by offense, defense, and RS/PS criteria first
    filtered_df = df[(df['Over 110 EFF'] == val) &
                     (df['RS/PS'] == 'RS')]
    
    teams = pd.unique(filtered_df[['Home Team', 'Away Team']].values.ravel())
    
    records = {}
    for team in teams:
        year = 2024
        # Home games for team
        home_games = filtered_df[filtered_df['Home Team'] == team]
        home_overs = ((home_games['Just PPG Over'] == 1) & (home_games['Over Hit.6'] == 1) & (home_games['Year'] == year)).sum()
        home_unders = ((home_games['Just PPG Over'] == 1) & (home_games['Over Hit.6'] == " ") & (home_games['Year'] == year)).sum()

        # Away games for team
        away_games = filtered_df[filtered_df['Away Team'] == team]
        away_overs = ((away_games['Just PPG Over'] == 1) & (away_games['Over Hit.6'] == 1) & (away_games['Year'] == year)).sum()
        away_unders = ((away_games['Just PPG Over'] == 1) & (away_games['Over Hit.6'] == " ") & (away_games['Year'] == year)).sum()
        
        # Total overs/unders
        total_overs = home_overs + away_overs
        total_unders = home_unders + away_unders
        
        records[team] = {
            'Home Record': f"{home_overs} - {home_unders}",
            'Away Record': f"{away_overs} - {away_unders}",
            'Total Record': f"{total_overs} - {total_unders}"
        }
    
    return pd.DataFrame.from_dict(records, orient='index')

def home_away_over_under_by_team_E_over(df, offense, defense):
    # Filter dataframe by offense, defense, and RS/PS criteria first
    filtered_df = df[(df['OFF Over 105'] == offense) &
                     (df['DEF Over 105'] == defense) &
                     (df['RS/PS'] == 'RS')]
    
    teams = pd.unique(filtered_df[['Home Team', 'Away Team']].values.ravel())
    
    records = {}
    for team in teams:
        year = 2024
        # Home games for team
        home_games = filtered_df[filtered_df['Home Team'] == team]
        home_overs = ((home_games['Just Efficiency Over'] == 1) & (home_games['Over Hit.7'] == 1) & (home_games['Year'] == year)).sum()
        home_unders = ((home_games['Just Efficiency Over'] == 1) & (home_games['Over Hit.7'] == " ") & (home_games['Year'] == year)).sum()

        # Away games for team
        away_games = filtered_df[filtered_df['Away Team'] == team]
        away_overs = ((away_games['Just Efficiency Over'] == 1) & (away_games['Over Hit.7'] == 1) & (away_games['Year'] == year)).sum()
        away_unders = ((away_games['Just Efficiency Over'] == 1) & (away_games['Over Hit.7'] == " ") & (away_games['Year'] == year)).sum()
        
        # Total overs/unders
        total_overs = home_overs + away_overs
        total_unders = home_unders + away_unders
        
        records[team] = {
            'Home Record': f"{home_overs} - {home_unders}",
            'Away Record': f"{away_overs} - {away_unders}",
            'Total Record': f"{total_overs} - {total_unders}"
        }
    
    return pd.DataFrame.from_dict(records, orient='index')

def display_metrics_expand(percent):
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

    return percent_display

def get_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def show_trend(title: str,
               metrics_func,         # e.g. allover_count_win_loss
               metrics_func1,
               metrics_func2,
               records_func,         # e.g. home_away_over_under_by_team
               df: pd.DataFrame,
               game: pd.DataFrame,
               *args):               # variable extra params like o, d, etc.
    """
    Handles: metrics for all/current/previous seasons
             and home/away record display
    """
    # ---- Win/Loss metrics
    count, win, loss = metrics_func(df, *args)
    count_cur, win_cur, loss_cur = metrics_func1(df, *args)
    count_prev, win_prev, loss_prev = metrics_func2(df, *args)

    def pct(w, c): return round((w / c) * 100, 2) if c else 0

    st.markdown(f"<h4 style='text-align:center;margin-bottom:-15px'>{title}</h4>",
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h4 style='text-align:center;text-decoration:underline;'>All Seasons</h4>", unsafe_allow_html=True)
        display_metrics(pct(win, count), win, loss)
    with col2:
        st.markdown("<h4 style='text-align:center;text-decoration:underline;'>Current Season</h4>", unsafe_allow_html=True)
        display_metrics(pct(win_cur, count_cur), win_cur, loss_cur)
    with col3:
        st.markdown("<h4 style='text-align:center;text-decoration:underline;'>Previous Season</h4>", unsafe_allow_html=True)
        display_metrics(pct(win_prev, count_prev), win_prev, loss_prev)

    # ---- Team-specific records
    records_df = records_func(df, *args).reset_index().rename(columns={'index': 'Team'})
    home_map = records_df.set_index('Team')['Home Record'].to_dict()
    away_map = records_df.set_index('Team')['Away Record'].to_dict()
    total_map = records_df.set_index('Team')['Total Record'].to_dict()

    home, away = game['Home Team'], game['Away Team']
    colsb1, c1, c2, colsb2 = st.columns([0.5,5,5,0.5])

    def team_block(team, total, home_away):
        return f"""
        <div style="text-align:center;margin:0;padding:0;">
            <h4 style="text-decoration:underline;margin:0;">{team} vs Trend</h4>
            <div style="margin-top:-15px;"><b>Total: {total}</b></div>
            <div style="margin:0;"><b>{home_away}</b></div>
        </div>
        """

    with c1:
        st.markdown(team_block(home,
                               total_map.get(home,"N/A"),
                               f"Home: {home_map.get(home,'N/A')}"),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(team_block(away,
                               total_map.get(away,"N/A"),
                               f"Away: {away_map.get(away,'N/A')}"),
                    unsafe_allow_html=True)