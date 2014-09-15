import os
import unittest

from mock import mock_open, patch

from batfish.client import read_token_from_conf, write_token_to_conf


class TestReadToken(unittest.TestCase):

    @patch('os.path.exists', return_value=False)
    def test_read_token_no_file(self, _):
        token = read_token_from_conf()
        self.assertEqual(token, None)

    @patch('os.path.exists', return_value=True)
    def test_read_token_from_file(self, _):
        mo = mock_open(read_data="test_token")
        with patch("batfish.client.open", mo, create=True):
            token = read_token_from_conf()
        self.assertEqual(token, "test_token")


class TestWriteToken(unittest.TestCase):

    @patch('os.path.expanduser', return_value="/home/test/.batfish")
    def test_write_token_to_file(self, _):
        mo = mock_open()
        with patch("batfish.client.open", mo, create=True) as f:
            write_token_to_conf("test_token")
        mo.assert_called_once_with('/home/test/.batfish', 'w')
        h = mo()
        h.write.assert_called_once_with("test_token")
