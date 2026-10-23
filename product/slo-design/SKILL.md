---
name: slo-design
description: "Use when defining, reviewing or operating a service level objective: choose the SLI from what users feel, set the target as a product decision, write the error budget policy before the budget burns, and alert on burn rate over two windows rather than on a raw error threshold."
---

# slo-design

A method for turning "the service should be reliable" into a measured promise and a rule for what happens when
it is not kept. The usual failure is an objective with a number and nothing behind it: an indicator that stays
green while users suffer, a target nobody chose, a budget with no consequence, an alert that pages on noise or
fires after the damage. The block owns no monitoring product and no alert syntax. Related:
`skills/observability-instrumentation` §3 and §4 (the metrics and the symptom-based alert this builds on),
`skills/failure-classification-before-retry` §1 (which failures count as bad events), `skills/spend-guard-fail-closed`
§1 (a budget that closes by default, the same stance for money), `skills/feature-flag-lifecycle` §2 (a ramp whose
abort criterion is a burn rate).

## When
- A service, journey or pipeline gets a reliability target for the first time.
- An existing objective is reviewed: it never burns, always burns, or nobody acts when it does.
- An alert is added on an error rate, latency or availability figure.
- A launch, ramp or experiment needs a rule for how much risk is acceptable now.

## Steps

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | The SLI: specification versus implementation, what to measure per kind of system, good over valid events, what is excluded | an indicator is chosen or reviewed | [`01-choosing-the-sli.md`](./references/01-choosing-the-sli.md) |
| 2 | The target as a product decision, the window, the error budget and the policy for when it is spent | a target is set or a budget is spent | [`02-target-budget-policy.md`](./references/02-target-budget-policy.md) |
| 3 | Alerting on burn rate: criteria, why simple thresholds fail, two windows, low and extreme targets | an alert is written, tuned or complained about | [`03-burn-rate-alerting.md`](./references/03-burn-rate-alerting.md) |

## Output / checkpoint
No pipeline checkpoint. For each objective: the SLI as a ratio with its numerator, denominator, exclusions and
point of measurement; the target, the window and who approved them; the error budget in the SLI's own unit; the
written policy for what changes when it is spent, with its approvers and next review date; the alert conditions
with severity and responder. An objective without a policy is not "live".

## Guardrails
- Never carry another service's target or alert figures. Targets are chosen with the product owner from what
  users need and what the system sustains, and alert figures are re-derived (and re-read from the primary
  source) before use.
- Never use a resource figure (CPU, memory, restarts) as the SLI: users do not feel it.
- Never publish an objective nobody is empowered to enforce. If the people who would pay for the policy do not
  accept it, change the objective, not the policy's enforcement.
- Never mix the internal objective with a contractual promise to customers: they have different audiences and
  consequences, and the internal one should trigger action first.
- Never page on a condition the responder cannot act on (`skills/observability-instrumentation` §4).

## Origin
The Google SRE Workbook chapters "Implementing SLOs" and "Alerting on SLOs", read 2026-10-19 at sre.google, plus
one MIT skill collection's SLO workflow, rewritten. Provenance, what was removed and not verified:
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
