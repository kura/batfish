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
from datetime import datetime


class Image(object):
    _data = None

    def __init__(self, image_data):
        self._data = image_data

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Image {}>".format(self.name)

    @property
    def id(self):
        return self._data['id']

    @property
    def name(self):
        return self._data['name']

    @property
    def distribution(self):
        return self._data['distribution']

    @property
    def slug(self):
        return self._data['slug']

    @property
    def public(self):
        return self._data['public']

    def regions(self, client):
        return [client.region_from_slug(r['slug'] for r in self._data['region'])]

    def actions(self, client):
        j = client.get("images/{0}/actions".format(self.id))
        if 'actions' not in j:
            return None
        return [Action(a) for a in j['actions']]

    @property
    def created(self):
        return datetime.strptime(self._data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
