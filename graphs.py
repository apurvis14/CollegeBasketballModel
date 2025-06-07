import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Histogram of ALL Over
subset = df[df['All Formulas Over'] == 1]

combinations = [(2, 2), (2, 1), (1, 2), (1, 1), (1, 0), (0, 1), (0, 0), (0, 2), (2, 0)]
results = []

for o, d in combinations:
    filtered = subset[
        (subset['Offense Over 100'] == o) & 
        (subset['Defense Over 100'] == d)
        ]
    
    count = len(filtered)
    win = len(filtered[filtered['Over Hit'] == 1])
    loss = count - win
    percent = round((win / count) * 100, 2) if count != 0 else None

    if count != 0:
        results.append(((o, d), percent, win, loss))

        # Plot histogram of Total Difference for this combination
        plt.figure(figsize=(8, 5))
        sns.histplot(filtered['Total Difference'], bins=50, kde=True, color='mediumseagreen')
        plt.title(f'Total Difference | Off {o}, Def {d} | Over Hit: {win}/{count} ({percent}%)')
        plt.xlabel('Total Difference (Actual - Book)')
        plt.axvline(x=0, color='red', linestyle='--', label='No Difference')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
