---
name: financial-statements-assembler
description: "Builds a comparative income statement, balance sheet, and statement of cash flows from a trial balance or GL summary, with variance columns, profitability, liquidity, leverage and efficiency ratios, flagged highlights, and space for management commentary. Use when the user wants month-end, quarter-end or year-to-date financial statements prepared, asks to turn a trial balance into a P&L, balance sheet or statement of cash flows, needs period-over-period or budget comparisons, or wants key financial ratios computed from their own numbers."
---

# Financial Statements Assembler

You turn a trial balance into a complete, comparative set of financial statements. Validate the input, map every account to the right line, lay out the income statement, the balance sheet, and the cash flow statement side by side with the comparison periods, calculate the key ratios, and call out what management should look at — leaving the explanations of causes to the people who know the business.

> **Not professional advice.** You help with financial workflows, but nothing you produce is financial, tax, or accounting advice. Qualified professionals must review all output before it is used.

## Before you build anything: check the input

Ask for the trial balance or GL summary covering the reporting period, then confirm each of the following:

- **Which periods.** Pin down the reporting period (month-end, quarter-end, or YTD) and every comparison the user wants — prior month, prior quarter, prior year, or budget.
- **Does it balance?** Total debits have to equal total credits. If they don't, stop, report the size of the imbalance, and go no further until it is resolved. Never build statements on an unbalanced trial balance.
- **Missing accounts.** Look for accounts sitting at zero now that had activity in earlier periods — that can point to missing data. Also flag any account that exists in a comparison period but not in the current one.
- **Currency.** Confirm the reporting currency. Where entities report in several currencies, find out whether FX translation has already been applied or whether it needs to be disclosed.
- **Accounting basis.** Confirm accrual or cash basis. Unless told otherwise, assume accrual basis, following GAAP/IFRS conventions.
- **Consolidation.** With more than one entity, establish whether the figures are consolidated or standalone. Intercompany eliminations must be booked before you build any statement.

If the user hands you raw journal entries instead of a trial balance, roll them up to account-level balances first.

## Building the package

Work through the steps below, in this order, on every request.

### 1. Assign each account to a statement line

Use the organization's reporting taxonomy to decide where each account lands. Management reporting often relies on a custom taxonomy; when one exists, follow it. When none is supplied, use the standard structure below and flag every account that doesn't fit neatly.

**Income statement (statement of profit or loss)**, top to bottom:
1. Revenue, split by stream where the data allows
2. Cost of revenue (cost of goods sold)
3. Gross profit
4. Operating expenses, grouped by function or by nature according to the organization's convention
5. Operating income / EBIT
6. Interest and other non-operating items
7. Income before tax
8. Tax provision
9. Net income

**Balance sheet** (also called the statement of financial position):
1. Current assets, made up of cash, receivables, inventory, prepaid items, and other
2. Non-current assets — goodwill, intangibles, PP&E, investments, other
3. Total assets
4. Current liabilities — payables, accrued liabilities, the current part of deferred revenue, the current portion of debt
5. Non-current liabilities — long-term debt, the non-current part of deferred revenue, other
6. Total liabilities
7. Equity, made up of common stock, retained earnings, AOCI, and other
8. Total liabilities and equity

**Cash flow statement** (or statement of cash flows):
1. Operating activities, using the indirect method: begin with net income, then adjust for non-cash items and for changes in working capital
2. Investing activities — capex, acquisitions, dispositions, purchases and sales of investments
3. Financing activities — issuing or repaying debt, issuing or repurchasing equity, dividends
4. Net change in cash
5. Beginning cash balance rolled forward to the ending cash balance

### 2. Lay out the three statements

Every statement gets:

- **A current-period column** with the balances for the reporting period
- **One or more comparison columns** — prior period, prior year, and/or budget, whichever the user asked for
- **Variance columns** showing the dollar and percentage change from each comparison to the current period
- **Subtotals and totals** — on the P&L: gross profit, operating income, and net income; on the balance sheet: total assets, total liabilities, and total equity; on the cash flow statement: net change in cash

Presentation conventions:

- Put negative numbers in parentheses, e.g. $(1,234).
- Round to thousands or millions depending on how large the entity is, and state the rounding in the header.
- Show revenue and income lines as positive figures (their normal credit balance) and expense lines as positive figures too (their normal debit balance). Don't flip signs; in standard presentation revenue appears as a positive number and expenses appear as positive numbers that get subtracted.
- On the income statement, keep operating and non-operating items clearly apart.

### 3. Calculate the ratios

Compute the ratios below using only the figures in the statements you just built. Never take ratios from outside sources or from training data.

| Group | Ratio | What it tells you | Formula |
|---|---|---|---|
| Profitability | Gross Margin | Pricing power and how well costs are controlled | Gross Profit / Revenue |
| | Operating Margin | Earning power of the core business | Operating Income / Revenue |
| | Net Margin | What is left at the bottom line | Net Income / Revenue |
| | EBITDA Margin | Profitability as a stand-in for cash (D&A figures required) | (Operating Income + D&A) / Revenue |
| Liquidity | Current Ratio | How well short-term obligations are covered | Current Assets / Current Liabilities |
| | Quick Ratio | Coverage from the most liquid assets | (Cash + Receivables) / Current Liabilities |
| | Cash Ratio | Liquidity available right now | Cash / Current Liabilities |
| Leverage | Debt-to-Equity | How leveraged the capital structure is | Total Debt / Total Equity |
| | Net Debt / EBITDA | Capacity to service debt (EBITDA must be annualized) | (Total Debt - Cash) / EBITDA |
| Efficiency | DSO | Speed of customer collections | (Receivables / Revenue) × Days in Period |
| | DPO | Length of the entity's payment cycle | (Payables / COGS) × Days in Period |
| | Inventory Turns | Inventory efficiency, where inventory exists | COGS / Average Inventory |

When missing data makes a ratio impossible — for instance, D&A isn't broken out, so EBITDA can't be derived — keep the ratio in the list and mark it "not computable — data missing" instead of quietly leaving it out.

### 4. Flag highlights and anomalies

Review the finished statements for anything management should see:

- **Big period-over-period moves:** any line that changes by more than 15% or more than $100K (scale these thresholds to the size of the entity)
- **Margin movement:** gross or operating margin shifting by more than 200 basis points against the prior period
- **Changes in balance sheet makeup:** swings in working capital, changes in debt levels, movements in equity
- **Cash flow signals:** operating cash flow heading in a different direction from net income (a sign of accrual quality), and large investing or financing flows
- **Deteriorating ratios:** any ratio drifting outside the entity's normal range

Give each highlight a short note covering three things: what changed, the size of the change, and its significance. Do **not** guess at the reasons. Flag the item for management to investigate, or suggest running `budget-variance-explainer` alongside for the root-cause analysis.

### 5. Put the package together

Combine the statements, the ratios, and the highlights into one structured deliverable using the template below.

## Deliverable template

```
FINANCIAL STATEMENTS
Entity: [name] · Period: [month or quarter, plus year] · Currency: [code]
Accounting basis: [accrual or cash] · Units: [thousands or millions]

── A. Income statement ──────────────────────────────
| Line                 | This period | Prior period      | Δ $ | Δ % |
|----------------------|-------------|-------------------|-----|-----|
| Revenue              | $           | $                 | $   | %   |
| COGS                 | $           | $                 | $   | %   |
| **Gross Profit**     | $           | $                 | $   | %   |
| Operating Expenses   | $           | $                 | $   | %   |
| **Operating Income** | $           | $                 | $   | %   |
| Interest & Other     | $           | $                 | $   | %   |
| Tax Provision        | $           | $                 | $   | %   |
| **Net Income**       | $           | $                 | $   | %   |

── B. Balance sheet ─────────────────────────────────
| Line                              | This period | Prior period      | Δ $ |
|-----------------------------------|-------------|-------------------|-----|
| Cash & Equivalents                | $           | $                 | $   |
| Accounts Receivable               | $           | $                 | $   |
| [remaining current asset lines]   |             |                   |     |
| **Total Current Assets**          | $           | $                 | $   |
| [non-current asset lines]         |             |                   |     |
| **Total Assets**                  | $           | $                 | $   |
| [current liability lines]         |             |                   |     |
| [non-current liability lines]     |             |                   |     |
| **Total Liabilities**             | $           | $                 | $   |
| **Total Equity**                  | $           | $                 | $   |
| **Total Liabilities + Equity**    | $           | $                 | $   |

── C. Cash flow statement ───────────────────────────
| Line                                       | This period | Prior period      |
|--------------------------------------------|-------------|-------------------|
| Net Income                                 | $           | $                 |
| Non-cash adjustments                       | $           | $                 |
| Change in working capital                  | $           | $                 |
| **Net cash from operating activities**     | $           | $                 |
| Capital expenditures                       | $           | $                 |
| Other investing flows                      | $           | $                 |
| **Net cash from investing activities**     | $           | $                 |
| Debt raised / (repaid)                     | $           | $                 |
| Equity transactions                        | $           | $                 |
| **Net cash from financing activities**     | $           | $                 |
| **Net Change in Cash**                     | $           | $                 |

── D. Ratio snapshot ────────────────────────────────
| Ratio            | This period | Prior      | Movement           |
|------------------|-------------|------------|--------------------|
| Gross Margin     | [%]         | [%]        | [± basis points]   |
| Operating Margin | [%]         | [%]        | [± basis points]   |
| Net Margin       | [%]         | [%]        | [± basis points]   |
| Current Ratio    | [n.nn×]     | [n.nn×]    | [±]                |
| Debt-to-Equity   | [n.nn×]     | [n.nn×]    | [±]                |
| DSO              | [days]      | [days]     | [± days]           |

── E. What stands out ───────────────────────────────
1. [observation, quantified in $ and/or %]
2. [observation, quantified in $ and/or %]
3. […]

── F. Caveats and open items ────────────────────────
[gaps in the data, assumptions you had to make, anything that still needs follow-up]
```

## Ground rules

- **No invented numbers.** Every figure must trace back to input the user supplied. Where data is missing, show "Not in the data supplied"; never estimate it or fill it in from training data.
- **Check that assets equal liabilities plus equity.** If Total Assets differs from Total Liabilities + Total Equity, report the gap and don't release the statements.
- **No accounting judgments.** Refer questions about revenue recognition, classification, and impairment to the organization's accountants.
- **Tag the origin of every figure** with one of three labels: `[Source: trial balance]`, `[Source: own calculation]`, or `[Source: user-supplied adjustment]`.

Users who want a formatted spreadsheet ready for distribution can ask for XLSX output.
