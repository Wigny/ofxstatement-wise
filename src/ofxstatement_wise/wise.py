from csv import DictReader
from datetime import datetime
from typing import Dict, Iterable, Optional
from decimal import Decimal

from ofxstatement.plugin import Plugin
from ofxstatement.parser import StatementParser
from ofxstatement.statement import Statement, StatementLine


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
        self.running_balance: Dict[datetime, Decimal] = {}

    def parse(self) -> Statement:
        stmt = super().parse()
        stmt.currency = self.currency
        stmt.account_id = self.account_id
        stmt.bank_id = self.bank_id
        stmt.branch_id = self.branch_id
        stmt.account_type = self.account_type
        if stmt.lines:
            stmt.start_date = min(self.running_balance)
            stmt.end_date = max(self.running_balance)

            first_transaction = next(
                (l for l in stmt.lines if l.date == stmt.start_date)
            )
            assert first_transaction is not None

            stmt.start_balance = (
                self.running_balance[stmt.start_date] - first_transaction.amount
            )
            stmt.end_balance = self.running_balance[stmt.end_date]

        return stmt

    def split_records(self) -> Iterable[Dict[str, str]]:
        with open(self.filename, "rt") as f:
            yield from DictReader(f)

    def parse_record(self, line: Dict[str, str]) -> StatementLine:
        """Parse given transaction line and return StatementLine object"""
        stmt_line = StatementLine()

        stmt_line.id = line["TransferWise ID"]
        stmt_line.date = datetime.strptime(line["Date Time"], "%d-%m-%Y %H:%M:%S.%f")
        stmt_line.memo = line["Description"]
        stmt_line.amount = Decimal(line["Amount"])
        stmt_line.trntype = line["Transaction Type"]

        currency = line["Currency"]
        if self.currency is None:
            self.currency = currency
        elif self.currency != currency:
            raise ValueError(
                f"Expected transactions in the {self.currency} currency only, but got one the {currency} currency"
            )

        self.running_balance[stmt_line.date] = Decimal(line["Running Balance"])

        return stmt_line
