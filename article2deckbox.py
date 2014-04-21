# -*- coding: utf-8 -*-

import json
from mcm import Api
from mcm.tools import deckbox


if __name__ == '__main__':
    with open('tests/config.txt', 'r') as f:
        data = f.read()
    data = json.loads(data)
    api = Api(user=data['user'], apikey=data['apikey'])

    deckbox.export2csv(api, 'list.csv')
