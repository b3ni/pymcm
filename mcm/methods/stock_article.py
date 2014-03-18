
import core
from mcm.models import Article


class GetSingleArticleStock(core.Method):
    _namespace = 'stock'
    _name = 'article'

    def __call__(self, id_article):
        self._obj = None
        self.api.iterate_response(u'stock/{}/{}'.format(self._name, id_article), tag='article', callback=self._parse)
        return self._obj

    def _parse(self, xml):
        self._obj = Article.parse(xml)
