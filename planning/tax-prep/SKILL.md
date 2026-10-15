---
name: tax-prep
description: Organize deductions, receipts, quarterly estimates for tax filing. Solo founder focus.
version: 0.1.0
execution-mode: advisory
argument-hint: "[--action organize|estimate|deductions] [--quarter Q1|Q2|Q3|Q4]"
category: finance-legal
status: candidate
---
# Tax Prep

Organize tax-related data for a solo founder: categorize deductions, track quarterly estimated payments, summarize receipts by category, and flag missing documentation. Focused on US Schedule C / self-employment tax.

## When to Use
- Quarterly estimated tax payments are due (Apr 15, Jun 15, Sep 15, Jan 15)
- You need to organize deductions before filing
- You want to estimate your tax liability for the current quarter
- You need to verify receipt coverage for claimed deductions

## Execution
1. Parse `$ARGUMENTS` for action (organize/estimate/deductions) and quarter
2. If `organize`: pull from expense log, categorize by IRS Schedule C line items
3. If `estimate`: compute estimated tax from YTD revenue and deductions
   - Self-employment tax: 15.3% on 92.35% of net earnings
   - Income tax: apply marginal brackets to net earnings
   - Subtract already-paid quarterly estimates
4. If `deductions`: list all deductible expenses with receipt status
5. Flag common solo founder deductions: home office, software/SaaS, equipment, travel, health insurance, retirement contributions
6. Identify missing receipts or uncategorized expenses
7. Present summary with actionable items

## Output Format
```
Tax Prep | <action> (<quarter>)

## Revenue & Deductions Summary
| Category | Amount | Receipts | Status |
|----------|--------|----------|--------|
| Gross Revenue | $<N> | N/A | - |
| Software/SaaS | -$<N> | <N>/<N> | OK/MISSING |
| Home Office | -$<N> | <N>/<N> | OK/MISSING |
| Equipment | -$<N> | <N>/<N> | OK/MISSING |
| Travel | -$<N> | <N>/<N> | OK/MISSING |
| Health Insurance | -$<N> | <N>/<N> | OK/MISSING |
| **Net Earnings** | **$<N>** | | |

## Estimated Tax (if estimate)
| Tax | Amount |
|-----|--------|
| Self-employment (15.3%) | $<N> |
| Federal income tax | $<N> |
| State income tax | $<N> |
| **Total estimated** | **$<N>** |
| Already paid (Q1-Q<N>) | -$<N> |
| **Remaining due** | **$<N>** |

## Action Items
- [ ] <missing receipt or uncategorized expense>
- [ ] <upcoming deadline>

Next action: <recommendation>
```

## Skill Chains

### Mandatory

- None — tax-prep is `advisory` mode (read-only analysis and estimation).

### Advisory

| After this skill... | Consider... |
|--------------------|-------------|
| Need expense detail | `[expense-log]` to review and categorize |
| Need invoice history | `[invoice-generate]` for revenue records |
| Need runway context | `[runway]` for cash flow impact |

## Authority

- **T1 (TRUSTED)**: May run without restriction
- **T2 (Active/High)**: May run without restriction (read-only analysis)
- **T3 (Medium)**: May run without restriction (read-only analysis)
- **T4 (Probationary)**: May run (read-only — no side effects)
- **Operator**: Override any restriction

## Disclaimer

Tax-prep provides estimates for planning only. It is NOT a substitute for
professional tax advice. Always consult a CPA before filing.
