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


import json
import os
import re

import requests

from batfish.__about__ import __title__, __version__
from .models import Droplet, Image, Region, Size


valid_chars = re.compile(r"^[a-zA-Z0-9\.\-]*$")


def read_token_from_conf():
    if not os.path.exists(os.path.expanduser('~/.batfish')):
        return None
    with open(os.path.expanduser('~/.batfish')) as f:
        return f.read()


def write_token_to_conf(token):
    with open(os.path.expanduser('~/.batfish'), 'w') as f:
        f.write(token)


class Client(object):
    """A Digital Ocean V2 client wrapper."""

    token = None
    """API authentication token."""
    api_base = "https://api.digitalocean.com/v2/"
    """API URL."""
    ua = "{0} ({1})".format(__title__.title(), __version__)
    """Default User-Agent header."""

    def __init__(self):
        token = read_token_from_conf()
        if token is not None:
            self.token = token

    def get(self, url, headers=None):
        """
        Send a GET request to the specified URL.

            >>> cli = batfish.Client()
            >>> cli.get("droplets", {'Custom-Header': "Something, something"})
            {'response': "Nothing", 'reason': "Meh."}

        :param url: URI part to query.
        :param headers: Dictionary of headers to send.
        :rtype: Dictionary of the JSON response.
        """
        if headers is None:
            headers = {'Authorization': "Bearer {0}".format(self.token)}
        headers['User-Agent'] = self.ua
        r = requests.get("{0}{1}".format(self.api_base, url), headers=headers)
        r.raise_for_status()
        return json.loads(r.text)

    def post(self, url, payload):
        """
        Send a POST request to the specified URL with the payload.

            >>> cli = batfish.Client()
            >>> cli.post("droplets", {'droplet': 123456})
            {'response': "Nothing", 'reason': "Meh."}

        :param url: URI part to query.
        :param payload: Dictionary of payload data.
        :rtype: Dictionary of the JSON response.
        """
        headers = {'Authorization': "Bearer {0}".format(self.token),
                   'User-Agent': self.ua,
                   'Content-Type': "application/json"}
        r = requests.post("{0}{1}".format(self.api_base, url),
                          headers=headers, data=json.dumps(payload))
        return json.loads(r.text)

    def put(self, url, payload):
        """
        Send a PUT request to the specified URL with the payload.

            >>> cli = batfish.Client()
            >>> cli.put("droplets", {'droplet': 123456})
            {'response': "Nothing", 'reason': "Meh."}

        :param url: URI part to query.
        :param payload: Dictionary of payload data.
        :rtype: Dictionary of the JSON response.
        """
        headers = {'Authorization': "Bearer {0}".format(self.token),
                   'User-Agent': self.ua,
                   'Content-Type': "application/json"}
        r = requests.put("{0}{1}".format(self.api_base, url),
                         headers=headers, data=json.dumps(payload))
        return json.loads(r.text)

    def delete(self, url):
        """
        Send a DELETE request to the specified URL.

            >>> cli = batfish.Client()
            >>> cli.delete("droplet/123456")

        :param url: URI part to query.
        """
        headers = {'Authorization': "Bearer {0}".format(self.token),
                   'User-Agent': self.ua,}
        r = requests.delete("{0}{1}".format(self.api_base, url),
                            headers=headers)

    def authorize(self, token):
        """
        Authorize the provided API token with the server.

            >>> cli = batfish.Client()
            >>> cli.authorize('abcdefghijkl1234567890')
            OK

        :param token: String token
        :rtype: String "OK" or raise an exception on error.
        """
        h = {'Authorization': "Bearer {0}".format(token)}
        try:
            r = self.get('actions', headers=h)
        except requests.HTTPError as e:
            raise e
        write_token_to_conf(token)
        self.token = token
        return "OK"

    @property
    def droplets(self):
        """
        Get a list of `batfish.models.Droplet` objects.

            >>> cli = batfish.Client()
            >>> cli.droplets()
            [<Droplet droplet-1>, <Droplet droplet-2>, <Droplet droplet-3>]

        :rtype: List of `batfish.models.Droplet` objects.
        """
        j = self.get('droplets')
        if 'droplets' not in j:
            return None
        return [Droplet(d) for d in j['droplets']]

    def droplet_from_id(self, droplet_id):
        """
        Get an instance `batfish.models.Droplet` for the provided droplet ID.

            >>> cli = batfish.Client()
            >>> cli.droplet_from_id(123456)
            <Droplet droplet-1>

        :param droplet_id: Integer represenation of the droplet ID.
        :rtype: Instance of `batfish.models.Droplet` or None.
        """
        url = "droplets/{0}".format(droplet_id)
        try:
            j = self.get(url)
        except requests.HTTPError as e:
            if e.message.startswith('404'):
                return None
            else:
                raise
        if 'droplet' not in j:
            return None
        return Droplet(j['droplet'])

    def droplet_from_name(self, name):
        """
        Get an instance `batfish.models.Droplet` for the provided droplet name.

            >>> cli = batfish.Client()
            >>> cli.droplet_from_name("droplet-1")
            <Droplet droplet-1>

        :param droplet_id: Name of the droplet to query.
        :rtype: Instance of `batfish.models.Droplet` or None.
        """
        j = self.get('droplets')
        if 'droplets' not in j:
            return None
        for d in j['droplets']:
            if d['name'].lower().startswith(name.lower()):
                return Droplet(d)
        return None

    def simple_droplet_image_action(self, action, droplet, image):
        """
        Send an API request to modify a droplet based on an image.

            >>> cli = batfish.Client()
            >>> cli.simple_droplet_image_action("restore", 123456, 98765)
            {'response': "Nothing", 'reason': "Meh."}

        :param action: The action to perform (restore, rebuild)
        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :param image: The image to use, either an image ID or an
                      instance of `batfish.models.Image`.
        :rtype: Dictionary of the JSON response.
        """
        if action not in ['restore', 'rebuild', ]:
            raise NotImplemented
        if isinstance(droplet, Droplet):
            droplet = droplet.id
        if isinstance(image, Image):
            image = image.id
        print self.post('droplets/{0}/actions'.format(droplet),
                        {'type': action, 'image': image})

    def simple_droplet_action(self, action, droplet):
        """
        Send an API request to modify a droplet based on the action.

            >>> cli = batfish.Client()
            >>> cli.simple_droplet_action("reboot", 123456)
            {'response': "Nothing", 'reason': "Meh."}

        :param action: The action to perform ('reboot', 'power_cycle',
                       'power_off', 'enable_ipv6', 'power_on',
                       'password_reset', 'shutdown', 'disable_backups',
                       'enable_private_networking')
        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :rtype: Dictionary of the JSON response.
        """
        if action not in ['reboot', 'power_cycle', 'power_off', 'enable_ipv6',
                          'power_on', 'password_reset', 'shutdown',
                          'disable_backups', 'enable_private_networking', ]:
            raise NotImplemented()
        if isinstance(droplet, Droplet):
            droplet = droplet.id
        print self.post('droplets/{0}/actions'.format(droplet),
                        {'type': action})

    def droplet_rename(self, droplet, name):
        """
        Send an API request to rename a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_rename(123456, "kura-test")
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :param name: A string of the new name.
        :rtype: Dictionary of the JSON response.
        """
        if isinstance(droplet, Droplet):
            droplet = droplet.id
        if not valid_chars.match(name):
            raise ValueError("""Only valid characters are allowed. """
                             """(a-z, A-Z, 0-9, . and -)""")
        print self.post('droplets/{0}/actions'.format(droplet),
                        {'type': 'rename', 'name': name})

    def droplet_snapshot(self, droplet, name):
        """
        Send an API request to snapshot a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_snapshot(123456, "kura-test")
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :param name: A string of the snapshot name.
        :rtype: Dictionary of the JSON response.
        """
        if isinstance(droplet, Droplet):
            droplet = droplet.id
        if not valid_chars.match(name):
            raise ValueError("""Only valid characters are allowed. """
                             """(a-z, A-Z, 0-9, . and -)""")
        print self.post('droplets/{0}/actions'.format(droplet),
                        {'type': 'snapshot', 'name': name})

    def droplet_resize(self, droplet, size):
        """
        Send an API request to resize a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_resize(123456, "512MB")
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :param size: A size to resize to, either a string or an instance of
                     `batfish.models.Size`.
        :rtype: Dictionary of the JSON response.
        """
        if isinstance(droplet, Droplet):
            droplet = droplet.id
        if isinstance(size, Size):
            size = size.slug
        print self.post('droplets/{0}/actions'.format(droplet),
                        {'type': 'resize', 'size': size})

    def droplet_restore(self, droplet, image):
        """
        Send an API request to restore a droplet from an image.

            >>> cli = batfish.Client()
            >>> cli.droplet_restore(123456, 9087765)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :param image: An image ID, slug or an instance of
                      `batfish.models.Image`.
        :rtype: Dictionary of the JSON response.
        """
        self.simple_droplet_image_action('restore', droplet, image)

    def droplet_rebuild(self, droplet, image):
        """
        Send an API request to rebuild a droplet from an image.

            >>> cli = batfish.Client()
            >>> cli.droplet_rebuild(123456, 9087765)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :param image: An image ID, slug or an instance of
                      `batfish.models.Image`.
        :rtype: Dictionary of the JSON response.
        """
        self.simple_droplet_image_action('rebuild', droplet, image)

    def droplet_enable_ipv6(self, droplet):
        """
        Send an API request to enable IPv6 on a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_enable_ipv6(123456)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :rtype: Dictionary of the JSON response.
        """
        self.simple_droplet_action('enable_ipv6', droplet)

    def droplet_disable_backups(self, droplet):
        """
        Send an API request to disable backups for a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_disable_backups(123456)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :rtype: Dictionary of the JSON response.
        """
        self.simple_droplet_action('disable_backups', droplet)

    def droplet_enable_private_networking(self, droplet):
        """
        Send an API request to enable private networking on a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_enable_private_networking(123456)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :rtype: Dictionary of the JSON response.
        """
        self.simple_droplet_action('enable_private_networking', droplet)

    def droplet_reboot(self, droplet):
        """
        Send an API request to reboot a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_reboot(123456)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :rtype: Dictionary of the JSON response.
        """
        self.simple_droplet_action('reboot', droplet)

    def droplet_power_cycle(self, droplet):
        """
        Send an API request to power cycle a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_power_cycle(123456)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :rtype: Dictionary of the JSON response.
        """
        self.simple_droplet_action('power_cycle', droplet)

    def droplet_power_off(self, droplet):
        """
        Send an API request to power off a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_power_off(123456)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :rtype: Dictionary of the JSON response.
        """
        self.simple_droplet_action('power_off', droplet)

    def droplet_power_on(self, droplet):
        """
        Send an API request to power on a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_power_on(123456)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :rtype: Dictionary of the JSON response.
        """
        self.simple_droplet_action('power_on', droplet)

    def droplet_password_reset(self, droplet):
        """
        Send an API request to reset the root password of a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_password_reset(123456)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :rtype: Dictionary of the JSON response.
        """
        self.simple_droplet_action('password_reset', droplet)

    def droplet_shutdown(self, droplet):
        """
        Send an API request to shutdown a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_shutdown(123456)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :rtype: Dictionary of the JSON response.
        """
        self.simple_droplet_action('shutdown', droplet)

    def droplet_delete(self, droplet):
        """
        Send an API request to delete a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_delete(123456)
            {'response': "Nothing", 'reason': "Meh."}

        :param droplet: The droplet to modify, either a droplet ID or an
                        instance of `batfish.models.Droplet`.
        :rtype: Dictionary of the JSON response.
        """
        if isinstance(droplet, Droplet):
            droplet = droplet.id
        print self.delete('droplets/{0}'.format(droplet))

    def droplet_create(self, name, region, size, image):
        """
        Send an API request to create a droplet.

            >>> cli = batfish.Client()
            >>> cli.droplet_power_off('kura-new', 'ams2', '512MB', 908765)
            {'response': "Nothing", 'reason': "Meh."}

        :param name: The name of the new droplet.
        :param region: The region to create the droplet in. Accepts a name,
                       slug or an instance of `batfish.models.Region`.
        :param size: The size of the new droplet. Accepts a slug or instance
                     of `batfish.models.Size`.
        :param image: An image to build the droplet from. Accepts a name, slug
                      or an instance of `batfish.models.Image`.
        :rtype: Dictionary of the JSON response.
        """
        if isinstance(size, Size):
            size = size.slug
        if isinstance(image, Image):
            image = image.id
        if isinstance(region, Region):
            region = region.slug
        if not image.isdigit():
            image = image.lower()
        if not valid_chars.match(name):
            raise ValueError("""Only valid characters are allowed. """
                             """(a-z, A-Z, 0-9, . and -)""")
        d = {'name': name, 'size': size.lower(), 'image': image,
             'region': region}
        print self.post('droplets', d)

    @property
    def images(self):
        """
        Get a list of images from the API.

            >>> cli = batfish.Client()
            >>> cli.images
            [<Image test1>, <Image test2>]

        :rtype: List of `batfish.models.Image` objects.
        """
        j = self.get('images')
        if 'images' not in j:
            return None
        return [Image(i) for i in j['images']]

    def image_from_id(self, image_id):
        """
        Get an instance of `batfish.models.Image` for the provided image ID.

            >>> cli = batfish.Client()
            >>> cli.image_from_id(12345)
            <Image test1>

        :param image_id: An integer ID of an image.
        :rtype: An instance of `batfish.models.Image`.
        """
        url = "images/{0}".format(image_id)
        j = self.get(url)
        if 'image' not in j:
            return None
        return Image(j['image'])

    def image_from_name(self, name):
        """
        Get an instance of `batfish.models.Image` for the provided image name.

            >>> cli = batfish.Client()
            >>> cli.image_from_name('test1')
            <Image test1>

        :param name: A string name of an image.
        :rtype: An instance of `batfish.models.Image`.
        """
        j = self.get('images')
        if 'images' not in j:
            return None
        for i in j['images']:
            if i['name'].lower().startswith(name.lower()):
                return Image(i)
        return None

    def image_from_slug(self, slug):
        """
        Get an instance of `batfish.models.Image` for the provided image slug.

            >>> cli = batfish.Client()
            >>> cli.image_from_slug('test1')
            <Image test1>

        :param slug: A string slug of an image.
        :rtype: An instance of `batfish.models.Image`.
        """
        url = "images/{0}".format(slug.lower())
        j = self.get(url)
        if 'image' not in j:
            return None
        return Image(j['image'])

    def image_delete(self, image):
        """
        Send an API request to delete an image.

            >>> cli = batfish.Client()
            >>> cli.image_delete(123456)

        :param image: The string name, slug, integer ID of an image or an
                      instance of `batfish.models.Image`.
        """
        if isinstance(image, Image):
            image = image.id
        print self.delete('images/{0}'.format(image))

    def image_rename(self, image, name):
        """
        Send an API request to rename an image.

            >>> cli = batfish.Client()
            >>> cli.image_rename(90876, "kura-test")
            {'response': "Nothing", 'reason': "Meh."}

        :param image: The image to modify, either a image ID, name, slug or an
                        instance of `batfish.models.Image`.
        :param name: A string of the new name.
        :rtype: Dictionary of the JSON response.
        """
        if isinstance(image, Image):
            image = image.id
        if not valid_chars.match(name):
            raise ValueError("""Only valid characters are allowed. """
                             """(a-z, A-Z, 0-9, . and -)""")
        print self.put("images/{0}".format(image), {'name': name})

    def image_transfer(self, image, region):
        if isinstance(image, Image):
            image = image.id
        if isinstance(region, Region):
            region = region.slug
        d = {'type': 'transfer', 'region': region}
        print self.post("images/{0}/actions".format(image), d)

    @property
    def regions(self):
        j = self.get('regions')
        return [Region(r) for r in j['regions']]

    def region_from_name(self, name):
        j = self.get('regions')
        for r in j['regions']:
            if r['name'].lower().startswith(name.lower()):
                return Region(r)
        return None

    def region_from_slug(self, slug):
        j = self.get('regions')
        for r in j['regions']:
            if r['slug'].lower().startswith(slug.lower()):
                return Region(r)
        return None

    @property
    def sizes(self):
        j = self.get('sizes')
        return [Size(s) for s in j['sizes']]

    def size_from_slug(self, slug):
        j = self.get('sizes')
        for s in j['sizes']:
            if s['slug'].lower().startswith(slug.lower()):
                return Size(s)
        return None
