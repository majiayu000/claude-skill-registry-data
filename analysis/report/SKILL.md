---
description: Generate profit and loss, balance sheet, and cash flow statements from reconciled data
---

# Report

Generate financial statements for "$ARGUMENTS" from reconciled data. Produce a profit and loss statement, balance sheet, and cash flow statement with trend analysis.

## Prerequisites

Read `.metapowers/bookkeeping/$ARGUMENTS/03-reconcile.md` for reconciled balances and adjusting entries.

## Process

1. **Prepare trial balance:**
   - List all accounts with their reconciled balances
   - Verify total debits equal total credits
   - Apply any period-end adjustments (accruals, deferrals, depreciation)

2. **Generate Profit & Loss (Income Statement):**
   - Revenue accounts (4000-series)
   - Less: Cost of Goods Sold (5000-series)
   - Equals: Gross Profit
   - Less: Operating Expenses (6000-series)
   - Equals: Operating Income
   - Plus/Minus: Other Income/Expenses (7000-series)
   - Equals: Net Income

3. **Generate Balance Sheet:**
   - Assets (1000-series) — current and fixed
   - Liabilities (2000-series) — current and long-term
   - Equity (3000-series) — including net income from P&L
   - Verify: Assets = Liabilities + Equity

4. **Generate Cash Flow Statement:**
   - **Operating Activities** — cash from core business
   - **Investing Activities** — asset purchases and sales
   - **Financing Activities** — loans, equity, dividends
   - Net change in cash for the period

5. **Analyze and highlight:**
   - Key ratios (gross margin, net margin, current ratio, quick ratio)
   - Period-over-period trends if prior data exists
   - Anomalies or areas of concern
   - Cash runway estimate

6. **Write the artifact** to `.metapowers/bookkeeping/$ARGUMENTS/04-report.md` with sections:
   - **Trial Balance** — all accounts with balances
   - **Profit & Loss** — full income statement
   - **Balance Sheet** — full statement of financial position
   - **Cash Flow Statement** — cash movements by category
   - **Key Ratios** — financial health indicators
   - **Commentary** — narrative on trends and concerns

## Output

The financial report written to `.metapowers/bookkeeping/$ARGUMENTS/04-report.md`. Present a summary highlighting:
- Net income/loss for the period
- Total assets and liabilities
- Cash position and runway
- Key ratios and any concerns
