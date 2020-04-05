import arrow
from pathlib import Path
import yaml
import datetime
import csv
from util.zcta import get_zcta_defs
from collections import OrderedDict

def parse_datestr(datestr: str) -> datetime.datetime:
    return arrow.get(datestr, "YYYYMMDD").datetime

def parse_fname(fname: Path):
    if isinstance(fname, str): fname = Path(fname)
    stem = fname.stem
    parts = stem.split("-")
    if len(parts) == 1:
        return (parse_datestr(parts[0]), 0)
    if len(parts) == 2:
        return (parse_datestr(parts[0]), int(parts[1]))
    raise RuntimeError()

def process_file_time(dir_from: Path):

    with open(dir_from / "meta.yml") as fp:
        flist = yaml.load(fp, yaml.SafeLoader)

    file_time = flist["file_time"]

    for fname in file_time.keys():
        if file_time[fname] == '':
            time, _ = parse_fname(dir_from / fname)
            file_time[fname] = time.date()

    with open(dir_from / "meta.yml", "w") as fp:
        yaml.dump(flist, fp, yaml.SafeDumper)

    return flist


def dump_csv(dir_from, csv_to):

    dir_from = Path(dir_from)

    flist = process_file_time(dir_from)

    res = OrderedDict()

    zcta_defs = get_zcta_defs()

    for fname, fdate in flist["file_time"].items():
        with open(dir_from / fname) as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                for zcta, stat in {
                    (row["MODZCTA"], "Positive"),
                    (row["MODZCTA"], "Total")
                }:
                    if (zcta, stat) not in res.keys():
                        res[(zcta, stat)] = { "status": stat, "zip_code": zcta }
                    if zcta in zcta_defs.keys():
                        res[(zcta, stat)].update(zcta_defs[zcta])
                    res[(zcta, stat)].update({
                        str(fdate): row[stat]
                    })

    with open("data/NYC-github-coronavirus-data-tests-by-zcta.csv", "w") as fp:
        writer = csv.DictWriter(fp, fieldnames=[
            "zip_code",
            "uhf_code",
            "neighborhood_name",
            "uhf_name",
            "borough",
            "status"
        ] + [
            str(date) for date in sorted(list(flist["file_time"].values()))
        ])
        writer.writeheader()
        for row in res.values():
            writer.writerow(row)


if __name__ == "__main__":

    dump_csv("documents/NYC-github-coronavirus-data-tests-by-zcta", None)