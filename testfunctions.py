import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functions import home_away_over_under_by_team


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

# def all_over_combinations_by_team_table(df):
#     # Filter to "All Formulas Over"
#     subset = df[df['All Formulas Over'] == 1]

#     # Define combinations of (PPG Over, Efficiency Over)
#     combinations = [(2, 2), (2, 1), (1, 2), (1, 1), (1, 0), (0, 1), (0, 0), (0, 2), (2, 0)]

#     # Store all combinations in one list of DataFrames
#     all_tables = []

#     for o, d in combinations:
#         # Filter for this specific combo and regular season
#         filtered = subset[
#             (subset['Offense Over 100'] == o) &
#             (subset['Defense Over 100'] == d) &
#             (subset['RS/PS'] == "RS")
#         ]

#         # Group by Home Team and count wins/losses
#         summary = filtered.groupby('Home Team').agg(
#             Over_Hit=('Over Hit', lambda x: (x == 1).sum()),
#             Under_Hit=('Over Hit', lambda x: (x == " ").sum())
#         ).reset_index()

#         # Add combination as a new column
#         summary['Combo'] = f"OFF {o}, DEF {d}"

#         all_tables.append(summary)

#     # Concatenate all combinations into one table
#     final_table = pd.concat(all_tables, ignore_index=True)

#     return final_table

# table = all_over_combinations_by_team_table(df)
# print(table)

df_records = home_away_over_under_by_team(df, 2, 2)
print(df_records)

