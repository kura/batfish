import collections
import unittest

import responses
from requests import HTTPError
from mock import patch

from batfish import Client
from batfish.__about__ import __version__


class TestClientGet(unittest.TestCase):

    def setUp(self):
        with patch('batfish.client.read_token_from_conf',
                   return_value="test_token"):
            self.cli = Client()

    @responses.activate
    def test_get_errors(self):
        url = "https://api.digitalocean.com/v2/kura"
        responses.add(responses.GET, url,
                      body='{"error": "something"}', status=500,
                      content_type="application/json")
        with self.assertRaises(HTTPError):
            self.cli.get('kura')

    @responses.activate
    def test_get_json(self):
        url = "https://api.digitalocean.com/v2/kura"
        responses.add(responses.GET, url,
                      body='{"message": "something"}', status=200,
                      content_type="application/json")
        j = self.cli.get('kura')
        self.assertEquals(j['message'], "something")

    @responses.activate
    def test_get_default_headers(self):
        url = "https://api.digitalocean.com/v2/kura"
        responses.add(responses.GET, url,
                      body='{"message": "something"}', status=200,
                      content_type="application/json")
        self.cli.get('kura')
        h = {'Accept': "*/*", 'Accept-Encoding': "gzip, deflate",
             'Authorization': "Bearer test_token",
             'User-Agent': "Batfish ({0})".format(__version__)}
        th = collections.OrderedDict(sorted(h.items()))
        rh = collections.OrderedDict(sorted(responses.calls[0].request.headers.items()))
        self.assertEquals(rh, th)

    @responses.activate
    def test_get_headers_modified_ua(self):
        url = "https://api.digitalocean.com/v2/kura"
        responses.add(responses.GET, url,
                      body='{"message": "something"}', status=200,
                      content_type="application/json")
        self.cli.ua = "Kura"
        self.cli.get('kura')
        h = {'Accept': "*/*", 'Accept-Encoding': "gzip, deflate",
             'Authorization': "Bearer test_token",
             'User-Agent': "Kura"}
        th = collections.OrderedDict(sorted(h.items()))
        rh = collections.OrderedDict(sorted(responses.calls[0].request.headers.items()))
        self.assertEquals(rh, th)

    @responses.activate
    def test_get_headers_custom(self):
        url = "https://api.digitalocean.com/v2/kura"
        responses.add(responses.GET, url,
                      body='{"message": "something"}', status=200,
                      content_type="application/json")
        h = {'Authorization': "Bearer test_token2", 'X-Random-Header': 'test'}
        self.cli.get('kura', headers=h)
        h = {'Accept': "*/*", 'Accept-Encoding': "gzip, deflate",
             'Authorization': "Bearer test_token2", 'X-Random-Header': "test",
             'User-Agent': 'Batfish ({0})'.format(__version__)}
        self.assertEquals(responses.calls[0].request.headers, h)
