# -*- coding: utf-8 -*-

__all__ = ['Api']

import methods


class Api(object):
    def __init__(self, user, apikey):
        self.user = user
        self.apikey = apikey

    stock = methods.stock
    stock_article = methods.stock_article
    stock_add_article = methods.add_article
