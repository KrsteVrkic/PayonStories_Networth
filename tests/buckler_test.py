import requests


API_BASE = "https://tools.payonstories.com/api"


def inspect_buckler():

    response = requests.get(
        f"{API_BASE}/pc/history",
        params={"id": 2103},
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    matches = []

    for entry in data["sellHistory"]:

        for price, filter_data in zip(
            entry["y"],
            entry["filter"]
        ):

            if (
                filter_data["r"] == 0
                and filter_data["c0"] == 0
                and filter_data["c1"] == 0
                and filter_data["c2"] == 0
                and filter_data["c3"] == 0
            ):

                matches.append({
                    "date": entry["x"],
                    "price": int(float(price))
                })

                if len(matches) >= 10:
                    return matches

    return matches


for sale in inspect_buckler():
    print(sale)