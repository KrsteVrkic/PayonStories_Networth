import requests

search_url = "https://tools.payonstories.com/api/db/search"
params = {"q": "Hat"}

response = requests.get(search_url, params=params)
response.raise_for_status()

data = response.json()

items = [
    result
    for result in data.get("results", [])
    if result.get("type") == "item"
    and result.get("title") == "Hat"
]

results = []

for item in items:
    item_id = item["id"]

    item_url = "https://tools.payonstories.com/api/pc/item"
    item_params = {"id": item_id}

    response = requests.get(item_url, params=item_params)
    response.raise_for_status()

    item_data = response.json()

    results.append({
        "id": item_id,
        "name": item_data.get("name"),
        "slots": item_data.get("slots")
    })
best = max(results, key=lambda item: item["slots"])
print(best)