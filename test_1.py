# test_capitalize.py
import requests
import pytest
import json


# test_capitalize.py

@pytest.fixture
def get_req():
    headers = {'Accept': 'application/json'}
    get_r = requests.get("https://splunk.mocklab.io/movies?q=batman", headers=headers)
    d = json.loads(get_r.content)
    return (get_r, d)


def test_get_req(get_req):
    contents = get_req
    assert (contents[0].status_code) == 200

def test_same_image(get_req):
    d = get_req[1]
    results = ((d['results']))
    poster_images = {}
    for movies in results:
        if 'poster_path' not in movies:
            continue
        assert (movies['poster_path']) not in poster_images  # check if 2 movies have same image
        poster_images[(movies['poster_path'])] = 1


def test_valid_poster_link(get_req):
    d = get_req[1]
    results = ((d['results']))
    for movies in results:
        if 'poster_path' not in movies:
            continue
        if (movies['poster_path']) is None:
            continue
        ret = requests.head(movies['poster_path'])
        assert ret.status_code < 400


