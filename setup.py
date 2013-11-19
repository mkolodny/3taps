#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wininst upload')
    sys.exit()

with open('README.md') as f:
    readme = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    name='threetaps',
    version='0.1.3',
    description='3taps API Client.',
    long_description=readme,
    author='Michael Kolodny',
    author_email='michaelckolodny@gmail.com',
    url='https://github.com/mkolodny/3taps',
    packages=['threetaps'],
    package_data={'': ['LICENSE']},
    package_dir={'threetaps': 'threetaps'},
    install_requires=['requests'],
    license=license,
)
