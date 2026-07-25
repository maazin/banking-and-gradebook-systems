from decimal import Decimal
from decimal import ROUND_HALF_UP
from typing import Dict, List, Optional
from datetime import datetime
from .account import Account, AccountType
from .transaction import Transaction, TransactionStatus, TransactionType

"""Enforces all account type business rules for every transcation"""
class Bank:
    CHECKING_TRANSACTION_FEE = Decimal("2.50")
    SAVINGS_MINIMUM_BALANCE = Decimal("100.00")
    SAVINGS_MONTHLY_INTEREST = Decimal("0.02")
    DECIMAL_QUANTIZER = Decimal("0.01")

    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self._next_account_number = 1001
    
    def open_account(self, customer_name:str, account_type: AccountType, intial_deposit) -> Account:
        if not isinstance(account_type, AccountType):
            raise ValueError("Invalid account type")
        
        if not customer_name or not customer_name.strip():
            raise ValueError("customer_name is required")

        initial_deposit = self._to_money(intial_deposit)
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
        if account_type == AccountType.SAVINGS and initial_deposit < self.SAVINGS_MINIMUM_BALANCE:
            raise ValueError("Savings accounts require a minimum initial deposit of 100.00")

        account_number = str(self._next_account_number)
        self._next_account_number += 1

        account = Account(account_number, customer_name, account_type, initial_deposit)
        self.accounts[account_number] = account
        return account

    def close_account(self, account_number:str) -> bool:
        account = self.accounts.get(account_number)
        if account is None:
            raise ValueError(f'Account {account_number} does not exist')
        if account.balance != 0:
            return False
        del self.accounts[account_number]
        return True

    def deposit(self, account_number:str, amount) -> Transaction:
        account = self.accounts.get(account_number)
        amount_value = self._to_money(amount)
        if account is None:
            return self._failed_transaction(
                transaction_type=TransactionType.DEPOSIT,
                amount=amount_value,
                balance_before=Decimal("0.00"),
                reason="Account not found",
                account_number=account_number,
            )

        preview = self._preview_transaction(account, amount_value, is_withdrawal=False)
        if not preview["ok"]:
            return self._failed_transaction(
                transaction_type=TransactionType.DEPOSIT,
                amount=amount_value,
                balance_before=account.balance,
                reason=preview["reason"],
                account_number=account.account_number,
            )

        transactions = self._apply_previewed_transaction(
            account=account,
            transaction_type=TransactionType.DEPOSIT,
            amount=amount_value,
            preview=preview,
        )
        return transactions[0]

    def withdraw(self, account_number:str, amount) -> Transaction:
        account = self.accounts.get(account_number)
        amount_value = self._to_money(amount)
        if account is None:
            return self._failed_transaction(
                transaction_type=TransactionType.WITHDRAWAL,
                amount=amount_value,
                balance_before=Decimal("0.00"),
                reason="Account not found",
                account_number=account_number,
            )

        preview = self._preview_transaction(account, amount_value, is_withdrawal=True)
        if not preview["ok"]:
            return self._failed_transaction(
                transaction_type=TransactionType.WITHDRAWAL,
                amount=amount_value,
                balance_before=account.balance,
                reason=preview["reason"],
                account_number=account.account_number,
            )

        transactions = self._apply_previewed_transaction(
            account=account,
            transaction_type=TransactionType.WITHDRAWAL,
            amount=amount_value,
            preview=preview,
            is_withdrawal=True,
        )
        return transactions[0]

    def transfer(self, from_account_number:str,to_account_number:str, amount) -> Transaction:
        from_account = self.accounts.get(from_account_number)
        to_account = self.accounts.get(to_account_number)
        amount_value = self._to_money(amount)

        if from_account is None:
            failed = self._failed_transaction(
                transaction_type=TransactionType.TRANSFER,
                amount=amount_value,
                balance_before=Decimal("0.00"),
                reason="From account not found",
                account_number=from_account_number,
                related_account=to_account_number,
            )
            return failed

        if from_account_number == to_account_number:
            failed = self._failed_transaction(
                transaction_type=TransactionType.TRANSFER,
                amount=amount_value,
                balance_before=from_account.balance,
                reason="Self-transfer is not allowed",
                account_number=from_account_number,
                related_account=to_account_number,
            )
            return failed

        if to_account is None:
            failed = self._failed_transaction(
                transaction_type=TransactionType.TRANSFER,
                amount=amount_value,
                balance_before=from_account.balance,
                reason="To account not found",
                account_number=from_account_number,
                related_account=to_account_number,
            )
            return failed

        from_preview = self._preview_transaction(from_account, amount_value, is_withdrawal=True)
        if not from_preview["ok"]:
            failed = self._failed_transaction(
                transaction_type=TransactionType.TRANSFER,
                amount=amount_value,
                balance_before=from_account.balance,
                reason=from_preview["reason"],
                account_number=from_account.account_number,
                related_account=to_account.account_number,
            )
            return failed

        to_preview = self._preview_transaction(to_account, amount_value, is_withdrawal=False)
        if not to_preview["ok"]:
            failed = self._failed_transaction(
                transaction_type=TransactionType.TRANSFER,
                amount=amount_value,
                balance_before=from_account.balance,
                reason=to_preview["reason"],
                account_number=from_account.account_number,
                related_account=to_account.account_number,
            )
            return failed
        
        from_transactions = self._apply_previewed_transaction(
            account=from_account,
            transaction_type=TransactionType.TRANSFER,
            amount=amount_value,
            preview=from_preview,
            is_withdrawal=True,
            related_account=to_account.account_number,
        )
        to_transactions = self._apply_previewed_transaction(
            account=to_account,
            transaction_type=TransactionType.TRANSFER,
            amount=amount_value,
            preview=to_preview,
            related_account=from_account.account_number,
        )
        return from_transactions[0] #debit part is the transaction of record for the transfer

    def apply_monthly_interest(self) -> List[Transaction]:
        transactions: List[Transaction] = []
        for account in self.accounts.values():
            if account.account_type != AccountType.SAVINGS:
                continue

            balance_before = account.balance
            interest_amount = self._to_money(balance_before * self.SAVINGS_MONTHLY_INTEREST)
            balance_after = balance_before + interest_amount

            transaction = Transaction.create(
                type=TransactionType.INTEREST,
                amount=interest_amount,
                balance_before=balance_before,
                balance_after=balance_after,
                status=TransactionStatus.SUCCESS,
                reason="Monthly savings interest",
                account_number=account.account_number,
            )
            account.balance = balance_after
            account.transaction_history.append(transaction)
            transactions.append(transaction)

        return transactions

    def reset_monthly_counters(self) -> None:
        for account in self.accounts.values():
            account.monthly_transaction_count = 0
            account.monthly_withdrawal_count = 0

    def generate_monthly_statement(self, account_number: str) -> str:
        account = self.accounts.get(account_number)
        if account is None:
            return "Account not found"

        lines = [
            f"Monthly Statement for Account {account.account_number}",
            f"Customer: {account.customer_name}",
            f"Account Type: {account.account_type.value}",
            f"Current Balance: {account.balance:.2f}",
            "Transactions:",
        ]

        if not account.transaction_history:
            lines.append("No transactions.")
        else:
            lines.extend(str(transaction) for transaction in account.transaction_history)

        lines.append(f"Ending Balance: {account.balance:.2f}")
        return "\n".join(lines)

    def get_transaction_history(self, account_number: str, start_date=None, end_date=None) -> List[Transaction]:
        account = self.accounts.get(account_number)
        if account is None:
            return []

        history = account.transaction_history
        if start_date is not None:
            history = [transaction for transaction in history if transaction.timestamp >= start_date]
        if end_date is not None:
            history = [transaction for transaction in history if transaction.timestamp <= end_date]
        return list(history)

    def _to_money(self, amount) -> Decimal:
        return Decimal(str(amount)).quantize(self.DECIMAL_QUANTIZER, rounding=ROUND_HALF_UP)

    def _checking_fee(self, account: Account) -> Decimal:
        if account.account_type == AccountType.CHECKING and account.monthly_transaction_count >= 10:
            return self.CHECKING_TRANSACTION_FEE
        return Decimal("0.00")

    def _preview_transaction(self, account: Account, amount: Decimal, is_withdrawal: bool) -> dict:
        if amount <= 0:
            return {"ok": False, "reason": "Amount must be positive"}

        fee = self._checking_fee(account)
        balance_before = account.balance
        balance_after_base = balance_before - amount if is_withdrawal else balance_before + amount

        if account.account_type == AccountType.SAVINGS and is_withdrawal:
            if account.monthly_withdrawal_count >= 5:
                return {"ok": False, "reason": "Savings withdrawal limit reached"}
            if balance_after_base < self.SAVINGS_MINIMUM_BALANCE:
                return {"ok": False, "reason": "Savings accounts must maintain a minimum balance of 100.00"}

        if balance_after_base < 0:
            return {"ok": False, "reason": "Transaction would result in a negative balance"}
        
        balance_after = balance_after_base - fee

        return {
            "ok": True,
            "balance_before": balance_before,
            "balance_after_base": balance_after_base,
            "balance_after": balance_after,
            "fee": fee,
        }

    def _apply_previewed_transaction(
        self,
        account: Account,
        transaction_type: TransactionType,
        amount: Decimal,
        preview: dict,
        is_withdrawal: bool = False,
        related_account: Optional[str] = None,
    ) -> List[Transaction]:
        transactions: List[Transaction] = []

        base_transaction = Transaction.create(
            type=transaction_type,
            amount=amount,
            balance_before=preview["balance_before"],
            balance_after=preview["balance_after_base"],
            status=TransactionStatus.SUCCESS,
            account_number=account.account_number,
            related_account=related_account,
        )
        account.transaction_history.append(base_transaction)
        transactions.append(base_transaction)

        if account.account_type == AccountType.CHECKING:
            account.monthly_transaction_count += 1

        if is_withdrawal and account.account_type == AccountType.SAVINGS:
            account.monthly_withdrawal_count += 1

        account.balance = preview["balance_after_base"]

        if preview["fee"] > 0:
            fee_transaction = Transaction.create(
                type=TransactionType.FEE,
                amount=preview["fee"],
                balance_before=preview["balance_after_base"],
                balance_after=preview["balance_after"],
                status=TransactionStatus.SUCCESS,
                reason="Monthly checking transaction fee",
                account_number=account.account_number,
                related_account=related_account,
            )
            account.balance = preview["balance_after"]
            account.transaction_history.append(fee_transaction)
            transactions.append(fee_transaction)

        return transactions

    def _failed_transaction(
        self,
        transaction_type: TransactionType,
        amount: Decimal,
        balance_before: Decimal,
        reason: str,
        account_number: str,
        related_account: Optional[str] = None,
    ) -> Transaction:
        transaction = Transaction.create(
            type=transaction_type,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_before,
            status=TransactionStatus.FAILED,
            reason=reason,
            account_number=account_number,
            related_account=related_account,
        )

        account = self.accounts.get(account_number)
        if account is not None:
            account.transaction_history.append(transaction)

        return transaction
