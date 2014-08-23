from collections import namedtuple
from datetime import datetime


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
        return datetime.strptime(self._data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
