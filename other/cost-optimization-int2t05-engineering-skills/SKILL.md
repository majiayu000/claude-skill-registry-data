---
name: cost-optimization
description: Reduce measured cost while preserving required service quality. Triggers on "cost", "成本优化".
---

# Cost Optimization

## When to use

- Reduce measured cost while preserving required service quality.

**Not for:** performance for latency; architecture for unbuilt systems.

## Steps

1. Establish comparable billing, workload and service-quality baselines; redact account details.

2. Attribute dominant controllable costs across actual compute, storage, network, services and model calls.

3. Compare savings, effort, reliability and recovery; apply the smallest authorized change.

4. Re-measure under comparable conditions and label observed, estimated and unmeasurable savings.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `COST.md` only for a useful continuing ledger.

## Verify

- Cost comparisons state period and workload; quality regressions and estimated savings are explicit.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/cost-drivers.md](references/cost-drivers.md) — symptom→cause map for cloud spend: over-provisioning, idle resources, egress, storage lifecycle, reserved-capacity gaps, with per-platform levers
