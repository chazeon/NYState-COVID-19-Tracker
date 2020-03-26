import scipy.interpolate
import scipy.stats
import numpy
import datetime

def calc_rate(x_array, y_array,  window=4, num=100, Interpolator=scipy.interpolate.InterpolatedUnivariateSpline):

    lny_array = numpy.log(y_array)
    length = len(x_array)

    def yield_rate_reg():
        for i, j in zip(range(0, length - window), range(window, length)):
            dlny_dx, _, _, _, _ = scipy.stats.linregress(x_array[i:j], lny_array[i:j])
            x_avg = numpy.average(x_array[i:j])
            y_avg = numpy.average(y_array[i:j])
            yield x_avg, dlny_dx * y_avg

    x_rough, dy_dx_rough = zip(*list(yield_rate_reg()))
    x_new = numpy.linspace(min(x_rough), max(x_rough), num=num)

    #print(numpy.array(dy_dx_rough) * (3600 * 24))

    return x_new, Interpolator(x_rough, dy_dx_rough)(x_new) 

def calc_timeseries_rate(t_array, y_array):
    x_array = [t.timestamp for t in t_array]
    x_new, dy_dx_new = calc_rate(x_array, y_array)
    t_new = [datetime.datetime.fromtimestamp(x) for x in x_new]
    dy_dt_new = dy_dx_new * (3600 * 24)
    return t_new, dy_dt_new
