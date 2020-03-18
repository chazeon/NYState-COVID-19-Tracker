import json
import arrow
import numpy
import re
import locale
import datetime

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def calc_doubling_date(x_array, y_array):
    delta = numpy.log(2) / (numpy.log(y_array[-1]) - numpy.log(y_array[-3])) * (x_array[-1] - x_array[-3])
    return delta.days + delta.seconds / 86400

def calc_increase_rate(x_array, y_array):
    delta_x = x_array[-1] - x_array[-2]
    log_delta_y = numpy.log(y_array[-1]) - numpy.log(y_array[-2])
    rate = numpy.exp(log_delta_y * datetime.timedelta(days=1) / delta_x)
    return rate

import si_prefix

from matplotlib.ticker import LogFormatter

with open("data/dataset.json") as fp:
    dataset = json.load(fp)

#with open("data/dataset-nyc.json") as fp:
    #dataset2 = json.load(fp)

#dataset.extend(dataset2)

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

#print(number_by_area.keys())

from matplotlib import pyplot as plt


plt.figure()

for area_name in number_by_area.keys():

    #print(area_name)

    if area_name in {"New York State(Outside of NYC)", "New York City(NYC)", "New York State (Outside of NYC)", "Positive Cases"}:
        continue

    data = number_by_area[area_name]

    x_array = [item["date"] for item in data]
    y_array = [item["count"] for item in data]

    x_array, y_array = zip(*sorted(zip(x_array, y_array), key=lambda  item: (item[0], item[1])))

    if max(y_array) < 50: continue

    color = None 
    linewidth = 1.5
    if area_name == "Total Positive Cases (Statewide)":
        area_name = "NYState total"
        color = "#666666"
        linewidth = 2.5

    line, = plt.plot_date(x_array, y_array, marker="o", linestyle="-", label=area_name, linewidth=linewidth, color=color)

    for x, y in zip(x_array, y_array):
        if y < 10: continue
        plt.text(x, y*1.1, str(y), va="bottom", ha="center", size=6, c=line.get_color())

    # print(calc_doubling_date(x_array, y_array))
    plt.text(x_array[-1].shift(days=.5), y_array[-1], area_name, va="bottom", ha="left", size=6, c=line.get_color(), fontsize=8, fontweight="bold")
    plt.text(x_array[-1].shift(days=.5), y_array[-1] / 1.04, f"Double every {calc_doubling_date(x_array, y_array):.1f} days", va="top", ha="left", size=5, c="k")
    plt.text(x_array[-1].shift(days=.5), y_array[-1] / 1.18, f"Increase by {calc_increase_rate(x_array, y_array) * 100 - 100:.1f}% daily", va="top", ha="left", size=5, c="k")

for sname in ["top", "right"]:
    spine = plt.gca().spines[sname]
    spine.set_visible(False)

plt.semilogy()

plt.xlabel("Time")
plt.ylabel("Positive cases")

from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import LogLocator, NullLocator, LogFormatter

plt.gca().xaxis.set_major_locator(AutoDateLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter("%m/%d"))
#plt.gca().xaxis.set_minor_locator(AutoDateLocator())
plt.gca().yaxis.set_major_locator(LogLocator(subs=(1, 2, 5)))
plt.gca().yaxis.set_major_formatter(LogFormatter(labelOnlyBase=False, minor_thresholds=(numpy.inf, numpy.inf)))
plt.gca().yaxis.set_minor_locator(NullLocator())


#plt.title("New York State COVID-19 positive case count (county with > 100 cases)")

plt.xlim(left=arrow.get("2020-03-03"))
plt.xlim(right=1.05*(plt.xlim()[1] - plt.xlim()[0])+plt.xlim()[0])
plt.ylim(bottom=10)

# plt.legend()
plt.tight_layout()

plt.savefig("plots/NYState2.png", dpi=300)
