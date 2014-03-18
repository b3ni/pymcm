import core
from mcm.models import Article


class GetStock(core.Method):
    _namespace = 'stock'
    _name = 'stock'

    def __call__(self):
        self._response = []

        status_code = 0
        start = 1

        while True:
            response = self.api.iterate_response(u'{}/{}'.format(self._name, start), tag='article', callback=self._parse_article)
            status_code = response.status_code

            for article in self._response:
                yield article
            self._response = []

            if status_code == 206:
                start += 100
            elif status_code == 204:
                break

    def update(self):
        raise NotImplementedError()

    def _parse_article(self, xml):
        self._response.append(Article.parse(xml))
