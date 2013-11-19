3taps
=====

 A Python interface for the 3taps API.

 The goal of this library is to map 3taps' endpoints one-to-one with clean, Pythonic methods. It only handles raw data, allowing you to define your own models.

 Dependencies:

 - requests


Installation
____________

Install via pip:

    $ pip install threetaps

Install from source:

    $ git clone https://github.com/mkolodny/3taps.git
    $ cd 3taps
    $ python setup.py install


Usage
_____

Instantiating a client:

    client = threetaps.Threetaps(auth_token='YOUR_API_KEY')


Examples
________

### [Reference](http://docs.3taps.com/reference_api.html)

#### Sources

    client.reference.sources()

#### Category Groups

    client.reference.category_groups()

#### Categories

    client.reference.categories()

#### Locations

    client.reference.locations('locality', params={'city': 'USA-NYM-NEY'})

#### Locations Lookup

    client.reference.location_lookup('CAN-YUL')


### [Search](http://docs.3taps.com/reference_api.html)

#### Search

    client.search.search(params={'location.city': 'USA-NYM-NEY'})

#### Count

    client.search.count('category', params={'status': 'for_sale'})


### [Polling](http://docs.3taps.com/polling_api.html)

#### Anchor

    utc_dt = datetime.today()
    client.polling.anchor(utc_dt)

#### Poll

    client.polling.poll(params={'anchor': '306785687'})
