---
name: finance-manager-en
description: Use this skill for personal finance management, spending analysis, budget planning, cash-flow review, savings-rate calculation, debt payoff planning, transaction categorization, monthly finance reports, anomaly detection, and practical money habit recommendations. Trigger when users ask to analyze finances, track spending, review bank or card transactions, make a budget, understand where money goes, compare income and expenses, improve savings, reduce debt, or create a personal finance report.
license: MIT
packageType: instruction-skill
instructionOnly: true
---

# Finance Manager

## Execution Priority (Highest · Hard Requirement)

> When using this skill to **generate any application that lets users upload statement/transaction files, converts file formats, or produces generated analysis text**, the following are non-negotiable hard requirements and take precedence over every other section of this skill:
>
> 1. **File parsing MUST directly integrate** the matching platform skills: `@Excel` (.xlsx / .xls / .csv transaction tables), `@PDF` (PDF statements), `@Word` (.doc/.docx).
> 2. **Text generation MUST integrate** `@Large language Model` for spending analysis, monthly reports, and recommendation copy. Do not wire up a model API yourself.
> 3. **PDF text MUST be extracted before it reaches the model**: extract the full text page by page on the frontend with `pdfjs-dist` and **validate it is non-empty**; never pass an empty-string placeholder to `@Large language Model`.
> 4. **MUST NOT** hand-roll Excel/PDF/Word parsing inside the generated app, and **MUST NOT** use any "simplified/fallback" approach that decodes raw file bytes as text.
> 5. Failing to integrate the applicable skills above is an implementation error.
> 6. Note the distinction: **this skill itself** is pure prompt/workflow and calls nothing on its own — the requirement above applies to the **application generated from it**.
> 7. For any bank/wallet statement import, you **MUST** follow every red line in `references/bill-parsing-rules.md` (header location, column normalization, quoted-field state machine, encoding, error messages).

### Required Excel (.xlsx / .xls / .csv) Stack (Do Not Deviate)

| Layer | Must use | Notes |
| --- | --- | --- |
| Parse / generate | **SheetJS** (`import * as XLSX from 'npm:xlsx'`) | Read worksheets, convert rows to JSON, and generate `.xlsx` from data |
| Runtime | **Supabase Edge Function (Deno)** | Do parsing/generation server-side; keep large-file logic out of the frontend |
| File storage | **Supabase Storage (all buckets private)** | `uploads` holds files awaiting parsing; `exports` holds generated files and **must be served via short-lived signed URLs — never a public bucket** |
| Data landing | **Supabase Postgres** | Store each row as `jsonb` for querying and re-export |
| Frontend | Browser File API + fetch (Web) / Taro (mini program / H5) | File selection, upload, download, preview |

Standard flows:
- **Import**: pick file → upload to Storage → Edge Function parses the worksheet with SheetJS → batch-insert into Postgres `row_data(jsonb)`.
- **Export**: query rows → expand `jsonb` into columns → generate `.xlsx` with SheetJS → upload to the public bucket → return a download link.

**Hard rules for xlsx parsing:**

- Never hand-roll ZIP/XML parsing for `.xlsx` (it is ZIP + XML, just like `.docx`).
- Never decode raw `.xlsx` bytes as UTF-8/latin1.
- If low-level handling is unavoidable: cell text usually lives in `xl/sharedStrings.xml`, and the `5` in `<c t="s"><v>5</v></c>` is an **index, not a value** — it must be dereferenced or you get a wall of numbers; dates are **serial numbers** (1900 epoch) and must be converted. SheetJS handles all of this for you.
- For transaction data, **prefer asking the user to export `.csv`** (plain text, least error-prone).

**Terminology:** there is no such thing as converting "`.xlsx` → Excel" — `.xlsx` *is* an Excel file format. Meaningful conversions are `.xlsx ↔ .xls`, `.xlsx ↔ .csv`, `.xlsx ↔ .pdf`, and `.xlsx → database`.

Use this skill to help users understand and improve their personal finances from transaction data, budgets, financial goals, or plain-language descriptions of income and spending.

This skill is a pure prompt/workflow skill: on its own it does not call external APIs, bank connections, brokerage access, or tax software, and it does not execute code. When it is used to generate an application, file parsing, format conversion, and text generation must be delegated to the platform skills listed above rather than implemented by hand.

## Safety and Advice Boundaries

Always include a concise boundary statement when giving recommendations:

> This is educational personal finance guidance, not financial, investment, tax, legal, or debt-counseling advice. Verify numbers and consult a qualified professional for decisions with legal, tax, investment, credit, or insolvency consequences.

Do not:

- Recommend specific securities, brokers, loans, insurance policies, or financial products as personalized advice.
- Tell the user to hide income, evade taxes, misrepresent information, or skip required payments.
- Give definitive tax, legal, bankruptcy, or credit-repair conclusions.
- Ask for full account numbers, card numbers, passwords, government IDs, or bank login credentials.
- Store or expose sensitive financial data.

## Supported Inputs

Work with whatever the user provides:

- CSV-like transaction tables.
- Bank or credit-card statement text.
- Monthly income and expense summaries.
- Category totals.
- Debt balances, APRs, and minimum payments.
- Budget goals.
- Savings goals.
- Irregular income or freelance income.
- Household spending notes.

If raw transactions are missing, proceed with estimates and mark assumptions clearly.

## Output Modes

Choose the smallest complete output that fits the request.

### Spending Analysis

Use when the user asks where money is going or provides transactions.

Include:

- Total income.
- Total expenses.
- Net cash flow.
- Savings rate.
- Spending by category.
- Largest expenses.
- Recurring expenses.
- Unusual or anomalous transactions.
- Practical next actions.

### Budget Plan

Use when the user asks for a budget or wants to control spending.

Include:

- Baseline monthly income and expenses.
- Fixed, variable, discretionary, and savings categories.
- Recommended target amounts.
- Tradeoffs and cuts by priority.
- Weekly or monthly tracking plan.

### Monthly Finance Report

Use when the user asks for a report, dashboard, or review.

Include:

- Executive summary.
- Key metrics.
- Category breakdown.
- Month-over-month or period comparison, if available.
- Wins.
- Risks.
- Recommendations for next month.

### Savings and Goal Plan

Use when the user wants to save for an emergency fund, purchase, trip, education, home, or other goal.

Include:

- Target amount.
- Current saved amount.
- Gap.
- Monthly contribution required.
- Timeline options.
- Budget changes needed.
- Risk buffer.

### Debt Payoff Plan

Use when the user provides debts, balances, APRs, and payments.

Include:

- Debt inventory.
- Minimum payment baseline.
- Avalanche plan: highest APR first.
- Snowball plan: lowest balance first.
- Estimated tradeoffs.
- Cash-flow cautions.

Do not present payoff timelines as exact unless the user provides full balances, APRs, fees, payment dates, and compounding assumptions.

### Financial Health Check

Use when the user wants an overall assessment.

Include:

- Cash-flow health.
- Savings rate.
- Emergency fund coverage.
- Debt burden.
- Spending concentration.
- Income stability.
- Risk flags.
- 3 to 5 priority actions.

## Workflow

1. Clarify the objective: analyze, budget, report, save, reduce debt, or diagnose.
2. Identify the time period and currency.
3. Normalize data into income, fixed expenses, variable expenses, discretionary spending, savings, debt payments, and transfers.
4. Avoid double-counting transfers, credit-card payments, reimbursements, and refunds.
5. Calculate core metrics.
6. Compare against user goals and reasonable benchmarks.
7. Produce practical recommendations with estimated impact.
8. Flag uncertainty, missing data, and professional-review points.

## Core Metrics

Use these formulas when data allows:

- Net cash flow = total income - total expenses.
- Savings rate = savings or net cash flow / total income.
- Expense ratio = total expenses / total income.
- Category share = category spend / total expenses.
- Housing ratio = housing cost / gross or net income, matching the user's data.
- Debt payment ratio = minimum debt payments / monthly income.
- Emergency fund months = liquid savings / essential monthly expenses.

If transfers distort the math, explain and calculate both "cash movement" and "true spending" views.

## Recommendation Rules

Recommendations should be specific and actionable:

- Name the category.
- Estimate the monthly impact.
- Explain the tradeoff.
- Prioritize by impact and feasibility.
- Preserve essential spending before optimizing discretionary spending.

Good:

- "Reduce delivery spending from 1,200 to 700 per month to free roughly 500 for emergency savings."

Weak:

- "Spend less money."

## Data Quality Rules

If the user provides raw transactions:

- Ask for column meaning only when ambiguous.
- Group similar merchants.
- Identify likely transfers and repayments.
- Do not treat credit-card payments as expenses if the underlying card transactions are also present.
- Separate refunds from income.
- Separate one-time purchases from recurring costs.
- Mark unknown categories instead of guessing too aggressively.

## Reference Material

Load `references/personal-finance-frameworks.md` for budgeting, savings, emergency fund, debt payoff, and financial health benchmarks.

Load `references/transaction-analysis-templates.md` for transaction categorization, report structures, dashboard fields, and output tables.

**When generating a statement-import feature you MUST load** `references/bill-parsing-rules.md`: hard rules for parsing bank/wallet statements (header location, column-name normalization, direction columns, quoted-field state machine, GBK encoding, PDF text extraction, duplicate Edge Function declarations, actionable errors).
