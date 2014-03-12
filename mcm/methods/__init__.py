
def get():
    from core import MetaMethod

    modules_name = ("stock", )

    for name in modules_name:
        __import__(name, globals(), locals(), [], -1)

    modules = []
    for cls in MetaMethod._methods:
        obj = cls.create_instance()
        modules.append(obj)

    return modules
