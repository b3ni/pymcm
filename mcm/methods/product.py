
import core
from mcm.models import Product


class GetProduct(core.Method):
    _namespace = 'products'
    _name = 'product'

    def __call__(self, id_article):
        self._obj = None
        self.api.iterate_response(u'product/{}'.format(id_article), tag='product', callback=self._parse)
        return self._obj

    def _parse(self, xml):
        self._obj = Product.parse(xml)
