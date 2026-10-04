---
description: Record journal entries with debits and credits for each transaction
---

# Journal

Record journal entries for "$ARGUMENTS". Convert analyzed transactions into formal double-entry journal entries with equal debits and credits.

## Prerequisites

Read `.metapowers/accounting/$ARGUMENTS/01-analyze.md` for the transaction register and chart of accounts.

## Process

1. **Review the transaction register:**
   - Load the analysis artifact from Phase 1
   - Confirm all transactions are accounted for
   - Resolve any flagged items before journalizing

2. **Create journal entries:**
   - For each transaction, record:
     - **Date** — when the transaction occurred
     - **Accounts** — debit account(s) and credit account(s)
     - **Amounts** — debit and credit amounts (must be equal)
     - **Description** — brief explanation of the transaction
   - Number entries sequentially (JE-001, JE-002, etc.)

3. **Validate entries:**
   - Every entry must have at least one debit and one credit
   - Total debits must equal total credits for each entry
   - Verify account names match the chart of accounts
   - Flag compound entries (more than two accounts) with clear explanations

4. **Write the artifact** to `.metapowers/accounting/$ARGUMENTS/02-journal.md` with sections:
   - **General Journal** — all entries in chronological order with debit/credit columns
   - **Entry Summary** — count of entries by type (revenue, expense, asset, liability)
   - **Validation** — confirmation that all entries balance

## Output

The journal written to `.metapowers/accounting/$ARGUMENTS/02-journal.md`. Present a summary highlighting:
- Total number of journal entries
- Total debits and credits (should match)
- Any compound or noteworthy entries
