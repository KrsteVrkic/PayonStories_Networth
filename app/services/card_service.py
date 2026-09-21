import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "cards.json"
)


with open(DATA_FILE, encoding="utf-8") as file:
    CARDS = json.load(file)


def get_card(card_id: int):

    return CARDS.get(str(card_id))


def get_all_cards():

    return CARDS