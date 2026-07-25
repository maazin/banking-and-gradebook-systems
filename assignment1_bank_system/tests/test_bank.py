import unittest
from decimal import Decimal

from bank.bank import Bank
from bank.account import AccountType
from bank.transaction import TransactionStatus, TransactionType


class BankTestCase(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()

    def test_open_checking_account_with_zero(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))

        self.assertEqual(account.account_type, AccountType.CHECKING)
        self.assertEqual(account.balance, Decimal("0.00"))
        self.assertEqual(account.account_number, "1001")

    def test_reject_savings_below_minimum(self):
        with self.assertRaises(ValueError):
            self.bank.open_account("Bob", AccountType.SAVINGS, Decimal("99.99"))

    def test_reject_blank_customer_name(self):
        with self.assertRaises(ValueError):
            self.bank.open_account("   ", AccountType.CHECKING, Decimal("0.00"))

    def test_reject_negative_initial_deposit(self):
        with self.assertRaises(ValueError):
            self.bank.open_account("Charlie", AccountType.CHECKING, Decimal("-1.00"))

    def test_deposit_increases_balance(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))

        transaction = self.bank.deposit(account.account_number, Decimal("25.00"))

        self.assertEqual(transaction.status, TransactionStatus.SUCCESS)
        self.assertEqual(account.balance, Decimal("25.00"))

    def test_deposit_zero_amount_rejected(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))

        transaction = self.bank.deposit(account.account_number, Decimal("0.00"))

        self.assertEqual(transaction.status, TransactionStatus.FAILED)
        self.assertEqual(transaction.reason, "Amount must be positive")
        self.assertEqual(account.balance, Decimal("0.00"))

    def test_deposit_negative_amount_rejected(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))

        transaction = self.bank.deposit(account.account_number, Decimal("-10.00"))

        self.assertEqual(transaction.status, TransactionStatus.FAILED)
        self.assertEqual(transaction.reason, "Amount must be positive")
        self.assertEqual(account.balance, Decimal("0.00"))

    def test_deposit_unknown_account_fails(self):
        transaction = self.bank.deposit("9999", Decimal("10.00"))

        self.assertEqual(transaction.status, TransactionStatus.FAILED)
        self.assertEqual(transaction.reason, "Account not found")

    def test_withdraw_success_within_balance(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))
        self.bank.deposit(account.account_number, Decimal("20.00"))

        transaction = self.bank.withdraw(account.account_number, Decimal("5.00"))

        self.assertEqual(transaction.status, TransactionStatus.SUCCESS)
        self.assertEqual(transaction.type, TransactionType.WITHDRAWAL)
        self.assertEqual(account.balance, Decimal("15.00"))

    def test_checking_can_withdraw_to_exactly_zero(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))
        self.bank.deposit(account.account_number, Decimal("10.00"))

        transaction = self.bank.withdraw(account.account_number, Decimal("10.00"))

        self.assertEqual(transaction.status, TransactionStatus.SUCCESS)
        self.assertEqual(account.balance, Decimal("0.00"))

    def test_checking_overdraft_is_rejected(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))

        transaction = self.bank.withdraw(account.account_number, Decimal("1.00"))

        self.assertEqual(transaction.status, TransactionStatus.FAILED)
        self.assertEqual(transaction.reason, "Transaction would result in a negative balance")
        self.assertEqual(account.balance, Decimal("0.00"))

    def test_savings_withdraw_below_minimum_is_rejected(self):
        account = self.bank.open_account("Bob", AccountType.SAVINGS, Decimal("150.00"))

        transaction = self.bank.withdraw(account.account_number, Decimal("60.00"))

        self.assertEqual(transaction.status, TransactionStatus.FAILED)
        self.assertEqual(
            transaction.reason,
            "Savings accounts must maintain a minimum balance of 100.00",
        )
        self.assertEqual(account.balance, Decimal("150.00"))

    def test_savings_withdrawal_limit_enforced(self):
        account = self.bank.open_account("Bob", AccountType.SAVINGS, Decimal("200.00"))

        for _ in range(5):
            transaction = self.bank.withdraw(account.account_number, Decimal("10.00"))
            self.assertEqual(transaction.status, TransactionStatus.SUCCESS)

        failed = self.bank.withdraw(account.account_number, Decimal("10.00"))

        self.assertEqual(failed.status, TransactionStatus.FAILED)
        self.assertEqual(failed.reason, "Savings withdrawal limit reached")
        self.assertEqual(account.balance, Decimal("150.00"))

    def test_transfer_moves_funds_between_two_accounts(self):
        source = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))
        target = self.bank.open_account("Bob", AccountType.SAVINGS, Decimal("100.00"))
        self.bank.deposit(source.account_number, Decimal("50.00"))

        transaction = self.bank.transfer(source.account_number, target.account_number, Decimal("20.00"))

        self.assertEqual(transaction.status, TransactionStatus.SUCCESS)
        self.assertEqual(transaction.type, TransactionType.TRANSFER)
        self.assertEqual(source.balance, Decimal("30.00"))
        self.assertEqual(target.balance, Decimal("120.00"))

    def test_transfer_fails_cleanly_on_insufficient_funds(self):
        source = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))
        target = self.bank.open_account("Bob", AccountType.SAVINGS, Decimal("100.00"))

        transaction = self.bank.transfer(source.account_number, target.account_number, Decimal("10.00"))

        self.assertEqual(transaction.status, TransactionStatus.FAILED)
        self.assertEqual(transaction.reason, "Transaction would result in a negative balance")
        self.assertEqual(source.balance, Decimal("0.00"))
        self.assertEqual(target.balance, Decimal("100.00"))

    def test_transfer_self_transfer_is_rejected(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))

        transaction = self.bank.transfer(account.account_number, account.account_number, Decimal("1.00"))

        self.assertEqual(transaction.status, TransactionStatus.FAILED)
        self.assertEqual(transaction.reason, "Self-transfer is not allowed")
        self.assertEqual(account.balance, Decimal("0.00"))

    def test_transfer_unknown_target_fails_without_touching_source(self):
        source = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))
        self.bank.deposit(source.account_number, Decimal("40.00"))

        transaction = self.bank.transfer(source.account_number, "9999", Decimal("10.00"))

        self.assertEqual(transaction.status, TransactionStatus.FAILED)
        self.assertEqual(transaction.reason, "To account not found")
        self.assertEqual(source.balance, Decimal("40.00"))

    def test_interest_applied_only_to_savings_account(self):
        checking = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))
        savings = self.bank.open_account("Bob", AccountType.SAVINGS, Decimal("200.00"))

        transactions = self.bank.apply_monthly_interest()

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].type, TransactionType.INTEREST)
        self.assertEqual(savings.balance, Decimal("204.00"))
        self.assertEqual(checking.balance, Decimal("0.00"))
        self.assertEqual(len(checking.transaction_history), 0)

    def test_interest_not_applied_to_checking_account(self):
        checking = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("10.00"))

        transactions = self.bank.apply_monthly_interest()

        self.assertEqual(transactions, [])
        self.assertEqual(checking.balance, Decimal("10.00"))

    def test_checking_fee_is_free_for_first_ten_transactions(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))

        for _ in range(10):
            transaction = self.bank.deposit(account.account_number, Decimal("1.00"))
            self.assertEqual(transaction.status, TransactionStatus.SUCCESS)

        self.assertEqual(account.balance, Decimal("10.00"))
        self.assertEqual(len(account.transaction_history), 10)
        self.assertTrue(all(item.type == TransactionType.DEPOSIT for item in account.transaction_history))

    def test_checking_fee_charged_separately_on_eleventh_and_later_transactions(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))

        for _ in range(10):
            self.bank.deposit(account.account_number, Decimal("1.00"))

        eleventh = self.bank.deposit(account.account_number, Decimal("1.00"))
        twelfth = self.bank.deposit(account.account_number, Decimal("1.00"))

        self.assertEqual(eleventh.status, TransactionStatus.SUCCESS)
        self.assertEqual(twelfth.status, TransactionStatus.SUCCESS)
        self.assertEqual(account.balance, Decimal("7.00"))
        self.assertEqual(account.transaction_history[-4].type, TransactionType.DEPOSIT)
        self.assertEqual(account.transaction_history[-3].type, TransactionType.FEE)
        self.assertEqual(account.transaction_history[-2].type, TransactionType.DEPOSIT)
        self.assertEqual(account.transaction_history[-1].type, TransactionType.FEE)

    def test_monthly_resets_restore_free_transactions_and_withdrawal_limits(self):
        checking = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))
        savings = self.bank.open_account("Bob", AccountType.SAVINGS, Decimal("200.00"))

        for _ in range(10):
            self.bank.deposit(checking.account_number, Decimal("1.00"))

        fee_transaction = self.bank.deposit(checking.account_number, Decimal("1.00"))
        self.assertEqual(fee_transaction.status, TransactionStatus.SUCCESS)
        self.assertEqual(checking.balance, Decimal("8.50"))

        for _ in range(5):
            withdraw_transaction = self.bank.withdraw(savings.account_number, Decimal("10.00"))
            self.assertEqual(withdraw_transaction.status, TransactionStatus.SUCCESS)

        self.bank.reset_monthly_counters()

        post_reset_deposit = self.bank.deposit(checking.account_number, Decimal("1.00"))
        post_reset_withdraw = self.bank.withdraw(savings.account_number, Decimal("10.00"))

        self.assertEqual(post_reset_deposit.status, TransactionStatus.SUCCESS)
        self.assertEqual(checking.balance, Decimal("9.50"))
        self.assertEqual(post_reset_withdraw.status, TransactionStatus.SUCCESS)
        self.assertEqual(savings.balance, Decimal("140.00"))

    def test_close_account_succeeds_at_zero_balance(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))

        closed = self.bank.close_account(account.account_number)

        self.assertTrue(closed)
        self.assertNotIn(account.account_number, self.bank.accounts)

    def test_close_account_rejected_at_nonzero_balance(self):
        account = self.bank.open_account("Alice", AccountType.CHECKING, Decimal("0.00"))
        self.bank.deposit(account.account_number, Decimal("5.00"))

        closed = self.bank.close_account(account.account_number)

        self.assertFalse(closed)
        self.assertIn(account.account_number, self.bank.accounts)


if __name__ == "__main__":
    unittest.main()
