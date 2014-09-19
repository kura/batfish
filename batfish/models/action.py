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


from datetime import datetime

from .region import Region


class Action(object):
    """
    A Digital Ocean action.

    :param action_data: A dictionary of action data from the API.
    """
    _data = None

    def __init__(self, action_data):
        self._data = action_data

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Action {0}>".format(self.type)

    @property
    def id(self):
        """
        The ID of the action.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.actions[0].id
            1234

        :rtype: `integer`
        """
        return self._data['id']

    @property
    def status(self):
        """
        The status of the action.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.actions[0].status
            'completed'

        :rtype: `string`.
        """
        return self._data['status']

    @property
    def type(self):
        """
        The type of action.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.actions[0].type
            'rebuild'

        :rtype: `string`.
        """
        return self._data['type']

    @property
    def started(self):
        """
        The date and time the action was started.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.actions[0].started
            datetime.datetime(2014, 1, 7, 23, 19, 49)

        :rtype: `datetime.datetime` object.
        """
        return datetime.strptime(self._data['started_at'],
                                 '%Y-%m-%dT%H:%M:%SZ')

    @property
    def completed(self):
        """
        The date and time the action was completed.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.actions[0].completed
            datetime.datetime(2014, 1, 7, 23, 19, 49)

        :rtype: `datetime.datetime` object, `None` if not completed.
        """
        if self._data['completed_at'] is None:
            return None
        return datetime.strptime(self._data['completed_at'],
                                 '%Y-%m-%dT%H:%M:%SZ')

    @property
    def resource_id(self):
        """
        The ID of the resource the action was done on.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.actions[0].resource_id
            3

        :rtype: `integer`.
        """
        return self._data['resource_id']

    @property
    def resource_type(self):
        """
        The type of the resource the action was done on.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.actions[0].resource_type
            'droplet'

        :rtype: `string`.
        """
        return self._data['resource_type']

    def region(self, client):
        """
        The region the action was done in.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.actions[0].region
            <Region Amsterdam 2>

        :rtype: An instance `of batfish.models.region.Region`.
        """
        return client.region_from_slug(self._data['region']['slug'])

    def region_name(self, client):
        """
        The region name the action was done in.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.actions[0].region_name
            'Amsterdam 2'

        :rtype: `string`.
        """
        return Region.name_from_slug(self._data['region']['slug'])
