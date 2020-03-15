import requests
import json
from bs4 import BeautifulSoup

URL = "https://www.health.ny.gov/diseases/communicable/coronavirus/"

def get_table(soup: BeautifulSoup):
    date_string = soup.select(".top_box > .left_side > p > strong")[0].text
    table = soup.select("table#case_count_table")[0]
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
            "raw_version": "4.0"
        })
    
    with open("data/dataset.json", "w") as fp:
        json.dump(dataset, fp, indent=2)


