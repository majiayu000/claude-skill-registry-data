---
description: Capture and log financial transactions with source documents
---

# Record

Capture and log all financial transactions for "$ARGUMENTS". Document each transaction with date, amount, parties, description, and source document reference.

## Prerequisites

None — this is the first phase.

## Process

1. **Identify transaction sources:**
   - What accounts are active? (bank, credit card, cash, digital payments)
   - What period are we recording? (month, quarter, year)
   - What source documents are available? (receipts, invoices, bank feeds, contracts)

2. **Capture each transaction:**
   - **Date** — when the transaction occurred
   - **Amount** — exact figure with currency
   - **Direction** — inflow (revenue, loan) or outflow (expense, payment)
   - **Counterparty** — who paid or was paid
   - **Description** — what the transaction was for
   - **Source** — receipt number, invoice ID, or bank reference
   - **Payment method** — bank transfer, card, cash, etc.

3. **Organize the transaction log:**
   - Sort chronologically
   - Flag any transactions missing source documents
   - Note any unusual or large transactions for review
   - Identify recurring transactions (subscriptions, rent, payroll)

4. **Write the artifact** to `.metapowers/bookkeeping/$ARGUMENTS/01-record.md` with sections:
   - **Period** — date range covered
   - **Transaction Log** — table of all transactions
   - **Missing Documents** — transactions without source references
   - **Flags** — unusual items requiring review

## Output

The transaction log written to `.metapowers/bookkeeping/$ARGUMENTS/01-record.md`. Present a summary highlighting:
- Total transactions recorded
- Total inflows and outflows
- Any missing documents or flagged items
