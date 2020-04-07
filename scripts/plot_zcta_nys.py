import numpy
from matplotlib import pyplot as plt
import csv
from collections import OrderedDict
import arrow
from datetime import timedelta
from matplotlib import lines
import matplotlib.patheffects as PathEffects


if __name__ == "__main__":

    with open("data/NYS-county-testing-records.csv") as fp:
        reader = csv.DictReader(fp)
        records = list(reader)
    
    counties = set(r["County"] for r in records)
    data_by_county = OrderedDict((c, [
        r for r in records
        if r["County"] == c
    ]) for c in counties)

    for idx, (county_name, county_data) in enumerate(data_by_county.items()):
        if county_name == "Total": continue
        x_array = list(reversed([int(d["Daily Tested"] if d['Daily Tested'] != '' else 0) for d in county_data]))
        y_array = list(reversed([int(d["Daily Positive"] if d['Daily Positive'] != '' else 0) for d in county_data]))
        d_array = list(reversed([arrow.get(d["Test Date"], "MM/DD/YYYY").date() for d in county_data]))

        d_diff = numpy.diff(d_array) / timedelta(days=1) 
        x_array = x_array[1:] / d_diff
        y_array = y_array[1:] / d_diff

        if max(x_array) < 20: continue

        line, = plt.plot(x_array[-7:], y_array[-7:], marker="o", alpha=.6, ls="dashed", markersize=1, lw=.75)
        # plt.plot(x_array[-5:], y_array[-5:], marker="o", alpha=.4, ls="", markersize=1, lw=.75, color=line.get_color())
        plt.plot(x_array[-1], y_array[-1], marker="o", c=line.get_color(), markersize=6, mec="white", zorder=10)

        print(y_array, x_array)

        if x_array[-1] < 10 or y_array[-1] < 5: continue

        if idx % 2 == 1:
            text = plt.text(
                x_array[-1] / 1.15, y_array[-1],
                "     " + county_name + f" ({int(y_array[-1])}/{int(x_array[-1])})",
                # color=colors[uhf_data["borough"]],
                color=line.get_color(),
                va="center", ha="right",
                size=6, alpha=.9,
                rotation=-0,
                zorder=15
            )
        else:
            text = plt.text(
                x_array[-1] * 1.15, y_array[-1],
                county_name + f" ({int(y_array[-1])}/{int(x_array[-1])})" + "     ",
                # color=colors[uhf_data["borough"]],
                color=line.get_color(),
                va="center", ha="left",
                size=6, alpha=.9,
                weight="bold",
                rotation=-0,
                zorder=15
            )
        text.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w', alpha=.5)])

    

    plt.loglog()

    plt.xlabel("Daily tested for COVID-19")
    plt.ylabel("Daily positive for COVID-19")

    # plt.legend([
    #     lines.Line2D([], [], c=color, marker="o")
    #     for color in colors.values()
    # ], boroughs)
    plt.gca().set_aspect("equal")
    plt.xlim(left=10)
    plt.ylim(bottom=5, top=2500)
    for percent in numpy.arange(0, 0.7, .25):
        plt.plot(plt.xlim(), numpy.array(plt.xlim()) * percent, c="grey", lw=.5, ls="dotted")
        plt.text(plt.xlim()[1], plt.xlim()[1]*percent, f"  {percent*100:.0f}%", ha="left", va="bottom", c="k", rotation=45)
        
    for percent in numpy.arange(.75, 1.1, .25):
        plt.plot(plt.xlim(), numpy.array(plt.xlim()) * percent, c="grey", lw=.5, ls="dotted")
        plt.text(plt.ylim()[1]/percent, plt.ylim()[1], f"  {percent*100:.0f}%", ha="left", va="bottom", c="k", rotation=45)

    plt.text(plt.xlim()[0] * 1.1, 15, "daily positive rate $\\uparrow$", rotation=45, size=8)

    from matplotlib.ticker import LogLocator
    from util import LogFormatterSI

    plt.gca().xaxis.set_major_locator(LogLocator(subs=(1, 2, 5)))
    plt.gca().xaxis.set_major_formatter(LogFormatterSI(labelOnlyBase=False, minor_thresholds=(numpy.inf, numpy.inf)))
    plt.gca().yaxis.set_major_locator(LogLocator(subs=(1, 2, 5)))
    plt.gca().yaxis.set_major_formatter(LogFormatterSI(labelOnlyBase=False, minor_thresholds=(numpy.inf, numpy.inf)))

    plt.savefig("plots/NYS-county-positive.png")


    #for neighboor, data in data_by_zcta.items():
        
        #plot(, c=[])