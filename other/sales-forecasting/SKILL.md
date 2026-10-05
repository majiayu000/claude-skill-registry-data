---
name: sales-forecasting
displayName: Sales Forecasting
tagline: Generate accurate sales forecasts based on pipeline data, historical trends, and win rates.
description: |
  Produces revenue forecasts by analyzing CRM pipeline data, historical close
  rates, seasonal trends, and deal velocity. Provides best-case, worst-case,
  and most-likely scenarios. Highlights risks to forecast accuracy and recommends
  pipeline coverage targets.
department:
  - Sales
  - Revenue Operations
  - Finance
use_cases:
  - Revenue Forecasting
  - Pipeline Analysis
  - Sales Planning
tools_required:
  - HubSpot MCP
  - Salesforce MCP
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
  Forecast Q3 2026 revenue based on current pipeline and historical win rates.
  Include scenario analysis (best/worst/likely).
exampleOutput: |
  Sales Forecast — Q3 2026

  SCENARIOS
  Best Case:    $2.1M  (pipeline * optimistic win rates)
  Most Likely:  $1.5M  (pipeline * historical win rates)
  Worst Case:   $980K  (pipeline * conservative win rates)

  PIPELINE COVERAGE
  Target:       $1.8M
  Coverage:     3.2x  (healthy: >3x)
  At Risk:      $320K  (5 deals with declining engagement)

  HISTORICAL WIN RATES
  Enterprise:   28%  |  Mid-Market: 35%  |  SMB: 42%
---

# Sales Forecasting

Generate accurate sales forecasts based on pipeline data, historical trends, and win rates.

**Integrations:** HubSpot, Salesforce

## When to Use

- Leadership needs revenue projections for upcoming quarters
- The user wants to assess pipeline health and coverage
- The user mentions "forecast", "revenue projection", or "pipeline coverage"

## Steps

### Step 1: Gather Pipeline Data

Pull all open deals with stage, value, close date, and engagement metrics.

### Step 2: Apply Historical Win Rates

Calculate expected revenue using historical conversion rates by segment.

### Step 3: Generate Scenarios

Produce best-case, worst-case, and most-likely revenue scenarios.

### Step 4: Identify Risks

Flag deals with declining engagement or overdue close dates.

## Output

Deliver:
- Three-scenario revenue forecast
- Pipeline coverage analysis
- Risk assessment with recommended actions
