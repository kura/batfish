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
