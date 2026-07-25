##Account
- Fields: accountNumber, customerName, accountType, balance, transactionHistory, monthlyTransactionCount, monthlyWithdrawalCount
- Checking: no minimum balance, monthlyTtansactionCount drives 10 free/$2.50
- Savings: $100 minimum balance, monthlyWithdrawalCount drives 5/month cap, 2% monthly interest

##transfer (from,to, amount):
- composed of debit part (withdrawal  process) from and credit part (deposit process) to, validate both the accounts and all rules for both parts before chaging the balance of either accounts.
- Each part increments its own account's monthlyTransactionCount if that account is CHECKING
- Debit part always increments monthlyWithdrawals if 'from' is SAVINGS, and is blocked by the same 5/month + $100 minimum check as withdraw()
- If "to" doesn't exist: fail whole transfer before touching "from" 

## How to handle monthly resets
- Reset explictly Bank.resetMonthlyCounters(), called once a month alongside applyMonthlyInterest() and not lazy/per-transaction reset
