# -*- coding: utf-8 -*-
import mechanize
import cookielib

import codecs
import datetime
import logging
import sys
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
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9')]

        self.br.open(self.base)

    def login(self):
        self.br.select_form(predicate=lambda f: 'class' in f.attrs and f.attrs['class'] == 'loginForm')
        self.br['username'] = self.username
        self.br['userPassword'] = self.password
        self.br.submit()

        print self.br.response().read()
        self._page()

    def get_wants_list(self):
        page = self._page({'mainPage': 'showWants'})

    def _page(self):
        text = self.br.response().read().decode('utf-8')

        print type(text)
        t = datetime.datetime.now()
        with codecs.open("last{0}{1}{2}_{3}{4}{5}.html".format(t.year, t.month, t.day, t.hour, t.minute, t.second), "w", "utf-8") as f:
            f.write(text)

if __name__ == '__main__':
    mcm = MCMApi(username='xxx', password='xxx')

    mcm.login()
    #mcm.get_wants_list()
