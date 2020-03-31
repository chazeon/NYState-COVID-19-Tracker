from util import extract_map_data
import yaml, json
from pathlib import Path
import csv


def get_map_dataset(dir_from):
    map_dataset = []
    dir_from = Path(dir_from)
    with open(dir_from / "meta.yml") as fp:
        meta = yaml.safe_load(fp)
    for fname in meta["file_time"].keys():
        map_dataset.append(extract_map_data(dir_from / fname))
    return map_dataset

if __name__ == "__main__":

    dataset = get_map_dataset("documents/NYC-covid-19-data-map")
    yaml.SafeDumper.ignore_aliases = lambda *args : True
    with open("data/test_map.yml", "w") as fp:
        yaml.safe_dump(dataset, fp)
    with open("data/test_map.csv", "w") as fp:
        writer = csv.DictWriter(fp, ["Neighborhood ID", "Neighborhood Name", "Borough", "Date", "Test Positive Percentage Min", "Test Positive Percentage Max"])
        writer.writeheader()
        for map_data in dataset:
            for row in map_data["neighbor_data"]:
                writer.writerow({
                    "Neighborhood ID": row["neighbor_id"],
                    "Neighborhood Name": row["neighbor_name"],
                    "Borough": row["borough"],
                    "Date": str(map_data["date"]),
                    "Test Positive Percentage Min": row["test_positive_rate_range"][0],
                    "Test Positive Percentage Max": row["test_positive_rate_range"][1]
                })
                
