---
name: "market-scanner"
description: "Automated market and competitive intelligence for the Strategy department. Monitors market shifts, competitor moves, regulatory changes, and financial trends. Produces strategic briefs with scenario analysis. Use when tracking market movements, analyzing competitive landscape, monitoring regulations, or running the strategy UAOP pipeline."
risk: low
tags: [strategy, competitive-intel, market-research, trends]
created: 2026-03-23
updated: 2026-03-23
---

# Market Scanner — Strategy Department Intelligence Engine

Automated market monitoring that keeps the Strategy department ahead of shifts. UAOP Stage 1 for Strategy.

## When to use

- Weekly competitive monitoring — "what did competitors announce?"
- Before strategic decisions — "what's the market context?"
- Board prep — "what's changed since last quarter?"
- Fundraising — "what's the market narrative?"

## Pipeline

### Step 1: Scan Sources
- Competitor announcements (product launches, pricing, funding)
- Market reports (Gartner AI governance, CNCF surveys, dev tool surveys)
- Regulatory changes (EU AI Act updates, SOC 2 changes, GDPR enforcement)
- Funding rounds in the space (Crunchbase, TechCrunch)
- Industry commentary (analyst blogs, Twitter/X threads, HN discussions)

### Step 2: Classify Signals
| Signal Type | Urgency | Action |
|------------|---------|--------|
| Competitor launch in our space | High | Analyze positioning, update battlecard |
| Regulatory change affecting us | High | Assess compliance impact |
| Market narrative shift | Medium | Update positioning |
| Funding round in space | Medium | Assess competitive threat |
| Technology trend | Low | Add to architecture-radar |

### Step 3: Produce Strategic Brief
- Market context summary (3 bullets)
- Competitor moves (what, so what, now what)
- Regulatory watch (changes, deadlines, impact)
- Scenario analysis (bull/base/bear for key trends)
- Recommended strategic actions (with owner + timeline)

### Step 4: Self-Improvement Loop
- Track forecast accuracy — did our predictions match reality?
- Reinforce sources that produced actionable intelligence
- Kill monitoring of signals that never led to action

## Cadence
```
DAILY:    Scan for competitor announcements + regulatory changes
WEEKLY:   Market intelligence brief
MONTHLY:  Competitive landscape update + battlecard refresh
QUARTERLY: Full strategic review with scenario analysis
```

## Agents
| Agent | Role |
|-------|------|
| business-panel-experts (L1) | Strategic analysis + recommendations |
| trend-researcher (L4) | Executes market scans |
| finance-tracker (L3) | Tracks financial signals |
| analytics-reporter (L3) | Quantifies market data |
