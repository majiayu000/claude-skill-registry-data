---
name: csat-tracking
displayName: CSAT Tracking
tagline: Track customer satisfaction scores across support channels with trend analysis and alerts.
description: |
  Monitors customer satisfaction (CSAT) scores across all support channels.
  Tracks satisfaction trends by agent, team, and issue category. Identifies
  patterns in low scores, generates improvement recommendations, and alerts
  managers when satisfaction drops below thresholds.
department:
  - Customer Support
  - Customer Success
use_cases:
  - Customer Satisfaction
  - Support Quality
  - Performance Tracking
tools_required:
  - Zendesk MCP
  - Slack MCP
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
  Generate a CSAT report for April.
  Break down by channel and agent. Flag any scores below 4.0.
exampleOutput: |
  CSAT Report — April 2026

  OVERALL SCORE: 4.3/5.0 (86% satisfaction)
  Response Rate: 34% (580/1,700 tickets rated)

  BY CHANNEL
  Live Chat:     4.5/5.0 (92%)
  Email:         4.2/5.0 (84%)
  Phone:         4.1/5.0 (82%)

  BY AGENT (top performers)
  @sarah:   4.7/5.0 (120 ratings)
  @mike:    4.5/5.0 (95 ratings)
  @lisa:    4.4/5.0 (88 ratings)

  LOW SCORE ALERTS
  ⚠️ @tom: 3.8/5.0 — common complaint: slow response time
  ⚠️ Billing category: 3.9/5.0 — refund process too complex

  RECOMMENDATIONS
  1. Coaching session for @tom on response speed
  2. Simplify refund workflow (top driver of low scores)
---

# CSAT Tracking

Track customer satisfaction scores across support channels with trend analysis and alerts.

**Integrations:** Zendesk, Slack

## When to Use

- The user needs to track customer satisfaction across support channels
- Low satisfaction trends need investigation
- The user mentions "CSAT", "customer satisfaction", or "support quality"

## Steps

### Step 1: Collect Ratings

Aggregate CSAT data from all support channels.

### Step 2: Analyze Trends

Break down scores by channel, agent, and issue category.

### Step 3: Flag Issues

Identify agents or categories with below-threshold scores.

### Step 4: Generate Recommendations

Provide actionable improvement suggestions based on patterns.

## Output

Deliver:
- CSAT summary by channel and agent
- Low-score alerts with root causes
- Improvement recommendations
