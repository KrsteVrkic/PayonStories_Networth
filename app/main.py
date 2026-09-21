from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.controllers.item_controller import router
from app.exceptions.exceptions import InvalidInventoryCSV
from app.exceptions.exception_handler import invalid_inventory_csv_handler


templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_exception_handler(
    InvalidInventoryCSV,
    invalid_inventory_csv_handler
)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

