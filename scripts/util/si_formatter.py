import si_prefix
from matplotlib.ticker import LogFormatter

class LogFormatterSI(LogFormatter):
    def _num_to_string(self, x, vmin, vmax):
        return si_prefix.si_format(x, precision=0, format_str='{value}{prefix}')