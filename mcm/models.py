# -*- coding: utf-8 -*-


class Card:
    def __init__(self, id, name="", img=""):
        self.id = id
        self.name = name
        self.img = img

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
    def __init__(self, id, name, country='', cls=''):
        self.id = id
        self.name = name
        self.country = country
        self.cls = cls


class CardArticle:
    def __init__(self, card, price, language, expansion, condition, quantity=1):
        self.card = card
        self.price = price
        self.language = language
        self.expansion = expansion
        self.condition = condition
        self.quantity = quantity


class Ship:
    def __init__(self, id, hash, cart, seller):
        self.id = id
        self.hash = hash
        self.cart = cart
        self.seller = seller
        self.shipping = 0
        self.shipping_method = ''
        self.articles = []

    def total(self):
        total_articles = sum(a.price for a in self.articles)

        return total_articles + self.shipping


class Cart:
    def __init__(self, hash=''):
        self.hash = hash
        self.ships = []

    def total(self):
        return sum(s.total() for s in self.ships)


class SearchResult:
    def __init__(self, card, expansion, rarity, category, available, price_from):
        self.card = card
        self.expansion = expansion
        self.rarity = rarity
        self.category = category
        self.available = available
        self.price_from = price_from


class PriceCard:
    def __init__(self, id, card, seller, expansion, language, condition, price, available):
        self.id = id
        self.card = card
        self.seller = seller
        self.expansion = expansion
        self.language = language
        self.condition = condition
        self.price = price
        self.available = available
