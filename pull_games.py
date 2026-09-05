import requests

HEADERS = {
    "User-Agent": "AFL Season Engine - Sai Surapaneni - saisurapaneni49@gmail.com"
}

url = "https://api.squiggle.com.au/?q=games;year=2026"
response = requests.get(url, headers=HEADERS)

print("Status code:", response.status_code)
data = response.json()
games = data["games"]
print("Games returned:", len(games))
print("First game:", games[0])
