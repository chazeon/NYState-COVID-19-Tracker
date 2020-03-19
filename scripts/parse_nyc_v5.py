import json
import arrow
from dateutil import tz
import re

URL = "https://www1.nyc.gov/site/doh/health/health-topics/coronavirus.page"

with open("data/dataset-nyc.json") as fp:
    dataset = json.load(fp)

for item in dataset:

    if item["raw_version"] != "5.0": continue
    if "raw_source" not in item.keys() or item["raw_source"] != URL: continue

    part = re.search(r"\(as of (.*)\)", item["raw_data"]["date_string"]).group(1)
    part = part.replace("a.m.", "am")
    part = part.replace("p.m.", "pm")

    try:
        date = arrow.get(part, "MMMM D [at] h:mm a", tzinfo=tz.gettz('US/Eastern')).replace(year=2020)
    except arrow.parser.ParserMatchError:
        date = arrow.get(part, "MMMM D [at] h a", tzinfo=tz.gettz('US/Eastern')).replace(year=2020)

    item["timestr"] = str(date)
    item["timestamp"] = date.timestamp

with open("data/dataset-nyc.json", "w") as fp:
    json.dump(dataset, fp, indent=2)