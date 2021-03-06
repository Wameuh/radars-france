# -*- coding: utf-8 -*-
import json
import requests

from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://stackoverflow.com', HTTPAdapter(max_retries=5))


def endpoint(part):
    return 'https://{base}/{part}?_format=json'.format(
        base='radars.securite-routiere.gouv.fr/radars',
        part=part
    )


def do_request(url):
    r = requests.get(
        url,
        verify=False,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
    )
    r.raise_for_status()

    return r

radars = do_request(endpoint('all'))
radars.raise_for_status()

for radar in radars.json():
    id = radar['id']

    r = do_request(endpoint(id))
    r.raise_for_status()

    path = 'data/{id}.json'.format(id=id)
    with open(path, 'w') as f:
        f.write(json.dumps(r.json()))
