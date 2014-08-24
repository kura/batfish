# -*- coding: utf-8 -*-

# (The MIT License)
#
# Copyright (c) 2014 Kura
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from collections import namedtuple

from .region import Region


class Size(object):
    _data = None
    mapping = ('512MB', '1GB', '2GB', '4GB', '8GB', '16GB', '32GB',
               '48GB', '64GB')

    def __init__(self, size_data):
        self._data = size_data

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Size {0}>".format(self.slug.upper())

    @staticmethod
    def mappings():
        return Size.mapping

    @property
    def slug(self):
        return self._data['slug']

    @property
    def memory(self):
        return self._data['memory']

    @property
    def cpus(self):
        return self._data['vcpus']

    @property
    def disk_size(self):
        return "{0}GB".format(self._data['disk'])

    @property
    def transfer(self):
        return "{0}TB".format(self._data['transfer'])

    @property
    def price(self):
        price = namedtuple("Price", "hourly monthly")
        return price(hourly=self._data['price_hourly'],
                     monthly=self._data['price_monthly'])

    @property
    def region_names(self):
        return [Region.name_from_slug(r) for r in self._data['regions']]

    def regions(self, client):
        return [client.region_from_slug(r) for r in self._data['regions']]
