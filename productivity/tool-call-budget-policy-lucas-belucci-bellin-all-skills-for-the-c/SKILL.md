---
name: tool-call-budget-policy
description: Set per-task tool-call, latency, and cost budgets with prioritization and recovery rules for agent workflows.
---

# Tool Call Budget Policy

## Goal

Keep tool-using agents efficient while preserving the calls required for evidence and safe verification.

## Inputs to inspect

Agent workflow, tools available, expected task complexity, cost/latency constraints, and completion criteria.

## Workflow

1. Estimate the necessary evidence-gathering, mutation, and verification calls for each task class; define a soft budget and a hard stop.
2. Prioritize calls by expected information gain and dependency order, grouping independent reads when the runtime supports safe parallel execution.
3. Reserve capacity for post-mutation verification so an agent does not spend its entire budget on exploration or writes.
4. Define what happens when budget is nearly exhausted: summarize evidence, stop optional work, avoid repeated failing calls, and ask for approval before expanding scope.
5. Measure successful completion, verification coverage, retries, latency, and cost per task; revise budgets from observed traces.

## Validation checklist

- [ ] The hard budget is observable and has clear stopping behavior.
- [ ] Critical safety/evidence checks are not dropped to meet an arbitrary cost target.
- [ ] Failed calls have a bounded retry/backoff policy.
- [ ] Mutation workflows reserve verification capacity.
- [ ] Metrics compare task outcomes, not only number of calls.

## Required output

Deliver a budget matrix by task type, prioritization rules, escalation behavior, and a short evaluation plan using real execution traces.

## Boundaries and failure handling

Do not claim a budget is cost-optimal without measurements; do not let automation continue repeating a broken call until it exhausts the session.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
