import pytest
from pyfinance.finten import FinTen, InvalidCredentials
import json

@pytest.fixture
def finten_login():
  with open("./.credentials.json") as f:
    finten_login = json.load(f)
  return finten_login

def test_is_reachable():
    finten = FinTen()
    assert finten._is_reachable()
    finten.URI = "https://www.google.com"
    assert finten._is_reachable() == False

def test_login__no_login_set():
    with pytest.raises(InvalidCredentials):
      finten = FinTen() 
      finten._login()

def test_login__invalid_credentials():
  with pytest.raises(InvalidCredentials):
    finten = FinTen()
    finten.set_login(username = "foo", password = "bar")
    finten._login()

def test_login(finten_login):
  finten = FinTen()
  finten.set_login(**finten_login)
  finten._login()

def test_get_filings(finten_login):
  finten = FinTen()
  finten.set_login(**finten_login)
  filings = finten.get_filings(ticker="AAPL")
  assert len(filings) > 0
