---
name: mission-control-budget-control
description: >-
  Tracks and enforces agent spend in Mission Control. Use this skill when
  recording costs via api.agents.recordSpend, declaring budgetDaily and
  budgetPerRun limits at registration, or reacting to budgetRemaining and
  budgetExceeded values returned by the heartbeat before spending more money.
version: 1.0.0
owner: software-factory
risk: medium
capabilities:
  - spend-recording
  - budget-limits
  - cost-tracking
requires_tools:
  - convex
related_skills:
  - mission-control-heartbeat
  - mission-control-run-logging
  - mission-control-register-agent
---

# Record Spend

Track your costs per run:

```
Mutation: api.agents.recordSpend
Args:
  agentId: Id<"agents">
  amount: number      — USD spent
  runId?: Id<"runs">
  description?: string
```

## Budget Rules

1. **Respect your budget** — check `budgetRemaining` in the heartbeat response before starting costly work; stop when `budgetExceeded` is true.
2. Budget limits are declared at registration: `budgetDaily` (daily USD cap) and `budgetPerRun` (per-run USD cap) — see `mission-control-register-agent`.
3. Report `spendSinceLastHeartbeat` on every heartbeat so Mission Control's running totals stay accurate (`mission-control-heartbeat`).
4. Attach `runId` where possible so spend ties back to a specific run (`mission-control-run-logging`) and the audit trail stays honest.
