import csv

def get_zcta_defs():
    def get_defs():
        with open("data/nyc-zcta-defs-2.csv") as fp:
            for row in csv.DictReader(fp):
                yield row["zip_code"], row
    return dict(get_defs())
            

    