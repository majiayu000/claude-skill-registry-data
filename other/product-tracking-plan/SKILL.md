---
name: product-tracking-plan
description: "Design a privacy-aware product telemetry plan with event taxonomy, properties, identity rules, validation, and decision links. Use when asked what to track, to create an analytics plan, event schema, measurement plan, or telemetry specification. Turkish triggers: ürün tracking planı, hangi event ve property, ölçüm kapsamı ve doğrulama."
---

# Product Tracking: Design a Plan

Turn product decisions into a minimum useful telemetry contract. Prefer a small, well-defined event set over exhaustive click logging.

## Inputs

Read `product-tracking-model` and `product-tracking-audit` artifacts when available. If not, state which decisions remain assumptions.

## Workflow

1. Start from decision questions, success measures, and core value moments.
2. Define events as stable past-tense business actions, not UI implementation details.
3. For each event, specify trigger, required properties, optional properties, actor/context, destination boundary, and validation case.
4. Define identity, account/group, anonymous-to-known, consent, opt-out, deletion, retention, and internal/test-user handling without assuming provider APIs.
5. Add a test matrix for happy path, duplicate delivery, retry, offline/error, and prohibited-data cases.
6. Compare with the audit and label additions, renames, deprecations, and unresolved decisions.

## Deliverable

Produce a reviewable plan, optionally at `.telemetry/tracking-plan.md`:

```text
Objective and decisions
Event taxonomy
Event contract table
Identity and privacy contract
Measurement definitions and caveats
Implementation sequence
Validation and rollout plan
Delta from current state
```

## Guardrails

- Do not include secrets, unrestricted text, sensitive categories, or unnecessary identifiers.
- Do not silently choose a vendor or invoke external APIs.
- Require a reviewed plan before `product-tracking-implementation` changes code.
