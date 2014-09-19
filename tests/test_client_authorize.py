import collections
import json
import unittest

import responses
from requests import HTTPError
from mock import patch

from batfish import Client
from batfish.__about__ import __version__


class TestClientAuthorize(unittest.TestCase):

    def setUp(self):
        with patch('batfish.client.read_token_from_conf',
                   return_value=None):
            self.cli = Client()

    @responses.activate
    def test_authorize_error(self):
        url = "https://api.digitalocean.com/v2/actions"
        responses.add(responses.GET, url,
                      body='{"error": "something"}', status=500,
                      content_type="application/json")
        with self.assertRaises(HTTPError):
            self.cli.authorize("test_token")

    @responses.activate
    def test_authorize_unauthorized(self):
        url = "https://api.digitalocean.com/v2/kura"
        body = {'id': "unauthorized", 'message': "Unable to authenticate you."}
        responses.add(responses.GET, url, body=json.dumps(body), status=401,
                      content_type="application/json")
        self.cli.authorize("test_token")
        self.assertEquals(responses.calls[0].response.status_code, 401)

    @responses.activate
    def test_authorize_unauthorized(self):
        url = "https://api.digitalocean.com/v2/actions"
        responses.add(responses.GET, url,
                      body='{"error": "something"}', status=200,
                      content_type="application/json")
        auth = self.cli.authorize("test_token")
        self.assertEquals(auth, "OK")
        self.assertEquals(responses.calls[0].response.status_code, 200)
