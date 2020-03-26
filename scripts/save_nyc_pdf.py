import requests
from pathlib import Path
import hashlib
import arrow, datetime
import yaml
from util.extract_date import extract_date


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

def unparse_fname(tup):
    return f"{tup[0].strftime('%Y%m%d')}-{tup[1]}.pdf"

def write_meta(output_dir: str, info: dict):
    output_dir = Path(output_dir)
    with open(output_dir / "meta.yml") as fp:
        meta = yaml.load(fp, Loader=yaml.SafeLoader)
        print(meta)
    if meta["file_time"] is None: meta["file_time"] = {}
    meta["file_time"].update(info)
    with open(output_dir / "meta.yml", "w") as fp:
        yaml.dump(meta, fp, Dumper=yaml.SafeDumper)

def archive_url(output_dir: str, url: str):
    output_dir = Path(output_dir)
    lfnames = list(output_dir.glob("*.pdf"))
    stem = make_fname(lfnames)
    output_path = output_dir / f"{stem}.pdf"
    save_url(output_path, url)
    hashsum = hash_file(output_path)
    fnames_latest = sorted([parse_fname(fname) for fname in lfnames])[-5:]
    fnames_latest = [fname for fname in lfnames if parse_fname(fname) in fnames_latest]

    if hashsum in {hash_file(fname) for fname in fnames_latest}:
        output_path.unlink()
    else:
        try:
            date = extract_date(output_path)
            write_meta(output_dir, {f"{stem}.pdf": date})
        except Exception:
            write_meta(output_dir, {f"{stem}.pdf": ""})

if __name__ == "__main__":
    import sys
    #print(hash_file(sys.argv[1]))
    #print(parse_fname(sys.argv[1]))
    archive_url("documents/NYC-covid-19-daily-data-summary", "https://www1.nyc.gov/assets/doh/downloads/pdf/imm/covid-19-daily-data-summary.pdf")
    archive_url("documents/NYC-covid-19-daily-data-summary-deaths", "https://www1.nyc.gov/assets/doh/downloads/pdf/imm/covid-19-daily-data-summary-deaths.pdf")
    archive_url("documents/NYC-covid-19-daily-data-summary-hospitalizations", "https://www1.nyc.gov/assets/doh/downloads/pdf/imm/covid-19-daily-data-summary-hospitalizations.pdf")
