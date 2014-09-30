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
        The droplet ID.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.id
            1234

        :rtype: `integer`.
        """
        return self._data['id']

    @property
    def name(self):
        """
        The name of the droplet.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.name
            "kura-test"

        :rtype: `string`.
        """
        return self._data['name']

    @property
    def memory(self):
        """
        The amount of RAM of the droplet, including measurement unit.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.memory
            '512MB'

        :rtype: `string`.
        """
        return self._data['memory']

    @property
    def cpus(self):
        """
        The number of CPUs of the droplet.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.cpus
            1

        :rtype: `integer`.
        """
        return self._data['vcpus']

    @property
    def disk_size(self):
        """
        The disk size of the droplet, including measurement unit.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.disk_size
            '20GB'

        :rtype: `string`.
        """
        return "{0}GB".format(self._data['disk'])

    @property
    def region_name(self):
        """
        The name of the region the droplet is in.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.region_name
            <Region Amsterdam 2>
            >>> droplet.region_name.name
            'Amsterdam 2'

        :rtype: `string`.
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
        The size of the droplet.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.size
            Size(name='512MB', memory='512MB', disk='20GB',
                 hourly=0.00744, monthly=5.0)

        :rtype: `collections.NamedTuple`.
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
        The lock status of the droplet.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.locked
            False

        :rtype: `boolean`.
        """
        return self._data['locked']

    @property
    def created(self):
        """
        The date and time a droplet was created.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.created
            datetime.datetime(2014, 1, 7, 23, 19, 49)

        :rtype: `datetime.datime` object.
        """
        return datetime.strptime(self._data['created_at'],
                                 '%Y-%m-%dT%H:%M:%SZ')

    @property
    def status(self):
        """
        The status of the droplet.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.status
            'active'

        :rtype: `string`.
        """
        return self._data['status']

    @property
    def networks(self):
        """
        Network connections of a droplet.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.networks
            {'ipv4': [IPv4(ip='10.12.1.1', type='private',
                           gateway='10.12.0.1', netmask='255.255.0.0'),
                      IPv4(ip='95.85.62.206', type='public',
                           gateway='95.85.62.1', netmask='255.255.255.0')],
             'ipv6': []}

        :rtype: `dictionary` of `collection.NamedTuples`s.
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
        The currently active kernel of a droplet.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.kernel
            Kernel(id=140,
                   name='Debian 7.0 x64 vmlinuz-3.2.0-4-amd64  (3.2.41-2)',
                   version='3.2.0-4-amd64')

        :rtype: `collections.NamedTuple`.
        """
        kernel = namedtuple('Kernel', 'id name version')
        return kernel(id=int(self._data['kernel']['id']),
                      name=self._data['kernel']['name'],
                      version=self._data['kernel']['version'])

    @property
    def backups(self):
        """
        Existing backups of a droplet.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.backups
            [123, 124, 125]

        :rtype: `list` of backup IDs.
        """
        return self._data['backup_ids']

    @property
    def snapshots(self):
        """
        Existing snapshops of a droplet.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.backups
            [123, 124, 125]

        :rtype: `list` of snapshot IDs.
        """
        return self._data['snapshot_ids']

    def actions(self, client):
        """
        A list of actions that have been performed on the droplet.

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
        A list of features currently active on a droplet.

            >>> cli = batfish.Client()
            >>> droplet = cli.droplet_from_id(1234)
            >>> droplet.features
            ['private_networking', 'virtio']

        :rtype: `list`.
        """
        return self._data['features']
