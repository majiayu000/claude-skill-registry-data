---
name: end-to-end-user-flow
description: Review, implement, or test complete user journeys across multiple screens, backend actions, API calls, database changes, permissions, state transitions, success states, failure states, and verification steps. Use when Codex needs to work on login, registration, onboarding, booking creation, checkout, payment flows, order tracking, order status updates, admin approval, staff invitation, staff management, rider assignment, delivery workflows, report generation, file uploads, customer profile updates, shop setup, inventory updates, notification workflows, password reset, role-based dashboard access, or any feature that must work from start to finish across frontend, backend, data, auth, state, and tests.
---

# End-to-End User Flow

Use this skill when the task is a real user journey rather than one isolated screen, endpoint, or component.

## Core Rule

Verify the workflow from the user's first action to the final business result. Do not assume the full flow works just because one screen renders or one API returns success.

## Workflow

1. Identify the user journey:
   - flow name, primary role, secondary roles, starting screen, ending screen or final state, business goal, required data, permissions, and systems involved
2. Map every step:
   - user action, screen/component, data entered or displayed, API call, backend behavior, database behavior, expected UI result, and possible failure state
3. Identify required data:
   - auth user, role, customer profile, shop profile, address, booking/order details, payment info, status values, assignments, report filters, uploads, notifications, route/query params, local state, server cache, and external services
4. Identify screens and navigation:
   - routes, navigation names, auth/role requirements, screen-entry data loading, actions, next screen, back behavior, empty states, and error states
5. Identify API calls:
   - method, endpoint, payload, query params, auth, permission, success response, error response, status codes, and frontend consumer
6. Identify backend and database effects:
   - records created/updated, status changes, history/audit rows, notifications, payment records, assignments, inventory changes, report effects, and cache invalidation
7. Identify permissions and access rules for every step:
   - who can start, view, update, approve, reject, report on, or be denied from the record; include user, role, shop, branch, tenant, and ownership scope
8. Identify state management requirements:
   - cache refresh, query invalidation, local/form state reset, dashboard refresh, logout behavior, role/scope switch behavior, and back-navigation behavior
9. Define success states:
   - confirmation, new record visible in list, dashboard count update, status change, redirect, notification, payment status, report inclusion, or audit entry
10. Define failure states:
   - invalid input, missing data, unauthorized, wrong role, expired session, API/network/payment/external service failure, duplicate submit, not found, stale data, and backend validation errors
11. Define edge cases:
   - refresh after submit, double submit, back after success, offline mid-flow, session expiration, payment succeeds but confirmation fails, API creates record but cache stays stale, scope changes, concurrent approval, mobile keyboard issues, timezone boundaries
12. Decide whether the task is implementation, testing, review, or all three.
13. Create an end-to-end test plan:
   - user role, data setup, start route, ordered actions, expected UI after each step, API/database effect, final result, and cleanup
14. Add automated E2E tests when practical and the project has a setup.
15. Add supporting API or integration tests when full E2E is unavailable or too fragile.
16. Provide a manual QA checklist when automation is unavailable or incomplete.
17. Run relevant checks discovered from project scripts or docs.
18. Summarize flow, roles, screens, APIs, data effects, permissions, success/failure states, tests, manual QA, files, commands, risks, and follow-up recommendations.

Read `references/user-flow-checklist.md` for journey mapping tables, API/backend/state checks, permission and edge-case prompts, E2E/manual QA planning, and the final report format.

## Non-Negotiable Rules

- Do not verify only one screen if the task is a full user journey.
- Do not ignore backend and database effects.
- Do not ignore permissions across steps.
- Do not ignore state refresh after successful actions.
- Do not skip failure states.
- Do not skip edge cases for critical workflows.
- Do not assume frontend success means backend success.
- Do not assume API success means user journey success.
- Do not rely only on the happy path for business-critical flows.
- Do not use fragile E2E selectors when stable selectors are available.
- Do not claim the full flow works unless it was verified or limitations are clearly stated.
- Keep flow steps clear enough for manual QA or automated test conversion.

## Output Contract

When using this skill, provide:

1. Flow name and business goal.
2. User roles involved.
3. Step-by-step flow map.
4. Required data.
5. Screens and navigation.
6. API calls.
7. Backend and database effects.
8. Permission rules.
9. State refresh requirements.
10. Success states, failure states, and edge cases.
11. Automated tests added, supporting tests, or manual QA checklist.
12. Files changed.
13. Commands run and real result.
14. Risks and follow-up recommendations.
