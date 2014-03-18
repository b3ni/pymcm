
class MetaMethod(type):
    _methods = []

    def __init__(self, name, bases, attrs):
        super(MetaMethod, self).__init__(name, bases, attrs)

        module_parts = self.__module__.split('.')
        if module_parts[-1] != 'core':
            self._methods.append(self)


class MethodBase(object):
    __metaclass__ = MetaMethod

    _name = None
    _namespace = None

    @classmethod
    def create_instance(cls, api):
        obj = object.__new__(cls)
        obj.__init__(api)
        return obj

    def __init__(self):
        if not self._name:
            name = type(self).__name__.split('.')[0]
            raise ValueError("The class %s has to have a _name attribute" % name)

        if not self._namespace:
            name = type(self).__name__.split('.')[0]
            raise ValueError("The class %s has to have a _namespace attribute" % name)


class Method(MethodBase):
    def __init__(self, api):
        self.api = api
        self.log = self.api.log
