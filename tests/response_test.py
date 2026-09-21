import time
import requests

ITEM_ID = 2103

for i in range(5):

    start = time.perf_counter()

    response = requests.get(
        "https://tools.payonstories.com/api/pc/item",
        params={"id": ITEM_ID},
        timeout=30
    )

    elapsed = time.perf_counter() - start

    print(
        f"Request {i + 1}: "
        f"{elapsed:.3f}s | "
        f"status={response.status_code} | "
        f"bytes={len(response.content)}"
    )