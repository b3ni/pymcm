# -*- coding: utf-8 -*-
import __builtin__
from datetime import datetime as dt

__builtin_float = getattr(__builtin__, "float")
__builtin_int = getattr(__builtin__, "int")
# __builtin_bool = getattr(__builtin__, "bool")


def txt(xml, tag):
    if isinstance(tag, tuple):
        if len(tag) > 1:
            for t in tag[0:-1]:
                xml = xml.find(t)
                if xml is None:
                    return u''
            tag = tag[-1]
        else:
            tag = tag[0]

    v = xml.find(tag)
    return unicode(v.text) if v is not None else u''


def float(xml, tag):
    v = txt(xml, tag)
    return __builtin_float(v)


def int(xml, tag):
    v = txt(xml, tag)
    return __builtin_int(v)


def bool(xml, tag):
    v = txt(xml, tag)
    return True if v == u'true' else False


def datetime(xml, tag):
    v = txt(xml, tag)
    return dt.strptime(v, '%Y-%m-%d %H:%M:%S')
