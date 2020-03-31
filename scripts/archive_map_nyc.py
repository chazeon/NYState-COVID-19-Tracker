import requests
from update_v3 import get_table
from bs4 import BeautifulSoup
import pathlib
import json

URL="https://www.health.ny.gov/diseases/communicable/coronavirus/"
CAL_URL="http://web.archive.org/__wb/calendarcaptures/2"
ARCH_URL="http://web.archive.org/web"
year = 2020

res = requests.get(CAL_URL, params={
    "url": URL,
    "date": year
})

with open("data/dataset.json") as fp:
    dataset = json.load(fp)

for date, code, num in res.json()["items"]:

    time = f"{year:4d}{date:010d}"

    if int(time) <= 20200309021350: continue

    url = f"{ARCH_URL}/{time}/{URL}"

    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    try:
        raw_data = get_table(soup)

        print(raw_data)
        
        data = {"raw_data": raw_data, "raw_version": "3.0"}

        if data not in dataset:

            dataset.append(data)

        with open("data/dataset.json", "w") as fp:
            json.dump(dataset, fp, indent=2)

    except BaseException:
        #print(res.text)
        pass
        
print(dataset)

#with open("dataset.json", "w") as fp:
    #json.dump(dataset, fp, indent=2)