from csv import DictReader
from datetime import datetime
from typing import Dict, Iterable, Optional
from decimal import Decimal

from ofxstatement.plugin import Plugin
from ofxstatement.parser import StatementParser
from ofxstatement.statement import (
    Statement,
    StatementLine,
    BankAccount,
)


class WisePlugin(Plugin):
    """Wise CSV format"""

    def get_parser(self, filename: str) -> "WiseParser":
        return WiseParser(
            filename,
            account_id=self.settings.get("account"),
            bank_id=self.settings.get("bank_id"),
            branch_id=self.settings.get("branch_id"),
            account_type=self.settings.get("account_type"),
            currency=self.settings.get("currency"),
        )


class WiseParser(StatementParser[Dict[str, str]]):
    def __init__(
        self,
        filename: str,
        account_id: Optional[str],
        bank_id: Optional[str],
        branch_id: Optional[str],
        account_type: Optional[str],
        currency: Optional[str],
    ) -> None:
        super().__init__()
        self.filename = filename
        self.currency = currency
        self.account_id = account_id
        self.bank_id = bank_id
        self.branch_id = branch_id
        self.account_type = account_type

    def parse(self) -> Statement:
        stmt = super().parse()
        stmt.currency = self.currency
        stmt.account_id = self.account_id
        stmt.bank_id = self.bank_id
        stmt.branch_id = self.branch_id
        stmt.account_type = self.account_type
        return stmt

    def split_records(self) -> Iterable[Dict[str, str]]:
        with open(self.filename, "rt") as f:
            yield from DictReader(f)

    def parse_record(self, line: Dict[str, str]) -> StatementLine:
        """Parse given transaction line and return StatementLine object"""
        sl = StatementLine()

        sl.id = line["TransferWise ID"]
        sl.date = datetime.strptime(line["Date Time"], "%d-%m-%Y %H:%M:%S.%f")
        sl.memo = line["Description"]
        sl.amount = Decimal(line["Amount"])

        currency = line["Currency"]
        if self.currency is None:
            self.currency = currency
        elif self.currency != currency:
            raise ValueError(
                f"Expected transactions in the {self.currency} currency only, but got one the {currency} currency"
            )

        sl.memo = self._make_memo(line)

        payee_acc_no = line["Payee Account Number"]
        if payee_acc_no:
            sl.bank_account_to = BankAccount("", payee_acc_no)

        assert sl.amount is not None
        sl.trntype = line["Transaction Type"]
        return sl

    def _make_memo(self, line: Dict[str, str]) -> str:
        descr = line["Description"]
        payref = line["Payment Reference"]
        exc_from = line["Exchange From"]
        exc_to = line["Exchange To"]
        exc_rate = line["Exchange Rate"]

        memo = descr
        if payref:
            memo += f" ({payref})"
        if exc_from and exc_to and exc_rate:
            memo += f", {exc_rate} {exc_from}/{exc_to}"
        return memo
