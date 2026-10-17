---
name: month-end-close
description: >
  Run, document, or review a structured month-end close process. Use when an accountant
  says "help me with month-end close", "close checklist", "end of month tasks",
  "what do I need to do to close the books", "journal entries for close", "reconciliation
  checklist", "accruals and prepaids", "intercompany eliminations", "trial balance
  review", "close sign-off", or anything related to closing a financial period.
  Also trigger when someone is preparing for a quarterly or year-end close and needs
  a structured approach - even if they don't say "month-end close" explicitly.
---

## Overview

Based on **"Intermediate Accounting"** by Kieso, Weygandt, and Warfield - the definitive reference for GAAP-compliant period-end accounting. Month-end close is not a checklist of tasks; it is a controlled process that ensures the financial statements for the period are complete, accurate, and consistent with prior periods.

The principle: close in the right order. Work from operational accounts inward to the general ledger. Reconcile before you close. Review before you certify.

## Workflow

### Step 1: Pre-close - collect and cut off

Before posting any entries, establish a clean cutoff.

```
Revenue cutoff date: [date] - no revenue after this date posts to the current period
AP cutoff: [date] - all invoices received by this date must be accrued if not yet posted
Payroll cutoff: [date] - confirm last pay date and any accrued but unpaid wages
Inventory cutoff: [date] - confirm no receiving or shipping activity after cutoff
```

Actions:
- Communicate cutoff dates to operations, AP, and payroll before period end
- Pull a list of open POs and confirm which have been received (goods received, not yet invoiced = accrual needed)
- Confirm bank activity through the last business day of the period

### Step 2: Post adjusting journal entries

Work through the standard recurring entries in this order:

**Accruals (expenses incurred, not yet invoiced)**
```
DR: [Expense account]          $[amount]
    CR: Accrued Liabilities        $[amount]
Basis: [contract / estimate / PO / schedule]
```

**Prepaids (expenses paid in advance, to be amortized)**
```
DR: [Expense account]          $[amount]
    CR: Prepaid [Asset]            $[amount]
Basis: Monthly amortization of [insurance / rent / software / etc.]
```

**Depreciation**
```
DR: Depreciation Expense       $[amount]
    CR: Accumulated Depreciation   $[amount]
Basis: Fixed asset schedule, [straight-line / declining balance]
```

**Deferred revenue (cash received, revenue not yet earned)**
```
DR: Deferred Revenue           $[amount]
    CR: Revenue                    $[amount]
Basis: Performance obligation satisfied per ASC 606
```

**Intercompany eliminations (consolidated entities only)**
```
DR: Intercompany Revenue / Payable     $[amount]
    CR: Intercompany Expense / Receivable  $[amount]
Confirm: Intercompany balances agree between entities before eliminating
```

### Step 3: Reconcile key balance sheet accounts

Every material balance sheet account needs a reconciliation. Complete these before closing:

| Account | Reconcile To | Tolerance |
|---|---|---|
| Cash | Bank statement + outstanding items | $0 |
| Accounts Receivable | Aging report | $0 |
| Prepaid expenses | Prepaid schedule | $0 |
| Fixed assets | Fixed asset register | $0 |
| Accounts payable | AP subledger / aging | $0 |
| Accrued liabilities | Accrual schedule | $0 |
| Deferred revenue | Deferred revenue schedule | $0 |
| Intercompany | Agreed balances with counterparty | $0 |

For each reconciliation, document:
```
Account: [name and GL code]
Book balance per GL: $[amount]
Balance per supporting schedule / subledger: $[amount]
Difference: $[amount]
Explanation of difference (if any): [explanation]
Preparer: [name]   Date: [date]
Reviewer: [name]   Date: [date]
```

### Step 4: Review the trial balance

Pull the unadjusted and adjusted trial balance. Review for:

- Any account with an unexpected balance direction (e.g., a credit balance in an asset account)
- Any account with a zero balance that normally has activity (may indicate a posting error)
- Any account with a balance much larger or smaller than prior periods (investigate outliers >10% variance without a known explanation)
- Revenue and COGS alignment - gross margin should be within expected range

Flag any unexplained variance over $[threshold] for investigation before certifying close.

### Step 5: Produce the close package and certify

Compile the close package for review and sign-off:

```
PERIOD-END CLOSE PACKAGE - [Month / Year]

1. Income Statement - current month and YTD, with prior year comparison
2. Balance Sheet - end of period, with prior month comparison
3. Cash Flow Statement - current month
4. Reconciliation sign-off matrix (all accounts, preparer + reviewer initials)
5. Journal entry log - all entries posted in the period with supporting docs
6. Open items / exceptions - anything posted with an estimate or pending resolution
7. Key metric summary - gross margin %, headcount costs, top 5 variances vs. budget

Sign-off:
Preparer: _________________   Date: _______
Controller / Reviewer: _____   Date: _______
CFO (if required): _________   Date: _______
```

Do not certify close if any balance sheet reconciliation is open, any unexplained variance over threshold is unresolved, or any required journal entry is missing.

## Anti-Patterns

**1. Closing before reconciling**
Bad: Running the income statement and signing off before completing balance sheet reconciliations.
Good: Reconcile first, close second. If a reconciliation reveals an error, the income statement changes. Sequence matters.

**2. Accruals without documentation**
Bad: Posting an accrual for "estimated legal fees - $50K" with no supporting basis.
Good: Every accrual needs a basis: a contract, a PO, an invoice, an email, or a calculation. "Management estimate" without support will not survive an audit.

**3. Ignoring intercompany**
Bad: Allowing intercompany receivables and payables to differ between entities before elimination.
Good: Agree intercompany balances before month-end. Unreconciled intercompany creates a fictitious asset or liability that distorts the consolidated balance sheet.

**4. Posting adjustments after close**
Bad: Allowing operations to post invoices or receipts after the cutoff date into the closed period.
Good: Hard-lock the period in the ERP after close. All late items go to the next period with a documented reason.

**5. Close package without prior period comparison**
Bad: Presenting a single-period income statement with no prior period context.
Good: Every close package should include at minimum a prior month and prior year column. A number without context cannot be reviewed.

## Quality Checklist

- [ ] Cutoff dates communicated and documented before period end
- [ ] All recurring journal entries posted with supporting documentation
- [ ] All material balance sheet accounts reconciled (no open reconciliations)
- [ ] Trial balance reviewed for unexpected balances and outliers
- [ ] Intercompany balances agreed between entities (if applicable)
- [ ] Close package includes income statement, balance sheet, and cash flow
- [ ] Prior period comparison included in the package
- [ ] Open items and exceptions documented with owner and resolution date
- [ ] Formal sign-off from preparer and reviewer before certifying close
- [ ] Period locked in ERP after sign-off
