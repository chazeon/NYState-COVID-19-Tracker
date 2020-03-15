import json
import arrow
from dateutil import tz

with open("data/dataset.json") as fp:
    dataset = json.load(fp)

for item in dataset:
    if item["raw_version"] != "2.0": continue
    try:
        date = arrow.get(item["raw_data"]["caption"], "[Data last updated] h:mma MMMM D, YYYY", tzinfo=tz.gettz('US/Eastern'))
    except arrow.parser.ParserMatchError:
        try: 
            date = arrow.get(item["raw_data"]["caption"], "[Data last updated] ha MMMM D, YYYY", tzinfo=tz.gettz('US/Eastern'))
        except:
            continue

    item["timestr"] = str(date)
    item["timestamp"] = date.timestamp

    print(item)

with open("data/dataset.json", "w") as fp:
    json.dump(dataset, fp, indent=2)