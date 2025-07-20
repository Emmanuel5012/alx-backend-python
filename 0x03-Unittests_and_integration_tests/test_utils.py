#!/usr/bin/env python3
"""Unit test for utils.access_nested_map"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json

class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test accessing nested maps with valid paths
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    def test_access_nested_map_key_exception(self):
        with self.assertRaises(KeyError) as cm:
            access_nested_map({}, ("a",))
        self.assertEqual(str(cm.exception), "'a'")
        
        with self.assertRaises(KeyError) as cm:
            access_nested_map({"a": 1}, ("a", "b"))
        self.assertEqual(str(cm.exception), "'b'")



class TestGetJson(unittest.TestCase):
    """Test get_json function"""

    def test_get_json(self):
        """Tests get_json returns expected result from mocked requests.get"""

        # First test case
        test_url1 = "http://example.com"
        test_payload1 = {"payload": True}

        with patch("utils.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload1
            mock_get.return_value = mock_response

            result = get_json(test_url1)
            self.assertEqual(result, test_payload1)
            mock_get.assert_called_once_with(test_url1, timeout=10)

        # Second test case
        test_url2 = "http://holberton.io"
        test_payload2 = {"payload": False}

        with patch("utils.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload2
            mock_get.return_value = mock_response

            result = get_json(test_url2)
            self.assertEqual(result, test_payload2)
            mock_get.assert_called_once_with(test_url2, timeout=10)
