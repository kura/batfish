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

from .action import Action
from .region import Region


class Droplet(object):
    """
    A Digital Ocean droplet.

    :param droplet_data: A dictionary of droplet data from the API.
    """
    _data = None

    def __init__(self, droplet_data):
        self._data = droplet_data

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Droplet {0}>".format(self.name)

    @property
    def id(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.id
            1234
        """
        return self._data['id']

    @property
    def name(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.name
            u"kura-test"
        """
        return self._data['name']

    @property
    def memory(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.memory
            u'512MB'
        """
        return self._data['memory']

    @property
    def cpus(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.cpus
            1
        """
        return self._data['vcpus']

    @property
    def disk_size(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.disk_size
            u'20GB'
        """
        return "{0}GB".format(self._data['disk'])

    @property
    def region_name(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.region_name
            <Region Amsterdam 2>
            >>> droplet.region_name.name
            u'Amsterdam 2'
        """
        return Region.name_from_slug(self._data['region']['slug'])

    def region(self, client):
        """
        Get an instance of `batfish.models.Region` from the droplet's region
        information.

        :param client: An instance of `batfish.client.Client`.
        :rtype: An instance of `batfish.models.Region`.
        """
        return client.region_from_slug(self._data['region']['slug'])

    def image(self, client):
        """
        Get an instance of `batfish.models.Image` from the droplet's image
        information.

        :param client: An instance of `batfish.client.Client`.
        :rtype: An instance of `batfish.models.Image`.
        """
        return client.image_from_id(self._data['image']['id'])

    @property
    def size(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.size
            Size(name=u'512MB', memory=u'512MB', disk='20GBGB', hourly=0.00744, monthly=5.0)
        """
        size = namedtuple('Size', 'name memory disk hourly monthly')
        return size(name=self._data['size']['slug'].upper(),
                    memory=self._data['size']['slug'].upper(),
                    disk="{0}GB".format(self.disk_size),
                    hourly=self._data['size']['price_hourly'],
                    monthly=self._data['size']['price_monthly'])

    @property
    def locked(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.locked
            False
        """
        return self._data['locked']

    @property
    def created(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.created
            datetime.datetime(2014, 1, 7, 23, 19, 49)
        """
        return datetime.strptime(self._data['created_at'], '%Y-%m-%dT%H:%M:%SZ')

    @property
    def status(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.status
            u'active'
        """
        return self._data['status']

    @property
    def networks(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.networks
            {'ipv4': [IPv4(ip=u'10.12.1.1', type=u'private',
                           gateway=u'10.12.0.1', netmask=u'255.255.0.0'),
                      IPv4(ip=u'95.85.62.206', type=u'public',
                           gateway=u'95.85.62.1', netmask=u'255.255.255.0')],
             'ipv6': []}
        """
        ipv4 = namedtuple('IPv4', 'ip type gateway netmask')
        ipv6 = namedtuple('IPv6', 'ip type gateway')
        networks = {}
        networks['ipv4'] = [ipv4(ip=n['ip_address'], type=n['type'],
                                 gateway=n['gateway'], netmask=n['netmask'])
                                 for n in self._data['networks']['v4']]
        networks['ipv6'] = [ipv6(ip=n['ip_address'], type=n['type'],
                                 gateway=n['gateway'])
                                 for n in self._data['networks']['v6']]
        return networks

    @property
    def kernel(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.kernel
            Kernel(id=140, name=u'Debian 7.0 x64 vmlinuz-3.2.0-4-amd64  (3.2.41-2) ', version=u'3.2.0-4-amd64')
        """
        kernel = namedtuple('Kernel', 'id name version')
        return kernel(id=int(self._data['kernel']['id']),
                      name=self._data['kernel']['name'],
                      version=self._data['kernel']['version'])

    @property
    def backups(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.backups
            [123, 124, 125]
        """
        return self._data['backup_ids']

    @property
    def snapshots(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.backups
            [123, 124, 125]
        """
        return self._data['snapshot_ids']

    def actions(self, client):
        """
        Get a list of actions that have been performed on the droplet.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.actions
            [<Action power_cycle>, <Action create>]

        :param client: An instance of `batfish.client.Client`.
        :rtype: A list of `batfish.models.Action` instances.
        """
        j = client.get("droplets/{0}/actions".format(self.id))
        if 'actions' not in j:
            return None
        return [Action(a) for a in j['actions']]

    @property
    def features(self):
        """
            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.features
            [u'private_networking', u'virtio']
        """
        return self._data['features']
