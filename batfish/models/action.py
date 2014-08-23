from collections import namedtuple
from datetime import datetime


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
        return datetime.strptime(self._data['started_at'], '%Y-%m-%dT%H:%M:%SZ')

    @property
    def completed(self):
        return datetime.strptime(self._data['completed_at'], '%Y-%m-%dT%H:%M:%SZ')

    @property
    def resource_id(self):
        return self._data['resource_id']

    @property
    def resource_type(self):
        return self._data['resource_type']

    def region(self, client):
        return client.region_from_slug(self._data['region']['slug'])
