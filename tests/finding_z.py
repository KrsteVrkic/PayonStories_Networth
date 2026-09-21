import requests
import re


BASE_URL = "https://tools.payonstories.com"

page = requests.get(
    f"{BASE_URL}/pc?name=2104"
).text

scripts = re.findall(
    r'<script[^>]+src="([^"]+)"',
    page
)

for script in scripts:

    js = requests.get(BASE_URL + script).text

    if "onModalCallback" not in js:
        continue

    print("\n" + "=" * 80)
    print(script)
    print("=" * 80)

    start = 0

    while True:

        index = js.find("onModalCallback", start)

        if index == -1:
            break

        print(
            js[max(0, index - 1500):
               index + 3000]
        )

        start = index + len("onModalCallback")