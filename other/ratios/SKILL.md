---
description: Calculate liquidity, profitability, leverage, and efficiency ratios
---

# Ratios

Calculate financial ratios for "$ARGUMENTS". Compute key ratios across liquidity, profitability, leverage, and efficiency to assess overall financial health and benchmark against industry standards.

## Prerequisites

None — utility skill, run anytime. Works best when financial data exists in `.metapowers/finance/$ARGUMENTS/`.

## Process

1. **Gather context:**
   - If prior phase artifacts exist, read them for financial data
   - Ask for income statement, balance sheet, and cash flow data
   - Determine the industry for benchmarking context
   - Reference `financial-model-template.md` for ratio definitions

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
   - **Interest Coverage:** EBITDA / Interest Expense
   - **Equity Multiplier:** Total Assets / Total Equity

5. **Calculate efficiency ratios:**
   - **Revenue per Employee:** Annual Revenue / Headcount
   - **Days Sales Outstanding (DSO):** (Receivables / Revenue) x 365
   - **Days Payable Outstanding (DPO):** (Payables / COGS) x 365
   - **Cash Conversion Cycle:** DSO + DIO - DPO
   - **Asset Turnover:** Revenue / Total Assets

6. **Benchmark and assess:**
   - Compare ratios to industry medians where known
   - Identify ratios that are strong, acceptable, or concerning
   - Track trends over time if historical data is available
   - Flag any ratios outside acceptable ranges

7. **Write the artifact** to `.metapowers/finance/$ARGUMENTS/ratios.md` with sections:
   - **Liquidity Ratios** — values, benchmarks, assessment
   - **Profitability Ratios** — values, benchmarks, assessment
   - **Leverage Ratios** — values, benchmarks, assessment
   - **Efficiency Ratios** — values, benchmarks, assessment
   - **Overall Financial Health** — summary scorecard
   - **Recommendations** — areas to improve

## Output

The ratio analysis written to `.metapowers/finance/$ARGUMENTS/ratios.md`. Present a summary highlighting:
- Overall financial health score
- Strongest and weakest ratio categories
- Key ratios outside acceptable ranges
- Priority improvement areas
