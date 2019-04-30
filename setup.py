#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""8chan/vichan Python Library.

py8chan is a Python library that gives access to the 8chan/vichan API
and an object-oriented way to browse and get board and thread
information quickly and easily.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
the LICENSE file for more details.
"""

from setuptools import setup

setup(
    name='py8chan',
    version='0.1.1',
    description=("Python 8chan/vichan API Wrapper. Based on BASC-py4chan by the Bbiliotheca Anonoma"),
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    author='Antonizoon',
    author_email='antonizoon@bibanon.org',
    url='http://github.com/bibanon/py8chan',
    packages=['py8chan'],
    package_dir={
        'py8chan': 'py8chan',
    },
    package_data={'': ['README.rst', 'LICENSE']},
    install_requires=['requests >= 1.0.0'],
    keywords='8chan api vichan',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
