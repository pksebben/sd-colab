# This should contain a series of scripts to test data input with post requests

import requests

BASE_URL = 'http://localhost:8080'

def test_register_user():
    URL_EXTENSION = '/register_user'
    postdata = {
        'email' : 'bob@test.com',
        'password' : 'bobspass'
    }
    url = BASE_URL + URL_EXTENSION
    res = requests.post(url, data = postdata)
    print(res)
