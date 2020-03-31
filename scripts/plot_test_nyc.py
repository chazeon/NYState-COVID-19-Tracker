import yaml

from matplotlib import pyplot as plt


if __name__ == "__main__":

    with open("data/test_map.yml") as fp:
        test_map = yaml.safe_load(fp)

    t_array = [tm["date"] for tm in test_map]
    n_array = [tm["total_test"] for tm in test_map]

    plt.plot_date(t_array, n_array, ls="-", marker="o")

    plt.semilogy()
        
    plt.xlabel("Date")
    plt.ylabel("Total tested")

    from matplotlib.dates import AutoDateLocator, DateFormatter, DayLocator
    from matplotlib.ticker import LogLocator, NullLocator, LogFormatter
    from util import LogFormatterSI
    import numpy

    plt.gca().xaxis.set_major_locator(DayLocator())
    plt.gca().xaxis.set_major_formatter(DateFormatter("%m/%d"))
    plt.gca().xaxis.set_minor_locator(AutoDateLocator())

    plt.gca().yaxis.set_major_locator(LogLocator(subs=(1, 2, 5)))
    plt.gca().yaxis.set_major_formatter(LogFormatterSI(labelOnlyBase=False, minor_thresholds=(numpy.inf, numpy.inf)))
    plt.gca().yaxis.set_minor_locator(NullLocator())


    plt.title("New York City COVID-19 total tested")

    #plt.xlim(left=arrow.get("2020-03-01"))
    #plt.ylim(bottom=10)

    plt.legend()
    plt.savefig("plots/nyc_test.png")