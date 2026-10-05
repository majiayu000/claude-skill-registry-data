---
name: lead-scoring
displayName: Lead Scoring
tagline: Score and prioritize leads based on engagement, firmographics, and behavioral signals.
description: |
  Implements a lead scoring model that evaluates prospects based on
  demographic fit, firmographic data, behavioral engagement, and intent
  signals. Assigns numerical scores to prioritize sales outreach and
  route leads to the right team. Continuously refines scores based on
  conversion outcomes.
department:
  - Marketing
  - Sales
use_cases:
  - Lead Qualification
  - Sales Prioritization
  - Marketing Automation
tools_required:
  - HubSpot MCP
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
  Create a lead scoring model for our B2B SaaS product.
  ICP: 50-500 employee tech companies in North America.
exampleOutput: |
  Lead Scoring Model — B2B SaaS

  SCORING CRITERIA (0-100)
  Firmographic (40 pts max)
    Company size 50-500:     +15
    Tech industry:           +10
    North America:           +10
    Revenue >$5M:            +5

  Behavioral (40 pts max)
    Visited pricing page:    +10
    Downloaded whitepaper:   +8
    Attended webinar:        +8
    Multiple site visits:    +7
    Opened 3+ emails:        +7

  Engagement (20 pts max)
    Requested demo:          +15
    Replied to outreach:     +5

  THRESHOLDS
  Hot (80-100):   Route to SDR immediately
  Warm (50-79):   Add to nurture sequence
  Cold (0-49):    Continue marketing touches
---

# Lead Scoring

Score and prioritize leads based on engagement, firmographics, and behavioral signals.

**Integrations:** HubSpot

## When to Use

- The user wants to build or refine a lead scoring model
- Sales teams need to prioritize which leads to contact first
- The user mentions "lead scoring", "lead qualification", or "MQL"

## Steps

### Step 1: Define ICP Criteria

Establish firmographic and demographic criteria for ideal customers.

### Step 2: Set Behavioral Signals

Define engagement actions and their point values.

### Step 3: Configure Thresholds

Set score ranges for hot, warm, and cold lead categories.

### Step 4: Test and Refine

Validate the model against historical conversion data.

## Output

Deliver:
- Scoring model with criteria and point values
- Threshold definitions with routing rules
- Validation report against historical data
