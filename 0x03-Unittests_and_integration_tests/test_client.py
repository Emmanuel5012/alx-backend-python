#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized_class


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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns True if repo has the correct license"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get and return appropriate payloads"""
        cls.get_patcher = patch('requests.get')

        mocked_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                mock_resp = Mock()
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            elif url == cls.org_payload["repos_url"]:
                mock_resp = Mock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            else:
                return Mock()

        mocked_get.side_effect = side_effect

        def test_public_repos(self):
            """Test public_repos returns expected repo names"""
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), self.expected_repos)

        def test_public_repos_with_license(self):
            """Test public_repos filters repos by license"""
            client = GithubOrgClient("google")
            self.assertEqual(
                client.public_repos(license="apache-2.0"),
                self.apache2_repos
            )

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()
