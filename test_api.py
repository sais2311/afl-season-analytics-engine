import requests

HEADERS = {
    "User-Agent": "AFL Season Engine - Sai Surapaneni - saisurapaneni49@gmail.com"
}

url = "https://api.squiggle.com.au/?q=teams"
response = requests.get(url, headers=HEADERS)

print("Status code:", response.status_code)
data = response.json()
print("Teams returned:", len(data["teams"]))
print("First team:", data["teams"][0])
