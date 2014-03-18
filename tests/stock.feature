Feature: Funcionalidades para gestionar el stock

    Operaciones sobre el stock

    Scenario: Devuelve todas la cartas que tienes en stock
        Given el listado de stock de un usuario
        When quiero obtener que cartas tengo en stock
        Then obtengo un listado con las cartas que tengo en stock con los siguientes datos

    Scenario: Obtener un el detalle de un articulo en stock
        Given los siguientes ids de articulos articulo
            | article_id    |
            | 108793085     |
            | 108793101     |
            | 108696358     |
        When quiero obtener el detalle de los articulos en mi stock conociendo su id
        Then obtengo los articulos de mi stock
