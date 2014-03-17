# -*- coding: utf-8 -*-
import datetime
from lettuce import step, world
from mcm import models


@step(u'Given el listado de stock de un usuario')
def given_el_listado_de_stock_de_un_usuario(step):
    world.stock = world.api.stock.stock()


@step(u'When quiero obtener que cartas tengo en stock')
def when_quiero_obtener_que_cartas_tengo_en_stock(step):
    try:
        iter(world.stock)
    except:
        assert False, u"no es iterable"


@step(u'Then obtengo un listado con las cartas que tengo en stock con los siguientes datos')
def then_obtengo_un_listado_con_las_cartas_que_tengo_en_stock_con_los_siguientes_datos(step):
    for article in world.stock:
        assert isinstance(article, models.Article), u"no es un articulo"
        assert isinstance(article.id_product, unicode)
        assert isinstance(article.id_lang, unicode)
        assert isinstance(article.comments, unicode)
        assert isinstance(article.price, float)
        assert isinstance(article.count, int)
        assert isinstance(article.id_seller, unicode)
        assert isinstance(article.last_edited, datetime.datetime)
        assert isinstance(article.condition, unicode)
        assert isinstance(article.foil, bool), u"No es bool, es value {}".format(article.foil)
        assert isinstance(article.signed, bool)
        assert isinstance(article.altered, bool)
        assert isinstance(article.playset, bool)

        assert article.condition in (u'MT', u'NM', u'EX', u'GD', u'LP', u'PL', u'PO'), u"No entiendo la condición {}".format(article.condition)
        assert article.price > 0.0
        assert article.count > 0


@step(u'Given los siguientes ids de articulos articulo')
def given_los_siguientes_ids_de_articulos_articulo(step):
    world.id_articles = []
    for data in step.hashes:
        world.id_articles.append(int(data['article_id']))


@step(u'When quiero obtener el detalle de los articulos en mi stock conociendo su id')
def when_quiero_obtener_el_detalle_de_los_articulos_en_mi_stock_conociendo_su_id(step):
    world.articles = []
    for id_article in world.id_articles:
        article = world.api.stock.article(id_article)
        world.articles.append(article)


@step(u'Then obtengo los articulos de mi stock')
def then_obtengo_los_articulos_de_mi_stock(step):
    for data in step.hashes:
        article_id = int(data['article_id'])

        article = None
        for a in world.articles:
            if a.id == article_id:
                article = a
                break

        assert article is not None, u"No encontrado articulo {}".format(article_id)

        assert isinstance(article, models.Article), u"no es un articulo"
        assert isinstance(article.id_product, unicode)
        assert isinstance(article.id_lang, unicode)
        assert isinstance(article.comments, unicode)
        assert isinstance(article.price, float)
        assert isinstance(article.count, int)
        assert isinstance(article.id_seller, unicode)
        assert isinstance(article.last_edited, datetime.datetime)
        assert isinstance(article.condition, unicode)
        assert isinstance(article.foil, bool), u"No es bool, es value {}".format(article.foil)
        assert isinstance(article.signed, bool)
        assert isinstance(article.altered, bool)
        assert isinstance(article.playset, bool)

        assert article.condition in (u'MT', u'NM', u'EX', u'GD', u'LP', u'PL', u'PO'), u"No entiendo la condición {}".format(article.condition)
        assert article.price > 0.0
        assert article.count > 0


@step(u'Given los siguientes ids de productos')
def given_los_siguientes_ids_de_productos(step):
    world.id_products = []
    for data in step.hashes:
        world.id_products.append(int(data['product_id']))


@step(u'When quiero los datos de los productos')
def when_quiero_los_datos_de_los_productos(step):
    world.products = []
    for id_product in world.id_products:
        p = world.api.products.product(id_product)
        world.products.append(p)


@step(u'Then obtengo los productos con sus datos')
def then_obtengo_los_productos_con_sus_datos(step):
    for data in step.hashes:
        product_id = int(data['product_id'])

        product = None
        for p in world.articles:
            if p.id == product_id:
                product = p
                break

        assert product is not None, u"No encontrado producto {}".format(product_id)

        assert isinstance(product, models.Product), u"no es un producto"
        assert isinstance(product.id_metaproduct, unicode)
        assert isinstance(product.names, dict)
        for id_lang in product.names:
            lang = product.names[id_lang]
            assert isinstance(lang, models.Language)
            assert hasattr(lang, 'name')
        assert isinstance(product.category, models.Category)
        assert hasattr(product.category, 'name')

        assert isinstance(product.price_sell, float)
        assert isinstance(product.price_low, float)
        assert isinstance(product.price_avg, float)
        assert product.price_sell > 0
        assert product.price_low > 0
        assert product.price_avg > 0

        assert isinstance(product.image, unicode)

        assert isinstance(product.expansion, models.Expansion)
        assert hasattr(product.expansion, 'name')

        assert isinstance(product.rarity, unicode)
        assert product.rarity in (u'Common', ), u"No entiendo la rareza {}".format(product.rarity)

        assert product.count > 0
