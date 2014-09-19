import unittest

from mock import patch

from batfish import Client


class TestClientToken(unittest.TestCase):

    def test_client_token(self):
        with patch('batfish.client.read_token_from_conf',
                   return_value="test_token"):
            cli = Client()
            self.assertEqual(cli.token, "test_token")
