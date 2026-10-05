---
name: financial-reporting
displayName: Financial Reporting
tagline: Generate financial statements, P&L reports, and budget vs actuals for leadership review.
description: |
  Generates financial reports including profit and loss statements,
  balance sheets, cash flow reports, and budget variance analysis.
  Pulls data from accounting systems and payment processors to
  create executive-ready financial summaries with trend analysis.
department:
  - Finance
  - Accounting
  - Executive
use_cases:
  - Financial Reporting
  - Budget Analysis
  - Executive Dashboards
tools_required:
  - QuickBooks MCP
  - Stripe MCP
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
  Generate the April P&L report and compare against budget.
  Include revenue breakdown by product line.
exampleOutput: |
  Profit & Loss — April 2026

  REVENUE
  Total Revenue:     $420,000 (budget: $400,000, +5%)
    SaaS Subscriptions: $310,000 (74%)
    Professional Svcs:  $80,000 (19%)
    Add-ons:            $30,000 (7%)

  EXPENSES
  Total Expenses:    $340,000 (budget: $350,000, -3%)
    Payroll:            $220,000
    Cloud/Infra:        $48,000
    Sales/Marketing:    $42,000
    G&A:                $30,000

  NET INCOME
  Actual:            $80,000
  Budget:            $50,000
  Variance:          +$30,000 (+60%)

  KEY METRICS
  Gross Margin:      72%
  Burn Rate:         $260K/month (excl. payroll: $120K)
  Runway:            18 months at current burn
---

# Financial Reporting

Generate financial statements, P&L reports, and budget vs actuals for leadership review.

**Integrations:** QuickBooks, Stripe

## When to Use

- Leadership needs monthly or quarterly financial reports
- Budget variance analysis is required
- The user mentions "P&L", "financial report", "budget vs actuals", or "cash flow"

## Steps

### Step 1: Pull Financial Data

Extract revenue and expense data from accounting and payment systems.

### Step 2: Generate Statements

Create P&L, balance sheet, and cash flow reports.

### Step 3: Analyze Variances

Compare actuals against budget with explanations for variances.

### Step 4: Create Executive Summary

Summarize key metrics and trends for leadership.

## Output

Deliver:
- Financial statements (P&L, Balance Sheet, Cash Flow)
- Budget variance analysis
- Executive summary with key metrics
