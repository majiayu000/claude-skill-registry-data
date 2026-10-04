---
name: cloud-cost-review
description: Review cloud, hosting, CI, storage, database, and observability cost risks. Use when Codex is asked to estimate or reduce infrastructure cost, review usage drivers, flag cost surprises, or plan cost guardrails across cloud providers.
license: MIT
---

# Cloud Cost Review

## Core Workflow

1. Identify provider, services, environments, workloads, usage drivers, and
   billing owner.
2. Review cost drivers: compute, storage, database, bandwidth, logs, traces,
   build minutes, queues, backups, and managed services.
3. Flag unbounded scale, duplicate environments, retention risk, over-provision
   settings, and missing budgets or alerts.
4. Recommend right-sizing, retention limits, scheduling, caching, quotas, and
   budget guardrails.
5. Separate rough estimates from verified billing data.
6. Include monitoring and review cadence.

## Safety Rules

- Do not invent current spend, pricing, discounts, or commitments.
- Verify provider-specific prices from current official pricing pages before
  making precise cost claims.
- Do not delete resources, reduce retention, or change capacity without
  approval.

## Deliverable Shape

For cost reviews, provide:

- Scope and assumptions
- Cost drivers
- Risk areas
- Estimate confidence
- Guardrails and alerts
- Optimization options
- Approval needs
- Follow-up data needed

## References

- Read `references/cloud-cost-review-checklist.md` when reviewing cloud or
  hosting cost risk.
