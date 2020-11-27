import pytest
from pyfinance.finten import FinTen, InvalidCredentials, InvalidQuery
import json
import httpretty


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
    finten = FinTen()
    assert finten._token == None
    finten._login()
    assert finten._username == "pyfinance"
    assert finten._password == "pyfinance"
    assert finten._token != None


def test_login__invalid_credentials():
    with pytest.raises(InvalidCredentials):
        finten = FinTen()
        finten.set_login(username="foo", password="bar")
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


def test_get_filings_with_public_login():
    httpretty.enable()
    httpretty.register_uri(
        httpretty.GET,
        "https://finten.weirwood.ai/api/company/filings?ticker=AAPL",
        body='{"filings": [{"foo": "bar", "manchu": "massachusets"}]}',
    )
    httpretty.register_uri(
        httpretty.POST,
        "https://finten.weirwood.ai/api/users/login",
        body='{"token": "test"}',
    )

    filings = FinTen().get_filings(ticker="AAPL")
    assert len(filings) > 0


def test_get_prices():
    aapl = FinTen().get_prices(ticker="AAPL")
    assert len(aapl) > 0


def test_get_prices_last_year():
    aapl = FinTen().get_prices(ticker="AAPL", start="2019-01-01", end="2020-01-01")
    assert len(aapl) == 253


def test_unknown_ticker():
    with pytest.raises(InvalidQuery):
        FinTen().get_prices(ticker="asdf")

