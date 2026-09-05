import requests
import json

HEADERS = {
    "User-Agent": "AFL Season Engine - Sai Surapaneni - saisurapaneni49@gmail.com"
}
url = "https://api.squiggle.com.au/?q=games;year=2026"

print("Fetching 2026 season from Squiggle...")
r = requests.get(url, headers=HEADERS)

if r.status_code == 200:
    data = r.json()
    with open("season_2026.json", "w") as f:
        json.dump(data, f)
    print(f"Saved {len(data['games'])} games to season_2026.json")
else:
    print(f"Request failed with status {r.status_code} - wait a bit and retry.")
