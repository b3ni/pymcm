#!/usr/bin/env python
from setuptools import setup, find_packages

LONGDESCRIPTION = """ pymcm is a library for interacting with web https://www.magiccardmarket.eu/.
For example, you can read the list of wants and add card to the cart."""

from mcm import __version__

setup(
    name="pymcm",
    version=__version__,
    description="MagicCardMarket API client",
    long_description=LONGDESCRIPTION,
    license="MIT",
    install_requires=["lxml", "requests"],
    author="Benito Rodríguez",
    author_email="brarcos@gmail.com",
    url="http://github.com/b3ni/pymcm",
    packages=find_packages(),
    keywords="mcm, magic the gathering",
    zip_safe=True
)
