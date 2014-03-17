# -*- coding: utf-8 -*-

import json
import csv
import cStringIO
import codecs
from mcm import Api


class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


if __name__ == '__main__':
    with open('tests/config.txt', 'r') as f:
        data = f.read()

    data = json.loads(data)
    api = Api(user=data['user'], apikey=data['apikey'])

    articles = {}
    for article in api.stock.stock():
        product = api.products.product(article.id_product)

        if product.expansion.id not in articles:
            articles[product.expansion.id] = []

        articles[product.expansion.id].append((article, product))

    with codecs.open('list.csv', 'wb') as csvfile:
        writer = UnicodeWriter(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['id_expansion', 'expansion', 'id_article', 'id_product', 'product_name', 'cuantity'])
        for id_expansion in articles:
            for article, product in articles[id_expansion]:
                writer.writerow([id_expansion, product.expansion.name, article.id, product.id, product.name, unicode(article.count)])
