import json
import os

import requests

from .models import Droplet, Image, Region


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
        r = requests.get("{0}{1}".format(self.api_base, url), headers=headers)
        r.raise_for_status()
        return json.loads(r.text)

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
        j = self.get(url)
        if 'droplet' not in j:
            return None
        return Droplet(j['droplet'])

    def droplet_from_name(self, name):
        j = self.get('droplets')
        if 'droplets' not in j:
            return None
        for d in j['droplets']:
            if d['name'].startswith(name):
                return Droplet(d)
        return None

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
            if i['name'].startswith(name):
                return Image(i)
        return None

    def image_from_slug(self, slug):
        url = "images/{0}".format(slug)
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
            if r['name'].startswith(name):
                return Region(r)
        return None

    def region_from_slug(self, slug):
        j = self.get('regions')
        for r in j['regions']:
            if r['name'].startswith(slug):
                return Region(r)
        return None
