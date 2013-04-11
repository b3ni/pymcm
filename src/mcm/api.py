# -*- coding: utf-8 -*-

import requests
import re
from lxml import etree

BASE = 'https://www.magiccardmarket.eu/'


def search(query, lang='en'):
    # http://lxml.de/xpathxslt.html

    pagenow = 0
    npages = None
    qs = {'mainPage': 'showSearchResult', 'searchFor': query, 'resultsPage': 0}
    while pagenow <= npages or npages is None:
        qs['resultsPage'] = pagenow
        r = requests.get(BASE, params=qs)
        r.raise_for_status()

        print "PAGE: {0}/{1}".format(pagenow, npages)
        utf8_parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.fromstring(r.text.encode('utf-8'), parser=utf8_parser)

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
                    result['from'] = 0
                else:
                    m = re.search("(\d+,\d+) ", data[0].text)
                    result['from'] = float(m.group(1).replace(',', '.'))

            yield result

        # next page
        pagenow += 1


def detail(id):
    r = requests.get(BASE + id)
    r.raise_for_status()

    utf8_parser = etree.HTMLParser(encoding='utf-8')
    tree = etree.fromstring(r.text.encode('utf-8'), parser=utf8_parser)

    obj = {'title': ''}

    title = tree.xpath("//h1")[0].text

    m = re.search('([\w\s]+)', title)
    obj['title'] = m.group(1).strip() if m else ''

    m = re.search('\(([\w\s]+)\)', title)
    obj['expansion'] = m.group(1).strip() if m else ''

    table = tree.xpath("//table[contains(@class, 'infoTable')]/tbody")[0]

    obj['rarity'] = table.xpath("tr[1]/td[2]/img/@alt")[0]
    obj['number'] = int(table.xpath("tr[2]/td[2]")[0].text)

    return obj


def list_prices(id, only_personal_seller=False, type_seller=None, language=None, condition=None, foil=None, signed=None, altered=None, amount=None):
    qs = {'mainPage': 'showProduct', 'idCategory': 0, 'idProduct': 0}

    m = re.search("c(\d+)p(\d+)", id)
    if m:
        qs['idCategory'] = m.group(1)
        qs['idProduct'] = m.group(2)

    if only_personal_seller:
        qs['productFilter[onlyPro]'] = 'on'

    if type_seller is not None:
        qs['productFilter[sellerRatings][]'] = type_seller

    if language is not None:
        qs['productFilter[idLanguage][]'] = language

    if condition is not None:
        qs['productFilter[condition][]'] = condition

    if foil is not None:
        qs['productFilter[isFoil]'] = foil

    if signed is not None:
        qs['productFilter[isSigned]'] = signed

    if altered is not None:
        qs['productFilter[isAltered]'] = altered

    if amount is not None:
        qs['productFilter[minAmount]'] = amount

    r = requests.get(BASE + id, params=qs)
    r.raise_for_status()

    utf8_parser = etree.HTMLParser(encoding='utf-8')
    tree = etree.fromstring(r.text.encode('utf-8'), parser=utf8_parser)

    # results?
    node = tree.xpath('//*[@id="siteContents"]/p[@class="warn bigFont"]')
    if len(node):
        return

    # table results
    tree = tree.xpath("//table[contains(@class, 'specimenTable')]/tbody")
    if len(tree) == 0:
        return
    tree = tree[0]

    for row in tree.xpath("tr"):
        result = {'seller_id': '', 'seller_name': '', 'seller_value': ''}

        # sellers data
        for span in row.xpath("td[1]/span"):



        data = row.xpath("td[1]/span/span[1]/a")
        if data:
            result['seller_id'] = data[0].attrib['href']
            result['seller_name'] = data[0].text

        data = row.xpath("td[1]/span/span[1]/text()")
        if data:
            result['seller_value'] = data[0].strip()[1:-1]

        data = row.xpath("td[1]/span/span[2]/span/@onmouseover")
        if data:
            m = re.search("'Item location: ([\w\s]+)'", data[0])
            result['seller_location'] = m.group(1)

        yield result











if __name__ == '__main__':
    # for r in search('magic'):
    #     print r

    for p in list_prices('Rancor_Magic_2013.c1p256673.prod'):
        print p
