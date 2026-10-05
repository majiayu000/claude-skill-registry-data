---
name: deal-tracking
displayName: Deal Tracking
tagline: Track deal progress, pipeline stages, and revenue forecasts across your CRM.
description: |
  Monitors deal progression through pipeline stages in HubSpot or Salesforce.
  Tracks deal values, close dates, win probabilities, and stalled opportunities.
  Generates pipeline reports with revenue forecasts and highlights deals that
  need attention or follow-up.
department:
  - Sales
  - Revenue Operations
use_cases:
  - Pipeline Management
  - Revenue Forecasting
  - Sales Automation
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
  Show me all deals in the pipeline for Q2 2026.
  Flag any deals stalled for more than 14 days.
exampleOutput: |
  Deal Pipeline — Q2 2026

  SUMMARY
  Total Deals:      42
  Pipeline Value:   $1.2M
  Weighted Value:   $680K
  Stalled (>14d):   7 deals

  TOP DEALS
  1. Acme Corp — $120K — Negotiation (85%)
  2. TechStart — $95K  — Proposal (60%)
  3. GlobalFin — $80K  — Discovery (30%)

  STALLED ALERTS
  - DataFlow Inc — 21 days in Proposal — Last activity: email opened
  - CloudNet — 18 days in Discovery — No recent activity
---

# Deal Tracking

Track deal progress, pipeline stages, and revenue forecasts across your CRM.

**Integrations:** HubSpot, Salesforce

## When to Use

- The user wants a pipeline overview or revenue forecast
- Deals need to be monitored for stalls or missed follow-ups
- The user mentions "deal tracking", "pipeline", or "forecast"

## Steps

### Step 1: Pull Pipeline Data

Query CRM for all active deals with stage, value, and close date.

### Step 2: Analyze Pipeline Health

Identify stalled deals, overdue tasks, and deals with low activity.

### Step 3: Generate Forecast

Calculate weighted pipeline value and project revenue by close date.

## Output

Deliver:
- Pipeline summary with deal counts and values by stage
- Stalled deal alerts with recommended actions
- Revenue forecast for the selected period
