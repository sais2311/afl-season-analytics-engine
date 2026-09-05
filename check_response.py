import requests

HEADERS = {
    "User-Agent": "AFL Season Engine - Sai Surapaneni - your.email@example.com"
}
url = "https://api.squiggle.com.au/?q=games;year=2026"
r = requests.get(url, headers=HEADERS)

print("Status code:", r.status_code)
print("First 300 chars of response:")
print(r.text[:300])
