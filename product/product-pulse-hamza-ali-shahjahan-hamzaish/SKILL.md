---
name: product-pulse
description: Snapshot of one product — current metrics, stage, blockers, and the #1 recommended action today.
---

# /product-pulse

Usage: `/product-pulse <product-slug>`

## What this does
Quick read on one product, designed to fit in 30 seconds.

Output:
```
## <Product> — <stage> — <date>

### Numbers (last 7 days)
- MRR: $X (Δ vs prev 7d)
- Paying customers: N (Δ)
- Active users (7d): N (Δ)
- Signups (7d): N (Δ)
- Errors (24h): N
- Top organic queries: <top 3>

### Status
<one-paragraph current state>

### Today's #1 action
<task> — because <reason> — estimated time: <est>

### Watch list
- <thing that might break or matter soon>
- <thing>

### Don't worry about
- <distraction>
```

## What you do as the assistant
1. Read `products/<slug>/product.config.json`, `metrics.md`, latest 3 `decisions/`.
2. Pull telemetry via `agents/portfolio/telemetry-aggregator/`.
3. Match stage to operating priorities:
   - **Idea**: Today's action is usually "do N interviews" or "synthesize batch"
   - **MVP**: Today's action is usually "ship feature X" or "run Sean Ellis at week 4"
   - **Launch**: Today's action is usually "publish post Y" or "outreach to N prospects"
   - **Scale**: Today's action is usually "fix retention drop in cohort Z" or "raise prices"
4. Force one action, not three.

## When connectors aren't wired
If `product.config.json` shows missing connectors, fill metrics with `not_connected` and recommend wiring them as part of next action.
