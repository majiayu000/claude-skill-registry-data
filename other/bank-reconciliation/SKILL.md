---
name: bank-reconciliation
displayName: Bank Reconciliation
tagline: Automate bank reconciliation by matching transactions across bank feeds and accounting records.
description: |
  Automates the bank reconciliation process by matching transactions
  from bank feeds with accounting records in QuickBooks or Xero.
  Identifies unmatched transactions, suggests matches for review,
  and flags discrepancies. Reduces manual reconciliation time and
  improves financial accuracy.
department:
  - Finance
  - Accounting
use_cases:
  - Bank Reconciliation
  - Financial Accuracy
  - Month-end Close
tools_required:
  - QuickBooks MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Reconcile the operating account for April 2026.
  Flag any transactions that don't match.
exampleOutput: |
  Bank Reconciliation — Operating Account, April 2026

  SUMMARY
  Bank Balance:        $284,500
  Book Balance:        $283,200
  Difference:          $1,300

  MATCHED
  Auto-matched:        342 transactions (96%)
  Manual match needed: 12 transactions

  UNMATCHED — BANK ONLY
  Apr 15: $800 — Wire transfer (unknown sender)
  Apr 22: $500 — ACH credit (no matching invoice)

  UNMATCHED — BOOKS ONLY
  Apr 18: $420 — Vendor payment (check not yet cleared)
  Apr 28: $180 — Subscription charge (pending bank post)

  STATUS: 4 items need review to close reconciliation
---

# Bank Reconciliation

Automate bank reconciliation by matching transactions across bank feeds and accounting records.

**Integrations:** QuickBooks

## When to Use

- Month-end reconciliation needs to be completed
- Transaction discrepancies need investigation
- The user mentions "bank reconciliation", "reconcile", or "month-end close"

## Steps

### Step 1: Import Transactions

Pull bank feed and accounting records for the period.

### Step 2: Auto-match Transactions

Match transactions by amount, date, and reference number.

### Step 3: Flag Discrepancies

Identify unmatched items and suggest potential matches.

### Step 4: Close Reconciliation

Resolve remaining items and finalize the reconciliation.

## Output

Deliver:
- Reconciliation summary with match rate
- Unmatched transaction lists
- Recommended actions for discrepancies
