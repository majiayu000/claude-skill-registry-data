---
name: product-analytics
description: Measure what matters — event taxonomy, privacy-aware analytics, decided dashboards, honest A/B tests.
version: 1
triggers: product analytics, metrics, a/b test, event tracking, dashboards, kpi
category: Money & markets
blurb: Measure what matters — event design, privacy-aware analytics and honest experiments.
archetype: knowledge
example: Define the metrics that tell me if this feature worked.
---

# Product Analytics & Measurement

Measurement exists to make decisions. Define events before shipping, keep them privacy-safe, and let dashboards carry owners and targets — or don't build them.

## When to use
- Shipping any feature whose success should be knowable.
- Designing events, dashboards, funnels, or experiments.
- Fixing "we can't tell if this worked".

## Method
1. **Question first**: what decision will this data change? If none — don't track it. Metrics tie to a KPI tree (north star → inputs), not to curiosity.
2. **Event taxonomy**: naming convention (`object_action`, snake_case); versioned event spec per feature (properties, types, required/optional) reviewed BEFORE code; analytics reviewed in the PR.
3. **Data quality**: validation at capture; test events in staging; audit dashboards for dupes/drops; document definitions — a metric with two definitions is two bugs.
4. **Privacy-aware by construction**: no PII in events (IDs only, pseudonymous); consent gating where required (`privacy-compliance`); aggregate before export where possible.
5. **Dashboards with owners**: each chart = question + definition + owner + target; trends over snapshots; segment thoughtfully; retire dead metrics (no vanity walls).
6. **Experiments (A/B)**: hypothesis + primary metric + guardrails + sample-size rationale BEFORE launch; one change per test; assignment/blinding checks; write results down — including "no effect" (a result, not a failure).
7. **Feedback joins data**: qualitative themes (support) beside quantitative; both feed the backlog (`community-support`).

## Quality gates
- [ ] Event spec exists before the feature ships; validated in staging.
- [ ] No PII in events; consent respected.
- [ ] Dashboards have owners + definitions; dead ones retired.
- [ ] Experiments registered; results recorded.

## Red lines
- No PII in analytics; no unregistered experiments; no metrics without definitions; never dark-pattern measurement.

## Related
`privacy-compliance` · `agent-evaluation` · `community-support`.
