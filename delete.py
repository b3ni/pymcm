# -*- coding: utf-8 -*-

import json
import csv
import cStringIO
import codecs
from mcm import Api


if __name__ == '__main__':
    with open('tests/config.txt', 'r') as f:
        data = f.read()

    data = json.loads(data)
    api = Api(user=data['user'], apikey=data['apikey'])

    print api.stock.delete(id_article="108793085", amount=1)
