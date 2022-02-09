from io import BytesIO

import requests
from PIL import Image

API_KEY_GEOCODER = "40d1649f-0493-4b70-98ba-98533de7710b"
API_KEY_SEARCH = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"


def geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": API_KEY_GEOCODER,
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(f"""Ошибка выполнения запроса: {response.url}\nHTTP статус: {response.status_code}({response.reason})""")

    return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


def get_ll_spn(address):
    toponym = geocode(address)
    if not toponym:
        return None, None
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])

    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    dx, dy = abs(float(l) - float(r)) / 2, abs(float(t) - float(b)) / 2
    spn = ",".join([str(dx), str(dy)])
    return ll, spn


def show_map(ll, spn, map_type="map", add_params=None):
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": map_type
    }
    if isinstance(add_params, dict):
        map_params.update(add_params)

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(response.content)).show()


def find_organizations(ll, spn, request, lang="ru_RU"):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": API_KEY_SEARCH,
        "text": request,
        "ll": ll,
        "spn": spn,
        "lang": lang
    }
    response = requests.get(search_api_server, params=search_params)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса: {response.url}\nHTTP статус: {response.status_code}({response.reason})""")
    organizations = json_response["features"]
    return organizations


def find_nearest_organization(ll, spn, request, lang="ru_RU"):
    organizations = find_organizations(ll, spn, request, lang)
    if len(organizations):
        return organizations[0]