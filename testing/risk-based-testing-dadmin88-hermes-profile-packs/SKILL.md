---
name: risk-based-testing
description: Prioritize testing by identifying plausible failures, affected users/assets, likelihood, impact, detectability, change novelty, and existing controls, then spend validation effort where it buys the most confidence.
---
# Risk-Based Testing

Use when the test surface is larger than the available time or when a change needs deeper validation in some areas than others.

## Procedure
1. Identify the changed and preserved behavior, critical journeys, data/state, integrations, platforms, and operational boundaries in scope.
2. Enumerate plausible failure modes from requirements, code/design changes, architecture, historical defects, incidents, complexity, concurrency, dependencies, migrations, and user behavior.
3. Assess consequence and likelihood using the project's normal risk language. Include user harm, data loss/corruption, security/privacy, revenue/operations, availability, compatibility, and support burden as relevant.
4. Consider detectability and recovery. A moderate defect that is silent and hard to recover from may deserve more validation than a visible reversible failure.
5. Account for existing controls: strong automated tests, type/schema checks, independent review, monitoring, feature flags, rollback, or proven unchanged components can reduce incremental test need.
6. Rank risks and select the cheapest reliable technique for each: focused automated tests, exploratory charters, contract/E2E, performance, accessibility, security, migration, fault/recovery, or production monitoring.
7. Allocate depth to the highest risks, but retain lightweight smoke coverage for low-risk critical paths so obvious wiring failures are not missed.
8. Update the risk ranking when testing finds unexpected defects, scope changes, or evidence disproves an assumption.
9. Record what was intentionally not tested and why, along with the monitoring/rollback/control that contains the residual risk.
10. Report quality confidence in terms of covered risks and remaining uncertainty rather than hours spent or number of test cases executed.

## Decision rules
- Risk is about plausible consequence and uncertainty, not file count or developer seniority.
- Historical stability is evidence but can become stale when dependencies or architecture change.
- Do not use risk scoring to rationalize skipping basic validation of critical journeys.
- Testing should follow the risk as it crosses profiles/nodes/services; organizational boundaries do not make the failure less important.

## Quality gate
The approach is risk-based when material failure modes are explicitly ranked, validation effort matches consequence and uncertainty, existing controls are credited without blind trust, new findings update the plan, residual untested risk is visible, and release confidence can be explained from evidence rather than test volume.