# Banking and Gradebook Systems

Two standalone Python OOP systems built to demonstrate clean domain modeling, precise business-rule handling, and thorough unit testing.

## Projects

### 1. Bank Account System (`assignment1_bank_system/`)

A bank account and transaction engine supporting checking and savings accounts.

- Checking accounts: no minimum balance, 10 free transactions/month then a $2.50 fee
- Savings accounts: $100 minimum balance, 2% monthly interest, capped at 5 withdrawals/month
- Deposits, withdrawals, and atomic transfers between accounts
- Full transaction history with success/failure reasons and monthly statement generation
- Currency handled with `Decimal` throughout

### 2. Student Gradebook (`assignment2_gradebook/`)

A gradebook system that tracks assignments across weighted categories and computes course grades and GPA.

- Weighted categories (homework, quizzes, midterm, final exam) with renormalization when a category has no assignments
- Course grade and letter grade calculation, GPA weighted by credit hours
- Per-student transcript rendering as an ASCII table

## Tech Stack

- Python 3.9+
- `Decimal` for currency-safe, precision-safe math
- `Enum` for account types, transaction types, and letter grades
- `pytest` for unit tests

## Running Each Project

```bash
cd assignment1_bank_system   # or assignment2_gradebook
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m pytest tests -v
python demo.py
```

Each project folder has its own README with more setup detail, sample input/output, and documented assumptions.
