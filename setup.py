#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from distutils.core import setup

required = []

setup(
        name='monitor',
        version='0.0.1',
        description='Python Library for monitoring devices',
        long_description=open('README.rst').read() + '\n\n' +
                         open('HISTORY.rst').read(),
        author='tigeroses',
        author_email='me@tigeroses.com',
        usr='https://github.com/tigerRose/monitor',
        packages=[
                'monitor',
        ],
        install_requires=required,
        license='ISC',
        classifiers=(
            'Intended Audience :: Developers',
            'Natural Language :: Chinese, English',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
        ),
)
