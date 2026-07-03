import requests
from bs4 import BeautifulSoup
import json
import time

CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"


def fetch_catalog_page():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        CATALOG_URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.text

if __name__ == "__main__":
    html = fetch_catalog_page()

    with  open("catalog.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("HTML saved successfully!")