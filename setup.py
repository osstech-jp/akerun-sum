#!/usr/bin/env python3
# -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

from setuptools import setup, find_packages
from src import __version__

__author__ = 'Shun Kawai'

setup(
  name='akerun-sum',
  version=__version__,
  description='Enter and leave data totalization program for Akerun',
  author='Shun Kawai',
  author_email='shun@isasaka.jp',
  url='https://github.com/osstech-jp/akerun-sum',
  license='GPL',
  classifiers=[
    'Environment :: Console',
    'Natural Language :: Japanese',
    'Operating System :: Microsoft :: Windows :: Windows 7',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'License :: OSI Approved :: GNU General Public License (GPL)',
  ],
  packages=find_packages(),
  include_package_data=False,
  keywords=['akerun'],
  entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    akerun-sum = akerun_sum:main
    """,
)
