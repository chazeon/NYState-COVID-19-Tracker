import camelot
import PyPDF2
import arrow
import re
import locale
import dateutil
import csv
import yaml
from pathlib import Path
from collections import OrderedDict

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def extract_table(fname, *args, **argv):
    table = camelot.read_pdf(fname, *args, **argv)
    return table[table.n - 1].data

def process_table(fname, altkey: dict = None, *args, **argv):
    if altkey == None: altkey = {}
    def yield_row():
        group = None
        subgroup = None
        for row in extract_table(fname, *args, **argv):
            #if len(row) != 2: continue
            key = row[0]
            val = row[-1]
            if key in altkey.keys(): key = altkey[key]
            if re.search(r"^\-\s+", key):
                subgroup = re.sub(r"^\-\s+", "", key)
            else:
                group = key
                subgroup = None
            res = re.search("^(\d+)\s*(\(\d+%\))?$", val)
            if res:
                yield (group, subgroup), locale.atoi(res.group(1))
    return list(yield_row())

def dump_csv(dir_from, csv_to):
    dir_from = Path(dir_from)

    with open(dir_from / "meta.yml") as fp:
        flist = yaml.load(fp, yaml.SafeLoader)

    res = {}
    for fname, ftime in flist["file_time"].items():
        res[ftime] = dict(process_table(str(dir_from / fname), altkey=flist["altkeys"], flavor=flist["flavor"]))

    
    res_by_group = OrderedDict.fromkeys(key for value in res.values() for key, count in value.items())
    for key in res_by_group.keys():
        res_by_group[key] = dict(
            (time, res[time][key])
            for time in res.keys()
            if key in res[time].keys()
        )
    
    with open(csv_to, "w") as fp:
        writer = csv.DictWriter(fp, fieldnames=["Group", "Subgroup", *flist["file_time"].values()])
        writer.writeheader()
        #for item in res_by_group.items():
            #print(item)
        for (group, subgroup), values in res_by_group.items():
            row = dict([
                ("Group", group),
                ("Subgroup", subgroup),
                *values.items()
            ])
            writer.writerow(row)


if __name__ == "__main__":
    import sys
    dump_csv(sys.argv[1], sys.argv[2])
