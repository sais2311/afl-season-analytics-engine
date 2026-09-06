import requests
import pandas as pd

HEADERS = {
    "User-Agent": "AFL Season Engine - Sai Surapaneni - saisurapaneni49@gmail.com"
}

# The ladder
url = "https://api.squiggle.com.au/?q=standings;year=2026;round=24"
r = requests.get(url, headers=HEADERS)
print("Status code:", r.status_code)

data = r.json()
ladder = pd.DataFrame(data["standings"])

# print the finishing order
print(ladder[["rank", "name", "wins", "losses", "draws", "pts", "percentage"]].to_string(index=False))
