import pytest
from pyfinance.finten import FinTen


def test_is_reachable():
    finten = FinTen()
    assert finten._is_reachable()
    finten.URI = "https://www.google.com"
    assert finten._is_reachable() == False


def test_login():
    finten = FinTen()
    finten.set_key(API_KEY="foo")

