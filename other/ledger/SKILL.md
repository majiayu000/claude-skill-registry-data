---
description: Post journal entries to the general ledger and compute running balances
---

# Ledger

Post journal entries to the general ledger for "$ARGUMENTS". Organize all debits and credits by account and calculate running balances.

## Prerequisites

Read `.metapowers/accounting/$ARGUMENTS/02-journal.md` for the journal entries.

## Process

1. **Set up ledger accounts:**
   - Create a T-account or tabular format for each account in the chart of accounts
   - Include the account number, name, and normal balance side (debit or credit)
   - Carry forward any opening balances from the prior period

2. **Post journal entries:**
   - Transfer each journal entry to the appropriate ledger accounts
   - Record the date, journal entry reference (JE-001, etc.), and amount
   - Post debits to the debit side and credits to the credit side
   - Calculate the running balance after each posting

3. **Verify completeness:**
   - Cross-reference every journal entry to confirm it has been posted
   - Check that no entries were double-posted or missed
   - Ensure running balances are mathematically correct

4. **Write the artifact** to `.metapowers/accounting/$ARGUMENTS/03-ledger.md` with sections:
   - **General Ledger** — each account with all postings and running balance
   - **Account Summary** — closing balance for each account
   - **Cross-Reference** — journal entry to ledger posting map

## Output

The ledger written to `.metapowers/accounting/$ARGUMENTS/03-ledger.md`. Present a summary highlighting:
- Number of active accounts
- Top accounts by transaction volume
- Closing balances for key accounts
