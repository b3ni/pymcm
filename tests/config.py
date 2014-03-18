from lettuce import world


def get_config():
    import os
    import json

    if not os.path.exists('tests/config.txt'):
        assert False, "No tests/config.txt"

    with open('tests/config.txt', 'r') as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception as e:
        assert False, "File config.txt fail data: {} ERROR: {}".format(data, e)

    if 'user' not in data:
        assert False, "user not defined"

    if 'apikey' not in data:
        assert False, "apikey not defined"

    return data['user'], data['apikey']


def get_api():
    user, apikey = get_config()

    assert isinstance(user, unicode)
    assert isinstance(apikey, unicode)
    assert len(user) > 0
    assert len(apikey) > 0

    import mcm
    _api = mcm.Api(user=user, apikey=apikey)

    return _api

world.api = get_api()
