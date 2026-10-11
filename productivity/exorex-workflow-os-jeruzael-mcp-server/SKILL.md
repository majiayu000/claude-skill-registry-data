---
name: exorex-workflow-os
description: End-to-end delivery workflow and best-practice enforcement for Exorex engineering projects across web, mobile, automations, and VPS deployments. Use when Codex needs to plan work, define acceptance criteria, implement changes, run quality gates, deploy safely, and keep documentation/handover artifacts current.
---

# Exorex Workflow OS

Execute work using a gated workflow so delivery is fast, consistent, and auditable.
Prefer simple implementation choices, but do not skip quality gates.

## Workflow Decision

Choose one path before implementation:

1. Full flow: new feature, architecture change, integration change, deployment change.
2. Fast lane: urgent fix with narrow scope and no contract/schema change.

Use Fast lane only if all are true:
- Scope is one behavior fix.
- Rollback is straightforward.
- Existing tests can cover the change quickly.

If any condition fails, use Full flow.

## Full Flow

### 1) Intake and Scope

- Define goal, user impact, constraints, and non-goals in bullets.
- Define measurable success criteria.
- Write acceptance criteria before coding.
- Identify risks early (security, data integrity, availability, cost).

Read `references/workflow.md` for templates.

### 2) Plan and Slice

- Break work into vertical slices that are independently testable.
- Set exit criteria for each slice.
- Keep one active slice at a time.
- Record explicit assumptions.

Read `references/workflow.md` for planning templates and slice format.

### 3) Build

- Keep business logic out of UI.
- Enforce feature boundaries.
- Validate input server-side.
- Apply idempotency for retries and background jobs.
- Use least-privilege auth and deny-by-default authz.

Read `references/web-mobile-structure.md` if the task touches app structure.

### 4) Verify

- Run lint, typecheck, and relevant tests.
- Validate edge cases and failure paths.
- Confirm logs and error signals are meaningful.
- Confirm secrets are not exposed.

Read `references/checklists.md` for release gates.

### 5) Deploy and Operate

- Use staged rollout when risk is non-trivial.
- Verify post-deploy health and critical user journey.
- Keep rollback path ready and tested.

Read `references/vps-deploy.md` for VPS web deployment tasks.

### 6) Document and Handover

- Update docs in the same change set as code.
- Record major decisions and operational procedures.
- Update deploy and runbook instructions when behavior changes.

Read `references/documentation.md` for required docs and templates.

## Fast Lane

Use only for urgent, contained fixes:

1. Write a one-paragraph problem statement and blast radius.
2. Implement the minimum safe fix.
3. Run targeted tests plus smoke verification.
4. Update changelog/runbook entry.
5. Schedule follow-up hardening if debt was introduced.

## Non-Negotiable Rules

1. Never ship without explicit acceptance criteria.
2. Never skip server-side validation.
3. Never commit or log secrets.
4. Never merge behavior changes without docs updates.
5. Never deploy without rollback steps.

## Output Contract

When completing work with this skill, report:

1. Scope and assumptions.
2. Changes made (code/config/docs).
3. Validation performed.
4. Risks and mitigations.
5. Follow-up tasks.

## Reference Map

- `references/workflow.md`: planning model, phases, templates.
- `references/checklists.md`: quality gates for engineering and release.
- `references/documentation.md`: documentation standards and handover.
- `references/web-mobile-structure.md`: feature-first structure and routing.
- `references/vps-deploy.md`: VPS deployment baseline.
