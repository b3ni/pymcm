# -*- coding: utf-8 -*-
import mechanize
import cookielib
import error
import models

import codecs
import datetime
import logging
import sys
import re
from lxml import etree

logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


class MCMApi(object):
    base = 'https://www.magiccardmarket.eu/'

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.br = mechanize.Browser()
        self.cj = cookielib.LWPCookieJar()

        self.br.set_cookiejar(self.cj)

        self.br.set_handle_equiv(True)
        #self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)

        # follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9')]

        # debug
        #self.br.set_debug_http(True)
        #self.br.set_debug_redirects(True)
        #self.br.set_debug_responses(True)

        self.br.open(self.base)

    def login(self):
        self.br.select_form(predicate=lambda f: 'class' in f.attrs and f.attrs['class'] == 'loginForm')
        self.br['username'] = self.username
        self.br['userPassword'] = self.password
        self.br.submit()

        r = self.br.response().read()
        m = re.search(r"The password you entered was not correct", r)
        if m:
            raise error.LoginError()

    def get_wants_list(self):
        link = self.br.find_link(url="/?mainPage=showWants")
        self.br.follow_link(link)

        # read wants lists
        wants_lists = []
        utf8_parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.fromstring(self.br.response().read().decode('utf-8'), parser=utf8_parser)
        for wlnode in tree.xpath('//select[@name="sw_WantsListID"]/option'):
            name = re.search(r"([\w\s]+) ", wlnode.text)
            wl = models.WantList(int(wlnode.attrib['value']), name.group(1))

            # read wants card
            self.br.open(self.base + wl.url())
            tree = etree.fromstring(self.br.response().read().decode('utf-8'), parser=utf8_parser)
            for wantnode in tree.xpath('//table[contains(@class, "wantsTable")]/tbody/tr'):
                node = wantnode.xpath('td[3]/a')[0]
                card = models.Card(node.attrib['href'], node.text)

                node = wantnode.xpath('td[11]')[0]
                want = models.Want(card, int(node.text))

                wl.wants.append(want)

            wants_lists.append(wl)

        return wants_lists

    def get_cart(self):
        utf8_parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.fromstring(self.br.response().read().decode('utf-8'), parser=utf8_parser)

        node = tree.xpath('//*[@id="sc_menuhub"]')
        if node:
            m = re.search("\((\d+) articles", node[0].text)
            na = 0
            if m:
                na = int(m.group(1))
            if na == 0:
                return models.Cart()

        link = self.br.find_link(url="/?mainPage=showShoppingCart")
        self.br.follow_link(link)
        tree = etree.fromstring(self.br.response().read().decode('utf-8'), parser=utf8_parser)

        c = models.Cart()
        for shipnode in tree.xpath('//div[@class="sc_ShipTable"]'):
            # sumary
            sumarynode = shipnode.xpath('.//table[@class="nestedContent"]')[2]

            # read seller
            node = sumarynode.xpath('.//a[contains(@href, "showSellerChart")]')[1]
            seller = models.Seller(id=node.attrib['href'], name=node.text)

            # ship
            s = models.Ship(seller=seller)

            # shipping
            node = sumarynode.xpath('tr[6]/td[2]/text()')[0]
            m = re.search("([\d,]+) ", node)
            if m:
                s.shipping = float(m.group(1).replace(',', '.'))

            # shipping method
            node = None
            for tr in sumarynode.xpath('tr'):
                td = tr.xpath('td/text()')[0]
                if td.find('Shipping Method') != -1:
                    node = tr
            if node is not None:
                m = re.search("\(([\w\s]+)\)", etree.tostring(node))
                if m:
                    s.shipping_method = m.group(1)

            # items
            for item in shipnode.xpath('.//form[contains(@name, "itemViewForm")]/table/tbody/tr'):
                idcard = item.xpath('td[2]/a/@href')[0]
                namecard = item.xpath('td[2]/a/text()')[0]
                pricecard = item.xpath('td[9]/text()')[0]
                m = re.search("([\d,]+) ", pricecard)
                if m:
                    pricecard = float(m.group(1).replace(',', '.'))

                langcard = item.xpath('td[5]/a/span/@onmouseover')[0]
                m = re.search("\('([\w\s]+)'\)", langcard)
                if m:
                    langcard = m.group(1)
                expansion = item.xpath('td[3]/span/@onmouseover')[0]
                m = re.search("\('([\w\s]+)'\)", expansion)
                if m:
                    expansion = m.group(1)
                condition = item.xpath('td[6]/a/img/@onmouseover')[0]
                m = re.search("\('([\w\s]+)'\)", condition)
                if m:
                    condition = m.group(1)
                quantity = int(item.xpath('td[2]/text()')[0][0:-2])

                card = models.Card(idcard, namecard)
                cardarticle = models.CardArticle(card, pricecard, langcard, expansion, condition, quantity)

                s.articles.append(cardarticle)









            #print self.node_text(node[0])





            c.ships.append(s)

        return c

    def _page(self):
        text = self.br.response().read().decode('utf-8')
        t = datetime.datetime.now()
        with codecs.open("last{0}{1}{2}_{3}{4}{5}.html".format(t.year, t.month, t.day, t.hour, t.minute, t.second), "w", "utf-8") as f:
            f.write(text)

    def node_text(self, node):
        from lxml.etree import tostring
        return tostring(node)


if __name__ == '__main__':
    from pprint import pprint

    mcm = MCMApi(username='xx', password='xx')

    mcm.login()

    cart = mcm.get_cart()

    for s in cart.ships:
        pprint(vars(s))
        pprint(vars(s.seller))
        for a in s.articles:
            pprint(vars(a))
            pprint(vars(a.card))
        print "=" * 10

    # for wl in mcm.get_wants_list():
    #     print wl
