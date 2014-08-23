import json
import os

import requests

from .models import Droplet


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
        return r

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

    def list_droplets(self):
        r = self.get('droplets')
        j = json.loads(r.text)
        return [Droplet(d) for d in j['droplets']]


    def droplet_from_id(self, droplet_id):
        url = "droplets/{0}".format(droplet_id)
        r = self.get(url)
        j = json.loads(r.text)
        return Droplet(j['droplet'])

    def droplet_from_name(self, droplet_name):
        r = self.get('droplets')
        j = json.loads(r.text)
        for d in j['droplets']:
            if d['name'].startswith(droplet_name):
                return Droplet(d)
        return None
