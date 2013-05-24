# -*- coding: utf-8 -*-
import mechanize
import cookielib
import error
import models
import urllib2

import codecs
import datetime
import re
from lxml import etree


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

        # create cart
        c = models.Cart(tree.xpath('//*[@id="sc_hashCode"]/@value')[0])

        # ships
        for shipnode in tree.xpath('//div[@class="sc_ShipTable"]'):
            # id
            shipid = int(shipnode.xpath('div/@id')[0].split('_')[-1])

            # hash
            bhash = shipnode.xpath('.//button/@onclick')[0]
            m = re.search("jcp\('([^']+)'", bhash)
            if m:
                bhash = m.group(1)

            # sumary
            sumarynode = shipnode.xpath('.//table[@class="nestedContent"]')[2]

            # read seller
            node = sumarynode.xpath('.//a[contains(@href, "showSellerChart")]')[1]
            seller = models.Seller(id=node.attrib['href'], name=node.text)

            # ship
            s = models.Ship(shipid, bhash, c, seller)

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

            c.ships.append(s)

        return c

    def remove_ship_from_cart(self, ship):
        if not ship.id:
            return

        url = "{0}iajax.php".format(self.base)
        referer = "{0}?mainPage=showShoppingCart".format(self.base)

        hashremove = ship.hash + urllib2.quote("{0},{1}".format(ship.id, ship.cart.hash), safe='~@#$&()*!+=:;,.?/\'')
        self._create_ajax_request(url, referer, "args=" + hashremove)

    def search(self, query, lang='en'):
        pagenow = 0
        npages = None
        utf8_parser = etree.HTMLParser(encoding='utf-8')

        while pagenow <= npages or npages is None:
            print "PAGE: {0}/{1}".format(pagenow, npages)

            self.br.open("{0}?mainPage=showSearchResult&searchFor={1}&resultsPage={2}".format(self.base, query, pagenow))
            tree = etree.fromstring(self.br.response().read().decode('utf-8'), parser=utf8_parser)

            # number of pages
            if npages is None:
                href = tree.xpath('//*[@id="siteContents"]/div/div[1]/span[3]/a[2]/@href')
                npages = 1
                if len(href):
                    m = re.search('resultsPage=(\d+)', href[0])
                    npages = int(m.group(1)) + 1

            # serach table
            tree = tree.xpath("//table[contains(@class, 'SearchTable')]/tbody")
            if len(tree) == 0:
                return
            tree = tree[0]

            # rows
            rows = tree.xpath("tr[contains(@class, 'row_')]")
            for row in rows:
                result = {'img': '', 'expansion': '', 'rarity': '', 'name': '', 'id': '', 'category': '', 'available': '', 'from': 0}

                data = row.xpath("td[1]//img/@onmouseover")
                if data:
                    m = re.search("'(.+?)'", data[0])
                    result['img'] = m.group(1)

                data = row.xpath("td[2]/span/@onmouseover")
                if data:
                    m = re.search("'(.+?)'", data[0])
                    result['expansion'] = m.group(1)

                data = row.xpath("td[3]/img/@onmouseover")
                if data:
                    m = re.search("'(.+?)'", data[0])
                    result['rarity'] = m.group(1)

                data = row.xpath("td[5]/a")
                if data:
                    result['id'] = data[0].attrib['href']
                    result['name'] = data[0].text

                data = row.xpath("td[6]")
                if data:
                    result['category'] = data[0].text

                data = row.xpath("td[7]")
                if data:
                    result['available'] = int(data[0].text)

                data = row.xpath("td[8]")
                if data:
                    if data[0].text == u"N/A":
                        result['price_from'] = 0
                    else:
                        m = re.search("(\d+,\d+) ", data[0].text)
                        result['price_from'] = float(m.group(1).replace(',', '.'))

                c = models.Card(result['id'], name=result['name'], img=result['img'])
                yield models.SearchResult(c, result['expansion'], result['rarity'], result['category'], result['available'], result['price_from'])

            # next page
            pagenow += 1

    def list_prices(self, card, filters={}):
        self.br.open(card.url())
        utf8_parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.fromstring(self.br.response().read().decode('utf-8'), parser=utf8_parser)

        tree = tree.xpath('//table[contains(@class, "specimenTable")]')[0]

        results = []
        for cardnode in tree.xpath('tbody/tr'):
            node = cardnode.xpath('td[2]/span/span[1]/a')[0]
            sellerid = node.attrib['href']
            sellertext = node.text
            node = cardnode.xpath('td[2]/span/span[2]/span/@onmouseover')[0]
            m = re.search('location: ([\w\s]+)', node)
            sellerlang = m.group(1)
            node = cardnode.xpath('td[2]/span/span[3]/img/@onmouseover')[0]
            m = re.search("'([\w\s]+)'", node)
            sellerclass = m.group(1) if m else 'warning'

            s = models.Seller(sellerid, sellertext, country=sellerlang, cls=sellerclass)

            node = cardnode.xpath('td[3]/span/@onmouseover')[0]
            m = re.search("'([\w\s]+)'", node)
            expansion = m.group(1)

            node = cardnode.xpath('td[5]/a/span/@onmouseover')[0]
            m = re.search("'([\w\s-]+)'", node)
            lang = m.group(1)

            node = cardnode.xpath('td[6]/a/img/@onmouseover')[0]
            m = re.search("'([\w\s]+)'", node)
            condition = m.group(1)

            node = cardnode.xpath('td[9]/text()')[0]
            m = re.search("([\d,]+) ", node)
            price = float(m.group(1).replace(',', '.'))

            node = cardnode.xpath('td[10]/text()')[0]
            quantity = int(node)

            node = cardnode.xpath('td[11]//input[@type="image"]/@value')[0]
            idprice = int(node)

            results.append(models.PriceCard(idprice, card, s, expansion, lang, condition, price, quantity))

        return results

    def add_to_cart(self, pricecard, amount=1):
        if pricecard.available < 1:
            return False

        self.br.open(pricecard.card.url())
        self.br.select_form(predicate=lambda f: 'name' in f.attrs and f.attrs['name'].find('itemViewForm') != -1)

        form = None
        for f in self.br.forms():
            if 'name' in f.attrs and f.attrs['name'].find('itemViewForm') != -1:
                form = f
                break

        if not form:
            return False

        if amount > pricecard.available:
            amount = pricecard.available

        self.br.submit('putSingleArticleInCart{0}'.format(pricecard.id))

    def get_my_articles(self):
        link = self.br.find_link(url_regex="browseUserProducts")
        self.br.follow_link(link)

        utf8_parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.fromstring(self.br.response().read().decode('utf-8'), parser=utf8_parser)

        raise NotImplementedError()

    def _create_ajax_request(self, url, referer, data):
        req = mechanize.Request(url, data=data)
        req.add_header("User-Agent", "Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9")
        req.add_header("Referer", referer)
        self.cj.add_cookie_header(req)

        return mechanize.urlopen(req)

    def _page(self):
        text = self.br.response().read().decode('utf-8')
        t = datetime.datetime.now()
        with codecs.open("last{0}{1}{2}_{3}{4}{5}.html".format(t.year, t.month, t.day, t.hour, t.minute, t.second), "w", "utf-8") as f:
            f.write(text)

    def _node_text(self, node):
        from lxml.etree import tostring
        return tostring(node)


if __name__ == '__main__':
    from pprint import pprint

    mcm = MCMApi(username='foo', password='bar')
    mcm.login()

    # search
    mcm.get_my_articles()
