#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="pymcm",
    version="0.0.1",
    description="MagicCardMarket API client",
    license="MIT",
    install_requires=["lxml", "mechanize"],
    author="Benito Rodríguez",
    author_email="brarcos@gmail.com",
    url="http://github.com/b3ni/pymcm",
    packages=find_packages(),
    keywords="mcm",
    zip_safe=True
)
