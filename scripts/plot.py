import json
import arrow
import numpy
import re
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

from matplotlib.ticker import LogFormatter

with open("data/dataset.json") as fp:
    dataset = json.load(fp)

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

from matplotlib import pyplot as plt

plt.figure()

for area_name in ["New York City", "Total Positive Cases (Statewide)"]:

    data = number_by_area[area_name]

    x_array = [item["date"] for item in data]
    y_array = [item["count"] for item in data]

    x_array, y_array = zip(*sorted(zip(x_array, y_array), key=lambda  item: (item[0], item[1])))

    #print(x_array)

    plt.plot_date(x_array, y_array, marker="o", linestyle="-", label=area_name)

    for x, y in zip(x_array, y_array):

        plt.text(x, y * 1.2, str(y), va="center", ha="center", size=6)

plt.semilogy()

plt.xlabel("Time")
plt.ylabel("Positive case")

from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import LogLocator, NullLocator, LogFormatter

plt.gca().xaxis.set_major_locator(AutoDateLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter("%m/%d"))
#plt.gca().xaxis.set_minor_locator(AutoDateLocator())
plt.gca().yaxis.set_major_locator(LogLocator(subs=(1, 2, 5)))
plt.gca().yaxis.set_major_formatter(LogFormatter(labelOnlyBase=False, minor_thresholds=(numpy.inf, numpy.inf)))
plt.gca().yaxis.set_minor_locator(NullLocator())


plt.title("New York State COVID-19 positive case count")

plt.xlim(left=arrow.get("2020-03-01"))
plt.ylim(bottom=1)

plt.legend()

plt.savefig("plots/NYState.png", dpi=300)