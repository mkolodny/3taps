#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) 2013 Michael Kolodny

"""Tests for threetaps."""

from __future__ import unicode_literals
import unittest
import os
import json
import httpretty

import threetaps

AUTH_TOKEN = 'AUTH_TOKEN'


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.api = threetaps.Threetaps(AUTH_TOKEN)

        # default params
        self.params = {'auth_token': AUTH_TOKEN}

        # default http response body
        self.body = '[]'
        self.jbody = json.dumps(self.body)

        # mock http requests
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, self.uri,
                               body=self.jbody)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()


def get_last_query():
    return {key: val[0] for key, val in
            httpretty.last_request().querystring.items()}

class RequesterTestCase(BaseTestCase):

    def setUp(self):
        self.uri = 'http://3taps.com/'

        super(RequesterTestCase, self).setUp()

    def test_auth_token(self):
        self.assertEqual(self.api.requester.auth_token, AUTH_TOKEN)

    def test_get_request(self):
        response = self.api.requester.GET(self.uri, self.params)

        self.assertEqual(response, self.body)
        self.assertEqual(get_last_query(), self.params)

    def test_bad_get_request(self):
        # mock bad status code
        status = 302
        httpretty.reset()
        httpretty.register_uri(httpretty.GET, self.uri,
                               body=self.jbody,
                               status=status)

        response = self.api.requester.GET(self.uri, self.params)
        self.assertIn('error', response)

    def test_response_not_json(self):
        # mock html response
        httpretty.reset()
        httpretty.register_uri(httpretty.GET, self.uri,
                               body='<html></html>')

        response = self.api.requester.GET(self.uri, self.params)
        self.assertIn('error', response)

class SearchTestCase(BaseTestCase):

    def setUp(self):
        self.uri = 'http://search.3taps.com'

        super(SearchTestCase, self).setUp()

    def test_entry_points(self):

        self.api.search.search
        self.api.search.count

    def test_search_defaults(self):
        response = self.api.search.search()

        self.assertEqual(response, self.body)
        self.assertEqual(get_last_query(), self.params)

    def test_search_query(self):
        self.params['id'] = '234567'

        response = self.api.search.search(self.params)

        self.assertEqual(response, self.body)
        self.assertEqual(get_last_query(), self.params)

    def test_count_defaults(self):
        count_field = 'source'

        response = self.api.search.count(count_field)
        self.assertEqual(response, self.body)

        # field should be included in the params
        self.params['count'] = count_field
        self.assertEqual(get_last_query(), self.params)

    def test_count_query(self):
        self.params['id'] = 1234567
        count_field = 'source'

        response = self.api.search.count(count_field,
                                         params=self.params)
        self.assertEqual(response, self.body)


class PollingTestCase(BaseTestCase):

     def setUp(self):
        self.uri = 'http://polling.3taps.com'

        super(PollingTestCase, self).setUp()

     def test_entry_points(self):

        self.api.polling.anchor
        self.api.polling.poll


class ReferenceTestCase(BaseTestCase):

     def setUp(self):
        self.uri = 'http://reference.3taps.com/sources'

        super(ReferenceTestCase, self).setUp()

     def test_entry_points(self):

        self.api.reference.sources
        self.api.reference.category_groups
        self.api.reference.categories
        self.api.reference.locations
        self.api.reference.location_lookup


if __name__ == '__main__':
    unittest.main()
