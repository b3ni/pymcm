# -*- coding: utf-8 -*-
import requests
import codecs
import datetime
from lxml import etree


class MCMApi(object):
    base = 'https://www.magiccardmarket.eu/'

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.s = requests.Session()

    def login(self):
        data = {
            'action':       'processPost',
            'post':         'login',
            'username':     self.username,
            'userPassword': self.password
        }
        self._page(data, 'post')

    def get_wants_list(self):
        page = self._page({'mainPage': 'showWants'})

    def _page(self, data={}, method='get'):
        t = datetime.datetime.now()
        if method == 'get':
            r = self.s.get(self.base, params=data)
        else:
            r = self.s.post(self.base, data)
        r.raise_for_status()

        with codecs.open("last{0}{1}{2}_{3}{4}{5}.html".format(t.year, t.month, t.day, t.hour, t.minute, t.second), "w", "utf-8") as f:
            f.write(r.text)

        return r.text

if __name__ == '__main__':
    mcm = MCMApi(username='xxx', password='xxx')

    mcm.login()
    mcm.get_wants_list()
