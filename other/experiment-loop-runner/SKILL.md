---
name: experiment-loop-runner
description: >
  Run a controlled THINK-EXECUTE-REFLECT loop for coding, research, or ML
  experiments. Use when the user wants iterative improvement, benchmark-driven
  changes, autonomous experiment planning, low-cost monitoring, or progress
  reports without uncontrolled agent drift. Skip production release loops that
  require gateway policy, trace-to-regression evals, guardrail rollout, budgets,
  or shadow/canary traffic; use `$auto-skill-build-agent-reliability-loop`.
---

# Experiment Loop Runner

Use this when progress depends on repeated trials with measurable outcomes.

## Required Control Files

```text
PROJECT_BRIEF.md
workspace/
  MEMORY_LOG.md
  HUMAN_DIRECTIVE.md
  runs/
```

## Loop

1. **Think**: read brief, constraints, current best, and recent memory.
2. **Execute**: make one bounded change or launch one run.
3. **Verify**: run the agreed test/benchmark/dry-run.
4. **Reflect**: record result, decision, and next branch.
5. **Stop or iterate**: continue only when improvement signal exists.

## Low-Cost Monitoring

For long jobs, monitor with shell/process/log checks instead of repeatedly
asking the model to think:

- PID alive check
- tail last log lines
- GPU/CPU status when relevant
- metric parser script

## Stop Conditions

- target reached
- no improvement after N attempts
- verification becomes flaky
- human directive changes the objective
- cost/time budget exceeded

For production agent release loops that combine traces, eval groups, gateway
routing, guardrails, budgets, and shadow/canary traffic, use
`$auto-skill-build-agent-reliability-loop` first and use this skill for the
bounded experiment cycles inside that plan.

Reference pattern source: `sources/auto-deep-researcher-24x7`.

## Validation

- Each loop has a stop condition before execution.
- Each iteration records the change, verification command, result, and next decision.
- Experiments that affect production users/tools are escalated to the reliability-loop skill.
