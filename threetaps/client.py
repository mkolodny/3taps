# -*- coding: utf-8 -*-

"""
threetaps.client
~~~~~~~~~~~~~~~~

This module provides a Threetaps object to make requests to the 3taps
api.

"""

from __future__ import unicode_literals
import inspect
import json
import calendar
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
import requests


class Threetaps(object):
    """A 3taps API wrapper."""

    __attrs__ = ['auth_token']

    def __init__(self, auth_token):

        # prepare endpoints
        self.requester = self.Requester(auth_token)

        # dynamically attach endpoints
        self._attach_endpoints()

    def _attach_endpoints(self):
        """Dynamically attach endpoints to this client."""

        for name, endpoint in inspect.getmembers(self):
            if (inspect.isclass(endpoint) and
                    issubclass(endpoint, self._Endpoint) and
                    endpoint is not self._Endpoint):
                endpoint_instance = endpoint(self.requester)
                setattr(self, endpoint.name, endpoint_instance)

    class Requester(object):
        """An API requesting object."""

        def __init__(self, auth_token):

            self.auth_token = auth_token

        def GET(self, url, params={}):
            """Make a GET request to 3taps.

            :param url: String. 3taps endpoint.
            :param params: Dictionary. Params to send to 3taps.
            """
            params['auth_token'] = self.auth_token
            response = requests.get(url, params=params)
            if response.status_code != 200:
                error = 'HTTPError: {}'.format(response.status_code)
                return {'error': error}
            try:
                return response.json()
            except ValueError as err:
                return {'error': err}


    class _Endpoint(object):
        """Base class for endpoints."""

        def __init__(self, requester):

            self.requester = requester

        def _GET(self, path='', params={}):
            """Make a GET request to the current endpoint.

            :param path: String. Path to append to the endpoint url.
            :param params: Dictionary. Params to send to 3taps.
            """
            url = urljoin(self.url, path)
            return self.requester.GET(url, params)


    class Search(_Endpoint):
        """3taps Search API endpoints."""

        name = 'search'
        url = 'http://search.3taps.com'

        def search(self, params={}):
            """Search the 3taps database of postings."""

            return self._GET(self.url, params)

        def count(self, field, params={}):
            """Count the number of postings matching a search.

            :param field: String. Field to use for calculating the count.
            """
            params['count'] = field
            return self._GET(self.url, params)


    class Polling(_Endpoint):
        """3taps Polling API endpoints."""

        name = 'polling'
        url = 'http://polling.3taps.com'

        def anchor(self, utc_dt):
            """Get the value to use to find postings since `utc_dt`.

            :param utc_dt: Datetime <datetime> object. Start-time for finding
                postings.
            """
            url = urljoin(self.url, 'anchor')

            # set anchor timestamp
            params = {'timestamp': self._timestamp_from_utc(utc_dt)}

            return self._GET(url, params)

        def poll(self, params={}):
            """Retrieve postings that have changed since the last poll."""

            url = urljoin(self.url, 'poll')
            return self._GET(url, params)

        def _timestamp_from_utc(self, utc_dt):
            """Convert a UTC datetime object to a UTC timestamp.
            Returns an Integer representing the number of seconds since the
            epoch.
            """
            return calendar.timegm(utc_dt.timetuple())


    class Reference(_Endpoint):
        """3taps Reference API endpoints."""

        name = 'reference'
        url = 'http://reference.3taps.com'

        def sources(self):
            """Get a list of 3taps data sources."""

            return self._GET('sources')

        def category_groups(self):
            """Get a list of 3taps category groups."""

            return self._GET('category_groups')

        def categories(self):
            """Get a list of 3taps categories."""

            return self._GET('categories')

        def locations(self, level, params={}):
            """Get a list of 3taps locations.

            :param level: String. The level of the desired locations.
                Options: 'country', 'state', 'metro', 'region', 'county',
                         'city', 'locality', 'zipcode'.
            """
            params['level'] = level
            return self._GET('locations', params)

        def location_lookup(self, code):
            """Get the details for a location based on the 3taps location
            code.

            :param code: String. 3taps location code.
            """
            return self._GET('locations/lookup', {'code': code})
