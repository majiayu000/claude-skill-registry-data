---
name: foundations
description: "Cloud-agnostic principles: least-privilege IAM, network isolation, managed services first, staged deploys, cost guards, doc-driven provider choice. Use before any provider-specific work."
---

# foundations

Principles transfer, service names do not. Decide on principles, then resolve against the provider's current docs.
## Inspection

Inventory workloads, data sensitivity, compliance needs, traffic shape, team ops capacity, and current provider commitments.

## Decision rules

Managed services by default; least privilege always; multi-cloud only with a named reason (residency, negotiation, DR) — never by accident.


## Activate when

- Choosing compute, data, networking, or observability on any cloud; comparing providers.

## Do NOT activate for

- Provider API specifics (see aws-foundations, gcp, azure).

## Procedure

1. Identity: least privilege per workload, short-lived credentials, MFA on humans, full audit trail.
2. Network: private subnets for data/compute, narrow security-group/firewall rules, no public datastores.
3. Managed first: managed DB/queues/secrets over self-hosted unless a measured reason says otherwise.
4. Deploy: staged rollouts with health-checked rollback; infra as code with locked provider versions.
5. Observe: metrics/alarms, structured logs, tracing, SLOs with error budgets.
6. Cost: budgets + anomaly alerts from day one; lifecycle rules on logs/artifacts.
7. Research: resolve every service choice against the provider docs for the configured version (registry: `../../research/documentation-search/references/framework-registry.yaml` — aws, gcp, azure). Runtime procedure: `../../research/documentation-search/`.
8. Verify: scratch-env deploy, kill-and-recover drill, restore-from-backup drill, cost report reviewed.

## References
- Provider leaves: `../aws-foundations/`, `../gcp/`, `../azure/`.

## Failure modes

Premature multi-cloud; self-hosting undifferentiated services; open security groups/SGs 'temporarily'; no cost alerts until the bill.

## Escalation

Provider specifics → cloud/aws-foundations, gcp, azure (resolved against current docs).
