---
name: cost-guard
description: >-
  Per-session cost and token budget tracking for AI coding agents. Monitors
  cumulative spend, warns at thresholds, and enforces limits with three modes:
  reject (stop work), alert (warn and continue), downgrade (suggest cheaper
  approach). Ported from the LOCO-Agent BudgetManager.
  Trigger phrases: "set a budget", "track my spend", "cost limit",
  "how much have I spent", "token budget", "spending cap".
argument-hint: "[budget-amount] [mode: reject|alert|downgrade]"
allowed-tools: ""
---

# Cost Guard

Track and limit session costs to prevent runaway spend.

## When to Use

- User sets a budget: "/cost-guard $5" or "/cost-guard 100k tokens"
- User asks about spend: "how much have I spent?"
- Proactively, when a session involves many LLM calls, large context windows,
  or iterative loops that could accumulate significant cost

## Budget Configuration

When invoked with arguments, parse the budget:

- **Dollar amounts**: `/cost-guard $5`, `/cost-guard $0.50`
- **Token amounts**: `/cost-guard 100k tokens`, `/cost-guard 500000 tokens`
- **With mode**: `/cost-guard $10 alert`, `/cost-guard 200k tokens reject`

Default mode is **alert** (warn but don't stop).

## Three Enforcement Modes

Adapted from LOCO-Agent's BudgetManager:

### Reject
Stop work when the budget is exceeded. Report what was spent and what triggered
the limit. Ask the user if they want to increase the budget or end the session.

### Alert
Warn the user when the budget is exceeded but continue working. Show a clear
warning with current spend vs limit. Repeat the warning at each subsequent
25% increment above the limit.

### Downgrade
When approaching the budget (>80% consumed), proactively suggest cheaper
approaches:
- Shorter responses (skip verbose explanations)
- Fewer tool calls (batch operations instead of one-at-a-time)
- Skip optional validation steps
- Read smaller file sections instead of full files

## Cost Estimation

Track cost using these approximations:

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|---|---|---|
| Claude Opus | $15.00 | $75.00 |
| Claude Sonnet | $3.00 | $15.00 |
| Claude Haiku | $0.25 | $1.25 |

For each tool call and response in the session, estimate:
- **Input tokens**: prompt + context + tool results (rough: 1 token ≈ 4 chars)
- **Output tokens**: assistant response length
- **Cumulative total**: running sum across the session

These are estimates. State this clearly — actual billing may differ.

## Status Report Format

When the user asks about spend, or when a threshold is crossed:

```
## Cost Guard Status

Budget: $5.00 (alert mode)
Estimated spend: $3.42 (68% of budget)
├─ Input tokens:  ~284,000 ($0.85)
├─ Output tokens: ~51,200  ($2.56)
└─ Tool calls:    34

Status: ✓ Within budget
```

When a threshold is crossed:

```
⚠ Cost Guard: 82% of $5.00 budget consumed (~$4.10)

Downgrade suggestions:
- Consider reading specific line ranges instead of full files
- Batch remaining edits into fewer tool calls
- Skip re-reading files you've already seen

Continue at current pace? Or adjust budget with /cost-guard $10
```

## Tracking Rules

1. Start tracking from the moment the budget is set, not session start
2. If no budget is set, do not track or report costs
3. Report at these thresholds: 50%, 80%, 100%, and every 25% after
4. Include the threshold report inline — don't interrupt the user's task flow,
   just append a brief status line after your response
5. When the session is clearly ending (user says thanks, goodbye, etc.),
   include a final cost summary

## Limitations

Be transparent: this is estimation, not metering. State clearly that:
- Token counts are approximated from character length
- Actual costs depend on prompt caching, batching, and pricing changes
- This is a planning tool, not a billing tool
