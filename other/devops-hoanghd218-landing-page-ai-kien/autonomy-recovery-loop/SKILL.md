---
name: autonomy-recovery-loop
description: Autonomous failure recovery and self-healing loop for tasks, benchmarks, or services. Use when a run fails, dependencies break, or the system must diagnose, remediate, and re-run safely under guardrails.
---

# Autonomy Recovery Loop

Use this skill to recover from failed runs, missing dependencies, or unstable services.

## Workflow

1) Load a recovery plan (use assets/recovery_plan.json).
2) Check dependency health and environment drift.
3) Apply guardrails and select safe recovery actions.
4) Run the minimal failing step.
5) If it passes, re-run the full task.

## Scripts

- Run: python scripts/recover.py --plan assets/recovery_plan.json --auto-start

## Output Expectations

- Provide a short cause -> action -> result chain.
- State whether recovery succeeded and what fallback was used.
