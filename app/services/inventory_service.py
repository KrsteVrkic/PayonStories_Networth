import time
import csv

from io import StringIO

from app.exceptions.exceptions import InvalidInventoryCSV


def parse_inventory_csv(text: str):

    total_start = time.perf_counter()

    reader_start = time.perf_counter()

    reader = csv.reader(StringIO(text))

    print(
        f"CSV reader creation: "
        f"{time.perf_counter() - reader_start:.6f}s"
    )

    try:
        header_start = time.perf_counter()

        header = next(reader)

        print(
            f"Header read: "
            f"{time.perf_counter() - header_start:.6f}s"
        )

    except StopIteration:
        raise InvalidInventoryCSV("CSV is empty")

    validation_start = time.perf_counter()

    header = [field.strip() for field in header]

    if header != ["name", "quant"]:
        raise InvalidInventoryCSV(
            "Invalid CSV format. Expected: name,quant"
        )

    print(
        f"Header validation: "
        f"{time.perf_counter() - validation_start:.6f}s"
    )

    items = []

    rows_start = time.perf_counter()

    for line_number, row in enumerate(reader, start=2):

        if len(row) != 2:
            raise InvalidInventoryCSV(
                f"Invalid CSV format on line {line_number}. "
                "Expected: name,quant"
            )

        name = row[0].strip()
        quantity = row[1].strip()

        if not name:
            raise InvalidInventoryCSV(
                f"Missing item name on line {line_number}"
            )

        if not quantity.isdigit():
            raise InvalidInventoryCSV(
                f"Invalid quantity on line {line_number}: {quantity}"
            )

        quantity = int(quantity)

        if quantity <= 0:
            raise InvalidInventoryCSV(
                f"Quantity must be greater than 0 on line {line_number}"
            )

        items.append({
            "name": name,
            "quantity": quantity
        })

    print(
        f"CSV row processing: "
        f"{time.perf_counter() - rows_start:.6f}s"
    )

    print(
        f"Total CSV parsing: "
        f"{time.perf_counter() - total_start:.6f}s"
    )

    return items