#!/usr/bin/env python3
"""Unit test for utils.access_nested_map"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from .utils import access_nested_map, get_json

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

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"data": "value"}),
    ])
    @patch("requests.get")
    def test_get_json(self, url, expected, mock_get):
        """Test get_json returns expected JSON from mocked request"""
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_get.return_value = mock_response

        self.assertEqual(get_json(url), expected)
        mock_get.assert_called_once_with(url, timeout=10)
