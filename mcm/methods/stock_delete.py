
import core


class DeleteArticleStock(core.Method):
    _namespace = 'stock'
    _name = 'delete'

    def __call__(self, id_article, amount):
        xml = """<article>
                    <idArticle>{}</idArticle>
                    <amount>{}</amount>
                 </article>""".format(id_article, amount)

        response = self.api.delete('stock', data={'article': xml})
        if response.status_code != 200:
            return False
        else:
            return True
