import asyncio

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.inventory_service import parse_inventory_csv
from app.services.item_service import process_items
from app.services.results_service import pricecheck
from app.services.card_service import get_all_cards


router = APIRouter()


class InventoryRequest(BaseModel):
    text: str


@router.post("/search")
async def search(data: InventoryRequest):

    items = parse_inventory_csv(data.text)

    return await process_items(items)


@router.get("/cards")
def cards():

    return get_all_cards()


@router.post("/pc")
async def pricecheck_items(items: list[dict]):

    tasks = [
        asyncio.to_thread(
            pricecheck,
            item["id"],
            item.get("refine", 0),
            item.get("c0", 0),
            item.get("c1", 0),
            item.get("c2", 0),
            item.get("c3", 0)
        )
        for item in items
    ]

    market_data = await asyncio.gather(*tasks)

    results = []

    for item, data in zip(items, market_data):

        results.append({
            "id": item["id"],
            "name": item.get("name"),
            "quantity": int(item["quantity"]),
            "average": data["average"]
        })

    return results