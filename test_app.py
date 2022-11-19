import json
import subprocess

import pytest
import validators


@pytest.fixture
def script():
    return ['python', 'cli_app.py']


def test_validate_url():
    fixtures_good = [
        'https://httpbin.org/get',
        'https://httpbin.org/post'
        'https://httpbin.org/patch',
        'https://httpbin.org/put',
        'https://httpbin.org/delete',
    ]

    fixtures_bad = [
        'https://-httpbin.org/gett',
        'hello_world',
    ]

    for fix in fixtures_good:
        assert validators.url(fix) is True
    for fix in fixtures_bad:
        try:
            validators.url(fix)
        except validators.ValidationFailure:
            assert True


def test_url(script):
    script.append('https://httpbin.org/get')
    expected = {
        'https://httpbin.org/get': {'GET': 200, 'HEAD': 200, 'OPTIONS': 200}
    }
    expected_json = json.dumps(expected, indent=4)
    result = subprocess.Popen(script,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              encoding='utf-8',
                              text=True,
                              shell=True)
    outs, err = result.communicate()
    assert outs.strip() == expected_json


def test_url_404(script):
    script.append('https://httpbin.org/gett')
    expected = {'https://httpbin.org/gett': 'Not found'}
    expected_json = json.dumps(expected, indent=4)
    result = subprocess.Popen(script,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              encoding='utf-8',
                              text=True,
                              shell=True)
    outs, err = result.communicate()
    assert outs.strip() == expected_json


def test_bad_url(script):
    script.append('hello_world')
    expected = {'hello_world': 'Not correct url item'}
    expected_json = json.dumps(expected, indent=4)
    result = subprocess.Popen(script,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              encoding='utf-8',
                              text=True,
                              shell=True)
    outs, err = result.communicate()
    assert outs.strip() == expected_json


def test_many_urls(script):
    urls = ['https://httpbin.org/get',
            'https://httpbin.org/post',
            'https://httpbin.org/put',
            'https://httpbin.org/patch',
            'https://httpbin.org/delete']
    script.extend(urls)
    expected = {
        'https://httpbin.org/get': {'GET': 200, 'HEAD': 200, 'OPTIONS': 200},
        'https://httpbin.org/post': {'POST': 200, 'OPTIONS': 200},
        'https://httpbin.org/put': {'PUT': 200, 'OPTIONS': 200},
        'https://httpbin.org/patch': {'PATCH': 200, 'OPTIONS': 200},
        'https://httpbin.org/delete': {'DELETE': 200, 'OPTIONS': 200},
    }
    expected_json = json.dumps(expected, indent=4)
    result = subprocess.Popen(script,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              encoding='utf-8',
                              text=True,
                              shell=True)
    outs, err = result.communicate()
    assert outs.strip() == expected_json


def test_many_urls_with_404_and_bad(script):
    urls = ['https://httpbin.org/get',
            'https://httpbin.org/gett',
            'https://httpbin.org/post',
            'https://httpbin.org/put',
            'https://httpbin.org/patch',
            'https://httpbin.org/delete',
            'hello_world']
    script.extend(urls)
    expected = {
        'https://httpbin.org/get': {'GET': 200, 'HEAD': 200, 'OPTIONS': 200},
        'https://httpbin.org/gett': 'Not found',
        'https://httpbin.org/post': {'POST': 200, 'OPTIONS': 200},
        'https://httpbin.org/put': {'PUT': 200, 'OPTIONS': 200},
        'https://httpbin.org/patch': {'PATCH': 200, 'OPTIONS': 200},
        'https://httpbin.org/delete': {'DELETE': 200, 'OPTIONS': 200},
        'hello_world': 'Not correct url item'
    }
    expected_json = json.dumps(expected, indent=4)
    result = subprocess.Popen(script,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              encoding='utf-8',
                              text=True,
                              shell=True)
    outs, err = result.communicate()
    assert outs.strip() == expected_json
