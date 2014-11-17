# -*- coding: utf-8 -*-

__all__ = ['Api']

import methods
import requests
import logging
import mcm
from lxml import etree
from cStringIO import StringIO

logging.basicConfig(level=logging.DEBUG)


class Namespace(object):
    pass


class Api(object):
    def __init__(self, user, apikey):
        self.user = user
        self.apikey = apikey
        self.log = logging.getLogger(__name__)

        for m in methods.get(self):
            if not hasattr(self, m._namespace):
                setattr(self, m._namespace, Namespace())
            namespace = getattr(self, m._namespace)
            setattr(namespace, m._name, m)

    @property
    def urlbase(self):
        return "https://www.mkmapi.eu/ws/{user}/{key}/".format(user=self.user,
                                                               key=self.apikey)

    def get(self, action, params={}):
        self.log.info("GET: {}".format(self.urlbase + action))
        response = requests.get(self.urlbase + action)
        return response

    def delete(self, action, data):
        self.log.info(u"DELETE: {}".format(self.urlbase + action))
        response = requests.delete(self.urlbase + action, data=data)
        return response

    def iterate_response(self, action, params={}, tag=None, callback=None):
        def _fast_iter(context, func, func_error):
            def _clear(elem):
                # elem.clear()
                # while elem.getprevious() is not None:
                #     del elem.getparent()[0]
                pass

            for index, (event, elem) in enumerate(context):
                if elem.tag == 'errors':
                    func_error(elem)
                    break
                elif elem.tag == tag:
                    func(elem)
                    _clear(elem)

            del context

        response = self.get(action, params)
        #self.log.debug("RESPONSE:\n{}".format(response.content))

        if response.content:
            context = etree.iterparse(StringIO(response.content),
                                      events=('end',))
            _fast_iter(context, callback, self._callback_error)

        return response

    def _callback_error(self, xml):
        msg = mcm.txt(xml, 'message')
        error = mcm.txt(xml, 'error')
        #exc = self.txt(xml, 'exception')

        self.log.error(u"ERROR: <{}> {}".format(error, msg))
