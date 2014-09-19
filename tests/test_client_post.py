import collections
import unittest

import responses
from requests import HTTPError
from mock import patch

from batfish import Client
from batfish.__about__ import __version__


class TestClientPost(unittest.TestCase):

    def setUp(self):
        with patch('batfish.client.read_token_from_conf',
                   return_value="test_token"):
            self.cli = Client()
        self.base_payload = {}

    @responses.activate
    def test_post_errors(self):
        url = "https://api.digitalocean.com/v2/kura"
        responses.add(responses.POST, url,
                      body='{"error": "something"}', status=500,
                      content_type="application/json")
        with self.assertRaises(HTTPError):
            self.cli.post('kura', self.base_payload)

    @responses.activate
    def test_post_json(self):
        url = "https://api.digitalocean.com/v2/kura"
        responses.add(responses.POST, url,
                      body='{"message": "something"}', status=200,
                      content_type="application/json")
        j = self.cli.post('kura', self.base_payload)
        self.assertEquals(j['message'], "something")

    @responses.activate
    def test_post_headers(self):
        url = "https://api.digitalocean.com/v2/kura"
        responses.add(responses.POST, url,
                      body='{"message": "something"}', status=200,
                      content_type="application/json")
        self.cli.post('kura', self.base_payload)
        h = {'Accept': "*/*", 'Accept-Encoding': "gzip, deflate",
             'Authorization': "Bearer test_token",
             'User-Agent': "Batfish ({0})".format(__version__),
             'Content-Length': '2', 'Content-Type': "application/json"}
        th = collections.OrderedDict(sorted(h.items()))
        rh = collections.OrderedDict(sorted(responses.calls[0].request.headers.items()))
        self.assertEquals(rh, th)
