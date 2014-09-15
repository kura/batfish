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


class Region(object):
    _data = None
    mapping = {'ams1': 'Amsterdam 1', 'ams2': 'Amsterdam 2',
               'ams3': 'Amsterdam 3', 'lon1': 'London 1',
               'nyc1': 'New York 1', 'nyc2': 'New York 2',
               'nyc3': 'New York 3', 'sfo1': 'San Fancisco 1',
               'sgp1': 'Singapore 1'}

    def __init__(self, region_data):
        self._data = region_data

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Region {0}>".format(self.name)

    @staticmethod
    def mappings():
        return Region.mapping

    @staticmethod
    def name_from_slug(slug):
        if slug not in Region.mapping:
            return "Unknown"
        else:
            return Region.mapping[slug]

    @property
    def slug(self):
        return self._data['slug']

    @property
    def name(self):
        return self._data['name']

    @property
    def sizes(self):
        return self._data['sizes']

    @property
    def available(self):
        return self._data['available']

    @property
    def features(self):
        return self._data['features']
