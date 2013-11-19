3taps
=====

A Python interface for the 3taps API.

The goal of this library is to map 3taps' endpoints one-to-one with clean, Pythonic methods. It only handles raw data, allowing you to define your own models.

Dependencies:

- requests


Installation
------------

Install via pip:

.. code-block:: bash

    $ pip install threetaps

Install from source:

.. code-block:: bash

    $ git clone https://github.com/mkolodny/3taps.git
    $ cd 3taps
    $ python setup.py install


Usage
-----

Instantiating a client:

.. code-block:: bash

    >>> client = threetaps.Threetaps('YOUR_API_KEY')


Examples
--------

`Reference`_

Sources:

.. code-block:: pycon

    >>> client.reference.sources()

Category Groups:

.. code-block:: pycon

    >>> client.reference.category_groups()

Categories:

.. code-block:: pycon

    >>> client.reference.categories()

Locations:

.. code-block:: pycon

    >>> client.reference.locations('locality', params={'city': 'USA-NYM-NEY'})

Locations Lookup:

.. code-block:: pycon

    >>> client.reference.location_lookup('CAN-YUL')

.. _Reference: http://docs.3taps.com/reference_api.html

----

`Search`_

Search:

.. code-block:: pycon

    >>> client.search.search(params={'location.city': 'USA-NYM-NEY'})

Count:

.. code-block:: pycon

    >>> client.search.count('category', params={'status': 'for_sale'})

.. _Search: http://docs.3taps.com/search_api.html

----

`Polling`_

Anchor:

.. code-block:: pycon

    >>> utc_dt = datetime.today()
    >>> client.polling.anchor(utc_dt)

Poll:

.. code-block:: pycon

    >>> client.polling.poll(params={'anchor': '306785687'})

.. _Polling: http://docs.3taps.com/polling_api.html
