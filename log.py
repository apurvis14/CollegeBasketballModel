import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report


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
df = df.fillna(0)
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

df['trend_overs_szn'] = (
    df.groupby(['Trend', 'Year'], observed=True)['Over']
    .transform(lambda x: x.cumsum().shift(1).fillna(0)))
df['trend_occur_szn'] = df.groupby(['Trend', 'Year'], observed=True)['Over'].cumcount()
df['trend_pct_szn'] = (df['trend_overs_szn'] / df['trend_occur_szn']) * 100

### --- LOG REGRESSION --- ###
# Filter out rows without a defined trend
df = df[df['Trend'].notnull()]

# Create dummy variables for trends
trend_dummies = pd.get_dummies(df['Trend'], prefix='Trend')

# Combine back into dataframe
df_model = pd.concat([df, trend_dummies], axis=1)

# Define target variable (Over)
y = df_model['Over']

# Example: include your engineered trend metrics
features = ["trend_pct", "trend_L10", "trend_pct_szn"]

# Combine with trend dummies
X = df_model[features + list(trend_dummies.columns)]

# Force numeric conversion for all features
X = X.apply(pd.to_numeric, errors='coerce')

# Fill NaN (from conversion failures) with 0
X = X.fillna(0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_prob))
print(classification_report(y_test, y_pred))

coefficients = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=False)

print(coefficients)