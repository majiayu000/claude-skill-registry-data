---
name: finance-ratios
description: Calculate liquidity, profitability, leverage and efficiency ratios from the financial statements, benchmark them and summarize overall financial health. Use when the user has an income statement and balance sheet and asks how healthy the business looks or how it compares with its industry. Not for producing the statements; see /accounting-statements.
metadata:
  argument-hint: "[project] [--skip-checks]"
---

# Ratios

Calculate financial ratios for "$ARGUMENTS". Compute key ratios across liquidity, profitability, leverage, and efficiency to assess overall financial health and benchmark against industry standards.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"finance-ratios","workflow":"finance","phase":null,"project":"<project>","event":"skipped","artifact":"<artifact file>","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

None — utility skill, run anytime. Works best when financial data exists in `.singularskills/finance/<project>/`.

## Process

1. **Gather context:**
   - If prior phase artifacts exist, read them for financial data
   - Ask for income statement, balance sheet, and cash flow data
   - Determine the industry for benchmarking context
   - Reference `references/financial-model-template.md` for ratio definitions

2. **Calculate liquidity ratios:**
   - **Current Ratio:** Current Assets / Current Liabilities (target: > 1.5)
   - **Quick Ratio:** (Cash + Receivables) / Current Liabilities (target: > 1.0)
   - **Cash Ratio:** Cash / Current Liabilities
   - **Working Capital:** Current Assets - Current Liabilities

3. **Calculate profitability ratios:**
   - **Gross Margin:** (Revenue - COGS) / Revenue
   - **Operating Margin:** Operating Income / Revenue
   - **Net Margin:** Net Income / Revenue
   - **EBITDA Margin:** EBITDA / Revenue
   - **Return on Equity (ROE):** Net Income / Shareholders' Equity
   - **Return on Assets (ROA):** Net Income / Total Assets

4. **Calculate leverage ratios:**
   - **Debt-to-Equity:** Total Debt / Total Equity
   - **Debt-to-Assets:** Total Debt / Total Assets
   - **Interest Coverage:** EBIT / Interest Expense
   - **Equity Multiplier:** Total Assets / Total Equity

5. **Calculate efficiency ratios:**
   - **Revenue per Employee:** Annual Revenue / Headcount
   - **Days Sales Outstanding (DSO):** (Receivables / Revenue) x 365
   - **Days Payable Outstanding (DPO):** (Payables / COGS) x 365
   - **Days Inventory Outstanding (DIO):** (Inventory / COGS) x 365
   - **Cash Conversion Cycle:** DSO + DIO - DPO
   - **Asset Turnover:** Revenue / Total Assets

6. **Benchmark and assess:**
   - Compare ratios to industry medians where known
   - Identify ratios that are strong, acceptable, or concerning
   - Track trends over time if historical data is available
   - Flag any ratios outside acceptable ranges

7. **Write the artifact** to `.singularskills/finance/<project>/ratios.md` with sections:
   - **Liquidity Ratios** — values, benchmarks, assessment
   - **Profitability Ratios** — values, benchmarks, assessment
   - **Leverage Ratios** — values, benchmarks, assessment
   - **Efficiency Ratios** — values, benchmarks, assessment
   - **Overall Financial Health** — summary scorecard rating each category (liquidity, profitability, leverage, efficiency) Strong / Acceptable / Concerning from its step-6 assessments
   - **Recommendations** — areas to improve

## Output

The ratio analysis written to `.singularskills/finance/<project>/ratios.md`. Present a summary highlighting:
- Overall financial health rating (Strong / Acceptable / Concerning, by category)
- Strongest and weakest ratio categories
- Key ratios outside acceptable ranges
- Priority improvement areas

End the artifact with this paragraph, verbatim:

> **Not financial or tax advice.** This artifact is generated analysis for review by a qualified accountant or financial professional before any filing, reporting or decision relies on it.
