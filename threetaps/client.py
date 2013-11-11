# -*- coding: utf-8 -*-

"""
threetaps.client
~~~~~~~~~~~~~~~~

This module provides a Threetaps object to make requests to the 3taps
api.

"""

import inspect


class Threetaps(object):
    """A 3taps API wrapper."""

    __attrs__ = [
        'auth_token']

    def __init__(self, auth_token):

        # 3taps API auth token
        self.auth_token = auth_token

        # dynamically attach endpoints
        self._attach_endpoints()

    def _attach_endpoints(self):
        """Dynamically attach endpoints to this client."""

        for name, endpoint in inspect.getmembers(self):
            if inspect.isclass(endpoint) \
                    and issubclass(endpoint, self._Endpoint) \
                    and (endpoint is not self._Endpoint):
                setattr(self, endpoint.name, endpoint)

    class _Endpoint(object):
        """Base class for endpoints."""


    class Search(_Endpoint):
        """3taps Search API endpoints.

        Logical Operators:
          >>> catagory = 'SBIK'
          >>> category = 'SBIK|SCAR|STRU' # OR
          >>> category = '~SBIK' # NOT

        Text Operators:
          >>> heading = 'big bike' # contain
          >>> heading = '"big bike"' # contain exact
          >>> heading = 'big|bike' # OR
          >>> heading = '"big bike"&blue' # AND
          >>> heading = '~"big bike"' # NOT
          >>> heading = '"big bike"&~"trek superfly"' # combine searches

        Radius-Based Searches:
        Simply supply the parameters `lat`, `long`, `radius` to find all
        postings within a given radius from a geographic point.
        """

        name = 'search'

        def search():
            """Search the 3taps database of postings."""

        def count():
            """Count the number of postings matching a search."""


    class Polling(_Endpoint):
        """3taps Polling API endpoints."""

        name = 'polling'

        def anchor():
            """Find the value to use to find postings since a given time."""

        def poll():
            """Retrieve postings that have changed since the last poll."""


    class Reference(_Endpoint):
        """3taps Reference API endpoints."""

        name = 'reference'

        def sources():
            """Get a list of 3taps data sources."""

        def category_groups():
            """Get a list of 3taps category groups."""

        def categories():
            """Get a list of 3taps categories."""

        def locations():
            """Get a list of 3taps locations."""

        def location_lookup():
            """Get the details for a location based on the 3taps location code."""
