---
name: expense-management
displayName: Expense Management
tagline: Track, categorize, and approve business expenses with automated receipt processing.
description: |
  Manages business expenses from receipt capture to reimbursement.
  Categorizes expenses by department, project, and GL code. Enforces
  spending policies, routes approvals, and generates expense reports
  for accounting reconciliation.
department:
  - Finance
  - Accounting
use_cases:
  - Expense Tracking
  - Budget Management
  - Financial Controls
tools_required:
  - QuickBooks MCP
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
  Generate an expense report for the Engineering team for April.
  Flag any expenses that exceed policy limits.
exampleOutput: |
  Expense Report — Engineering, April 2026

  SUMMARY
  Total Expenses:   $24,800
  Budget:           $30,000 (83% utilized)
  Transactions:     142

  BY CATEGORY
  Software/SaaS:    $12,400 (50%)
  Cloud Infra:      $6,200 (25%)
  Travel:           $3,800 (15%)
  Equipment:        $1,600 (6%)
  Meals/Events:     $800 (3%)

  POLICY FLAGS
  ⚠️ $1,200 hotel (above $250/night limit) — @bob — pending manager approval
  ⚠️ $380 dinner (above $150/person limit) — @carol — pending justification

  STATUS
  Approved:         138 transactions
  Pending Review:   4 transactions
---

# Expense Management

Track, categorize, and approve business expenses with automated receipt processing.

**Integrations:** QuickBooks

## When to Use

- The user needs to track or report on business expenses
- Expense policy violations need to be flagged
- The user mentions "expenses", "reimbursement", or "expense report"

## Steps

### Step 1: Categorize Expenses

Automatically categorize transactions by type and department.

### Step 2: Check Policy Compliance

Flag expenses that exceed policy limits or require justification.

### Step 3: Route Approvals

Send flagged expenses to managers for approval.

### Step 4: Generate Reports

Create expense reports with budget comparisons and trends.

## Output

Deliver:
- Categorized expense report
- Policy violation flags
- Budget utilization summary
