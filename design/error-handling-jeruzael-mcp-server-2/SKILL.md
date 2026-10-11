---
name: error-handling
description: Standardize how applications handle failures across frontend, backend, APIs, databases, integrations, forms, and user workflows. Use when Codex needs to fix confusing error messages, app crashes, blank screens after failed requests, inconsistent API error formats, missing validation display, raw stack traces, network failures, retry behavior, authentication errors, authorization errors, not found states, conflict errors, external service failures, upload errors, payment errors, unsafe logging, empty states incorrectly treated as errors, or inconsistent error behavior across screens and endpoints.
---

# Error Handling

Use this skill when failures need to be safe, understandable, recoverable, and consistent.

## Core Rule

Handle expected failures deliberately. Do not expose internals, lose user input, treat empty results as server errors, or let one failed request crash the whole workflow when a graceful fallback is possible.

## Workflow

1. Identify the error handling scope:
   - feature, screen, endpoint, user role, error types, frontend/backend/API/database/integration layer, sensitive data, and critical workflow impact
2. Inspect existing error patterns:
   - backend exception handlers, API error response format, validation errors, error codes, HTTP status conventions, frontend parsers, toasts, banners, field errors, empty states, retry buttons, error boundaries, logging, monitoring, auth handling, and API interceptors
3. Classify error types:
   - validation, authentication, authorization, not found, conflict, network, server, external service, timeout, unexpected response, and empty state
4. Standardize backend error responses:
   - stable code, user-safe message, optional field details, request ID when available, no secrets, and no raw stack traces in production
5. Use consistent HTTP status codes:
   - 400, 401, 403, 404, 409, 422, 429, 500, and 503 according to project convention
6. Handle validation errors:
   - field-level details, actionable messages, backend validation, and frontend mapping to form fields
7. Handle authentication errors:
   - missing/expired/invalid credentials, session-expired messaging, login redirect, and private data cleanup
8. Handle authorization errors:
   - forbidden role/scope/ownership actions with backend enforcement and safe frontend access-denied behavior
9. Handle not found and conflict errors safely:
   - avoid revealing sensitive existence where needed and guide users on duplicate or stale business states
10. Handle network, server, and external service errors:
   - preserve user input, show retry where safe, avoid false success, log safely, and define partial-success behavior
11. Treat empty states separately from errors.
12. Handle form errors:
   - field errors, general form errors, server validation, duplicate submit prevention, submit loading, preserved input, and success feedback
13. Design retry behavior:
   - retry safe transient failures; require idempotency or confirmation for payments, duplicate creation, email sending, inventory changes, and destructive actions
14. Add resilient frontend fallbacks:
   - error boundary, fallback UI, retry action, optional chaining, skeleton, empty/access-denied/not-found states, login redirect, and graceful degradation
15. Log safely and usefully:
   - include safe context such as error type, request ID, endpoint, user ID, role/scope, timestamp, external service name, and retry count; exclude secrets and sensitive payloads
16. Add or update tests where practical.
17. Run relevant checks discovered from project scripts or docs.
18. Summarize scope, existing issue, covered error types, backend format, frontend display, user experience, logging, files, checks, risks, and follow-up recommendations.

Read `references/error-handling-checklist.md` for status code guidance, response examples, frontend patterns, retry decisions, logging rules, tests, and the final report format.

## Non-Negotiable Rules

- Do not expose raw stack traces to users in production.
- Do not expose secrets, tokens, database details, or internal paths in error messages.
- Do not show vague generic errors when field-level validation is available.
- Do not treat empty states as server errors.
- Do not lose user input after recoverable form errors.
- Do not retry risky operations without idempotency or confirmation.
- Do not swallow errors silently.
- Do not return inconsistent error shapes across similar endpoints.
- Do not rely only on frontend error handling for security problems.
- Do not log sensitive data.
- Do not let one failed component crash the entire application when fallback is possible.
- Keep error messages user-safe, actionable, and consistent.

## Output Contract

When using this skill, provide:

1. Error handling scope and existing problem.
2. Error types covered.
3. Backend error response format and status codes.
4. Frontend error display behavior.
5. User experience during failure.
6. Retry and empty state behavior.
7. Logging and debugging behavior.
8. Files changed.
9. Tests/checks or manual verification.
10. Risks and follow-up recommendations.
