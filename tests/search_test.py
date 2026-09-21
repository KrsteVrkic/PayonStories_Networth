import requests


URL = "http://127.0.0.1:8000/search"


tests = [
    {
        "name": "Valid CSV",
        "text": "name,quant\napple,20"
    },
    {
        "name": "Missing header",
        "text": "apple,20"
    },
    {
        "name": "Old format",
        "text": "apple 20"
    },
    {
        "name": "Invalid quantity",
        "text": "name,quant\napple,xyz"
    },
    {
        "name": "Zero quantity",
        "text": "name,quant\napple,0"
    },
    {
        "name": "Too many columns",
        "text": "name,quant\napple,20,foo"
    },
]


for test in tests:

    print()
    print("=" * 50)
    print(test["name"])
    print("=" * 50)

    response = requests.post(
        URL,
        json={
            "text": test["text"]
        }
    )

    print("Status:", response.status_code)
    print("Response:", response.json())