# -*- coding: utf-8 -*-


def bind(**config):

    class APIMethod(object):
        path = config['path']


    def _call(api, *args, **kargs):
        method = APIMethod(api, args, kargs)
        return method.execute()

    return _call
