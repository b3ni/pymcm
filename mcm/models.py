# -*- coding: utf-8 -*-
import mcm


class ObjectMCM(object):
    def __init__(self, id, name):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __eq__(self, other):
        return self._id == other._id


class Article(ObjectMCM):

    @staticmethod
    def parse(xml):
        """
        https://www.mkmapi.eu/ws/documentation/Entity:Article

        <article>
            <idArticle />        // Article's ID
            <idProduct />        // Product's ID
            <language>           // Language entity for the language of the article
                <idLanguage />
                <languageName />
            </language>
            <comments />         // Comments from the seller
            <price />            // Price for the article
            <count />            // Amount (see notes)
            <seller />           // User entity of the seller
            <lastEdited />       // Date the article was last updated
            <condition />        // Condition of the article (if applicable)
            <isFoil />           // Flag, if the article is foil (see notes)
            <isSigned />         // Flag, if the article is signed (see notes)
            <isAltered />        // Flag, if the article is altered (see notes)
            <isPlayset />        // Flag, if the article is offered as playset (see notes)
            <isFirstEd />        // Flag, if the article is first edition (see notes)
        </article>
        """
        article = Article(mcm.txt(xml, 'idArticle'), None)
        article.id_product = mcm.txt(xml, 'idProduct')
        article.id_lang = mcm.txt(xml, ('language', 'idLanguage'))
        article.comments = mcm.txt(xml, 'comments')
        article.price = mcm.float(xml, 'price')
        article.count = mcm.int(xml, 'count')
        article.id_seller = mcm.txt(xml, ('seller', 'idUser'))
        article.last_edited = mcm.datetime(xml, 'lastEdited')
        article.condition = mcm.txt(xml, 'condition')
        article.foil = mcm.bool(xml, 'isFoil')
        article.signed = mcm.bool(xml, 'isSigned')
        article.altered = mcm.bool(xml, 'isAltered')
        article.playset = mcm.bool(xml, 'isPlayset')

        return article


class Language(ObjectMCM):
    pass


class Category(ObjectMCM):
    pass


class Expansion(ObjectMCM):
    pass


class Product(ObjectMCM):

    @property
    def name(self):
        return self.names["1"]

    @staticmethod
    def parse(xml):
        """
        https://www.mkmapi.eu/ws/documentation/Entity:Product

        <product>
            <idProduct />         // Product's id
            <idMetaproduct />     // Metaproduct's id
            <name>                // A name entity for each localized version of the entity
                <idLanguage />
                <languageName />
                <productName />
            </name>
            <category>            // A category entity for each localized version of the entity
                <idCategory />
                <categoryName />
            </category>
            <priceGuide>          // A price guide entity for each localized version of the entity
                <SELL />
                <LOW />
                <AVG />
            </priceGuide>
            <image />             // Path to the product image
            <expansion />         // English name for the expansion of the product (if applicable)
            <rarity />            // Rarity of the product (if applicable)
        </product>
        """
        product = Product(mcm.txt(xml, 'idProduct'), None)
        product.id_metaproduct = mcm.txt(xml, 'idMetaproduct')

        product.names = {}
        for name in xml.findall('name'):
            product.names[mcm.txt(name, 'idLanguage')] = mcm.txt(name, 'productName')

        product.category = Category(mcm.txt(name, 'idCategory'), mcm.txt(name, 'categoryName'))
        product.price_sell = mcm.float(xml, ('priceGuide', 'SELL'))
        product.price_low = mcm.float(xml, ('priceGuide', 'LOW'))
        product.price_avg = mcm.float(xml, ('priceGuide', 'AVG'))

        product.image = mcm.txt(xml, 'image')
        product.expansion = Expansion(mcm.txt(xml, 'expansion'), mcm.txt(xml, 'expansion'))
        product.rarity = mcm.txt(xml, 'rarity')

        return product
