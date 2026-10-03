---
name: defect-triage
description: Triage defects by establishing reproducibility, user/system impact, severity, scope, regression status, ownership, duplicates, release relevance, and the evidence needed for a decision without turning priority into guesswork.
---
# Defect Triage

Use when new bug reports or test findings need consistent disposition and ownership.

## Procedure
1. Confirm the report contains enough evidence to evaluate: expected versus actual behavior, environment/revision, preconditions, steps or observed pattern, affected user/data, and artifacts/log identifiers when relevant.
2. Determine status: reproducible, intermittent with evidence, needs information, duplicate, expected/accepted behavior, environment/setup issue, or confirmed defect. Do not close uncertain reports merely because one reproduction attempt failed.
3. Assess impact: blocked versus degraded task, data/state correctness, security/accessibility, availability, frequency, number/type of users/tenants, recoverability/workaround, and consequence of leaving it unfixed.
4. Determine scope and regression status using nearby versions/environments/roles/data when evidence allows. A widespread shared-component defect may outrank a more dramatic isolated symptom.
5. Assign the owning product/engineering/design/infrastructure/integration role based on the first known failing boundary, or assign an investigation owner if root layer is still unclear.
6. Link duplicates and related incidents while preserving unique environment/evidence that may reveal a different trigger.
7. Set severity/priority using the project's definitions and release context. Separate defect severity from scheduling priority; business timing can change priority without changing technical/user impact.
8. Identify the minimum additional evidence required for ambiguous high-impact reports and route that request explicitly.
9. For release blockers, state the blocking acceptance/risk, required fix or approved exception owner, and re-test scope after remediation.
10. Keep triage disposition updated when new reproduction, impact, root-cause, or workaround evidence changes the decision.

## Decision rules
- Severity describes impact; priority describes when the organization chooses to act.
- A duplicate is not useless if it contains new scope or trigger evidence.
- Do not assign root cause from the visible symptom alone; assign investigation ownership when needed.
- QA can recommend/block based on quality criteria, but product/business risk acceptance belongs to the designated decision owner.

## Quality gate
Triage is complete when the report's evidence/status is clear, impact and scope support the severity, ownership and next action are explicit, duplicates and release relevance are handled, uncertain cases state exactly what evidence is missing, and the decision can be revisited when new facts arrive.