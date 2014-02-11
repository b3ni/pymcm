# -*- coding: utf-8 -*-
from lettuce import step, world


@step(u'Given el listado de stock de un usuario')
def given_el_listado_de_stock_de_un_usuario(step):
    pass


@step(u'When quiero obtener que cartas tengo en stock')
def when_quiero_obtener_que_cartas_tengo_en_stock(step):
    pass


@step(u'Then obtengo un listado con las cartas que tengo en stock con los siguientes datos')
def then_obtengo_un_listado_con_las_cartas_que_tengo_en_stock_con_los_siguientes_datos(step):
    for article in world.api.stock():
        pass


