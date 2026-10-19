---
name: operate-multi-agent-system
description: Prepare, operate, troubleshoot, or optimize a production multi-agent system. Use when defining system traces, SLOs, dashboards, alerts, budgets, capacity, privacy, manifests, incident response, rollback, topology changes, or dynamic registry operations.
---

# Operate a Multi-Agent System

Operate the whole coordination graph as one governed service while preserving member-level visibility.

## Workflow

1. Read the System Spec, operational ownership, SLOs, risk indicators, budgets, runbooks, and deployment topology.
2. Define a trace hierarchy for system run, workflow, delegation, member run, model request, tool call, approval, artifact, and effect.
3. Record composition manifest, policy decisions, graph state, budgets, terminal reason, and provenance without logging sensitive content by default.
4. Build SLOs for successful outcomes, critical safety gates, latency, cost, stuck workflows, partial effects, and human escalation.
5. Alert on unauthorized edges, budget exhaustion, depth or fan-out growth, disagreement, retry storms, duplicate effects, admission failures, stale approvals, and manifest drift.
6. Capacity-plan the full amplification envelope; apply admission control, concurrency pools, circuit breakers, and degraded modes.
7. Define rollback for member, prompt, policy, graph, registry, and workflow changes, including in-flight compatibility.
8. Exercise incident, quarantine, cancellation, and recovery runbooks.
9. Optimize only after measuring cost and latency per successful outcome.

## Required Output

Produce telemetry contracts, dashboards, alerts, system SLOs, capacity limits, privacy controls, incident runbooks, rollback and quarantine procedures, and owner mappings.

Read [the operations standard](references/standard.md) and adapt [the examples](references/examples.md).

## Guardrails

- Do not log prompts, full histories, credentials, or shared artifacts by default.
- Do not optimize one member while worsening system success cost or tail latency.
- Do not deploy graph or contract changes without in-flight compatibility analysis.
- Do not operate dynamic membership without rapid quarantine and manifest lookup.

## Completion Check

An on-call engineer must be able to identify the exact composition, locate a failed edge, bound further effects and spend, recover or terminate the run, and select a safe rollback.
