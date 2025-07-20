#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized
from client import GithubOrgClient


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

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

        @parameterized.expand([
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ])
        def test_has_license(self, repo, license_key, expected):
            """Test has_license returns True if repo has the correct license"""
            result = GithubOrgClient.has_license(repo, license_key)
            self.assertEqual(result, expected)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org"""
        test_url = "https://api.github.com/orgs/test-org/repos"

        with patch.object(GithubOrgClient, "org",
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": test_url}
            client = GithubOrgClient("test-org")

            result = client._public_repos_url
            self.assertEqual(result, test_url)

    def test_public_repos(self):
        """Test that public_repos returns the expected repo names"""
        test_repos = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        with patch("client.get_json", return_value=test_repos) as mock_get:
            with patch.object(GithubOrgClient, "_public_repos_url",
                              new_callable=PropertyMock) as mock_url:
                mock_url.return_value = "https://fake.url"
                client = GithubOrgClient("test-org")

                result = client.public_repos()
                self.assertEqual(result, ["repo1", "repo2"])
                mock_url.assert_called_once()
                mock_get.assert_called_once_with("https://fake.url")
