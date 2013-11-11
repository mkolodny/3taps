#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) 2013 Michael Kolodny

"""Tests for threetaps."""

import unittest
import os

import threetaps

AUTH_TOKEN = 'AUTH_TOKEN'


class BaseTestCase(unittest.TestCase):


    def setUp(self):
        self.api = threetaps.Threetaps(AUTH_TOKEN)


class APIWrapperTestCase(BaseTestCase):

    def test_auth_token(self):
        self.api.auth_token = AUTH_TOKEN


class SearchTestCase(BaseTestCase):

    def test_entry_points(self):

        self.api.search.search
        self.api.search.count


class SearchTestCase(BaseTestCase):

    def test_entry_points(self):

        self.api.polling.anchor
        self.api.polling.poll


class SearchTestCase(BaseTestCase):

    def test_entry_points(self):

        self.api.reference.sources
        self.api.reference.category_groups
        self.api.reference.categories
        self.api.reference.locations
        self.api.reference.location_lookup


if __name__ == '__main__':
    unittest.main()
