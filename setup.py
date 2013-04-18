#!/usr/bin/env python
from setuptools import setup, find_packages

LONGDESCRIPTION = """ pymcm is a library for interacting with web https://www.magiccardmarket.eu/.
For example, you can read the list of wants and add card to the cart."""

setup(
    name="pymcm",
    version="0.0.2",
    description="MagicCardMarket API client",
    long_description=LONGDESCRIPTION,
    license="MIT",
    install_requires=["lxml", "mechanize"],
    author="Benito Rodríguez",
    author_email="brarcos@gmail.com",
    url="http://github.com/b3ni/pymcm",
    packages=find_packages(),
    keywords="mcm",
    zip_safe=True
)
