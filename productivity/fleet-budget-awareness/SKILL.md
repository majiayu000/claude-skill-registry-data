---
name: fleet-budget-awareness
description: How fleet-ops monitors budget health, understands spending patterns, and recommends mode changes. Connects to Budget Monitor, Storm system, and fleet control modes.
---

# Budget Awareness — Fleet-Ops Fiscal Vigilance

The fleet runs on Claude API quota. When budget runs low, dispatch stops. When it runs out, the fleet halts. Your job is to understand the spending pattern and recommend adjustments BEFORE crisis hits.

## The Budget System

The Budget Monitor (`fleet/core/budget_monitor.py`) reads real Claude OAuth quota every orchestrator cycle:

| Metric | What It Means | Threshold |
|--------|-------------|-----------|
| Weekly usage % | How much of the weekly quota is consumed | 90% → dispatch blocked |
| Fast climb | Usage increasing >5% in 10 minutes | Triggers dispatch pause |
| Burn rate | Quota consumption per hour | Predicts when quota exhausts |
| Rollover distance | Time until weekly quota resets | Low distance + high usage = crisis |

## Budget Modes

The PO controls fleet tempo via budget modes:

| Mode | Dispatch | Effort | When |
|------|----------|--------|------|
| full-speed | Unlimited | High | Plenty of budget, sprint deadline |
| normal | Standard (2/cycle) | Medium | Default operation |
| conservative | Reduced (1/cycle) | Medium | Budget >70%, slowing down |
| finish-current | Zero new dispatch | Current tasks only | Budget >85%, wind down |
| work-paused | Zero dispatch | Heartbeats only | Budget critical or PO pause |

## What You Monitor

### During Heartbeat

Your `ops_budget_assessment` group call provides:
- Current weekly usage percentage
- Burn rate trend (increasing/stable/decreasing)
- Projected exhaustion time at current rate
- Active dispatches consuming budget

### What to Look For

1. **Steady burn under 70%** → Normal. No action needed.
2. **Approaching 80%** → Recommend: `fleet_chat("Budget at {pct}%. Suggest switching to conservative mode.", mention="human")`
3. **Approaching 90%** → Critical: `fleet_alert(category="budget", severity="high", details="Budget at {pct}%. Dispatch will auto-block at 90%.")`
4. **Fast climb** → Something is consuming budget rapidly. Check: which agents are active? Are there void sessions (heartbeats that do nothing)?
5. **Post-storm** → After a storm event, budget may have been forced down. Check if the storm is resolved and recommend mode restoration.

## The Storm Connection

Storms and budget are interlinked:
- Storm WARNING → dispatch limited to 1/cycle (saves budget)
- Storm STORM → dispatch blocked entirely (budget protected)
- Storm CRITICAL → fleet halted (budget irrelevant — everything stopped)

When you see storm indicators + budget pressure simultaneously, that's compound risk. Escalate immediately: `fleet_escalate(title="Compound risk: storm + budget pressure")`.

## Your Budget Assessment CRONs

Your **budget-assessment** CRON runs daily:
1. Read budget metrics from the orchestrator
2. Calculate: at current burn rate, when does quota exhaust?
3. Compare to rollover date — will we make it?
4. Post assessment to board memory [budget, assessment]
5. If critical: alert PO

## Recommending Mode Changes

You don't change modes — the PO does. You RECOMMEND based on data:

```
fleet_chat(
    "Budget assessment: weekly at 72%, burn rate 1.2%/hour, "
    "rollover in 38 hours. At current rate: quota exhausts in 23 hours. "
    "Recommend: switch to conservative mode to extend runway to rollover. "
    "Current active: 4 agents in work stage.",
    mention="human"
)
```

Include: current %, burn rate, projection, recommendation, and what's currently consuming budget.

## What Budget Awareness is NOT

- NOT deciding modes (PO decides — you recommend)
- NOT stopping dispatch (Budget Monitor does this automatically at 90%)
- NOT managing storms (Storm Monitor handles detection and response)

You're the analyst who sees the financial picture and helps the PO make informed decisions. The automated systems handle emergencies. You handle strategy.
