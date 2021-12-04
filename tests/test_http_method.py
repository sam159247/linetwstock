import pytest
import requests

from app.exceptions import RequestMethodNotSupportError
from app.internal.finmind_api import FindMindAPI


def test_get() -> None:
    url = "https://httpbin.org/get"
    parameter = {"test": "test"}
    resp = FindMindAPI._request_api(method="GET", url=url, payload=parameter)

    assert resp.status_code == 200


def test_post() -> None:
    url = "https://httpbin.org/post"
    parameter = {"test": "test"}
    resp = FindMindAPI._request_api(method="POST", url=url, payload=parameter)

    assert resp.status_code == 200


def test_method_error() -> None:
    url = "https://httpbin.org/"
    parameter = {"test": "test"}
    with pytest.raises(RequestMethodNotSupportError) as exc_info:
        FindMindAPI._request_api(method="XXX", url=url, payload=parameter)

    assert type(exc_info.value) is RequestMethodNotSupportError


def test_http_error() -> None:
    url = "https://httpbin.org/status/404"
    parameter = {"test": "test"}
    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        FindMindAPI._request_api(method="GET", url=url, payload=parameter)

    assert type(exc_info.value) is requests.exceptions.HTTPError
