import json
import arrow
from dateutil import tz

with open("data/dataset.json") as fp:
    dataset = json.load(fp)

for item in dataset:
    if item["raw_version"] != "5.0": continue

    try:
        date = arrow.get(item["raw_data"]["date_string"], "[Last Update:] MMMM D, YYYY | h:mm A", tzinfo=tz.gettz('US/Eastern'))
    except arrow.parser.ParserMatchError:
        date = arrow.get(item["raw_data"]["date_string"], "[Last Update:] MMMM D, YYYY | h:mmA", tzinfo=tz.gettz('US/Eastern'))

    item["timestr"] = str(date)
    item["timestamp"] = date.timestamp

    print(item)

with open("data/dataset.json", "w") as fp:
    json.dump(dataset, fp, indent=2)