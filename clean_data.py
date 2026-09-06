import json
import pandas as pd

with open("season_2026.json") as f:
    data = json.load(f)

games = pd.DataFrame(data["games"])
home_away = games[(games["is_final"] == 0) & (games["complete"] == 100)].copy()

# Labeling each game's result explicitly, so no winner would ever break anything
def result(row):
    if row["hscore"] > row["ascore"]:
        return "home"
    elif row["ascore"] > row["hscore"]:
        return "away"
    else:
        return "draw"

home_away["result"] = home_away.apply(result, axis=1)

print("Result breakdown:")
print(home_away["result"].value_counts())
print("-" * 40)

# Save the clean, analysis-ready dataset
home_away.to_csv("games_clean.csv", index=False)
print(f"Saved {len(home_away)} clean games to games_clean.csv")
