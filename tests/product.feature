Feature: Funcionalidades para gestionar productos

    Operaciones sobre productos

    Scenario: Devuelve un producto por su id
        Given los siguientes ids de productos
            | product_id    |
            | 3237          |
            | 3268          |
            | 3275          |
        When quiero los datos de los productos
        Then obtengo los productos con sus datos
