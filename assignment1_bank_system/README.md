# Assignment 1 Bank System

## Overview

This project implements a bank account system with support for checking and savings accounts, transaction history, monthly interest, and transaction rules such as savings withdrawal limits and checking fees.

## Setup Instructions

Needs Python 3.9 or higher.

1. Open a terminal in the `assignment1_bank_system` folder.
2. Activate the virtual environment.
3. Run the unit tests.
4. Run the demo script to see sample transactions and statements.

### Example Commands

```bash
cd assignment1_bank_system
source ../venv/bin/activate
pip install -r requirements.txt
python -m pytest tests -v   #runs the tests
python demo.py              #runs the demo script
```
### Sample Input
The demo script in `demo.py` performs the following workflow:

```text
1. Create a new GradeBook/Bank system object.
2. Add 5 accounts.
    - 3 checking accounts
    - 2 savings accounts
3. Run a mix of transactions.
    - deposits
    - withdrawals
    - transfers
    - overdraft failure
    - savings minimum-balance failure
    - invalid amount failure
    - self-transfer failure
    - savings withdrawal-cap failure
4. Trigger the checking-account fee after the free transaction limit is exceeded.
5. Apply monthly interest to savings accounts.
6. Print a monthly statement for each account.
```

### Sample Output
```
Opened accounts:
Account(account_number='1001', account_type=<AccountType.CHECKING: 'CHECKING'>, balance=Decimal('0.00'))
Account(account_number='1002', account_type=<AccountType.CHECKING: 'CHECKING'>, balance=Decimal('25.00'))
Account(account_number='1003', account_type=<AccountType.CHECKING: 'CHECKING'>, balance=Decimal('0.00'))
Account(account_number='1004', account_type=<AccountType.SAVINGS: 'SAVINGS'>, balance=Decimal('150.00'))
Account(account_number='1005', account_type=<AccountType.SAVINGS: 'SAVINGS'>, balance=Decimal('200.00'))

Deposit to checking_1: 2026-07-18 23:43:22.667801, DEPOSIT, 20.00, SUCCESS
Deposit to checking_2: 2026-07-18 23:43:22.667850, DEPOSIT, 5.00, SUCCESS
Deposit to savings_1: 2026-07-18 23:43:22.667871, DEPOSIT, 25.00, SUCCESS
Withdrawal from checking_1: 2026-07-18 23:43:22.667895, WITHDRAWAL, 5.00, SUCCESS
Overdraft fail from checking_3: 2026-07-18 23:43:22.667914, WITHDRAWAL, 1.00, FAILED (Transaction would result in a negative balance)
Savings minimum balance fail: 2026-07-18 23:43:22.667934, WITHDRAWAL, 80.00, FAILED (Savings accounts must maintain a minimum balance of 100.00)
Invalid amount fail: 2026-07-18 23:43:22.667951, DEPOSIT, 0.00, FAILED (Amount must be positive)

Transfer checking_1 to savings_2: 2026-07-18 23:43:22.667978, TRANSFER, 10.00, SUCCESS
Transfer insufficient funds fail: 2026-07-18 23:43:22.668007, TRANSFER, 10.00, FAILED (Transaction would result in a negative balance)
Self-transfer fail: 2026-07-18 23:43:22.668022, TRANSFER, 1.00, FAILED (Self-transfer is not allowed)

Checking fee warm-up deposit 1: 2026-07-18 23:43:22.668043, DEPOSIT, 1.00, SUCCESS
Checking fee warm-up deposit 2: 2026-07-18 23:43:22.668061, DEPOSIT, 1.00, SUCCESS
Checking fee warm-up deposit 3: 2026-07-18 23:43:22.668083, DEPOSIT, 1.00, SUCCESS
Checking fee warm-up deposit 4: 2026-07-18 23:43:22.668102, DEPOSIT, 1.00, SUCCESS
Checking fee warm-up deposit 5: 2026-07-18 23:43:22.668119, DEPOSIT, 1.00, SUCCESS
Checking fee warm-up deposit 6: 2026-07-18 23:43:22.668134, DEPOSIT, 1.00, SUCCESS
Checking fee warm-up deposit 7: 2026-07-18 23:43:22.668149, DEPOSIT, 1.00, SUCCESS
Checking fee warm-up deposit 8: 2026-07-18 23:43:22.668164, DEPOSIT, 1.00, SUCCESS
Checking fee warm-up deposit 9: 2026-07-18 23:43:22.668178, DEPOSIT, 1.00, SUCCESS
Fee-triggering deposit: 2026-07-18 23:43:22.668194, DEPOSIT, 1.00, SUCCESS

Savings withdrawal 1: 2026-07-18 23:43:22.668220, WITHDRAWAL, 10.00, SUCCESS
Savings withdrawal 2: 2026-07-18 23:43:22.668236, WITHDRAWAL, 10.00, SUCCESS
Savings withdrawal 3: 2026-07-18 23:43:22.668251, WITHDRAWAL, 10.00, SUCCESS
Savings withdrawal 4: 2026-07-18 23:43:22.668266, WITHDRAWAL, 10.00, SUCCESS
Savings withdrawal 5: 2026-07-18 23:43:22.668282, WITHDRAWAL, 10.00, SUCCESS
Savings withdrawal cap fail: 2026-07-18 23:43:22.668297, WITHDRAWAL, 10.00, FAILED (Savings withdrawal limit reached)

Applied monthly interest:
2026-07-18 23:43:22.668529, INTEREST, 3.50, SUCCESS
2026-07-18 23:43:22.668537, INTEREST, 3.20, SUCCESS

Monthly statements:

Monthly Statement for Account 1001
Customer: Alice
Account Type: CHECKING
Current Balance: 5.00
Transactions:
2026-07-18 23:43:22.667801, DEPOSIT, 20.00, SUCCESS
2026-07-18 23:43:22.667895, WITHDRAWAL, 5.00, SUCCESS
2026-07-18 23:43:22.667951, DEPOSIT, 0.00, FAILED (Amount must be positive)
2026-07-18 23:43:22.667978, TRANSFER, 10.00, SUCCESS
Ending Balance: 5.00

Monthly Statement for Account 1002
Customer: Bob
Account Type: CHECKING
Current Balance: 37.50
Transactions:
2026-07-18 23:43:22.667850, DEPOSIT, 5.00, SUCCESS
2026-07-18 23:43:22.668022, TRANSFER, 1.00, FAILED (Self-transfer is not allowed)
2026-07-18 23:43:22.668043, DEPOSIT, 1.00, SUCCESS
2026-07-18 23:43:22.668061, DEPOSIT, 1.00, SUCCESS
2026-07-18 23:43:22.668083, DEPOSIT, 1.00, SUCCESS
2026-07-18 23:43:22.668102, DEPOSIT, 1.00, SUCCESS
2026-07-18 23:43:22.668119, DEPOSIT, 1.00, SUCCESS
2026-07-18 23:43:22.668134, DEPOSIT, 1.00, SUCCESS
2026-07-18 23:43:22.668149, DEPOSIT, 1.00, SUCCESS
2026-07-18 23:43:22.668164, DEPOSIT, 1.00, SUCCESS
2026-07-18 23:43:22.668178, DEPOSIT, 1.00, SUCCESS
2026-07-18 23:43:22.668194, DEPOSIT, 1.00, SUCCESS
2026-07-18 23:43:22.668200, FEE, 2.50, SUCCESS
Ending Balance: 37.50

Monthly Statement for Account 1003
Customer: Charlie
Account Type: CHECKING
Current Balance: 0.00
Transactions:
2026-07-18 23:43:22.667914, WITHDRAWAL, 1.00, FAILED (Transaction would result in a negative balance)
2026-07-18 23:43:22.668007, TRANSFER, 10.00, FAILED (Transaction would result in a negative balance)
Ending Balance: 0.00

Monthly Statement for Account 1004
Customer: Dana
Account Type: SAVINGS
Current Balance: 178.50
Transactions:
2026-07-18 23:43:22.667871, DEPOSIT, 25.00, SUCCESS
2026-07-18 23:43:22.667934, WITHDRAWAL, 80.00, FAILED (Savings accounts must maintain a minimum balance of 100.00)
2026-07-18 23:43:22.668529, INTEREST, 3.50, SUCCESS
Ending Balance: 178.50

Monthly Statement for Account 1005
Customer: Evan
Account Type: SAVINGS
Current Balance: 163.20
Transactions:
2026-07-18 23:43:22.667987, TRANSFER, 10.00, SUCCESS
2026-07-18 23:43:22.668220, WITHDRAWAL, 10.00, SUCCESS
2026-07-18 23:43:22.668236, WITHDRAWAL, 10.00, SUCCESS
2026-07-18 23:43:22.668251, WITHDRAWAL, 10.00, SUCCESS
2026-07-18 23:43:22.668266, WITHDRAWAL, 10.00, SUCCESS
2026-07-18 23:43:22.668282, WITHDRAWAL, 10.00, SUCCESS
2026-07-18 23:43:22.668297, WITHDRAWAL, 10.00, FAILED (Savings withdrawal limit reached)
2026-07-18 23:43:22.668537, INTEREST, 3.20, SUCCESS
Ending Balance: 163.20
```

## Assumptions

- Failed transactions don't count towards the checking free 10 limit
- A transfer counts as one transaction on each side
- Transfering out of a savings account counts as a withdrawal
- Opening a Savings account below $100 is rejected but a $0 deposit is allowed for Checking accounts.
- The fee posts as its own transaction.
- Interest is rounded to the nearest cent using Round half up.
- Monthly counters do not reset automatically. They need to be explicitly called reset_monthly_counters() and similarly for apply_monthly_interest().nce is changed so a failed transfer never leaves money in limbo. The transfer either succeeds or fails as a whole.
- Transfers are atomic and all failure checks run before either bala
- Self transfers are rejected.
- An account can only be closed at zero balance. Closing an account with a non-zero balance is rejected.

## Project Structure

```
assignment1_bank_system/
├── demo.py
├── README.md
├── DESIGN_NOTES.md
├── requirements.txt
├── bank/
│   ├── __init__.py
│   ├── account.py
│   ├── bank.py
│   └── transaction.py
└── tests/
    ├── __init__.py
    └── test_bank.py
```
### Notes

- `bank/` contains the core banking package and business logic.

- `tests/` contains the unit test suite for the assignment.

- `demo.py` runs a full sample workflow demonstrating transactions, interest, fees, and statements.
