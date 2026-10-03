---
name: regression-testing
description: Plan and execute risk-based regression testing around a change by mapping affected behavior, preserved critical flows, integrations, data states, environments, and prior defect history.
---
# Regression Testing

Use before release or completion when a change could have broken previously working behavior beyond its immediate acceptance criteria.

## Procedure
1. Understand the change and its intended boundaries. Identify which existing behavior must remain unchanged and which shared components, services, data, permissions, or configuration the change touches.
2. Build a regression risk map from likely blast radius rather than rerunning a generic checklist. Include critical user journeys, adjacent features, shared state/components, integrations, persistence, migrations, permissions, and platform/device variants implicated by the change.
3. Prioritize by impact and plausibility. Test business-critical or irreversible flows, historically fragile areas, and shared paths first; low-risk isolated cosmetics should not consume the same effort as authentication, payments, data mutation, or core workflow changes.
4. Establish a known baseline or expected behavior for each selected scenario. Where possible compare with the previous accepted version, existing automated tests, specifications, or recorded behavior rather than memory alone.
5. Execute targeted regression around the changed surface, then broader critical-flow regression proportional to the blast radius. Vary realistic state such as existing/new users, permissions, empty/populated data, persisted sessions, retries, navigation, or alternate entry points where relevant.
6. Include failure and recovery paths when the change touches async work, dependencies, persistence, or networking. A feature that succeeds normally can still regress on retry, cancellation, partial failure, or recovery.
7. Use automation for stable repeatable coverage and manual/exploratory testing for visual, interaction, environment, or state combinations where human observation adds value. Do not duplicate automation manually without a reason.
8. Record defects with exact reproduction evidence and identify whether they are confirmed regressions, pre-existing defects, or uncertain because the prior behavior cannot be established.
9. Re-test fixes and the surrounding scenario after correction. A fix for one regression can introduce another change to the same shared path.
10. Summarize what was covered, what passed, what failed, what was intentionally not tested, and the residual release risk.

## Decision rules
- Regression scope follows risk and shared surface, not raw diff size.
- Do not call every discovered bug a regression unless prior accepted behavior supports that claim.
- Critical flows deserve stable repeatable coverage even when the current change did not touch their UI directly if the underlying shared path changed.
- A clean regression run is evidence for the tested scope, not proof that no defect exists anywhere.

## Quality gate
Regression testing is complete when the plausible blast radius has been translated into prioritized scenarios, critical preserved behavior and relevant failure paths have been exercised, findings distinguish new regressions from pre-existing issues, fixes are re-tested, and untested residual risk is explicit.