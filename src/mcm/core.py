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
        self.br.set_handle_gzip(True)
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
        pass

    def _page(self):
        text = self.br.response().read().decode('utf-8')
        t = datetime.datetime.now()
        with codecs.open("last{0}{1}{2}_{3}{4}{5}.html".format(t.year, t.month, t.day, t.hour, t.minute, t.second), "w", "utf-8") as f:
            f.write(text)

if __name__ == '__main__':
    mcm = MCMApi(username='xxx', password='xxx')

    mcm.login()

    for wl in mcm.get_wants_list():
        print wl
