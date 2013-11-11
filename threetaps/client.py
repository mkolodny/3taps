# -*- coding: utf-8 -*-

"""
threetaps.client
~~~~~~~~~~~~~~~~

This module provides a Threetaps object to make requests to the 3taps
api.

"""


class Threetaps(object):
    """A 3taps API wrapper."""

    __attrs__ = [
        'auth_token']

    def __init__(self, auth_token):

        # 3taps API auth token
        self.auth_token = auth_token

    class Search(object):
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

        def search():
            """Search the 3taps database of postings."""

        def count():
            """Count the number of postings matching a search."""


    class Polling(object):
        """3taps Polling API endpoints."""

        def anchor():
            """Find the value to use to find postings since a given time."""

        def poll():
            """Retrieve postings that have changed since the last poll."""


    class Reference(object):
        """3taps Reference API endpoints."""

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
