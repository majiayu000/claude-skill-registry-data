---
name: agent-observability
description: >
  Add lightweight local observability to Codex/agent workflows. Use when
  tracking local runs, traces, evals, cost, token usage, cache efficiency,
  model comparisons, failure rates, or claudetop-style monitoring. Skip when
  designing production gateway policy, staged guardrails, shadow traffic,
  model budgets, or trace-to-regression loops; use
  `$auto-skill-build-agent-reliability-loop`.
---

# Agent Observability

Use lightweight local observability before adopting a full platform.

## Minimal Run Ledger

Create:

```text
.agent-runs/
  runs.jsonl
  evals.md
  costs.md
```

Each `runs.jsonl` entry should include:

```json
{"ts":"","task":"","model":"","inputs":"","commands":[],"result":"","tokens_est":"","cost_est":"","status":""}
```

## What To Track

- task type and outcome
- commands run
- tests passed/failed
- estimated tokens and cost
- repeated failure causes
- user corrections
- guardrail or safety decisions

## Eval Loop

1. Define 3-10 realistic tasks.
2. Run the same task across workflow variants.
3. Score correctness, time, tokens, and human intervention.
4. Keep the cheaper path only if quality is comparable.

## Skip Or Escalate

When observability needs gateway policy, staged guardrails, shadow traffic,
trace-to-regression feedback, or model budgets, switch to
`$auto-skill-build-agent-reliability-loop`. Keep this skill for local ledgers
and lightweight eval/cost tracking.

Use full platforms like Future AGI when you need hosted traces, simulations,
gateway routing, or production guardrails. Use local ledgers for personal workflows.

For appending or summarizing `.agent-runs/runs.jsonl`, use
`$auto-skill-build-agent-run-ledger-dashboard`.

For Codex Supercharge artifact grades and subagent/automation handoff status,
use `$auto-skill-build-supercharge-feedback-loop`; it writes a separate local
feedback stream under `plugins/codex-supercharge/.agent-runs/`.

## Validation

- Each tracked run has a task, status, commands/tests, and outcome.
- Cost/token notes are marked as estimates unless measured.
- Repeated failures are summarized into a follow-up or eval case.
