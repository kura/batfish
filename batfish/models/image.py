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

from .action import Action
from .region import Region


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
        """
        The image ID.

            >>> cli = batfish.Client()
            >>> image = cli.image_from_id(1234)
            >>> image.id
            1234

        :rtype: `integer`.
        """
        return self._data['id']

    @property
    def name(self):
        """
        The image name.

            >>> cli = batfish.Client()
            >>> image = cli.image_from_id(1234)
            >>> image.name
            'image-1'

        :rtype: `string`.
        """
        return self._data['name']

    @property
    def distribution(self):
        """
        The image distribution name.

            >>> cli = batfish.Client()
            >>> image = cli.image_from_id(1234)
            >>> image.distribution
            'Ubuntu 14.04'

        :rtype: `string`.
        """
        return self._data['distribution']

    @property
    def slug(self):
        """
        The image slug.

            >>> cli = batfish.Client()
            >>> image = cli.image_from_id(1234)
            >>> image.slug
            'image-1'

        :rtype: `string` or `None`.
        """
        return self._data['slug']

    @property
    def public(self):
        """
        The public status of the image.

            >>> cli = batfish.Client()
            >>> image = cli.image_from_id(1234)
            >>> image.public
            False

        :rtype: `boolean`.
        """
        return self._data['public']

    @property
    def region_names(self):
        """
        A list of region names the image is available in.

            >>> cli = batfish.Client()
            >>> image = cli.image_from_id(1234)
            >>> image.region_names
            ['Amsterdam 1', 'Amsterdam 2', 'Amsterdam 3']

        :rtype: `list`.
        """
        return [Region.name_from_slug(r) for r in self._data['regions']]

    def regions(self, client):
        """
        A list of regions the image is available in.

            >>> cli = batfish.Client()
            >>> image = cli.image_from_id(1234)
            >>> image.regions
            [<Region Amsterdam 1>, <Region Amsterdam 2>, <Region Amsterdam 3>]

        :rtype: `list` of `batfish.models.region.Region` instances.
        """
        return [client.region_from_slug(r) for r in self._data['regions']]

    @property
    def created(self):
        """
        The date and time an image was created.

            >>> cli = batfish.Client()
            >>> image = cli.image_from_id(1234)
            >>> image.created
            datetime.datetime(2014, 1, 7, 23, 19, 49)

        :rtype: `datetime.datime` object.
        """
        return datetime.strptime(self._data['created_at'],
                                 '%Y-%m-%dT%H:%M:%SZ')
