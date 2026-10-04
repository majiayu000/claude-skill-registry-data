---
description: Identify and review financial transactions from source documents
---

# Analyze

Analyze financial transactions for "$ARGUMENTS". Review source documents, identify events with financial impact, and determine which accounts are affected.

## Prerequisites

None — this is the first phase.

## Process

1. **Gather source documents:**
   - What type of entity is this? (sole proprietorship, LLC, corporation, nonprofit)
   - What accounting period are we covering?
   - Collect invoices, receipts, bank statements, contracts, and payroll records
   - Identify the chart of accounts in use (or create one)

2. **Classify transactions:**
   - For each document, determine the transaction date and amount
   - Identify which accounts are affected (assets, liabilities, equity, revenue, expenses)
   - Determine whether each account increases or decreases
   - Flag any unusual or complex transactions requiring further review

3. **Assess accounting basis:**
   - Is the entity using cash basis or accrual basis?
   - Are there any special recognition rules (percentage-of-completion, subscription revenue, etc.)?
   - Note any multi-currency or intercompany considerations

4. **Write the artifact** to `.metapowers/accounting/$ARGUMENTS/01-analyze.md` with sections:
   - **Entity Profile** — type, size, industry, accounting basis
   - **Chart of Accounts** — account categories and numbering
   - **Transaction Register** — chronological list of transactions with accounts affected
   - **Flags & Notes** — unusual items, open questions, items needing further documentation

## Output

The analysis written to `.metapowers/accounting/$ARGUMENTS/01-analyze.md`. Present a summary highlighting:
- Number of transactions identified
- Account categories involved
- Any flagged items requiring attention
