from unittest.mock import patch

from src.parsers import parser_currency, parser_stocks


@patch("requests.get")
def test_parser_currency(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"USD": 1.00, "RUB": 90.00}}
    assert parser_currency(["USD"]) == {"USD": 90.00}


@patch("requests.get")
def test_parser_stocks(mock_get):
    mock_get.return_value.json.return_value = {"Global Quote": {"05. price": 300.00}}
    assert parser_stocks(["AAPL"]) == {"AAPL": 300.00}
