import os

from ofxstatement.ui import UI

from ofxstatement_wise.wise import WisePlugin


def test_wise(snapshot) -> None:
    config = {"currency": "USD", "account": "TW1"}
    plugin = WisePlugin(UI(), config)
    here = os.path.dirname(__file__)
    sample_filename = os.path.join(here, "sample-statement.csv")

    parser = plugin.get_parser(sample_filename)
    statement = parser.parse()

    assert statement == snapshot
