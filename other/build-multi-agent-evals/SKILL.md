---
name: build-multi-agent-evals
description: Build evaluation datasets, harnesses, baselines, and release gates for multi-agent systems. Use when testing topology choice, routing, interaction contracts, coordination, durability, dynamic membership, adversarial propagation, end-to-end quality, or system cost and latency.
---

# Build Multi-Agent Evals

Evaluate the composition, not only its members.

## Workflow

1. Read the System Spec, risk scenarios, topology decision, member evals, and release policy.
2. Preserve member-level gates, then add interaction, coordination, durability, adversarial, and end-to-end datasets.
3. Compare against deterministic and single-agent baselines using matched tasks and budgets.
4. Test routing choices, undeclared-edge denial, context minimization, authority narrowing, aggregation, dissent, termination, and budget enforcement.
5. Inject member failures, malformed and late results, duplicates, reordered events, crashes, stale approvals, registry poisoning, and partial effects.
6. Measure task quality, risk-scenario pass rates, latency distribution, total and per-success cost, model and tool calls, fan-out, depth, and human intervention.
7. Require exact composition provenance: system, members, versions, prompts, policies, graph, datasets, evaluator, models, and settings.
8. Run system evals and release checks through the project's own validation tooling or CI so results carry provenance and gates fail closed.

## Required Output

Produce versioned datasets, deterministic evaluators where possible, an approved baseline, normalized system report, and fail-closed release policy.

Read [the evaluation standard](references/standard.md) and adapt [the examples](references/examples.md).

## Guardrails

- Member pass rates do not prove composition safety.
- Do not average away a failed critical scenario.
- Do not compare architectures with different task sets or unreported budgets.
- Do not use an unversioned LLM judge as the only hard gate.

## Completion Check

The evidence must show whether multi-agent coordination beats the simpler baseline and whether every critical system-risk scenario, authority boundary, budget, and recovery path passes.
