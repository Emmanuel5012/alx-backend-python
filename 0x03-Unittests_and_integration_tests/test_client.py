#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected data"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

        def test_public_repos_url(self):
            """Test that _public_repos_url returns correct URL from org"""
            test_url = "https://api.github.com/orgs/test-org/repos"
            
            with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
                mock_org.return_value = {"repos_url": test_url}
                client = GithubOrgClient("test-org")
                
                result = client._public_repos_url
                self.assertEqual(result, test_url)