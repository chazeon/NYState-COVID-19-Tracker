import PyPDF2
import re
import arrow
from dateutil import tz
import csv
import yaml

from .extract_color_nyc import extract_pdf_data


nyc_boroughs = {
     1: "Bronx",
     2: "Brooklyn",
     3: "Manhattan",
     4: "Queens",
     5: "Staten Island"
}


def extract_text(fname):
    with open(fname, "rb") as fp:
        reader = PyPDF2.PdfFileReader(fp)
        page = reader.getPage(0)
        return page.extractText()

def extract_total_tests(text):
    for line in text.split("\n"):
        res = re.search("^N\s*=\s*(\d+)", line)
        if res:
            return int(res.group(1))

def extract_date(text):
    for line in text.split("\n"):
        res = re.search(r"as of ([A-Z][a-z]+ [123]?\d, 20\d+)", line)
        if res:
            return arrow.get(
                res.group(1),
                "MMMM D, YYYY",
                tzinfo=tz.gettz('US/Eastern')
            )

def extract_segmentation(text):
    def yield_segment():
        for line in text.split("\n"):
            all_res = list(re.finditer(r"(\d*\.?\d+)\%", line))
            for res1, res2 in zip(all_res[0::2], all_res[1::2]):
                yield (float(res1.group(1)), float(res2.group(1)))
            if len(all_res) > 1: break
    return list(yield_segment())


def get_neighbor_map():
    loc_map = {}
    with open("data/neighbor_name.csv") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            loc_map[int(row["Code"])] = row["Neighborhood"]
    return loc_map
    

def extract_data(fname):
    text = extract_text(fname)
    N = extract_total_tests(text)
    date = extract_date(text)
    segmentation = dict(enumerate(extract_segmentation(text)))
    neighbor_data = []
    neighbor_map = get_neighbor_map()
    #print(segmentation)
    for neighbor_code, severity in extract_pdf_data(fname):
        neighbor_data.append({
            "borough": nyc_boroughs[neighbor_code // 100],
            "neighbor_id": neighbor_code,
            "neighbor_name": neighbor_map[neighbor_code],
            "test_positive_rate_range": segmentation[severity - 1]
        })
    return {
        "time": date.datetime,
        "date": date.date(),
        "total_test": N,
        "neighbor_data": neighbor_data
    }

if __name__ == "__main__":
    import io
    sio = io.StringIO()
    yaml.dump(extract_data("20200329-1.pdf"), sio, Dumper=yaml.SafeDumper)
    print(sio.getvalue())