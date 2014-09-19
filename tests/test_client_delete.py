import collections
import unittest

import responses
from requests import HTTPError
from mock import patch

from batfish import Client
from batfish.__about__ import __version__


class TestClientDelete(unittest.TestCase):

    def setUp(self):
        with patch('batfish.client.read_token_from_conf',
                   return_value="test_token"):
            self.cli = Client()

    @responses.activate
    def test_delete_errors(self):
        url = "https://api.digitalocean.com/v2/kura"
        responses.add(responses.DELETE, url,
                      body='{"error": "something"}', status=500,
                      content_type="application/json")
        with self.assertRaises(HTTPError):
            self.cli.delete('kura')

    @responses.activate
    def test_delete_no_error(self):
        url = "https://api.digitalocean.com/v2/kura"
        responses.add(responses.DELETE, url,
                      body='{"message": "something"}', status=204,
                      content_type="application/json")
        self.cli.delete('kura')
        self.assertEquals(responses.calls[0].response.status_code, 204)

    @responses.activate
    def test_delete_headers(self):
        url = "https://api.digitalocean.com/v2/kura"
        responses.add(responses.DELETE, url,
                      body='{"message": "something"}', status=204,
                      content_type="application/json")
        self.cli.delete('kura')
        h = {'Accept': "*/*", 'Accept-Encoding': "gzip, deflate",
             'Authorization': "Bearer test_token",
             'User-Agent': "Batfish ({0})".format(__version__),
             'Content-Length': '0'}
        th = collections.OrderedDict(sorted(h.items()))
        rh = collections.OrderedDict(sorted(responses.calls[0].request.headers.items()))
        self.assertEquals(rh, th)
