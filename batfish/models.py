from collections import namedtuple
from datetime import datetime


class Droplet(object):
    _data = None

    def __init__(self, data):
        self._data = data

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
        return self._data['disk']

    @property
    def region(self):
        pass

    @property
    def image(self):
        pass

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
        return datetime.strptime(self._data['created_at'],
                                 '%Y-%m-%dT%H:%M:%SZ')

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

    @property
    def actions(self):
        return self._data['action_ids']

    @property
    def features(self):
        return self._data['features']
