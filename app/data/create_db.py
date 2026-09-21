import json
import re


INPUT_FILE = "app/data/cards.txt"
OUTPUT_FILE = "app/data/cards.json"


def parse_cards(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    cards = {}

    for i in range(0, len(lines), 3):

        match = re.match(
            r"(.+?)\s+\(ID:\s*(\d+)\)$",
            lines[i]
        )

        if not match:
            continue

        name = match.group(1)
        card_id = match.group(2)

        prefix = lines[i + 1]
        suffix = lines[i + 2]

        if prefix == "—":
            prefix = None

        if suffix == "—":
            suffix = None

        cards[card_id] = {
            "name": name,
            "prefix": prefix,
            "suffix": suffix
        }

    return cards


with open(INPUT_FILE, encoding="utf-8") as file:
    text = file.read()

cards = parse_cards(text)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        cards,
        file,
        indent=4,
        ensure_ascii=False
    )

print(f"Created {len(cards)} cards")