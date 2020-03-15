import requests
from bs4 import BeautifulSoup

URL = "https://www.health.ny.gov/diseases/communicable/coronavirus/"
URL = "http://web.archive.org/web/20200306211657/https://www.health.ny.gov/diseases/communicable/coronavirus/"

def get_table(soup: BeautifulSoup):
    table = soup.select("table#case_count_table")[0]
    caption = table.select("caption")[0].text

    th = table.select("th")[1:3]
    tr = table.select("tr")[1].select("td")[1:3]

    print(tr)

    results = [{ "key": str(k.text), "value": str(v.text) } for k, v in zip(th, tr)]

    return { "caption": caption, "data": results }

if __name__ == "__main__":
    res = requests.get(URL)
    soup = BeautifulSoup(res.text)
    print(get_table(soup))

