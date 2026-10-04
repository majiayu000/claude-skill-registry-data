---
name: planning-progressive-delivery
kind: skill
status: ready
provenance:
  principles:
  - P013
  - P016
  - P014
  - P023
  - P031
  - P038
  claims:
  - C00949
  - C01121
  - C01122
  - C02076
  - C00483
  - C00594
  - C00595
  - C00042
  - C00043
  - C01933
  - C00815
  - C00816
  evidence:
  - E00392
  - E00419
  - E00420
  - E00570
  - E00259
  - E00302
  - E00303
  - E00027
  - E00028
  - E00561
  - E00351
  - E00352
  source_anchors:
  - 9fe26df35c80-c0019
  - 9fe26df35c80-c0027
  - 0bea4daa68ab-c0017
  - 50b64948b031-c0006
  - 9fe26df35c80-c0004
  - 9d4b1cf206e5-c0002
  - 0bea4daa68ab-c0010
  - 9fe26df35c80-c0013
  authored_from_digest: b1fee07605452a435ac0ad2c584b50b165cbc2cd93c1377c7823f3f2a544f100
---

# Planning progressive delivery

## Purpose

Plan how a change reaches users so that deploying is low-risk and reversible. Decouple deployment
from release using feature toggles and dark launches, roll changes out gradually with blue-green or
canary patterns, and keep a fast, tested rollback path (P005). The point is to separate "the code
is in production" from "users see the feature", then expose the change in controlled steps you can
undo.

## When to use

- Planning how to release a risky or user-visible change.
- A team wants to deploy frequently without exposing unfinished features.
- Reviewing a deployment strategy for production readiness.

Skip the full apparatus for a trivial change to an internal tool where staged rollout adds no value
— say so rather than imposing ceremony.

## Procedure

1. **Decouple deployment from release (P005).** Use feature toggles and dark launching so deploying
   code to production no longer means exposing a feature to users (CL009). This lets the team
   integrate and deploy continuously while controlling who sees what, and turns a release into a
   configuration change rather than a redeploy.
2. **Choose the rollout pattern for the risk:**
   - **Blue-green** — run two identical environments and switch traffic between them to release with
     little or no downtime and roll back fast by switching back (CL010). Use when you want an
     instant, whole-environment cutover and an instant reverse.
   - **Canary** — expose a small fraction of traffic to the new version first, watch for
     regressions, and roll back quickly if the canary degrades (CL056). Use when you want to limit
     blast radius and gather real signal before full exposure.
   Toggles and dark launches compose with both: they gate the feature; the pattern gates the
   traffic.
3. **Instrument the rollout and define the abort condition (P005).** Before exposing traffic, wire
   production telemetry and automated anomaly detection so a bad release is detected and acted on
   before customers are widely affected (CL011). State the metric and threshold that trips a
   rollback up front — a rollback path is only real if it is fast, tested, and has a clear trigger.
4. **Stage the exposure.** Sequence the steps (dark launch → small canary → wider canary → full, or
   blue-green cutover with a hold-and-watch window), naming who/what is exposed at each step and the
   go/abort check between steps.
5. **For `review`/`validate` requests,** check the plan has: deployment decoupled from release, a
   rollout pattern matched to the risk, instrumentation with a named abort condition, and a fast
   tested rollback. Flag any plan that relies on a big-bang cutover with no rollback as the gap to
   close.

## Inputs

- The change, its blast radius, and how user-visible it is.
- Current deployment mechanism and whether toggles/dark launch, blue-green, or canary are available.
- The telemetry available to judge a release, and what "healthy" looks like for this service.

## Output

A staged rollout plan: how deployment is decoupled from release, the chosen pattern (blue-green or
canary) with rationale, the instrumentation and named abort condition, and the rollback path —
tied to P005. For `validate`, a pass-or-gap line per element.

## References

- `references/progressive-delivery-patterns-reference.md` — the pattern catalogue (toggle, dark
  launch, blue-green, canary, rollback).
- Sibling skills: `designing-deployment-pipelines` (what produces the deployable),
  `defining-slos-and-error-budgets` (the burn-rate signal that can drive an abort).

## Provenance

Derived from principle P005 (claims CL009, CL010, CL056, CL011; evidence EV009, EV010, EV056,
EV011) across `the-devops-handbook-c4933b3c` and `comp500-15893c30` (both distillation-only —
paraphrase, no verbatim quotation). Pattern names are stable practice; specific tooling for toggles,
traffic shifting, and telemetry changes quickly, so verify current vendor and project documentation.
