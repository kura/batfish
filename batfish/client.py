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

from batfish import __title__, __version__
from .models import Droplet, Image, Region, Size


hostname_valid_chars = re.compile(r"^[a-zA-Z0-9\.\-]*$")


def read_token_from_conf():
    if not os.path.exists(os.path.expanduser('~/.batfish')):
        return None
    with open(os.path.expanduser('~/.batfish')) as f:
        return f.read()


def write_token_to_conf(token):
    with open(os.path.expanduser('~/.batfish'), 'w') as f:
        f.write(token)


class Client(object):
    token = None
    api_base = "https://api.digitalocean.com/v2/"

    def __init__(self):
        token = read_token_from_conf()
        if token is not None:
            self.token = token

    def get(self, url, headers=None):
        if headers is None:
            headers = {'Authorization': "Bearer {0}".format(self.token)}
        headers['User-Agent'] = "{0} ({1})".format(__title__.title(),
                                                   __version__)
        r = requests.get("{0}{1}".format(self.api_base, url), headers=headers)
        r.raise_for_status()
        return json.loads(r.text)

    def post(self, url, payload):
        headers = {'Authorization': "Bearer {0}".format(self.token),
                   'User-Agent': "{0} ({1})".format(__title__,
                                                    __version__),
                   'Content-Type': "application/json"}
        r = requests.post("{0}{1}".format(self.api_base, url),
                          headers=headers, data=json.dumps(payload))
        return json.loads(r.text)

    def delete(self, url):
        headers = {'Authorization': "Bearer {0}".format(self.token),
                   'User-Agent': "{0} ({1})".format(__title__,
                                                    __version__)}
        r = requests.delete("{0}{1}".format(self.api_base, url),
                            headers=headers)

    def authorize(self, token):
        h = {'Authorization': "Bearer {0}".format(token)}
        r = self.get('actions', headers=h)
        if r.status_code == 200:
            write_token_to_conf(token)
            self.token = token
            return "OK"
        if r.status_code == 404:
            return "Unable to authorize"
        else:
            return """Unable to authorize due to unknown reason.""" \
                   """Server responded with {0} - {1}""".format(r.status_code,
                                                                r.reason)

    def droplets(self):
        j = self.get('droplets')
        if 'droplets' not in j:
            return None
        return [Droplet(d) for d in j['droplets']]

    def droplet_from_id(self, droplet_id):
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
        j = self.get('droplets')
        if 'droplets' not in j:
            return None
        for d in j['droplets']:
            if d['name'].lower().startswith(name.lower()):
                return Droplet(d)
        return None

    def droplet(self, action, droplet, image=None, name=None):
        if action not in ['reboot', 'resize', 'power_cycle', 'power_off',
                          'power_on', 'password_reset', 'shutdown', 'restore',
                          'rebuild', 'snapshot', 'rename']:
            raise NotImplemented("Invalid action")
        if isinstance(droplet, Droplet):
            droplet = droplet.id
        d = {'type': action}
        if action in ['restore', 'rebuild']:
            if image is None:
                raise KeyError("No image provided")
            if isinstance(image, Image):
                image = image.id
            d['image'] = image
        if action in ['rename', ]:
            if name is None:
                raise KeyError("No new name provided")
            if not hostname_valid_chars.match(name):
                raise ValueError("""Valid characters are allowed. """
                                 """(a-z, A-Z, 0-9, . and -)""")
            d['name'] = name
        print self.post('droplets/{0}/actions'.format(droplet), d)

    def delete_droplet(self, droplet):
        if isinstance(droplet, Droplet):
            droplet = droplet.id
        print self.delete('droplets/{0}'.format(droplet))

    def create_droplet(self, name, region, size, image):
        if isinstance(size, Size):
            size = size.name
        if isinstance(image, Image):
            image = image.id
        if isinstance(region, Region):
            region = region.slug
        if not image.isdigit():
            image = image.lower()
        if not hostname_valid_chars.match(name):
            raise ValueError("""Valid characters are allowed. """
                             """(a-z, A-Z, 0-9, . and -)""")
        d = {'name': name, 'size': size.lower(), 'image': image,
             'region': region}
        print self.post('droplets', d)

    def images(self):
        j = self.get('images')
        if 'images' not in j:
            return None
        return [Image(i) for i in j['images']]

    def image_from_id(self, image_id):
        url = "images/{0}".format(image_id)
        j = self.get(url)
        if 'image' not in j:
            return None
        return Image(j['image'])

    def image_from_name(self, name):
        j = self.get('images')
        if 'images' not in j:
            return None
        for i in j['images']:
            if i['name'].lower().startswith(name.lower()):
                return Image(i)
        return None

    def image_from_slug(self, slug):
        url = "images/{0}".format(slug.lower())
        j = self.get(url)
        if 'image' not in j:
            return None
        return Image(j['image'])

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

    def sizes(self):
        j = self.get('sizes')
        return [Size(s) for s in j['sizes']]

    def size_from_slug(self, slug):
        j = self.get('sizes')
        for s in j['sizes']:
            if s['slug'].lower().startswith(slug.lower()):
                return Size(s)
        return None
