import requests
import json
from bs4 import BeautifulSoup

URL = "https://coronavirus.health.ny.gov/county-county-breakdown-positive-cases"

def get_table(soup: BeautifulSoup):
    date_string = soup.select(".wysiwyg--field-webny-wysiwyg-title")[0].text
    table = soup.select(".wysiwyg--field-webny-wysiwyg-body > table")[0]
    cells = table.select("td")
    results = [{ "key": str(k.text), "value": str(v.text) } for k, v in zip(cells[0::2], cells[1::2])]

    return { "date_string": date_string, "data": results }

if __name__ == "__main__":
    res = requests.get(URL)
    soup = BeautifulSoup(res.text)

    with open("data/dataset.json") as fp:
        dataset = json.load(fp)

    raw_data = get_table(soup)

    if raw_data not in [data["raw_data"] for data in dataset]:
        dataset.append({
            "raw_data": raw_data,
            "raw_version": "5.0"
        })
    
    with open("data/dataset.json", "w") as fp:
        json.dump(dataset, fp, indent=2)


