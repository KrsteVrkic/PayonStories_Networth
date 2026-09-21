import time
import asyncio
import requests

API_BASE = "https://tools.payonstories.com/api"


def search_item(name: str):

    total_start = time.perf_counter()
    request_start = time.perf_counter()

    response = requests.get(
        f"{API_BASE}/db/search",
        params={"q": name},
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    print("API STATUS:", response.status_code)
    print("API HEADERS:", dict(response.headers))

    if response.status_code == 403:
        print("API 403 BODY:", response.text[:1000])

    response.raise_for_status()
    
    print(
        f"search_item request [{name}]: " f"{time.perf_counter() - request_start:.3f}s"
    )
    
    json_start = time.perf_counter()

    data = response.json()

    print(f"search_item JSON [{name}]: " f"{time.perf_counter() - json_start:.3f}s")

    results = data["results"]

    filter_start = time.perf_counter()

    matching_results = [
        item
        for item in results
        if item["title"].lower() == name.lower() and item["type"] == "item"
    ]

    print(
        f"search_item filtering [{name}]: " f"{time.perf_counter() - filter_start:.3f}s"
    )

    print(f"search_item total [{name}]: " f"{time.perf_counter() - total_start:.3f}s")

    return matching_results


def get_item(item_id: str):

    total_start = time.perf_counter()

    request_start = time.perf_counter()

    response = requests.get(
        f"{API_BASE}/pc/item",
        params={"id": item_id},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )

    print(
        f"get_item request [{item_id}]: " f"{time.perf_counter() - request_start:.3f}s"
    )

    response.raise_for_status()

    json_start = time.perf_counter()

    data = response.json()

    print(f"get_item JSON [{item_id}]: " f"{time.perf_counter() - json_start:.3f}s")

    print(f"get_item total [{item_id}]: " f"{time.perf_counter() - total_start:.3f}s")

    return data


def process_item(name: str, quantity: int):

    total_start = time.perf_counter()

    search_start = time.perf_counter()

    search_results = search_item(name)

    print(
        f"process_item search [{name}]: " f"{time.perf_counter() - search_start:.3f}s"
    )

    if not search_results:

        print(
            f"process_item total [{name}]: " f"{time.perf_counter() - total_start:.3f}s"
        )

        return {"name": name, "quantity": quantity, "found": False}

    variants = []

    for result in search_results:

        item_id = result["id"]

        item_start = time.perf_counter()

        item_data = get_item(item_id)

        print(
            f"process_item get_item [{name}, {item_id}]: "
            f"{time.perf_counter() - item_start:.3f}s"
        )

        if item_data["refine"]:

            variants.append(item_data)

        else:

            print(
                f"process_item total [{name}]: "
                f"{time.perf_counter() - total_start:.3f}s"
            )

            return {
                "name": name,
                "quantity": quantity,
                "equipment": False,
                "item": item_data,
            }

    print(f"process_item total [{name}]: " f"{time.perf_counter() - total_start:.3f}s")

    return {"name": name, "quantity": quantity, "equipment": True, "variants": variants}


async def process_items(items):

    total_start = time.perf_counter()

    task_start = time.perf_counter()

    tasks = [
        asyncio.to_thread(process_item, item["name"], int(item["quantity"]))
        for item in items
    ]

    print(f"process_items task creation: " f"{time.perf_counter() - task_start:.3f}s")

    gather_start = time.perf_counter()

    results = await asyncio.gather(*tasks)

    print(f"process_items gather: " f"{time.perf_counter() - gather_start:.3f}s")

    print(f"process_items total: " f"{time.perf_counter() - total_start:.3f}s")

    return results
