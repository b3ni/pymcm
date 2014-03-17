
import core


class IncreaseStock(core.Method):
    _namespace = 'stock'
    _name = 'increase'

    def __call__(self, id_article, amount):
        raise NotImplementedError()
