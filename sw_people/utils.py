# TODO: maybe the whole file is not needed, but likely can be extended with addtional functions
from functools import cache

import requests


@cache
def resolve_name(url):
    """Return the name from the payload of the `url`.
    Simple cache to reduce requests, as those are unlikely to change
    Can be used to lookup names of multiple things(planets, films, starships, etc)
    """
    # TODO: some error hadling
    return requests.get(url).json()["name"]
