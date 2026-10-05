---
name: cohort-analysis
displayName: Cohort Analysis
tagline: Analyze user retention and behavior patterns across cohorts defined by signup date or attributes.
description: |
  Performs cohort analysis to understand user retention, engagement, and
  revenue patterns over time. Groups users by signup date, acquisition
  channel, or plan type and tracks how their behavior changes week over
  week. Identifies which cohorts retain best and what drives long-term
  engagement.
department:
  - Product
  - Data & Analytics
  - Growth
use_cases:
  - Retention Analysis
  - User Behavior
  - Growth Analytics
tools_required:
  - Mixpanel MCP
  - PostgreSQL MCP
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
  Run a weekly retention cohort analysis for the last 3 months.
  Show retention through week 8. Break down by plan type.
exampleOutput: |
  Cohort Retention — Last 3 Months

  WEEKLY RETENTION (% returning)
          W1    W2    W3    W4    W5    W6    W7    W8
  Feb:    72%   58%   48%   42%   38%   35%   33%   31%
  Mar:    75%   61%   52%   45%   41%   38%   —     —
  Apr:    78%   64%   55%   —     —     —     —     —

  TREND: Improving (+3% W1 retention month over month)

  BY PLAN TYPE
  Pro Plan:      W4 retention: 62% (best performing)
  Team Plan:     W4 retention: 48%
  Free Plan:     W4 retention: 28%

  KEY INSIGHTS
  - Pro plan users retain 2.2x better than free users
  - Users who complete onboarding in Day 1 have 45% higher W4 retention
  - Referral cohorts retain 18% better than paid acquisition
---

# Cohort Analysis

Analyze user retention and behavior patterns across cohorts defined by signup date or attributes.

**Integrations:** Mixpanel, PostgreSQL

## When to Use

- The user wants to understand retention trends over time
- Different user segments need retention comparison
- The user mentions "cohort analysis", "retention", or "user behavior over time"

## Steps

### Step 1: Define Cohorts

Group users by signup date, plan, or acquisition channel.

### Step 2: Track Retention

Calculate return rates for each cohort over time periods.

### Step 3: Compare Segments

Identify which cohorts perform best and why.

### Step 4: Extract Insights

Find actionable patterns that drive retention.

## Output

Deliver:
- Cohort retention table
- Segment comparison analysis
- Key insights and recommendations
