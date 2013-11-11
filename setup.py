#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.rst') as f:
    readme = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    name='threetaps',
    version=threetaps.version,
    description='3taps Python API Client.',
    long_description=readme,
    author='Michael Kolodny',
    packages=['threetaps'],
    license=license,
)
