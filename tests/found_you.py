import requests

url = "https://tools.payonstories.com/api/pc/vend_details"

response = requests.get(
    url,
    params={
        "id": 2104,
        "r": 1,
        "c0": 0,
        "c1": 0,
        "c2": 0,
        "c3": 0,
    }
)

print(response.status_code)
print(response.text)