import requests


url = "https://tools.payonstories.com/_next/static/chunks/pages/pc-2becb834b3c23471.js"

js = requests.get(url).text

for term in [
    "ec=",
    "setEc",
    "setEc(",
]:

    print("\n" + "=" * 80)
    print(term)
    print("=" * 80)

    start = 0

    while True:

        index = js.find(term, start)

        if index == -1:
            break

        print(
            js[max(0, index - 1000):
               index + 2000]
        )

        start = index + len(term)