import requests
import lxml
from bs4 import BeautifulSoup


def get_link_data(url):
    headers = {
        "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Accept-Language": "en-GB, en-US;q=0.9,en;q=0.8",
    }
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    # print(soup.prettify())

    name = soup.select_one(selector="#productTitle").getText()
    name = name.strip()

    price = soup.select_one(selector=".a-offscreen").getText()
    price = price[1:]

    return name, price
