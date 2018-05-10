import requests
import pytest
import json


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
        if (movies['poster_path']) is None:
            continue
        ret = requests.head(movies['poster_path'])
        assert ret.status_code < 400  # invalid link


def test_sorting_req(get_req):
    d = get_req[1]
    results = ((d['results']))
    Genre_none_sort = True
    prev_id = -1
    for movies in results:
        assert (movies['id']) > prev_id  # not in ascending order
        prev_id = (movies['id'])
        if movies['genre_ids'] is None:
            assert Genre_none_sort is True  # Null genre ids after non nulls
            continue
        else:
            Genre_none_sort = False


def test_genreid_sum(get_req):
    d = get_req[1]
    results = ((d['results']))
    count_gid_400 = 0
    for movies in results:
        if movies['genre_ids'] is None:
            continue
        else:
            if sum(movies['genre_ids']) > 400:
                count_gid_400 += 1
        assert count_gid_400 < 8


def test_palind_title(get_req):
    d = get_req[1]
    results = ((d['results']))
    count_pals = 0
    pal_titles=[]
    for movies in results:
        if movies['title'] is None:
            continue
        else:
            title = movies['title']
            words_title = title.split()
            for word in words_title:
                len_t = len(word)
                pal = True
                for c in range(int(len_t / 2)):
                    if word[c] != word[len_t - 1 - c]:
                        pal = False
                if pal == True:
                    pal_titles.append(title)
                    count_pals += 1
    assert count_pals > 0
