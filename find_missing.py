import json
import pandas as pd

with open("season_2026.json") as f:
    data = json.load(f)

games = pd.DataFrame(data["games"])
home_away = games[(games["is_final"] == 0) & (games["complete"] == 100)].copy()

key_cols = ["hteam", "ateam", "hscore", "ascore", "round", "winner"]

# Which columns have missing values, and how many each?
print("Missing values per column:")
print(home_away[key_cols].isnull().sum())
print("-" * 40)

# Show the actual rows that have a missing value in any key column
bad_rows = home_away[home_away[key_cols].isnull().any(axis=1)]
print("Rows with a missing value:")
print(bad_rows[["round", "hteam", "ateam", "hscore", "ascore", "winner"]])
