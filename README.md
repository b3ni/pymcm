# pymcm

A python client for web MagicCardMarket https://www.magiccardmarket.eu/

## Installation

```bash
pip install pymcm
```

## Requires

  * httplib2
  * mechanize
  * lxml

## Usage

### Login and search card

```python
import pymcm

mcm = MCMApi(username='foo', password='duu')

for result in mcm.search('sun titan'):
    prind result.card.name, result.available
```

### Read want lists

```python
for wl in mcm.get_wants_list():
    print wl.name

    for want_card in wl.wants:
        print wants_card.card.name, wants_card.amount
```

### Read a card prices

```python
one_card = wl.wants[0].card

for pc in mcm.list_prices(one_card):
    print "{0} ({1}): {2} {3}".format(pc.seller.name, pc.seller.country, pc.condition, pc.price)
```

### Add a card to cart

```python
pc = mcm.list_prices(one_card)[0]
mcm.add_to_cart(pc)
```

### Read a cart

```python
cart = mcm.get_cart()

print cart.total()
for 

```

## Contacts

pymcm is written by:

* Benito Rodriguez - brarcos@gmail.com

Suggestions, bugs,... https://github.com/b3ni/pymcm/issues
