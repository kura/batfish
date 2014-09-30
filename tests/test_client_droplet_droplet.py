import collections
import json
import os
import unittest

import responses
from requests import HTTPError
from mock import patch

from batfish import Client
from batfish.models import Droplet


class TestClientDroplet_droplets(unittest.TestCase):

    def setUp(self):
        package = os.path.join(os.path.dirname(__file__),
                               'good_response.json')
        self.good_resp = open(package).read()
        with patch('batfish.client.read_token_from_conf',
                   return_value=None):
            self.cli = Client()

    @reponses.activate
    def test_droplets_none(self):
        url = "https://api.digitalocean.com/v2/droplets"
        responses.add(responses.GET, url,
                      body="{}", status=200,
                      content_type="application/json")
        droplets = self.cli.droplets
        self.assertEquals(responses.calls[0].response.status_code, 200)
        self.assertEquals(droplets, None)


    @responses.activate
    def test_droplets_list(self):
        url = "https://api.digitalocean.com/v2/droplets"
        responses.add(responses.GET, url,
                      body=self.good_resp, status=200,
                      content_type="application/json")
        droplets = self.cli.droplets
        d1 = Droplet({'name': 'test1'})
        d2 = Droplet({'name': 'test2'})
        self.assertEquals(responses.calls[0].response.status_code, 200)
        self.assertEquals(len(droplets), 2)
