from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import InvalidInventoryCSV


async def invalid_inventory_csv_handler(
    request: Request,
    exc: InvalidInventoryCSV
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )
