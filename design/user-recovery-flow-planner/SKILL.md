---
name: user-recovery-flow-planner
description: Plans how users recover from mistakes, invalid input, failed requests, expired sessions, interrupted workflows, and uncertain outcomes. Use when the user asks to design recovery paths, error handling, retry behavior, undo flows, reauthentication, draft preservation, conflict resolution, support escalation, or resilient user journeys before implementation.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: product-designers-and-frontend-teams
  tags:
    - user-recovery
    - error-handling
    - resilient-ux
    - validation
    - session-expiry
    - interruption-recovery
  status: draft
  side_effects: none
---

# User Recovery Flow Planner

## Purpose

Plan user-centered recovery paths for moments when an interface cannot complete the expected action. Turn mistakes, invalid input, request failures, expired sessions, interrupted workflows, and ambiguous outcomes into clear user actions, system responses, data-preservation rules, and acceptance scenarios.

## When to use this skill

Use this skill when:

- A feature needs explicit recovery behavior before design, implementation, or QA.
- Users may lose progress, submit invalid data, retry failed requests, reauthenticate, resolve conflicts, undo actions, or resume interrupted work.
- Requirements mention errors, failures, timeouts, drafts, sessions, offline states, duplicate submissions, or support escalation without defining the user path.
- A team needs implementation-ready recovery requirements for product, design, frontend, backend, QA, analytics, or support alignment.

Do not use this skill when:

- The user needs a complete happy-path user journey; use `user-flow-planner` first, then apply this skill to recovery branches.
- The task is only to audit already-built interface states; use `interface-state-coverage-review`.
- The request is only technical retry architecture with no observable user behavior.
- Recovery would require legal, security, payments, or account-risk decisions that must be made by an owner; identify the decision instead of inventing policy.

## Inputs to inspect

Start with available evidence, then state assumptions where context is missing:

- Feature brief, user stories, acceptance criteria, or current flow maps
- Forms, validation rules, data constraints, permissions, and authentication requirements
- Screens, routes, components, copy, wireframes, screenshots, or prototypes
- API, backend, integration, payment, upload, or long-running job behavior
- Session timeout rules, draft/autosave behavior, local storage, and persistence boundaries
- Known support issues, analytics events, error logs, bug reports, or user complaints
- Accessibility, localization, privacy, security, and compliance constraints that affect recovery

## Recovery scenarios to cover

Consider these scenarios and mark any non-applicable ones explicitly:

1. **User mistake:** typo, wrong selection, accidental deletion, duplicate action, navigation away, or cancellation.
2. **Invalid input:** missing required data, malformed value, constraint conflict, server-side validation failure, or stale client validation.
3. **Failed request:** network loss, timeout, service error, rate limit, dependency outage, upload failure, or partial success.
4. **Expired or changed session:** authentication timeout, permission change, signed-out state, revoked access, or multi-tab drift.
5. **Interrupted workflow:** browser refresh, tab close, device switch, backgrounding, offline transition, or long-running process abandonment.
6. **Conflict or concurrency:** stale data, simultaneous edits, optimistic update rollback, duplicate submission, inventory or slot conflict.
7. **Uncertain outcome:** user cannot tell whether an action succeeded, failed, is pending, or will complete later.
8. **Terminal failure:** recovery is impossible or unsafe, requiring support, safe exit, alternative path, or explicit loss notice.

## Workflow

1. **Frame the recovery boundary.** Restate the user goal, action at risk, critical data, success state, and what harm recovery must prevent.
2. **Map failure entry points.** Identify exactly where recovery may begin: before submission, during submission, after optimistic UI, after navigation, after timeout, after reauth, or on return.
3. **Classify each scenario.** Label the scenario type, trigger, detection method, affected users, severity, frequency if known, and whether recovery is automatic, guided, or impossible.
4. **Define preservation rules.** Specify what input, draft state, attachments, selections, unsaved edits, progress, and context must be retained, discarded, redacted, or revalidated.
5. **Plan the user-visible response.** Define message content, placement, tone, focus behavior, disabled/enabled actions, progress indicators, and accessible announcements.
6. **Choose recovery actions.** Provide concrete next actions such as fix field, retry, undo, restore draft, resume, reauthenticate, refresh data, choose alternative, contact support, or exit safely.
7. **Handle system safeguards.** Note idempotency, duplicate prevention, rollback, conflict merge, stale data refresh, background retry, timeout, cancellation, and confirmation needs.
8. **Close every path.** Define how the user knows recovery succeeded, failed again, escalated, or reached a terminal state. Avoid loops with no escalation or exit.
9. **Extract implementation implications.** List state model changes, persistence needs, validation responsibilities, API contracts, telemetry, support metadata, QA fixtures, and copy requirements.
10. **Write acceptance scenarios.** Convert recovery paths into Given/When/Then checks that include preserved data, visible feedback, accessible focus/announcement behavior, and final state.
11. **Record open decisions.** Call out policy, security, data retention, payments, support, or product decisions that materially change recovery.

## Output format

Return:

```md
## Recovery frame

- User goal:
- Risky action or workflow:
- Critical data to protect:
- Recovery goals:
- Assumptions:
- Out of scope:

## Recovery scenario inventory

| ID | Scenario | Trigger | Detection | Severity | Recovery type | Outcome |
|---|---|---|---|---|---|---|

## Recovery flow details

### R1 — Scenario name

- Scenario type:
- Entry point:
- User impact:
- Preserve or discard:
- User-visible response:
- Available actions:
- System safeguards:
- Success state:
- Repeat failure or terminal state:

## Preservation and feedback matrix

| Context | Preserve | Revalidate | User message | User action | System action |
|---|---|---|---|---|---|

## Implementation implications

- Interface states:
- Validation and permissions:
- Persistence and draft handling:
- Idempotency and duplicate prevention:
- API or integration contracts:
- Telemetry and support data:
- Copy and accessibility requirements:

## Acceptance scenarios

- [ ] Given ..., when ..., then ...

## Open decisions

| Priority | Decision | Why it matters | Suggested owner | Safe default |
|---|---|---|---|---|
```

## Quality bar

The task is complete only when:

- Every high-risk mistake, invalid input, failed request, expired session, and interruption has a planned recovery or an explicit not-applicable reason.
- Each recovery flow has an entry point, preserved data rule, user-visible response, available next action, success state, and terminal fallback.
- The plan distinguishes user actions from system actions.
- Retry, undo, resume, reauthentication, conflict resolution, and support escalation are included where relevant.
- Data loss, duplicate submission, ambiguity, and infinite retry loops are actively prevented.
- Accessibility requirements cover focus, announcements, keyboard path, and understandable error text.
- Implementation implications and acceptance scenarios are specific enough for design, engineering, and QA to act on.
- Open decisions are limited to choices that materially change recovery behavior.

## Edge cases

- If the operation has financial, destructive, privacy-sensitive, or account-security impact, prefer explicit confirmation and owner review over automatic recovery.
- If the action may have succeeded despite an error, avoid encouraging duplicate submission until idempotency or status checking is defined.
- If reauthentication is required, preserve non-sensitive progress and return the user to the exact recoverable context when safe.
- If an upload or long-running job fails midway, define partial progress visibility, retry granularity, cancellation, and cleanup.
- If multiple tabs or collaborators can change the same data, define stale-state refresh and conflict resolution before save.
- If offline use is possible, distinguish queued, saved locally, synced, failed-to-sync, and conflict states.
- If recovery is impossible, state what is lost, why it cannot be recovered, what evidence is available, and how the user exits or gets help.

## Related skills

- `user-flow-planner`
- `interface-state-coverage-review`
- `progressive-enhancement-planner`
- `requirements-gap-finder`
