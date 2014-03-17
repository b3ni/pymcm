
import core


class DecreaseStock(core.Method):
    _namespace = 'stock'
    _name = 'decrease'

    def __call__(self, id_article, amount):
        raise NotImplementedError()
