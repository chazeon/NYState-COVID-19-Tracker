import json
import arrow
import numpy
import re
import locale
import datetime
import itertools

import csv

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def calc_doubling_date(x_array, y_array):
    delta = numpy.log(2) / (numpy.log(y_array[-1]) - numpy.log(y_array[-2])) * (x_array[-1] - x_array[-2])
    return delta.days + delta.seconds / 86400

def calc_increase_rate(x_array, y_array):
    delta_x = x_array[-1] - x_array[-2]
    log_delta_y = numpy.log(y_array[-1]) - numpy.log(y_array[-2])
    rate = numpy.exp(log_delta_y * datetime.timedelta(days=1) / delta_x)
    return rate

def remove_duplicate(x_array, y_array):

    first, curr = itertools.tee(enumerate(zip(x_array, y_array)))


    def yield_xy():
        j, (_x, _y) = next(first)
        yield (_x, _y)

        for i, (x, y) in curr:
            if _y != y: 
                for j, (_x, _y) in first:
                    if j == i: break
                yield (_x, _y)
    
    x_array, y_array = zip(*list(yield_xy()))

    return x_array, y_array

with open("data/dataset.json") as fp:
    dataset = json.load(fp)

with open("data/dataset-nyc.json") as fp:
    dataset2 = json.load(fp)

dataset.extend(dataset2)

number_by_area = {}

for item in dataset:

    date = arrow.get(item["timestr"])

    for area in item["raw_data"]["data"]:

        area_name = area["key"]
        area_name = re.sub("\s*:\s*$", "", area_name)
        area_name = re.sub("\s+County\s*$", "", area_name)
        area_name = area_name.strip()
        area_count = locale.atoi(area["value"])

        if area_name not in number_by_area.keys():
            number_by_area[area_name] = []

        date_data = {
            "date": date,
            "count": area_count
        }

        if int(item["raw_version"].split(".")[0]) < 3:

            if area_name == "New York City(NYC)":
                area_name = "New York City"

            if area_name == "New York State(Outside of NYC)":
                area_name = "New York State (Outside of NYC)"

            if date_data not in number_by_area[area_name]:
                number_by_area[area_name].append(date_data)

        if int(item["raw_version"].split(".")[0]) >= 3:

            if area_name == "Total Number of Positive Cases":
                area_name = "Total Positive Cases (Statewide)"

            if date_data not in number_by_area[area_name]:
                number_by_area[area_name].append(date_data)
    
    if int(item["raw_version"].split(".")[0]) < 3:
        area_name = "Total Positive Cases (Statewide)"
        if area_name not in number_by_area.keys():
            number_by_area[area_name] = []
        number_by_area[area_name].append({
            "date": date,
            "count": number_by_area["New York City"][-1]["count"] + number_by_area["New York State (Outside of NYC)"][-1]["count"]
        })
    
for area_name in list(number_by_area.keys()):
    if len(number_by_area[area_name]) == 0:
        del number_by_area[area_name]

#print(number_by_area.keys())
from collections import OrderedDict

output_number_by_area = OrderedDict()

for area_name in number_by_area.keys():

    #print(area_name)

    if area_name in {"New York State(Outside of NYC)", "New York City(NYC)", "New York State (Outside of NYC)", "Positive Cases"}:
        continue

    data = number_by_area[area_name]

    x_array = [item["date"] for item in data]
    y_array = [item["count"] for item in data]

    x_array, y_array = remove_duplicate(x_array, y_array)
    #x_array, y_array = zip(*sorted(zip(x_array, y_array), key=lambda  item: item[0]))

    output_number_by_area[area_name] = dict((str(x), y) for x, y in zip(x_array, y_array))

with open("data/positive_cases.csv", "w") as fp:
    fieldnames = ["Location"] + [
        str(time)
        for time in sorted(
            set(time for value in output_number_by_area.values() for time in value.keys()),
            key=lambda timestr: arrow.get(timestr)
        )]
    writer = csv.DictWriter(fp, fieldnames=fieldnames)
    writer.writeheader()
    for area_name, result in output_number_by_area.items():
        writer.writerow(dict([("Location", area_name)] + list(result.items())))
