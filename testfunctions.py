import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functions import (
    TPOver_EFFUnder_count_win_loss,
    TPOver_EFFUnder_count_win_loss_current,
    TPOver_EFFUnder_count_win_loss_prev)

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
count, win, loss = TPOver_EFFUnder_count_win_loss(df)
count_current, win_current, loss_current = TPOver_EFFUnder_count_win_loss_current(df)
count_prev, win_prev, loss_prev = TPOver_EFFUnder_count_win_loss_prev(df)

# Print results
print(f"Count: {count}, Wins: {win}, Losses: {loss}")
print(f"Current Count: {count_current}, Wins: {win_current}, Losses: {loss_current}")
print(f"Previous Count: {count_prev}, Wins: {win_prev}, Losses: {loss_prev}")
