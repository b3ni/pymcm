
def get(api):
    from core import MetaMethod

    modules_name = ("stock_stock", "stock_article", "stock_decrease",
                    "stock_increase", "stock_delete", "product")

    for name in modules_name:
        __import__(name, globals(), locals(), [], -1)

    modules = []
    for cls in MetaMethod._methods:
        obj = cls.create_instance(api)
        modules.append(obj)

    return modules
