---
name: load-testing
description: Measure capacity under authorized representative traffic. Triggers on "load test", "压测".
---

# Load Testing

## When to use

- Measure capacity under authorized representative traffic.

**Not for:** performance for bottlenecks; api-testing for correctness.

## Steps

1. Agree environment, traffic budget, load targets and stop conditions; do not assume production access.

2. Build runnable scripts with realistic operations, datasets and arrivals; check functional responses first.

3. Run relevant ramp, sustained, burst or stress profiles and observe latency, errors and saturation within agreed limits.

4. Identify bottlenecks and recovery and record reproducible conditions in the approved capacity report.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/CAPACITY.md` for durable capacity decisions.

## Verify

- Scripts and actual measurements exist; errors and saturation inform conclusions and untested autoscaling remains unverified.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/load-profiles.md](references/load-profiles.md) — traffic-mix modeling, test-pattern catalog (ramp/soak/spike/stress), breaking-point characterization, autoscaling validation checklist
