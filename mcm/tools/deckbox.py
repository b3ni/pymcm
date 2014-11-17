# -*- coding: utf-8 -*-

import codecs
import csv
from mcm.misc.csv_writer import UnicodeWriter


def export2csv(api, csvfilename):
    """
    Export stock of a user to csv file Deckbox format
    """
    conditions = {
        'NM': u'Near Mint',
        "MT": u'Mint',
        "EX": u'Near Mint',
        "GD": u'Good (Lightly Played)',
        "LP": u'Played',
        "PL": u'Heavily Played',
        "PO": u'Poor'
    }
    languages = {
        '1': u'English',
        '2': u'French',
        '3': u'German',
        '4': u'Spanish',
        '5': u'Italian',
        '6': u'S-Chinese',
        '7': u'Japanese',
        '8': u'Portuguese',
        '9': u'Russian',
        '10': u'Korean',
        '11': u'T-Chinese'
    }
    expansions = {
        'Alara Reborn': u'Alara Reborn',
        'Alliances': u'Alliances',
        'Apocalypse': u'Apocalypse',
        'Avacyn Restored': u'Avacyn Restored',
        'Chronicles': u'Chronicles',
        'Commander': u'Commander',
        'Conflux': u'Conflux',
        'Dark Ascension': u'Dark Ascension',
        'Darksteel': u'Darksteel',
        'Dissension': u'Dissension',
        'Dragon\'s Maze': u'Dragon\'s Maze',
        'Duels of the Planeswalkers Promos': u'',  # special, promo y foil
        'Exodus': u'Exodus',
        'Fifth Dawn': u'Fifth Dawn',
        'Fifth Edition': u'Fifth Edition',
        'Fourth Edition': u'Fourth Edition',
        'Fourth Edition: Black Bordered': u'Fourth Edition',  # ??
        'Future Sight': u'Future Sight',
        'Gatecrash': u'Gatecrash',
        'Gateway Promos': u'',  # special, promo y foil
        'Homelands': u'Homelands',
        'Ice Age': u'Ice Age',
        'Innistrad': u'Innistrad',
        'Invasion': u'Invasion',
        'Judgment': u'Judgment',
        'Lorwyn': u'Lorwyn',
        'Magic 2010': u'Magic 2010',
        'Magic 2011': u'Magic 2011',
        'Magic 2012': u'Magic 2012',
        'Magic 2013': u'Magic 2013',
        'Magic 2014': u'Magic 2014 Core Set',
        'Mercadian Masques': u'Mercadian Masques',
        'Mirage': u'Mirage',
        'Mirrodin': u'Mirrodin',
        'Mirrodin Besieged': u'Mirrodin Besieged',
        'Nemesis': u'Nemesis',
        'New Phyrexia': u'New Phyrexia',
        'Odyssey': u'Odyssey',
        'Planar Chaos': u'Planar Chaos',
        'Planeshift': u'Planeshift',
        'Portal': u'Portal',
        'Portal Second Age': u'Portal Second Age',
        'Premium Deck Series: Fire & Lightning':
        u'Premium Deck Series: Fire and Lightning',
        'Prerelease Promos': u'',  # manual
        'Prophecy': u'Prophecy',
        'Ravnica: City of Guilds': u'Ravnica: City of Guilds',
        'Return to Ravnica': u'Return to Ravnica',
        'Revised': u'Revised Edition',
        'Rinascimento': u'Arabian Nights',  # special
        'Rise of the Eldrazi': u'Rise of the Eldrazi',
        'Saviors of Kamigawa': u'Saviors of Kamigawa',
        'Scars of Mirrodin': u'Scars of Mirrodin',
        'Seventh Edition': u'Seventh Edition',
        'Shards of Alara': u'Shards of Alara',
        'Sixth Edition': u'Classic Sixth Edition',
        'Stronghold': u'Stronghold',
        'Tempest': u'Tempest',
        'Tenth Edition': u'Tenth Edition',
        'Time Spiral': u'Time Spiral',
        'Unglued': u'Unglued',
        'Urza\'s Destiny': u'Urza\'s Destiny',
        'Urza\'s Legacy': u'Urza\'s Legacy',
        'Urza\'s Saga': u'Urza\'s Saga',
        'Visions': u'Visions',
        'Weatherlight': u'Weatherlight',
        'Worldwake': u'Worldwake',
        'Zendikar': u'Zendikar'
    }

    csvfile_fail = codecs.open(csvfilename + 'fail', 'w')
    writer_fail = UnicodeWriter(csvfile_fail, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)

    pack = 1
    csvfile = codecs.open(csvfilename + str(pack), 'w')
    writer = UnicodeWriter(csvfile, delimiter=',', quotechar='"',
                           quoting=csv.QUOTE_MINIMAL)
    writer.writerow([u'Count', u'Tradelist Count', u'Name', u'Foil',
                     u'Textless', u'Promo', u'Signed', u'Edition',
                     u'Condition', u'Language'])

    print "=" * 40, "Pack {}".format(pack), "=" * 40

    for index, article in enumerate(api.stock.stock()):
        product = api.products.product(article.id_product)

        if article.condition not in conditions:
            csvfile.close()
            csvfile_fail.close()
            raise Exception(u"Condition '{}' not defined".format(
                article.condition))

        if article.id_lang not in languages:
            csvfile.close()
            csvfile_fail.close()
            raise Exception(u"Id lang '{}' not defined".format(
                article.id_lang))

        if product.expansion.name not in expansions:
            csvfile.close()
            csvfile_fail.close()
            raise Exception(u"Expasion name '{}' not defined".format(
                product.expansion.name))

        # check character rare Æther Tide
        try:
            product.name.decode('ascii')
            ok_name = True
        except:
            ok_name = False

        # check versions
        if product.name.find('(Version ') != -1:
            ok_name = False

        row = [unicode(article.count),
               u"0",
               product.name,
               u"foil" if article.foil else u"",
               u'',
               u'',
               u"signed" if article.signed else u"",
               expansions[product.expansion.name],
               conditions[article.condition],
               languages[article.id_lang]]

        # special edition
        if product.expansion.name in ('Duels of the Planeswalkers Promos',
                                      'Gateway Promos'):
            row[3] = 'foil'
            row[5] = 'promo'

        if product.expansion.name in ('Rinascimento', ):
            row[9] = 'Italian'

        if product.expansion.name in ('Prerelease Promos', ):
            ok_name = False  # manual

        if ok_name:
            writer.writerow(row)
        else:
            writer_fail.writerow(row)

        if (index + 1) % 100 == 0:
            csvfile.close()
            pack += 1
            print "=" * 40, "Pack {}".format(pack), "=" * 40
            csvfile = codecs.open(csvfilename + str(pack), 'wb')
            writer = UnicodeWriter(csvfile, delimiter=',', quotechar='"',
                                   quoting=csv.QUOTE_MINIMAL)
            writer.writerow([u'Count', u'Tradelist Count', u'Name', u'Foil',
                             u'Textless', u'Promo', u'Signed', u'Edition',
                             u'Condition', u'Language'])

    csvfile.close()
    csvfile_fail.close()
