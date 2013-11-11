#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) 2013 Michael Kolodny

"""Tests for threetaps."""

import unittest
import os
import json
import urllib
import logging
import httpretty
from mock import patch

import threetaps

AUTH_TOKEN = 'AUTH_TOKEN'
# TODO: depend on requests and httpretty for testing


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.api = threetaps.Threetaps(AUTH_TOKEN)


class RequesterTestCase(BaseTestCase):

    url = 'http://3taps.com/'
    params = {'key': 'val'}

    def test_auth_token(self):
        self.assertEqual(self.api.requester.auth_token, AUTH_TOKEN)

    def test_get_request(self):
        body = ['hi']
        httpretty.register_uri(httpretty.GET, self.url,
                               body=json.dumps(body),
                               content_type='application/json')

        response = self.api.requester.GET(self.url, self.params)

        self.assertEqual(response, body)
        querystring = {key: val[0] for key, val in
                       httpretty.last_request().querystring.items()}
        self.assertEqual(querystring, self.params)

    def test_bad_get_request(self):
        httpretty.register_uri(httpretty.GET, 'aowiefj', status=100)

        with patch('threetaps.logger.error') as logger:
            response = self.api.requester.GET(self.url, self.params)
            logger.assert_called_with('Request failed.')
        self.assertIsNone(response)

    # TODO: response isn't json


class SearchTestCase(BaseTestCase):

    def test_entry_points(self):

        self.api.search.search
        self.api.search.count


class PollingTestCase(BaseTestCase):

    def test_entry_points(self):

        self.api.polling.anchor
        self.api.polling.poll


class ReferenceTestCase(BaseTestCase):

    def test_entry_points(self):

        self.api.reference.sources
        self.api.reference.category_groups
        self.api.reference.categories
        self.api.reference.locations
        self.api.reference.location_lookup


if __name__ == '__main__':
    httpretty.enable()
    unittest.main()
    httpretty.disable()
    httpretty.reset()
