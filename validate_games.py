import json
import pandas as pd

# Read the season from the saved file (no API call needed)
with open("season_2026.json") as f:
    data = json.load(f)

games = pd.DataFrame(data["games"])
home_away = games[(games["is_final"] == 0) & (games["complete"] == 100)].copy()

print("QA REPORT - 2026 home-and-away games")
print("Games to analyse:", len(home_away))
print("-" * 40)

# CHECK 1 - scores reconcile (goals x 6 + behinds)
bad_home = home_away[home_away["hgoals"] * 6 + home_away["hbehinds"] != home_away["hscore"]]
bad_away = home_away[home_away["agoals"] * 6 + home_away["abehinds"] != home_away["ascore"]]
print("Check 1 - score mismatches:", len(bad_home) + len(bad_away))

# CHECK 2 - no missing values in fields our analyses depend on
key_cols = ["hteam", "ateam", "hscore", "ascore", "round", "winner"]
missing = home_away[key_cols].isnull().sum().sum()
print("Check 2 - missing key values:", missing)

# CHECK 3 - every round 1-23 present, none skipped
rounds_present = sorted(home_away["round"].unique())
expected = list(range(1, 24))
missing_rounds = [r for r in expected if r not in rounds_present]
print("Check 3 - rounds present:", rounds_present)
print("Check 3 - missing rounds:", missing_rounds)
print("-" * 40)
print("QA complete.")
