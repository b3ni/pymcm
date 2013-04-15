# -*- coding: utf-8 -*-


class Card:
    def __init__(self, id, name=""):
        self.id = id
        self.name = name

        self.is_metacard = id.find('idMetacard') != -1

    def url(self):
        return "{0}".format(self.id)


class Want:
    def __init__(self, card, amount=1):
        self.card = card
        self.amount = amount


class WantList:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.wants = []

    def url(self):
        return "?mainPage=showWants&idWantsList={0}".format(self.id)

    def __str__(self):
        return "<WantList {0}> {1} ({2})".format(self.id, self.name, len(self.wants))


class Seller:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class CardArticle:
    def __init__(self, card, price, language, expansion, condition, quantity=1):
        self.card = card
        self.price = price
        self.language = language
        self.expansion = expansion
        self.condition = condition
        self.quantity = quantity


class Ship:
    def __init__(self, seller):
        self.seller = seller
        self.shipping = 0
        self.shipping_method = ''
        self.articles = []

    def total(self):
        return 0


class Cart:
    def __init__(self):
        self.ships = []

    def total(self):
        return 0
