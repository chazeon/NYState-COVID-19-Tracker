import requests
import json
from bs4 import BeautifulSoup

URL = "https://www1.nyc.gov/site/doh/health/health-topics/coronavirus.page"

def get_table(soup: BeautifulSoup):
    para = soup.select("div.about-description > div:nth-child(3) > div > p:nth-child(14)")
    date_string = para[0].text
    #table = soup.select(".wysiwyg--field-webny-wysiwyg-body > table")[0]
    #cells = table.select("td")
    print(str(para[0]))
    count = str(para[0].select("strong")[0].text)
    results = [{ "key": "New York City", "value": count }]

    return { "date_string": date_string, "data": results }

if __name__ == "__main__":
    res = requests.get(URL)
    soup = BeautifulSoup(res.text)

    with open("data/dataset-nyc.json") as fp:
        dataset = json.load(fp)

    raw_data = get_table(soup)

    if raw_data not in [data["raw_data"] for data in dataset]:
        dataset.append({
            "raw_data": raw_data,
            "raw_source": URL,
            "raw_version": "5.0"
        })
    
    with open("data/dataset-nyc.json", "w") as fp:
        json.dump(dataset, fp, indent=2)


