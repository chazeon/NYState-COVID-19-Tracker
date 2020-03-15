import requests
from bs4 import BeautifulSoup

URL = "https://www.health.ny.gov/diseases/communicable/coronavirus/"

def get_table(soup: BeautifulSoup):
    table = soup.select("table#case_count_table")[0]
    caption = table.select("caption")[0].text
    cells = table.select("td")
    results = [{ "key": str(k.text), "value": str(v.text) } for k, v in zip(cells[0::2], cells[1::2])]

    return { "caption": caption, "data": results }

if __name__ == "__main__":
    res = requests.get(URL)
    soup = BeautifulSoup(res.text)
    get_table(soup)

