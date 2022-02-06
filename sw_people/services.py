from datetime import datetime

import petl
import requests

from django.conf import settings


from sw_people.models import DownloadedFile
from sw_people.utils import resolve_name


def fetch_all_files():
    return DownloadedFile.objects.all()


def fetch_latest_characters():
    """Fetch all data from SWAPI /people endpoint.
    Follow the `next` in the result to get all pages while stacking them in petl table
    Clean all data by resolving the homeworld name and dropping unneeded fields
    Add a `date` field which is a reformatted `edited` date
    Dump everything in a csv file in the DATA_DIR and create a row with metadata(filename and timestamp) in db
    """
    # TODO: maybe move as a distributed task with some controls to not call multiple times in short time

    rq = requests.get(settings.SW_API_URL)
    json_payload = rq.json()
    data = petl.fromdicts(json_payload["results"])

    while json_payload["next"]:
        rq = requests.get(json_payload["next"])
        json_payload = rq.json()
        data = petl.stack(data, petl.fromdicts(json_payload["results"]))

    data = petl.convert(data, "homeworld", resolve_name)
    data = petl.addfield(
        data,
        "date",
        lambda row: datetime.strptime(row["edited"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
            "%Y-%m-%d"
        ),
    )
    data = petl.cutout(
        data, "films", "starships", "vehicles", "species", "created", "edited", "url"
    )
    filename = f"{datetime.now().timestamp()}.csv"
    petl.tocsv(data, f"{settings.DATA_DIR}/{filename}")
    DownloadedFile(filename=filename).save()


def view_file(filename, page):
    """Return 10 rows per page from `filename` and the header to be used in building the template"""
    # TODO: header is most likely unneeded
    data = petl.fromcsv(f"{settings.DATA_DIR}/{filename}")
    slice = petl.rowslice(data, 0, page * 10)
    return petl.dicts(slice), petl.header(data)


def get_value_counts(filename, headers):
    """Return a value counts table for a combination of fields passed via the headers list"""
    # TODO: header is most likely unneeded
    data = petl.fromcsv(f"{settings.DATA_DIR}/{filename}")
    value_counts = petl.valuecounts(data, *headers)
    value_counts = petl.cutout(value_counts, "frequency")
    return petl.dicts(value_counts), petl.header(value_counts)
