from util import timeseries_rate

import csv, arrow
from matplotlib import pyplot as plt


with open("data/positive_cases.csv") as fp:
    reader = csv.DictReader(fp)
    for area_data in reader:
        if area_data["Location"] == "Total Positive Cases (Statewide)": continue
        location = area_data["Location"]
        area_data = dict(
            (arrow.get(time), int(count))
            for time, count in list(area_data.items())[1:]
            if count != ""
        )
        time_array = list(area_data.keys())[1:]
        count_array = list(area_data.values())[1:]
        if len(count_array) < 5: continue
        try:
            time_new, rate_new = timeseries_rate(time_array, count_array)
        except Exception:
            continue
        if max(rate_new) < 100: continue
        line, = plt.plot_date(
            time_new, rate_new,
            ls="-", marker=None, lw=1.5 if location != "New York City" else 2.5,
            label=location
        )


with open("data/positive_cases.csv") as fp:
    reader = csv.DictReader(fp)
    for area_data in reader:
        if area_data["Location"] != "Total Positive Cases (Statewide)": continue
        location = area_data["Location"]
        area_data = dict(
            (arrow.get(time), int(count))
            for time, count in list(area_data.items())[1:]
            if count != ""
        )
        time_array = list(area_data.keys())[1:]
        count_array = list(area_data.values())[1:]
        if len(count_array) < 5: continue
        try:
            time_new, rate_new = timeseries_rate(time_array, count_array)
        except Exception:
            continue
        line, = plt.plot_date(
            time_new, rate_new,
            ls="-", marker=None, lw=2.5,
            label=location,
            c="k"
        )

plt.ylim(bottom=1)

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


plt.title("New York State COVID-19 daily case increase (approx.)")

#plt.xlim(left=arrow.get("2020-03-01"))
#plt.ylim(bottom=10)

plt.legend()
plt.savefig("plots/rate_nys.png")