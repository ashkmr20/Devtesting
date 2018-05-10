# test_capitalize.py
import requests
import pytest
import json


# test_capitalize.py

def get_req():
    headers = {'Accept': 'application/json'}
    return requests.get("https://splunk.mocklab.io/movies?q=batman", headers=headers)


def test_gets():
    contents = get_req()
    assert (contents.status_code) == 200
    print(contents.headers)
    file = open('testfile.txt', 'w')
    d = json.loads(contents.content)
    print(d)
    file.write(str(d))
    file.close()
