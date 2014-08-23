from collections import namedtuple
from datetime import datetime


DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class Action(object):
    _data = None

    def __init__(self, action_data):
        self._data = action_data

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Action {0}>".format(self.type)

    @property
    def id(self):
        return self._data['id']

    @property
    def status(self):
        return self._data['status']

    @property
    def type(self):
        return self._data['type']

    @property
    def started(self):
        return datetime.strptime(self._data['started_at'], DATE_FORMAT)

    @property
    def completed(self):
        return datetime.strptime(self._data['completed_at'], DATE_FORMAT)

    @property
    def resource_id(self):
        return self._data['resource_id']

    @property
    def resource_type(self):
        return self._data['resource_type']

    def region(self, client):
        return self.from_from_slug(self._data['region']['slug'])


class Region(object):
    _data = None

    def __init__(self, region_data):
        self._data = region_data

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Region {0}>".format(self.name)

    @property
    def slug(self):
        return self._data['slug']

    @property
    def name(self):
        return self._data['name']

    @property
    def sizes(self):
        return self._data['sizes']

    @property
    def available(self):
        return self._data['available']

    @property
    def features(self):
        return self._data['features']


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
        return self._data['disk']

    def region(self, client):
        return self.from_from_slug(self._data['region']['slug'])

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
        return datetime.strptime(self._data['created_at'], DATE_FORMAT)

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
        return self._data['id']

    @property
    def name(self):
        return self._data['name']

    @property
    def distribution(self):
        return self._data['distribution']

    @property
    def slug(self):
        return self._data['slug']

    @property
    def public(self):
        return self._data['public']

    def regions(self, client):
        return [client.region_from_slug(r['slug'] for r in self._data['region'])]

    def actions(self, client):
        j = client.get("images/{0}/actions".format(self.id))
        if 'actions' not in j:
            return None
        return [Action(a) for a in j['actions']]

    @property
    def created(self):
        return datetime.strptime(self._data['created_at'], DATE_FORMAT)
