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

from .region import Region


class Droplet(object):
    _data = None

    def __init__(self, droplet_data):
        self._data = droplet_data

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Droplet {0}>".format(self.name)

    @property
    def id(self):
        return self._data['id']

    @property
    def name(self):
        return self._data['name']

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
    def region_name(self):
        return Region.name_from_slug(self._data['region']['slug'])

    def region(self, client):
        return client.region_from_slug(self._data['region']['slug'])

    def image(self, client):
        return client.image_from_id(self._data['image']['id'])

    @property
    def size(self):
        size = namedtuple('DropletSize', 'name memory disk hourly monthly')
        return size(name=self._data['size']['slug'].upper(),
                    memory=self._data['size']['slug'].upper(),
                    disk="{0}GB".format(self.disk_size),
                    hourly=self._data['size']['price_hourly'],
                    monthly=self._data['size']['price_monthly'])

    @property
    def locked(self):
        return self._data['locked']

    @property
    def created(self):
        return datetime.strptime(self._data['created_at'], '%Y-%m-%dT%H:%M:%SZ')

    @property
    def status(self):
        return self._data['status']

    @property
    def networks(self):
        ipv4 = namedtuple('IPv4', 'ip type gateway netmask')
        ipv6 = namedtuple('IPv6', 'ip type gateway netmask')
        networks = {}
        networks['ipv4'] = [ipv4(ip=n['ip_address'], type=n['type'],
                                 gateway=n['gateway'], netmask=n['netmask'])
                                 for n in self._data['networks']['v4']]
        networks['ipv6'] = [ipv6(ip=n['ip_address'], type=n['type'],
                                 gateway=n['gateway'], netmask=n['netmask'])
                                 for n in self._data['networks']['v6']]
        return networks

    @property
    def kernel(self):
        kernel = namedtuple('Kernel', 'id name version')
        return kernel(id=int(self._data['kernel']['id']),
                      name=self._data['kernel']['name'],
                      version=self._data['kernel']['version'])

    @property
    def backups(self):
        return self._data['backup_ids']

    @property
    def snapshots(self):
        return self._data['snapshot_ids']

    def actions(self, client):
        j = client.get("droplets/{0}/actions".format(self.id))
        if 'actions' not in j:
            return None
        return [Action(a) for a in j['actions']]

    @property
    def features(self):
        return self._data['features']
