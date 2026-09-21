import requests


url = "https://tools.payonstories.com/card_database"

response = requests.get(
    url,
    timeout=30
)

print("Status:", response.status_code)
print("Bytes:", len(response.content))

print("Hydra Card" in response.text)
print("Bloody" in response.text)