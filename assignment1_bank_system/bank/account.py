from decimal import Decimal
from enum import Enum

class AccountType(Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"

class Account:
    def __init__(self, account_number, customer_name, account_type, initial_deposit):
        self.account_number = account_number
        self.balance = Decimal(str(initial_deposit))

    def __repr__(self):
        return (
            f"Account(account_number={self.account_number!r})"
        )
