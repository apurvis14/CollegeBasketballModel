import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

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

def determine_trend(row):
    if row['All Formulas Over'] == 1:
        o = row['Offense Over 100']
        d = row['Defense Over 100']
        return f"All Over - {o} OFF and {d} DEF over 100"
    
    elif row['All Formulas Under'] == 1:
        o = row['Offense Under 100']
        d = row['Defense Under 100']
        return f"All Under - {o} OFF and {d} DEF under 100"
    
    elif row['Efficiency/PPG over  (Tempo under)'] == 1:
        o1 = row['Count of OFF over 100']
        o2 = row['Count of OFF over 110']
        d1 = row['Count of DEF under 100']
        d2 = row['Count of DEF under 95']
        return f"EP Over/Tempo Under - {o1}/{o2} OFF over 100/110 - {d1}/{d2} DEF under 100/95"
    
    elif row['Tempo and Efficiency over (PPG under)'] == 1:
        o1 = row['OFF Under 100']
        o2 = row['OFF Under 95']
        d1 = row['DEF Under 100']
        d2 = row['DEF Under 95']
        return f"TE Over/PPG Under - {o1}/{o2} OFF under 100/95 - {d1}/{d2} DEF under 100/95"
    
    elif row['Tempo and PPG over (Efficiency Under)'] == 1:
        return "Tempo and PPG over (Efficiency Under)"
    
    elif row['Just Tempo Over'] == 1:
        val = row['Over 105 EFF']    
        return f"Only Tempo Over - {val} OFF/DEF over 105"
    
    elif row['Just PPG Over'] == 1:
        val = row['Over 110 EFF']
        return f"Only PPG Over - {val} OFF/DEF over 110"
    
    elif row['Just Efficiency Over'] == 1:
        o = row['OFF Over 105']
        d = row['DEF Over 105']
        return f"Only EFF Under - {o} OFF / {d} DEF over 105"
    
    else:
        return None  # or "" if you prefer

# Apply to the DataFrame
df['Trend'] = df.apply(determine_trend, axis=1)
df['Over'] = np.where(df['Book Total'] < df['Actual Total'], 1, 0)
df['Under'] = np.where(df['Over'] == 1, 0, 1)

trend_counts = df['Trend'].value_counts()
# Convert to a new DataFrame
trend_df = trend_counts.reset_index()
trend_df.columns = ['Trend', 'Count']
# print(trend_df)

df['trend_overs'] = (
    df.groupby('Trend')['Over']
    .transform(lambda x: x.cumsum().shift(1).fillna(0)))
df['trend_occur'] = df.groupby('Trend')['Over'].cumcount()
df['trend_pct'] = ((df['trend_overs'] / df['trend_occur']) * 100).fillna(0)

df['trend_L10'] = (
    df.groupby('Trend')['Over']
    .transform(lambda x: x.shift(1).rolling(window=25, min_periods=1).mean() * 100)
)

df['trend_pct_std'] = (
    df.groupby('Trend')['trend_pct']
      .apply(lambda x: x.expanding().std().shift(1))
      .reset_index(level=0, drop=True))

df['trend_pct_ratio'] = np.where(
    df['trend_pct_std'].fillna(0) == 0,  # condition: std is 0
    0,                                   # if true, set 0
    (df['trend_pct'] - 50) / df['trend_pct_std']  # else, do normal division
    )

window = 25

df['trend_pct_rolling_std'] = (
    df.groupby('Trend')['trend_L10']
      .transform(lambda x: x.rolling(window).std())
)

df['trend_pct_ratio_roll'] = np.where(
    df['trend_pct_rolling_std'].fillna(0) == 0,
    0,
    (df['trend_L10'] - 50) / df['trend_pct_rolling_std']
)

avg_ratio_over = df.loc[df['Over'] == 1, 'trend_pct_ratio_roll'].mean()
avg_ratio_under = df.loc[df['Over'] == 0, 'trend_pct_ratio_roll'].mean()

avg_std_over = df.loc[df['Over'] == 1, 'trend_pct_ratio_roll'].std()
avg_std_under = df.loc[df['Over'] == 0, 'trend_pct_ratio_roll'].std()

print(avg_ratio_over)
print(avg_ratio_under)
print(avg_std_over)
print(avg_std_under)

corr = df['trend_pct_ratio_roll'].corr(df['Over'])
print("Correlation between ratio and Over outcome:", corr)

# define bins for your ratio
bins = [-999, -2, -1, -0.5, 0, 0.5, 1, 2, 999]
labels = ["<-2", "-2 to -1", "-1 to -0.5", "-0.5 to 0", "0 to 0.5", "0.5 to 1", "1 to 2", ">2"]

df['ratio_bin'] = pd.cut(df['trend_pct_ratio_roll'], bins=bins, labels=labels)

# calculate Over hit rate within each bin
diagnostic = (
    df.groupby('ratio_bin')
      .agg(
          games=('Over', 'count'),
          over_hits=('Over', 'sum')
      )
      .assign(over_rate=lambda x: (x['over_hits'] / x['games']) * 100)
      .reset_index()
)

print(diagnostic)


# df['signal'] = np.where(
#     (df['trend_pct_ratio'] > 0.5) & (df['trend_pct_ratio_roll'] > 1),
#     "Bet Over",
#     np.where(
#         (df['trend_pct_ratio'] < -0.5) & (df['trend_pct_ratio_roll'] < -1),
#         "Bet Under",
#         "No Bet"
#     )
# )

# count = df['signal'].value_counts()
# over_count = (df['signal'] == 'Bet Over').sum()
# under_count = (df['signal'] == 'Bet Under').sum()

# over_win = ((df['signal'] == 'Bet Over') & (df['Over'] == 1)).sum()
# under_win = ((df['signal'] == 'Bet Under') & (df['Under'] == 1)).sum()

# print(over_win/over_count)
# print(under_win/under_count)

# trend_summary = df.groupby('Trend').apply(
#     lambda g: pd.Series({
#         'count_gt1': (g['trend_pct_ratio'] > 0.6).sum(),
#         'count_lt-1': (g['trend_pct_ratio'] < -0.8).sum(),
#         'over_hit_rate_gt1': g.loc[g['trend_pct_ratio'] > 0.6, 'Over'].mean(),
#         'under_hit_rate_lt-1': (1 - g.loc[g['trend_pct_ratio'] < -0.8, 'Over']).mean(),
#         'total_games': len(g)
#     })
# ).reset_index()

# trend_summary = trend_summary.fillna(0)
# trend_summary.sort_values('over_hit_rate_gt1', ascending=False)
# trend_summary.to_csv("Trend Ratio.csv", index=False)


df['trend_overs_szn'] = (
    df.groupby(['Trend', 'Year'], observed=True)['Over']
    .transform(lambda x: x.cumsum().shift(1).fillna(0)))
df['trend_occur_szn'] = df.groupby(['Trend', 'Year'], observed=True)['Over'].cumcount()
df['trend_pct_szn'] = (df['trend_overs_szn'] / df['trend_occur_szn']) * 100

# df['Suggestion'] = np.where((df['trend_pct'] > 60) & (df['trend_L10'] > 60) & (df['trend_pct_szn'] > 60), 
#                             "Over", np.where((df['trend_pct'] < 40) & (df['trend_L10'] < 40) & (df['trend_pct_szn'] < 40), "Under", "None"))

# count = df['Suggestion'].value_counts()
# over_count = (df['Suggestion'] == 'Over').sum()
# under_count = (df['Suggestion'] == 'Under').sum()

# over_win = ((df['Suggestion'] == 'Over') & (df['Over'] == 1)).sum()
# under_win = ((df['Suggestion'] == 'Under') & (df['Under'] == 1)).sum()

# print(over_win/over_count)
# print(under_win/under_count)

def get_suggestion(percent_cur, percent_all, count_cur, count_all):
    # Convert to numeric just in case
    if pd.isna(percent_cur) or pd.isna(percent_all):
        return "None"

    if count_all <= 50 and count_cur <= 15:
        return "None"
    elif count_cur <= 15:
        return "None"
    elif count_all <= 50:
        return "None"    

    if percent_cur >= 60 and percent_all >= 55:
        return "Strong Over"
    elif percent_cur >= 60 and 52 <= percent_all < 55:
        return "Over"
    elif percent_cur >= 60 and 50 <= percent_all < 52:
        return "Over / Avoid"
    elif percent_cur >= 60 and percent_all < 50:
        return "Avoid"

    elif percent_cur >= 55 and percent_all >= 60:
        return "Strong Over"
    elif percent_cur >= 55 and percent_all >= 52.5:
        return "Over"
    elif percent_cur >= 55 and 50 <= percent_all < 52.5:
        return "Over / Avoid"
    elif percent_cur >= 55 and percent_all < 50:
        return "Avoid"

    elif 52 <= percent_cur < 55 and percent_all >= 60:
        return "Strong Over"
    elif 52 <= percent_cur < 55 and percent_all >= 55:
        return "Over"
    elif 52 <= percent_cur < 55 and 52 <= percent_all < 55:
        return "Over"
    elif 52 <= percent_cur < 55 and percent_all < 52:
        return "Avoid"

    elif 50 < percent_cur < 52 and percent_all >= 60:
        return "Over"
    elif 50 < percent_cur < 52 and percent_all >= 53:
        return "Over"
    elif 50 < percent_cur < 52 and 50 <= percent_all < 53:
        return "Over Avoid"
    elif 48 < percent_cur < 50 and 42 < percent_all < 46:
        return "Under"
    elif 48 < percent_cur < 50 and percent_all <= 42:
        return "Under"

    elif 46 < percent_cur <= 48 and percent_all >= 60:
        return "Avoid"
    elif 46 < percent_cur <= 48 and percent_all >= 55:
        return "Avoid"
    elif 46 < percent_cur <= 48 and 48 < percent_all < 55:
        return "Avoid"
    elif 46 < percent_cur <= 48 and 46 < percent_all <= 48:
        return "Under / Avoid"
    elif 46 < percent_cur <= 48 and 42 < percent_all <= 46:
        return "Under"
    elif 46 < percent_cur <= 48 and percent_all <= 42:
        return "Moderate Under"

    elif 40 <= percent_cur <= 46 and percent_all >= 50:
        return "Avoid"
    elif 40 <= percent_cur <= 46 and 46 <= percent_all < 50:
        return "Under"
    elif 40 <= percent_cur <= 46 and 40 <= percent_all <= 46:
        return "Under"
    elif 40 <= percent_cur <= 46 and percent_all < 40:
        return "Strong Under"

    elif percent_cur < 40 and percent_all >= 50:
        return "Avoid"
    elif percent_cur < 40 and 48 <= percent_all < 50:
        return "Under"
    elif percent_cur < 40 and 40 <= percent_all < 48:
        return "Under"
    elif percent_cur < 40 and percent_all < 40:
        return "Strong Under"
    else:
        return "Avoid"

# def get_suggestion(percent_cur, percent_all, count_cur, count_all):
#     if pd.isna(percent_cur) or pd.isna(percent_all):
#         return "None"

#     # Require enough games to be meaningful
#     if count_all <= 15 or count_cur <= 10:
#         return "None"

#     # --- Strong Over / Over logic (relaxed) ---
#     if percent_cur >= 58 and percent_all >= 55:
#         return "Strong Over"
#     elif percent_cur >= 55 and percent_all >= 52:
#         return "Over"
#     elif percent_cur >= 52 and 50 <= percent_all < 52:
#         return "Over / Avoid"
#     elif percent_cur >= 52 and percent_all < 50:
#         return "Avoid"

#     # --- Neutral / Avoid zone ---
#     elif 48 <= percent_cur < 52:
#         return "Avoid"

#     # --- Strong Under / Under logic (relaxed) ---
#     elif percent_cur <= 42 and percent_all <= 45:
#         return "Strong Under"
#     elif percent_cur <= 45 and percent_all <= 48:
#         return "Under"
#     elif percent_cur <= 48 and 48 < percent_all <= 50:
#         return "Under / Avoid"
#     elif percent_cur <= 48 and percent_all > 50:
#         return "Avoid"

#     return "None"

df['Suggestion'] = df.apply(lambda x: get_suggestion(x['trend_pct'], x['trend_pct_szn'], x['trend_occur_szn'], x['trend_occur']), axis=1)

df['suggestion_overs'] = (
    df.groupby('Suggestion')['Over']
    .transform(lambda x: x.cumsum().shift(1).fillna(0)))
df['suggestion_unders'] = (df.groupby('Suggestion')['Under']
    .transform(lambda x: x.cumsum().shift(1).fillna(0)))

df['suggestion_total'] = df.groupby(['Suggestion',], observed=True)['Over'].cumcount()



# ## -- Plot -- ##
# # # Filter for All Formulas Over and dates after 12/01/2024 Add bck if need be & (df['Date'] > '2024-12-01')
# over_df = df[(df['All Formulas Over'] == 1)]

# # Get unique trends
# unique_trends = over_df['Trend'].dropna().unique()
# n_trends = len(unique_trends)

# # Grid layout: 3 subplots per row
# n_cols = 3
# n_rows = math.ceil(n_trends / n_cols)

# fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), sharex=False)

# # Flatten axes for easy indexing (in case of 1 row/column)
# axes = axes.flatten()

# # Plot each trend
# for i, trend in enumerate(unique_trends):
#     trend_data = over_df[over_df['Trend'] == trend]
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct'], marker='o')
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct_szn'], marker='o')
#     axes[i].set_title(trend)
#     axes[i].set_ylabel('Trend %')
#     axes[i].grid(True)

# # Turn off any unused subplots
# for j in range(i+1, len(axes)):
#     axes[j].axis('off')

# # Adjust layout
# plt.tight_layout()
# plt.show()

# under_df = df[(df['All Formulas Under'] == 1)]

# # Get unique trends
# unique_trends = under_df['Trend'].dropna().unique()
# n_trends = len(unique_trends)

# # Grid layout: 3 subplots per row
# n_cols = 3
# n_rows = math.ceil(n_trends / n_cols)

# fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), sharex=False)

# # Flatten axes for easy indexing (in case of 1 row/column)
# axes = axes.flatten()

# # Plot each trend
# for i, trend in enumerate(unique_trends):
#     trend_data = under_df[under_df['Trend'] == trend]
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct'], marker='o')
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct_szn'], marker='o')
#     axes[i].set_title(trend)
#     axes[i].set_ylabel('Trend %')
#     axes[i].grid(True)

# # Turn off any unused subplots
# for j in range(i+1, len(axes)):
#     axes[j].axis('off')

# # Adjust layout
# plt.tight_layout()
# plt.show()

# EPT_df = df[(df['Efficiency/PPG over  (Tempo under)'] == 1)]

# # Get unique trends
# unique_trends = EPT_df['Trend'].dropna().unique()
# n_trends = len(unique_trends)

# # Grid layout: 3 subplots per row
# n_cols = 3
# n_rows = math.ceil(n_trends / n_cols)

# fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), sharex=False)

# # Flatten axes for easy indexing (in case of 1 row/column)
# axes = axes.flatten()

# # Plot each trend
# for i, trend in enumerate(unique_trends):
#     trend_data = EPT_df[EPT_df['Trend'] == trend]
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct'], marker='o')
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct_szn'], marker='o')
#     axes[i].set_title(trend)
#     axes[i].set_ylabel('Trend %')
#     axes[i].grid(True)

# # Turn off any unused subplots
# for j in range(i+1, len(axes)):
#     axes[j].axis('off')

# # Adjust layout
# plt.tight_layout()
# plt.show()

# TEP_df = df[(df['Tempo and Efficiency over (PPG under)'] == 1)]

# # Get unique trends
# unique_trends = TEP_df['Trend'].dropna().unique()
# n_trends = len(unique_trends)

# # Grid layout: 3 subplots per row
# n_cols = 3
# n_rows = math.ceil(n_trends / n_cols)

# fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), sharex=False)

# # Flatten axes for easy indexing (in case of 1 row/column)
# axes = axes.flatten()

# # Plot each trend
# for i, trend in enumerate(unique_trends):
#     trend_data = TEP_df[TEP_df['Trend'] == trend]
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct'], marker='o')
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct_szn'], marker='o')
#     axes[i].set_title(trend)
#     axes[i].set_ylabel('Trend %')
#     axes[i].grid(True)

# # Turn off any unused subplots
# for j in range(i+1, len(axes)):
#     axes[j].axis('off')

# # Adjust layout
# plt.tight_layout()
# plt.show()

# TPE_df = df[(df['Tempo and PPG over (Efficiency Under)'] == 1)]

# # Get unique trends
# unique_trends = TPE_df['Trend'].dropna().unique()
# n_trends = len(unique_trends)

# # Grid layout: 3 subplots per row
# n_cols = 3
# n_rows = math.ceil(n_trends / n_cols)

# fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), sharex=False)

# # Flatten axes for easy indexing (in case of 1 row/column)
# axes = axes.flatten()

# # Plot each trend
# for i, trend in enumerate(unique_trends):
#     trend_data = TPE_df[TPE_df['Trend'] == trend]
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct'], marker='o')
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct_szn'], marker='o')
#     axes[i].set_title(trend)
#     axes[i].set_ylabel('Trend %')
#     axes[i].grid(True)

# # Turn off any unused subplots
# for j in range(i+1, len(axes)):
#     axes[j].axis('off')

# # Adjust layout
# plt.tight_layout()
# plt.show()

# T_df = df[(df['Just Tempo Over'] == 1)]

# # Get unique trends
# unique_trends = T_df['Trend'].dropna().unique()
# n_trends = len(unique_trends)

# # Grid layout: 3 subplots per row
# n_cols = 3
# n_rows = math.ceil(n_trends / n_cols)

# fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), sharex=False)

# # Flatten axes for easy indexing (in case of 1 row/column)
# axes = axes.flatten()

# # Plot each trend
# for i, trend in enumerate(unique_trends):
#     trend_data = T_df[T_df['Trend'] == trend]
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct'], marker='o')
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct_szn'], marker='o')
#     axes[i].set_title(trend)
#     axes[i].set_ylabel('Trend %')
#     axes[i].grid(True)

# # Turn off any unused subplots
# for j in range(i+1, len(axes)):
#     axes[j].axis('off')

# # Adjust layout
# plt.tight_layout()
# plt.show()

# P_df = df[(df['Just PPG Over'] == 1)]

# # Get unique trends
# unique_trends = P_df['Trend'].dropna().unique()
# n_trends = len(unique_trends)

# # Grid layout: 3 subplots per row
# n_cols = 3
# n_rows = math.ceil(n_trends / n_cols)

# fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), sharex=False)

# # Flatten axes for easy indexing (in case of 1 row/column)
# axes = axes.flatten()

# # Plot each trend
# for i, trend in enumerate(unique_trends):
#     trend_data = P_df[P_df['Trend'] == trend]
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct'], marker='o')
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct_szn'], marker='o')
#     axes[i].set_title(trend)
#     axes[i].set_ylabel('Trend %')
#     axes[i].grid(True)

# # Turn off any unused subplots
# for j in range(i+1, len(axes)):
#     axes[j].axis('off')

# # Adjust layout
# plt.tight_layout()
# plt.show()

# E_df = df[(df['Just Efficiency Over'] == 1)]

# # Get unique trends
# unique_trends = E_df['Trend'].dropna().unique()
# n_trends = len(unique_trends)

# # Grid layout: 3 subplots per row
# n_cols = 3
# n_rows = math.ceil(n_trends / n_cols)

# fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), sharex=False)

# # Flatten axes for easy indexing (in case of 1 row/column)
# axes = axes.flatten()

# # Plot each trend
# for i, trend in enumerate(unique_trends):
#     trend_data = E_df[E_df['Trend'] == trend]
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct'], marker='o')
#     axes[i].plot(trend_data['Date'], trend_data['trend_pct_szn'], marker='o')
#     axes[i].set_title(trend)
#     axes[i].set_ylabel('Trend %')
#     axes[i].grid(True)

# # Turn off any unused subplots
# for j in range(i+1, len(axes)):
#     axes[j].axis('off')

# # Adjust layout
# plt.tight_layout()
# plt.show()

df.to_csv("CSV of Model Data.csv", index=False)

avg_OFF_EFF = (
    df.loc[
        (df['All Formulas Under'] == 1) & (df['Over'] == 1),
        ['Home Adj OFF', 'Away Adj OFF']
    ]
    .mean()
    .mean()
)

avg_OFF_EFF_diff = (
    df.loc[
        (df['All Formulas Under'] == 1) & (df['Over'] == 1),
        ['Home Adj OFF', 'Away Adj OFF']
    ]
    .apply(lambda x: x['Home Adj OFF'] - x['Away Adj OFF'], axis=1)
    .mean()
)

avg_OFF_EFF_under = (
    df.loc[
        (df['All Formulas Under'] == 1) & (df['Over'] == 0),
        ['Home Adj OFF', 'Away Adj OFF']
    ]
    .mean()
    .mean()
)

avg_OFF_EFF_diff_under = (
    df.loc[
        (df['All Formulas Under'] == 1) & (df['Over'] == 0),
        ['Home Adj OFF', 'Away Adj OFF']
    ]
    .apply(lambda x: x['Home Adj OFF'] - x['Away Adj OFF'], axis=1)
    .mean()
)

print(avg_OFF_EFF)
print(avg_OFF_EFF_diff)
print(avg_OFF_EFF_under)
print(avg_OFF_EFF_diff_under)

count_under = (
    df.loc[
        (df['All Formulas Under'] == 1) &
        (df['Over'] == 1) &
        (df['Home Adj OFF'] > df['Away Adj OFF'])
    ]
    .shape[0]
)

count = (
    df.loc[
        (df['All Formulas Under'] == 1) &
        (df['Over'] == 1)
        #(df['Home Adj OFF'] > df['Away Adj OFF'])
    ]
    .shape[0]
)

print(count_under/count)