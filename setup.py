#!/usr/bin/env python

import os
import sys

import threetaps

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
    version=threetaps.__version__,
    description='3taps Python API Client.',
    long_description=readme,
    author='Michael Kolodny',
    author_email='michaelckolodny@gmail.com',
    url='https://github.com/mkolodny/3taps-python-client',
    packages=['threetaps'],
    license=license,
)
