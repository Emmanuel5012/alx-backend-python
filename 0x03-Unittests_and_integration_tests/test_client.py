#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class with memoization and license checking."""

import unittest
from unittest.mock import patch
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class"""

    @patch('client.get_json', return_value={"name": "google"})
    def test_org_memoization(self, mock_get_json):
        """Test that @memoize works: get_json is called only once"""
        client = GithubOrgClient("google")
        result_1 = client.org()
        result_2 = client.org()


        self.assertEqual(result_1, {"name": "google"})
        self.assertEqual(result_2, {"name": "google"})
        mock_get_json.assert_called_once()