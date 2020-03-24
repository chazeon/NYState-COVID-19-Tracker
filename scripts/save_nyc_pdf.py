import requests
from pathlib import Path

def archive_url(output_path: Path, url: str):
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        with open(output_path, "wb") as fp:
            for chunk in resp:
                fp.write(chunk)


from peewee import Model, SqliteDatabase

db = SqliteDatabase("archive_records.db")

class BaseModel(Model):
    class Meta:
        database = db

