import pandas as pd
import numpy as np

df = pd.read_csv("Final Regular Season Data/Final_Regular_Season_Data_2023_2024.csv")

# Get a Excel Worksheet from existing excel file
df_test = pd.read_excel("data/College Basketball Model.xlsm", sheet_name='Poss. Per Game')
df_test.to_csv('test.csv', index=False)

df_ppg = pd.read_excel("data/College Basketball Model.xlsm", sheet_name='OFF PPG')
df_ppg.to_csv('ppg.csv', index=False)

home_df = df[['game_id', 'game_day', 'home_team', 'home_id', 'home_score', 'is_neutral', 'home_poss']].copy()

# Create a Home average points per game column and possessions per game column
home_df['points_home'] = (
    home_df.groupby('home_team')['home_score']
    .transform(lambda x: x.shift().expanding().mean())
    .fillna(0)
)
home_df['poss_home'] = (
    home_df.groupby('home_team')['home_poss']
    .transform(lambda x: x.shift().expanding().mean())
    .fillna(0)
)

# home_df['home_binary'] = 1

home_df.sort_values(by=['home_team', 'game_day'], inplace=True)
home_df.to_csv('home_df.csv', index=False)

home_df.rename(columns={'home_team': 'team', 'home_id': 'team_id', 'home_score': 'points', 'home_poss': 'poss'}, inplace=True)

away_df = df[['game_id', 'game_day', 'away_team', 'away_id', 'away_score', 'is_neutral', 'away_poss']].copy()

# Create an Away average points per game column and possessions per game column
away_df['points_away'] = (
    away_df.groupby('away_team')['away_score']
    .transform(lambda x: x.shift().expanding().mean())
    .fillna(0)
)
away_df['poss_away'] = (
    away_df.groupby('away_team')['away_poss']
    .transform(lambda x: x.shift().expanding().mean())
    .fillna(0)
)

away_df.sort_values(by=['away_team', 'game_day'], inplace=True)
away_df.to_csv('away_df.csv', index=False)

away_df.rename(columns={'away_team': 'team', 'away_id': 'team_id', 'away_score': 'points', 'away_poss': 'poss'}, inplace=True)

long_df = pd.concat([home_df, away_df], ignore_index=True)
# Fill NaN values with 0
long_df = long_df.fillna(0)
# Sort by team and game date
long_df = long_df.sort_values(by=['team', 'game_day'])
long_df.to_csv('long_df.csv', index=False)

# Step 2: Sort by team and game date
long_df['game_day'] = pd.to_datetime(long_df['game_day'])
long_df = long_df.sort_values(by=['team', 'game_day'])

# Step 3: Group by team and calculate cumulative average **before** each game
long_df['points_before_game'] = (
    long_df.groupby('team')['points']
    .transform(lambda x: x.shift().expanding().mean())
    .fillna(0)
)

long_df['poss_before_game'] = (
    long_df.groupby('team')['poss']
    .transform(lambda x: x.shift().expanding().mean())
    .fillna(0)
)

# Add Last 3 Games Averages for Points and Possessions
long_df['points_last_3'] = (
    long_df.groupby('team')['points']
    .transform(lambda x: x.shift().rolling(window=3, min_periods=1).mean())
    .fillna(0)
)

long_df['poss_last_3'] = (
    long_df.groupby('team')['poss']
    .transform(lambda x: x.shift().rolling(window=3, min_periods=1).mean())
    .fillna(0)
)

# Add Last 1 Game Averages for Points and Possessions
long_df['points_last_1'] = (
    long_df.groupby('team')['points']
    .transform(lambda x: x.shift().rolling(window=1, min_periods=1).mean())
    .fillna(0)
)
long_df['poss_last_1'] = (
    long_df.groupby('team')['poss']
    .transform(lambda x: x.shift().rolling(window=1, min_periods=1).mean())
    .fillna(0)
)

# Optional: Round for cleaner view
long_df['points_before_game'] = long_df['points_before_game'].round(2)
long_df['poss_before_game'] = long_df['poss_before_game'].round(2)

# Final result
print(long_df[['game_id', 'team', 'points', 'points_before_game', 'poss_before_game']])

long_df.to_csv('team_avg.csv', index=False)

# I want to get the Poss Per Game that occurs last for each team in the season from the team_avg.csv file 
final_avg_df = long_df.sort_values(by=['team', 'game_day']).groupby('team').tail(1)
final_avg_df = final_avg_df[['team', 'points_before_game', 'poss_before_game']]
final_avg_df.rename(columns={'points_before_game': 'Avg Points Per Game', 'poss_before_game': 'Avg Poss Per Game'}, inplace=True)

# Remove any rows with 0 in either Avg Points Per Game or Avg Poss Per Game
final_avg_df = final_avg_df[(final_avg_df['Avg Points Per Game'] != 0) & (final_avg_df['Avg Poss Per Game'] != 0)]

# Reset index
final_avg_df = final_avg_df.reset_index(drop=True)
final_avg_df.to_csv('Final_Team_Averages_2023_2024.csv', index=False)