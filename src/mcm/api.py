import requests
import re
from lxml import etree

BASE = 'https://www.magiccardmarket.eu/'


def search(query, lang='en'):
    # http://lxml.de/xpathxslt.html
    qs = {'mainPage': 'showSearchResult', 'searchFor': query, 'resultsPage': 0}

    r = requests.get(BASE, params=qs)
    r.raise_for_status()

    utf8_parser = etree.HTMLParser(encoding='utf-8')
    s = r.text.encode('utf-8')
    tree = etree.fromstring(s, parser=utf8_parser)

    # number of pages
    href = tree.xpath('//*[@id="siteContents"]/div/div[1]/span[3]/a[2]/@href')
    npages = 1
    if len(href):
        m = re.search('resultsPage=(\d+)', href[0])
        npages = int(m.group(1)) + 1

    # serach table
    tree = tree.xpath("//table[contains(@class, 'SearchTable')]/tbody")
    if len(tree) == 0:
        return
    tree = tree[0].getroottree()

    # for e in tree.getroottree().iter():
    #     print tree.getpath(e)

    pagenow = 1
    while pagenow <= npages:
        print "PAGE: {0}/{1}".format(pagenow, npages)

        rows = tree.xpath("/tr[contains(@class, 'row_')]")

        print rows
        break
        for row in rows:
            result = {'img': '', 'expansion': '', 'rarity': '', 'name': '', 'id': ''}

            data = row.xpath("/td[1]/img/@onmouseover")
            if data:
                m = re.search("'(.+?)'", data[0])
                result['img'] = m.group(1)

            data = row.xpath("/td[2]/span/@onmouseover")
            if data:
                m = re.search("'(.+?)'", data[0])
                result['expansion'] = m.group(1)

            data = row.xpath("/td[3]/img/@onmouseover")
            if data:
                m = re.search("'(.+?)'", data[0])
                result['rarity'] = m.group(1)

            data = row.xpath("/td[5]/a")
            if data:
                result['id'] = data[0].attrib['href']

                # result['id'] = data.
                # m = re.search("'(.+?)'", data[0])
                # result['rarity'] = m.group(1)

            yield result

        pagenow += 1


if __name__ == '__main__':
    for r in search('magic'):
        print r
