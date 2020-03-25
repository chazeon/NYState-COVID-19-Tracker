from util import timeseries_rate

import csv, arrow
from matplotlib import pyplot as plt


with open("data/NYC-covid-19-daily-data-summary.csv") as fp:
    reader = csv.DictReader(fp)
    for area_data in reader:
        if area_data["Group"] != "Borough": continue
        if area_data["Subgroup"] == "Unknown": continue
        location = area_data["Subgroup"]
        area_data = dict(
            (arrow.get(time), int(count))
            for time, count in list(area_data.items())[2:]
            if count != ""
        )
        time_array = list(area_data.keys())
        count_array = list(area_data.values())
        time_new, rate_new = timeseries_rate(time_array, count_array)
        line, = plt.plot_date(
            time_new, rate_new,
            ls="-", marker=None, lw=1.5,
            label=location
        )


with open("data/NYC-covid-19-daily-data-summary.csv") as fp:
    reader = csv.DictReader(fp)
    for area_data in reader:
        if area_data["Group"] != "Total": continue
        area_data = dict(
            (arrow.get(time), int(count))
            for time, count in list(area_data.items())[2:]
            if count != ""
        )
        time_array = list(area_data.keys())
        count_array = list(area_data.values())
        time_new, rate_new = timeseries_rate(time_array, count_array)
        line, = plt.plot_date(
            time_new, rate_new,
            ls="-", marker=None, lw=2.5,
            label="NYC Total",
            c="k"
        )

plt.semilogy()
        
plt.xlabel("Time")
plt.ylabel("Case increase")

from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import LogLocator, NullLocator, LogFormatter
from util import LogFormatterSI
import numpy

plt.gca().xaxis.set_major_locator(AutoDateLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter("%m/%d"))
plt.gca().xaxis.set_minor_locator(AutoDateLocator())
plt.gca().yaxis.set_major_locator(LogLocator(subs=(1, 2, 5)))
plt.gca().yaxis.set_major_formatter(LogFormatterSI(labelOnlyBase=False, minor_thresholds=(numpy.inf, numpy.inf)))
plt.gca().yaxis.set_minor_locator(NullLocator())


plt.title("New York City COVID-19 daily case increase (approx.)")

#plt.xlim(left=arrow.get("2020-03-01"))
#plt.ylim(bottom=10)

plt.legend()
plt.savefig("plots/rate.png")