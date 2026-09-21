import requests


url = "https://tools.payonstories.com/_next/static/chunks/pages/pc-2becb834b3c23471.js"

js = requests.get(url).text

term = "eu("

start = 0

while True:

    index = js.find(term, start)

    if index == -1:
        break

    print("\n" + "=" * 80)

    print(
        js[max(0, index - 1500):
           index + 2500]
    )

    start = index + len(term)