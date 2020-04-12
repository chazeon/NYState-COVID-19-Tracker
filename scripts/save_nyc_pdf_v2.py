import requests
from pathlib import Path
import hashlib
import arrow, datetime
import yaml
from bs4 import BeautifulSoup
import urllib.parse
import re


def hash_file(fname, hasher=hashlib.sha256, blocksize=65536):
    _hash = hasher()
    with open(fname, "rb") as fp:
        while True:
            chunk = fp.read(blocksize)
            if chunk == b"": break
            _hash.update(chunk)
    return _hash.hexdigest()


def save_url(output_path: Path, url: str):
    resp = requests.get(url, stream=False)
    if resp.status_code == 200:
        with open(output_path, "wb") as fp:
            for chunk in resp:
                fp.write(chunk)

def parse_datestr(datestr: str):
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

def make_fname(lfnames: list):
    lfnames = [
        fname
        for fname in lfnames
        if parse_fname(fname)[0].date() == datetime.datetime.now().date()
    ]
    fid = max(0, len(lfnames), *[parse_fname(fname)[1] for fname in lfnames]) + 1
    return f"{datetime.datetime.now().strftime('%Y%m%d')}-{fid}"

def unparse_fname(tup, ext="pdf"):
    return f"{tup[0].strftime('%Y%m%d')}-{tup[1]}.{ext}"

def write_meta(output_dir: str, info: dict):
    output_dir = Path(output_dir)
    with open(output_dir / "meta.yml") as fp:
        meta = yaml.load(fp, Loader=yaml.SafeLoader)
        print(meta)
    if meta["file_time"] is None: meta["file_time"] = {}
    meta["file_time"].update(info)
    with open(output_dir / "meta.yml", "w") as fp:
        yaml.dump(meta, fp, Dumper=yaml.SafeDumper)

def archive_url(output_dir: str, url: str, ext: str = "pdf"):
    output_dir = Path(output_dir)
    lfnames = list(output_dir.glob(f"*.{ext}"))
    stem = make_fname(lfnames)
    output_path = output_dir / f"{stem}.{ext}"
    save_url(output_path, url)
    hashsum = hash_file(output_path)
    fnames_latest = sorted([parse_fname(fname) for fname in lfnames])[-5:]
    fnames_latest = [fname for fname in lfnames if parse_fname(fname) in fnames_latest]

    if hashsum in {hash_file(fname) for fname in fnames_latest}:
        output_path.unlink()
    else:
        write_meta(output_dir, {f"{stem}.{ext}": ""})

def check_pdf_urls():
    URL = "https://www1.nyc.gov/site/doh/covid/covid-19-data.page"
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.content, features="lxml")
    for anchor in soup.findAll("a"):
        if "href" not in anchor.attrs.keys(): continue
        href = anchor.attrs["href"]
        if href.endswith(".pdf"):
            yield urllib.parse.urljoin(URL, href)

if __name__ == "__main__":
    # import sys
    # print(hash_file(sys.argv[1]))
    # print(parse_fname(sys.argv[1]))

    urls = list(check_pdf_urls())

    for url in urls:
        for key in {
            "covid-19-data-map",
            "covid-19-daily-data-summary",
            "covid-19-daily-data-summary-deaths",
            "covid-19-daily-data-summary-hospitalizations",
            "covid-19-deaths-race-ethnicity"
        }:
            if re.search("/" + key + r"-\d{8,8}-\d+.pdf", url):
                archive_url(f"documents/NYC-{key}", url)

    archive_url(f"documents/NYC-github-coronavirus-data-tests-by-zcta", "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/tests-by-zcta.csv", ext="csv")
    archive_url(f"documents/NJ-COVID_Confirmed_Case_Summary", "https://www.nj.gov/health/cd/documents/topics/NCOV/COVID_Confirmed_Case_Summary.pdf")
