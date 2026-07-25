from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import uuid4
from typing import Optional

class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"
    FEE = "FEE"
    INTEREST = "INTEREST"

class TransactionStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

@dataclass
class Transaction:
    transaction_id: str
    timestamp: datetime
    type: TransactionType
    amount: Decimal
    balance_before: Decimal
    balance_after: Decimal
    status: TransactionStatus
    reason: str = ""
    account_number: str = ""
    related_account: Optional[str] = None

    @staticmethod
    def create(
        type: TransactionType,
        amount: Decimal,
        balance_before: Decimal,
        balance_after: Decimal,
        status: TransactionStatus,
        reason: str = "",
        account_number: str = "",
        related_account: Optional[str] = None,
    ) -> "Transaction":
        return Transaction(
            transaction_id=str(uuid4()),
            timestamp=datetime.now(),
            type=type,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
            status=status,
            reason=reason,
            account_number=account_number,
            related_account=related_account,
        )

    def __str__(self) -> str:
        summary = f"{self.timestamp}, {self.type.value}, {self.amount}, {self.status.value}"
        if self.status == TransactionStatus.FAILED and self.reason:
            return f"{summary} ({self.reason})"
        return summary
    
