---
name: retry-strategy-review
description: Use when reviewing payment retries for outcome certainty, idempotency, duplicate protection, decline semantics, budgets, backoff, customer consent, reconciliation, and operational stop conditions.
kind: skill
status: active
owner: APT
last_updated: 2026-08-16
source: consolidated APT guidance
title: "Retry Strategy Review"
domain: "payments"
source_paths: ["apt-principles-agents/skills/payments/retry-strategy-review/SKILL.md"]
---

# Retry Strategy Review

## Purpose

Determine when a payment operation may be retried safely, who may initiate it, what identity it retains, and how unknown outcomes and duplicate financial effects are prevented or reconciled.

## When to Use

Use for synchronous calls, queues, webhooks, scheduled/recurring payments, recovery workers, client retries, provider failover, incident remediation, or decline-handling changes.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Inventory each retried operation, initiator, lifecycle state, provider behavior, idempotency mechanism, attempt identity, timeout, and financial side effect.
2. Classify outcomes as confirmed success, confirmed terminal failure, correctable request, transient failure, rate-limited, authentication/configuration failure, or unknown outcome.
3. Define eligibility, maximum attempts, elapsed-time budget, backoff/jitter, concurrency control, circuit breaking, customer consent, and stop conditions per class.
4. Ensure all layers share or safely translate idempotency and correlation identifiers; prevent client, queue, worker, and provider retries from multiplying attempts.
5. Test lost responses, delayed callbacks, duplicate delivery, worker restart, concurrent retry, provider timeout/outage, failover, hard decline, recovery, and reconciliation.
6. Publish retry/non-retry matrices, residual duplicate risk, monitoring, alerts, manual recovery, customer/support messaging, rollback, and accountable approvals.

## Outputs

A retry eligibility matrix, idempotency/correlation design, budget and backoff policy, scenario evidence, duplicate/unknown-outcome controls, monitoring, recovery runbook, and approval record.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Classify confirmed success, terminal failure, correctable request, transient failure, rate limit, configuration/authentication failure, and unknown outcome separately.
- Retry only operations with verified idempotency, safe lifecycle state, preserved attempt identity, and bounded financial exposure.
- Coordinate client, API, queue, worker, webhook, and provider retries so layered mechanisms cannot multiply attempts.
- Set attempt and elapsed-time budgets, backoff/jitter, concurrency controls, circuit breakers, consent, and stop conditions.
- Test lost response, delayed callback, duplicate delivery, restart, concurrency, outage, failover, decline, and reconciliation scenarios.
- Monitor attempt chains, duplicates, unknown outcomes, recovery age, customer impact, and manual interventions with named owners.

## Required Reading

Read the canonical Payments principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Payments principles](../../../principles/payments/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
