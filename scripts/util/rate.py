import scipy.interpolate
import numpy
import datetime

def calc_rate(x_array, y_array, x_new, Interpolator=scipy.interpolate.UnivariateSpline):
    lny_array = numpy.log(y_array)
    lny_x = Interpolator(x_array, lny_array)
    lny_new = lny_x(x_new)
    if Interpolator == scipy.interpolate.KroghInterpolator:
        dlny_dx_new = lny_x.derivative(x_new)
    else:
        dlny_dx_new = lny_x.derivative()(x_new)
    return numpy.exp(lny_new) * dlny_dx_new

def calc_timeseries_rate(t_array, y_array, num=100, Interpolator=scipy.interpolate.UnivariateSpline):
    x_array = [t.timestamp for t in t_array]
    x_min = numpy.min(x_array)
    x_max = numpy.max(x_array)
    x_new = numpy.linspace(x_min, x_max, num)
    t_new = [datetime.datetime.fromtimestamp(x) for x in x_new]
    dy_dt_new = calc_rate(x_array, y_array, x_new, Interpolator=Interpolator) * (3600 * 24)
    return t_new, dy_dt_new
