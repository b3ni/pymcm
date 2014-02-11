from lettuce import *

Feature: Funcionalidades para gestionar el stock

    Operaciones sobre el stock

    Scenario: Devuelve todas la cartas que tienes en stock
        Given el listado de stock de un usuario
        When quiero obtener que cartas tengo en stock
        Then obtengo un listado con las cartas que tengo en stock con los siguientes datos

