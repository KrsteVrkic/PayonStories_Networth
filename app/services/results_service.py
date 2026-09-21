import time
import requests
from statistics import median


API_BASE = "https://tools.payonstories.com/api/pc/history"


def pricecheck(
    item_id: str,
    refine=0,
    c0=0,
    c1=0,
    c2=0,
    c3=0
):

    history = get_market_history(item_id)

    prices = filter_market_history(
        history,
        refine,
        c0,
        c1,
        c2,
        c3
    )

    return {
        "median": get_market_median(prices),
        "average": get_market_average(prices),
        "sales": len(prices)
    }


def get_market_history(item_id: str):

    start = time.perf_counter()

    response = requests.get(
        API_BASE,
        params={"id": item_id},
        timeout=30
    )

    print(
        f"History request [{item_id}]: "
        f"{time.perf_counter() - start:.3f}s"
    )

    if response.status_code == 400:

        data = response.json()

        if data.get("error") == "No data":
            return []

    response.raise_for_status()

    start = time.perf_counter()

    data = response.json()

    print(
        f"JSON parsing [{item_id}]: "
        f"{time.perf_counter() - start:.3f}s"
    )

    return data.get("sellHistory", [])


def filter_market_history(
    history,
    refine=0,
    c0=0,
    c1=0,
    c2=0,
    c3=0,
    sales_limit=10
):

    start = time.perf_counter()

    prices = []

    for entry in history:

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

                prices.append(float(price))

                if len(prices) >= sales_limit:

                    print(
                        f"History filtering: "
                        f"{time.perf_counter() - start:.3f}s"
                    )

                    return prices

    print(
        f"History filtering: "
        f"{time.perf_counter() - start:.3f}s"
    )

    return prices


def get_market_median(prices):

    if not prices:
        return None

    return round(median(prices))


def get_market_average(prices):

    if not prices:
        return None

    return round(sum(prices) / len(prices))


def get_market_min(prices):

    if not prices:
        return None

    return min(prices)


def get_market_max(prices):

    if not prices:
        return None

    return max(prices)