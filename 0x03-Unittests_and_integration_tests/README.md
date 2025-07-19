#!/usr/bin/env python3
# Unittests and Integration Tests

This project contains unit and integration tests for a GitHub organization client built with Python.

## 📁 Project Structure

- `utils.py`: Utility functions including `access_nested_map`, `get_json`, and `memoize`.
- `client.py`: Defines the `GithubOrgClient` class used to fetch organization data from GitHub.
- `fixtures.py`: Contains test data used for mocking API responses.
- `test_utils.py`: Contains parameterized unit tests for utility functions.

## 🧪 Features Tested

- Accessing values from nested dictionaries
- Mocking external API calls
- Memoization and caching
- Integration testing of GitHub org repositories

## ✅ Requirements

- Python 3.7 (Ubuntu 18.04 LTS)
- All files are executable and end with a new line
- Code follows `pycodestyle` 2.5
- Each module, class, and function has a proper documentation string
- All functions and coroutines are type-annotated

## 🧰 Setup

Install dependencies:
```bash
pip install requests parameterized

Run tests:

bash
python -m unittest test_utils.py