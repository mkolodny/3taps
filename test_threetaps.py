#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) 2013 Michael Kolodny

"""Tests for threetaps."""

from __future__ import unicode_literals
import unittest
import os
import json
from datetime import datetime
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
import httpretty

import threetaps

AUTH_TOKEN = 'AUTH_TOKEN'


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.api = threetaps.Threetaps(AUTH_TOKEN)

        # default params
        self.params = {'auth_token': AUTH_TOKEN}

        # default http response body
        self.body = []
        self.jbody = json.dumps(self.body)

        # mock http requests
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, self.uri,
                               body=self.jbody)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def get_last_query(self):
        return {key: val[0] for key, val in
                httpretty.last_request().querystring.items()}

    def register_uri(self, uri):
        uri = urljoin(self.uri, uri)
        httpretty.reset()
        httpretty.register_uri(httpretty.GET, uri,
                               body=self.jbody)


class RequesterTestCase(BaseTestCase):

    def setUp(self):
        self.uri = 'http://3taps.com/'

        super(RequesterTestCase, self).setUp()

    def test_auth_token(self):
        self.assertEqual(self.api.requester.auth_token, AUTH_TOKEN)

    def test_get_request(self):
        response = self.api.requester.GET(self.uri, self.params)

        self.assertEqual(response, self.body)
        self.assertEqual(self.get_last_query(), self.params)

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
        self.assertEqual(self.get_last_query(), self.params)

    def test_search_query(self):
        self.params['id'] = '234567'

        response = self.api.search.search(self.params)

        self.assertEqual(response, self.body)
        self.assertEqual(self.get_last_query(), self.params)

    def test_count_defaults(self):
        count_field = 'source'

        response = self.api.search.count(count_field)
        self.assertEqual(response, self.body)

        # field should be included in the params
        self.params['count'] = count_field
        self.assertEqual(self.get_last_query(), self.params)

    def test_count_query(self):
        self.params['id'] = 1234567
        count_field = 'source'

        response = self.api.search.count(count_field,
                                         params=self.params)
        self.assertEqual(response, self.body)

    # TODO: get next page


class PollingTestCase(BaseTestCase):

    def setUp(self):
        self.uri = 'http://polling.3taps.com'

        super(PollingTestCase, self).setUp()

    def test_entry_points(self):

        self.api.polling.anchor
        self.api.polling.poll

    def test_anchor(self):
        # mock the request
        self.register_uri('anchor')

        timestamp = 1384365735
        utc_date = datetime.utcfromtimestamp(timestamp)
        response = self.api.polling.anchor(utc_date)

        # response
        self.assertEqual(response, self.body)

        # timestamp should be included in the params
        self.params['timestamp'] = str(timestamp)
        self.assertEqual(self.get_last_query(), self.params)

    def test_poll_defaults(self):
        # mock the request
        self.register_uri('poll')

        response = self.api.polling.poll()

        # response
        self.assertEqual(response, self.body)

        # request
        self.assertEqual(self.get_last_query(), self.params)

    def test_poll_query(self):
        # mock the request
        self.register_uri('poll')

        # query
        params = {'anchor': 'awoiefj'}

        response = self.api.polling.poll(params)

        # response
        self.assertEqual(response, self.body)

        # the query should be added to the request
        self.params['anchor'] = params['anchor']
        self.assertEqual(self.get_last_query(), self.params)


class ReferenceTestCase(BaseTestCase):

    def setUp(self):
        self.uri = 'http://reference.3taps.com'

        super(ReferenceTestCase, self).setUp()

    def test_entry_points(self):

        self.api.reference.sources
        self.api.reference.category_groups
        self.api.reference.categories
        self.api.reference.locations
        self.api.reference.location_lookup

    def test_reference_sources(self):
        # mock the request
        self.register_uri('sources')

        response = self.api.reference.sources()

        # response
        self.assertEqual(response, self.body)

    def test_reference_category_groups(self):
        # mock the request
        self.register_uri('category_groups')

        response = self.api.reference.category_groups()

        # response
        self.assertEqual(response, self.body)

    def test_reference_categories(self):
        # mock the request
        self.register_uri('categories')

        response = self.api.reference.categories()

        # response
        self.assertEqual(response, self.body)

    def test_reference_locations_defaults(self):
        # mock the request
        self.register_uri('locations')

        level = 'country'
        response = self.api.reference.locations(level)

        # response
        self.assertEqual(response, self.body)

        # request
        self.params['level'] = level
        self.assertEqual(self.get_last_query(), self.params)

    def test_reference_locations_query(self):
        # mock the request
        self.register_uri('locations')

        # query
        params = {'country': 'awfeaw'}

        level = 'country'
        response = self.api.reference.locations(level, params)

        # response
        self.assertEqual(response, self.body)

        # request
        self.params['level'] = level
        self.params['country'] = params['country']
        self.assertEqual(self.get_last_query(), self.params)

    def test_reference_location_lookup_defaults(self):
        # mock the request
        self.register_uri('location/lookup')

        code = 'oaiwjef'
        response = self.api.reference.location_lookup(code)

        # response
        self.assertEqual(response, self.body)

        # request
        self.params['code'] = code
        self.assertEqual(self.get_last_query(), self.params)


if __name__ == '__main__':
    unittest.main()
