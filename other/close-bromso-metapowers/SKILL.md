---
description: Close temporary accounts and transfer balances to retained earnings
---

# Close

Close temporary accounts for "$ARGUMENTS". Zero out revenue, expense, and dividend accounts by transferring their balances to retained earnings.

## Prerequisites

Read `.metapowers/accounting/$ARGUMENTS/07-statements.md` for the financial statements and `.metapowers/accounting/$ARGUMENTS/06-adjusted-balance.md` for the adjusted trial balance.

## Process

1. **Close revenue accounts:**
   - Debit each revenue account for its full balance
   - Credit Income Summary for the total revenue
   - All revenue accounts should now have zero balances

2. **Close expense accounts:**
   - Credit each expense account for its full balance
   - Debit Income Summary for the total expenses
   - All expense accounts should now have zero balances

3. **Close Income Summary:**
   - If Income Summary has a credit balance (net income): debit Income Summary, credit Retained Earnings
   - If Income Summary has a debit balance (net loss): credit Income Summary, debit Retained Earnings
   - Income Summary should now have a zero balance

4. **Close dividends/draws:**
   - Credit Dividends (or Owner's Draws) for its full balance
   - Debit Retained Earnings
   - Dividends account should now have a zero balance

5. **Prepare post-closing trial balance:**
   - List only permanent accounts (assets, liabilities, equity)
   - Verify debits equal credits
   - These balances become the opening balances for the next period

6. **Write the artifact** to `.metapowers/accounting/$ARGUMENTS/08-close.md` with sections:
   - **Closing Journal Entries** — all closing entries with accounts and amounts
   - **Post-Closing Trial Balance** — permanent accounts only
   - **Period Summary** — net income transferred, dividends closed, ending retained earnings

## Output

The closing entries written to `.metapowers/accounting/$ARGUMENTS/08-close.md`. Present a summary highlighting:
- Net income transferred to retained earnings
- Ending retained earnings balance
- Confirmation that all temporary accounts are zeroed
