# -*- coding: utf-8 -*-
import mcm


class Article(object):

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
        article = Article()
        article.id = mcm.txt(xml, 'idArticle')
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
