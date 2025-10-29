from pathlib import Path
from pytest import raises

from ofxstatement.ui import UI

from ofxstatement_wise.wise import WisePlugin


def test_wise(snapshot) -> None:
    config = {
        "currency": "USD",
        "bank_id": "BANK1",
        "branch_id": "BRANCH2",
        "account": "TW1",
        "account_type": "CHECKING",
    }
    plugin = WisePlugin(UI(), config)
    parser = plugin.get_parser(Path("tests/sample-statement.csv"))
    statement = parser.parse()

    assert statement == snapshot


def test_parse_statement_currency():
    plugin = WisePlugin(None, {"currency": "GBP"})

    parser = plugin.get_parser(Path("tests/sample-statement.csv"))

    with raises(
        ValueError,
        match="Expected transactions in the GBP currency only, but got one the USD currency",
    ):
        parser.parse()
