from pathlib import Path
from pytest import mark, raises

from ofxstatement.ui import UI

from ofxstatement_wise.wise import WisePlugin


testdata = [
    (
        Path("tests/sample-statement-brl.csv"),
        "BRL",
        "40571694",
        "0001",
        "1176697",
        "CHECKING",
    ),
    (
        Path("tests/sample-statement-gbp.csv"),
        None,
        "230801",
        None,
        "25635393",
        "CHECKING",
    ),
]


@mark.parametrize(
    "sample_csv, currency, bank_id, branch_id, account, account_type", testdata
)
def test_parse_statement(
    sample_csv, currency, bank_id, branch_id, account, account_type, snapshot
):
    config = {
        "currency": currency,
        "bank_id": bank_id,
        "branch_id": branch_id,
        "account": account,
        "account_type": account_type,
    }
    plugin = WisePlugin(UI(), config)
    parser = plugin.get_parser(sample_csv)
    statement = parser.parse()

    assert statement == snapshot


def test_parse_statement_currency():
    plugin = WisePlugin(None, {"currency": "GBP"})

    parser = plugin.get_parser(Path("tests/sample-statement-brl.csv"))

    with raises(
        ValueError,
        match="Expected transactions in the GBP currency only, but got one the BRL currency",
    ):
        parser.parse()
