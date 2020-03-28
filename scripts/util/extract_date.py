import datetime
import arrow
from dateutil import tz

def extract_date(fname) -> datetime.datetime:
    import PyPDF2, re
    with open(fname, "rb") as fp:
        reader = PyPDF2.PdfFileReader(fp)
        page = reader.getPage(0)
        text = page.extractText()
    text = "".join(text.split("\n"))
    res = re.search(r"([A-Z]\S+ \d{1,2}, 20\d{2,2})\D+(\d+:\d+ (am|pm|AM|PM|a.m.|p.m.|A.M.|P.M.)?)", text)
    date = res.group(1)
    time = res.group(2)
    time.replace("a.m.", "am").replace("A.M.", "am").replace("p.m.", "pm").replace("P.M.", "pm")
    return arrow.get(
        f"{date} {time}",
        [
            "MMMM D, YYYY H:m a",
            "MMMM D, YYYY H:ma",
            "MMMM D, YYYY H a",
            "MMMM D, YYYY Ha",
        ],
        tzinfo=tz.gettz('US/Eastern')
    ).datetime

if __name__ == "__main__":
    import sys
    print(extract_date(sys.argv[1]))
