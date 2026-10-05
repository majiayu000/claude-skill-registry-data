---
name: product-tracking-feature-update
description: "Update product telemetry when a new feature, flow, experiment, or lifecycle change is introduced. Use for instrument this feature, add analytics to a flow, update tracking plan, or telemetry delta review. Turkish triggers: özellik değişince tracking planını güncelle, event/property etkisi ve sürüm notu."
---

# Product Tracking: Feature Update

Keep telemetry current as the product changes without accumulating unreviewed events.

## Workflow

1. Read the feature brief, acceptance criteria, relevant tracking plan, and current code boundary.
2. Identify the user decision or value moment that the feature changes. If there is none, explain why new telemetry may be unnecessary.
3. Propose a small delta: added, changed, deprecated, and intentionally unchanged events.
4. Update event contracts, identity/consent implications, measures, and test cases.
5. Implement only after the delta is reviewed, then verify source, tests, and documentation agree.

## Output

Use a short change record:

```text
Feature and decision link
Added / changed / deprecated events
Schema and privacy impact
Implementation locations
Validation evidence
Rollback or removal condition
```

## Guardrails

- Do not duplicate an existing event under a new name merely because the UI changed.
- Preserve historical comparability or document a clean measurement break.
- Do not collect experimental, sensitive, or user-generated content without an explicit legal/privacy decision.
