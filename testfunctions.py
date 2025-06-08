import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functions import (
    allover_count_win_loss,
    allover_count_win_loss_current,
    allover_count_win_loss_prev)

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


# All Over Function from import to get wins and losses
# Count Wins and Losses
percent, wins, losses = allover_count_win_loss(df, 2, 2)
percent_cur, wins_cur, losses_cur = allover_count_win_loss_current(df, 2, 2)
percent_prev, wins_prev, losses_prev = allover_count_win_loss_prev(df, 2, 2)

all_units_won = wins * .909
all_units_lost = losses * 1
all_net_units = all_units_won - all_units_lost
print(f"Units Won: {all_units_won}, Units Lost: {all_units_lost}, Net Units: {all_net_units}")

current_units_won = wins_cur * .909
current_units_lost = losses_cur * 1
current_net_units = current_units_won - current_units_lost
print(f"Current Units Won: {current_units_won}, Current Units Lost: {current_units_lost}, Current Net Units: {current_net_units}")

previous_units_won = wins_prev * .909
previous_units_lost = losses_prev * 1
previous_net_units = previous_units_won - previous_units_lost
print(f"Previous Units Won: {previous_units_won}, Previous Units Lost: {previous_units_lost}, Previous Net Units: {previous_net_units}")

