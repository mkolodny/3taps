# -*- coding: utf-8 -*-

"""
threetaps.client
~~~~~~~~~~~~~~~~

This module provides a Threetaps object to make requests to the 3taps
api.

"""

import inspect
import json
import urllib
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


class Threetaps(object):
    """A 3taps API wrapper."""

    __attrs__ = [
        'auth_token']

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
                endpoint_instance = endpoint()
                setattr(self, endpoint.name, endpoint_instance)

    class Requester(object):
        """An API requesting object."""

        def __init__(self, auth_token):

            self.auth_token = auth_token

        def GET(self, url, params):
            """Make a GET request to 3taps.

            :param url: String. 3taps endpoint.
            :param params: Dictionary. Params to send to 3taps.
            """
            params['auth_token'] = self.auth_token
            full_url = '{}?{}'.format(url, urllib.urlencode(params))
            connection = urllib.urlopen(full_url)
            if not 200 <= connection.code < 300:
                logger.error('Request failed.')
                return None
            response = connection.read()
            connection.close()
            return json.loads(response)


    class _Endpoint(object):
        """Base class for endpoints."""

        # TODO: self.requester


    class Search(_Endpoint):
        """3taps Search API endpoints."""

        name = 'search'

        def search(self):
            """Search the 3taps database of postings."""

        def count(self):
            """Count the number of postings matching a search.
            Returns :class:`Count <Count>` object.

            :param field: String. Field to use for calculating the count.
            """


    class Polling(_Endpoint):
        """3taps Polling API endpoints."""

        name = 'polling'

        def anchor(self):
            """Find the value to use to find postings since a given time."""

        def poll(self):
            """Retrieve postings that have changed since the last poll."""


    class Reference(_Endpoint):
        """3taps Reference API endpoints."""

        name = 'reference'

        def sources(self):
            """Get a list of 3taps data sources."""

        def category_groups(self):
            """Get a list of 3taps category groups."""

        def categories(self):
            """Get a list of 3taps categories."""

        def locations(self):
            """Get a list of 3taps locations."""

        def location_lookup(self):
            """Get the details for a location based on the 3taps location code."""
