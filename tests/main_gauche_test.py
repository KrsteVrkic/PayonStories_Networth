import requests


API_BASE = "https://tools.payonstories.com/api"


def inspect_matching_history(
    item_id,
    refine,
    c0,
    c1=0,
    c2=0,
    c3=0
):

    response = requests.get(
        f"{API_BASE}/pc/history",
        params={"id": item_id},
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
                filter_data["r"] == refine
                and filter_data["c0"] == c0
                and filter_data["c1"] == c1
                and filter_data["c2"] == c2
                and filter_data["c3"] == c3
            ):

                matches.append({
                    "date": entry["x"],
                    "price": float(price),
                    "filter": filter_data
                })

                if len(matches) >= 10:
                    return matches

    return matches


matches = inspect_matching_history(
    1208,
    refine=10,
    c0=0
)

for match in matches:
    print(match)