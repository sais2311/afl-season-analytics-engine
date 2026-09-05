import requests
import pandas as pd

HEADERS = {
    "User-Agent": "AFL Season Engine - Sai Surapaneni - saisurapaneni49@gmail.com"
}

url = "https://api.squiggle.com.au/?q=games;year=2026"
data = requests.get(url, headers=HEADERS).json()

# Turn the list of game dicts into a table
games = pd.DataFrame(data["games"])

print("Shape (rows, columns):", games.shape)
print()
print("Complete (100 = finished game):")
print(games["complete"].value_counts())
print()
print("Finals vs home-and-away (is_final, 0 = home-and-away):")
print(games["is_final"].value_counts())
