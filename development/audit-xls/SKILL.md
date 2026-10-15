---
name: audit-xls
description: Audit a spreadsheet for formula accuracy, errors, and common mistakes. Scopes to a selected range, a single sheet, or the entire model, including financial-model integrity checks like BS balance, cash tie-out, and logic sanity. Triggers on "audit this sheet", "check my formulas", "find formula errors", "QA this spreadsheet", "sanity check this", "debug model", "model check", "model won't balance", "something's off in my model", "model review", "데이터 검증해줘", "수식 확인", "정합성 체크", "엑셀 감사", "모델 검토", "수식 에러 찾아줘", "데이터 맞는지 봐줘".
---

# Audit Spreadsheet

Audit formulas and data for accuracy and mistakes. Scope determines depth, from quick formula checks on a selection up to full financial-model integrity audits.

## Preflight: Dependency Check

Before starting, verify required libraries are installed and install any that are missing.

```bash
python3 -c "import pandas" 2>/dev/null || python3 -m pip install pandas
python3 -c "import openpyxl" 2>/dev/null || python3 -m pip install openpyxl
```

**Important**: Do not skip this step — the workflow below will fail without these libraries.

## Step 1: Determine scope

If the user already gave a scope, use it. Otherwise ask:

> What scope do you want me to audit?
> - **selection** — just the currently selected range
> - **sheet** — the current active sheet only
> - **model** — the whole workbook, including financial-model integrity checks (BS balance, cash tie-out, roll-forwards, logic sanity)

The **model** scope is the deepest. Use it for DCF, LBO, 3-statement, merger, comps, or any integrated financial model before sending to a client or IC.

## Step 2: Formula-level checks (all scopes)

Run these regardless of scope:

| Check | What to look for |
|---|---|
| Formula errors | `#REF!`, `#VALUE!`, `#N/A`, `#DIV/0!`, `#NAME?` |
| Hardcodes inside formulas | `=A1*1.05` where the `1.05` should be a cell reference |
| Inconsistent formulas | A formula that breaks the pattern of its neighbors in a row or column |
| Off-by-one ranges | `SUM` or `AVERAGE` that misses the first or last row |
| Pasted-over formulas | A cell that looks like a formula location but is actually a hardcoded value |
| Circular references | Intentional or accidental |
| Broken cross-sheet links | References to cells that moved or were deleted |
| Unit or scale mismatches | Thousands mixed with millions, or percentages stored as whole numbers |
| Hidden rows or tabs | Could contain overrides or stale calculations |

## Step 3: Model-integrity checks (model scope only)

If scope is **model**, identify the model type: DCF, LBO, 3-statement, merger, comps, or custom, then run the appropriate checks.

### 3a. Structural review

| Check | What to look for |
|---|---|
| Input/formula separation | Are inputs clearly separated from calculations? |
| Color convention | Blue=input, black=formula, green=link, or the model's equivalent, applied consistently |
| Tab flow | Logical order such as Assumptions -> IS -> BS -> CF -> Valuation |
| Date headers | Consistent across all tabs |
| Units | Consistent: thousands vs millions vs actuals |

### 3b. Balance Sheet

| Check | Test |
|---|---|
| BS balances | Total Assets = Total Liabilities + Equity for every period |
| RE rollforward | Prior RE + Net Income - Dividends = Current RE |
| Goodwill/intangibles | Flow from acquisition assumptions if M&A applies |

If the balance sheet does not balance, quantify the gap per period and trace where it breaks. Nothing else matters until that is fixed.

### 3c. Cash Flow Statement

| Check | Test |
|---|---|
| Cash tie-out | CF Ending Cash = BS Cash for every period |
| CF sums | CFO + CFI + CFF = Delta Cash |
| D&A match | D&A on CF = D&A on IS |
| CapEx match | CapEx on CF matches PP&E rollforward on BS |
| WC changes | Signs match BS movements for AR, AP, and Inventory |

### 3d. Income Statement

| Check | Test |
|---|---|
| Revenue build | Ties to segment or product detail |
| Tax | Tax expense = Pre-tax income x tax rate, allowing for deferred tax adjustments |
| Share count | Ties to dilution schedule: options, converts, buybacks |

### 3e. Circular references

- Interest -> debt balance -> cash -> interest is a common intentional circularity in LBO and 3-statement models.
- If intentional, verify the iteration toggle exists and works.
- If unintentional, trace the loop and flag how to break it.

### 3f. Logic and reasonableness

| Check | Flag if |
|---|---|
| Growth rates | Greater than 100% revenue growth without explanation |
| Margins | Outside industry norms |
| Terminal value dominance | TV > about 75% of DCF EV |
| Hockey-stick | Projections ramp unrealistically in out-years |
| Compounding | EBITDA compounds to absurd levels by Year 10 |
| Edge cases | Model breaks at 0% or negative growth, negative EBITDA, or negative leverage |

### 3g. Model-type-specific bugs

**DCF**
- Discount rate applied to the wrong period: mid-year vs end-of-year
- Terminal value not discounted back
- WACC uses book values instead of market values
- FCF includes interest expense when it should be unlevered
- Tax shield double-counted

**LBO**
- Debt paydown does not match cash sweep mechanics
- PIK interest does not accrue to principal
- Management rollover is not reflected in returns
- Exit multiple applied to the wrong EBITDA period: LTM vs NTM
- Fees or expenses not deducted from Day 1 equity

**Merger**
- Accretion/dilution uses the wrong share count: pre- vs post-deal
- Synergies not phased in
- Purchase price allocation does not balance
- Foregone interest on cash not included
- Transaction fees not in sources and uses

**3-statement**
- Working capital changes have the wrong sign
- Depreciation does not match the PP&E schedule
- Debt maturity schedule does not match principal payments
- Dividends exceed net income without explanation

## Step 4: Report

Output a findings table:

| # | Sheet | Cell/Range | Severity | Category | Issue | Suggested Fix |
|---|---|---|---|---|---|---|

Severity:

- **Critical** — wrong output: BS does not balance, formula is broken, or cash does not tie
- **Warning** — risky: hardcodes, inconsistent formulas, edge-case failures
- **Info** — style or best-practice items: color coding, layout, naming

For **model** scope, prepend a summary line:

> Model type: [DCF/LBO/3-stmt/...] — Overall: [Clean / Minor Issues / Major Issues] — [N] critical, [N] warnings, [N] info

Do not change anything without asking. Report first, fix on request.

## Notes

- BS balance first. If it does not balance, everything downstream is suspect.
- Hardcoded overrides are the number one source of silent bugs. Search aggressively.
- Sign convention errors are extremely common.
- If the model uses VBA macros, note any macro-driven calculations that cannot be audited from formulas alone.
