import requests
import re
from lxml import etree

BASE = 'https://www.magiccardmarket.eu/'


def search(query, lang='en'):
    qs = {'mainPage': 'showSearchr', 'searchFor': query, 'resultsPage': 0}

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

    pagenow = 1
    while pagenow <= npages:
        print "PAGE: {0}/{1}".format(pagenow, npages)

        for row in tree.xpath("//*[@id=\"siteContents\"]/div/table/tbody/tr[contains(@class, 'row_')]"):
            result = {'img': '', 'rarity': '', 'name': ''}

            img = row.xpath("//td[1]//img/@onmouseover")
            if img:
                print img
                m = re.search("'(.+?)'", img[0])
                result['img'] = m.group(1)

            # rarity = row.xpath("//td[2]//img/@onmouseover")
            # if rarity:
            #     pass

            # name = row.xpath("//td[3]//img/@onmouseover")
            # if name:
            #     pass

            yield result

        pagenow += 1


if __name__ == '__main__':
    for r in search('magic'):
        print r
