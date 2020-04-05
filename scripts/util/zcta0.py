from csv import DictReader, DictWriter
import re

def get_uhf_neiborhood_defs():
    with open("data/neighbor_name.csv") as fp:
        reader = DictReader(fp)
        return list(reader)

def get_nyc_zcta_defs():
    zcta_defs = []
    neighborhood_defs = get_uhf_neiborhood_defs()
    with open("data/nyc-zcta-defs.csv") as fp:
        reader = DictReader(fp)
        for row in reader:
            for zcta in re.split("\,\s*", row["ZCTA"]):
                zcta_defs.append({
                    "zip_code": zcta,
                    "uhf_code": next((ndef["Code"] for ndef in neighborhood_defs if ndef["Neighborhood"] == row["UHF Neighborhood"]), None),
                    "uhf_name": row["Name"],
                    "borough": row["Borough"],
                    "neighborhood_name": row["UHF Neighborhood"],
                })
    return zcta_defs

if __name__ == "__main__":
    zcta_defs = get_nyc_zcta_defs()
    zcta_defs = [zcta_def for _, zcta_def in sorted([
        (zcta_def["zip_code"], zcta_def) for zcta_def in zcta_defs
    ])]
    with open("data/nyc-zcta-defs-2.csv", "w") as fp:
        writer = DictWriter(fp, fieldnames=[
            "zip_code",
            "neighborhood_name",
            "uhf_code",
            "uhf_name",
            "borough"
        ])
        writer.writeheader()
        for zcta_def in zcta_defs:
            writer.writerow(zcta_def)