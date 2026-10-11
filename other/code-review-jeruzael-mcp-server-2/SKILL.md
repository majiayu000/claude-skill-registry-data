---
name: code-review
description: Review code changes like a careful software engineer before merge, deployment, client demo, pull request, or handover. Use when Codex needs to inspect diffs or changed files after features, bug fixes, refactors, database migrations, authentication changes, authorization changes, API contract changes, frontend UI changes, backend changes, DevOps changes, tests, documentation updates, or business-critical workflows such as bookings, orders, payments, permissions, reports, staff management, customer data, and production data handling.
---

# Code Review

Use this skill when code needs a quality gate rather than more implementation.

## Core Rule

Inspect the actual diff or changed files before approving. Prioritize correctness, security, authorization, data integrity, user-visible behavior, and missing tests over style opinions.

## Workflow

1. Understand review context:
   - intended feature/fix/refactor, changed files, affected user flow, affected roles, frontend/backend/database/DevOps scope, production data impact, and security sensitivity
2. Inspect the diff or changed files:
   - added, modified, deleted, renamed, config, dependency, migration, test, and documentation files
3. Check requirement alignment:
   - requested behavior, acceptance criteria, missing behavior, unrelated behavior, unintended behavior changes, complete user journey, and documented assumptions
4. Check correctness:
   - conditions, calculations, data mapping, paths, methods, field names, status transitions, dates, nulls, async behavior, imports, returns, races, loops, and filters
5. Check API contract consistency:
   - method, path, params, body, response shape, status codes, error format, auth headers, permissions, pagination/filtering, and date/time format
6. Check validation:
   - required fields, types, lengths, formats, enums, numeric ranges, file restrictions, status rules, duplicates, backend validation, and frontend validation
7. Check authentication and authorization:
   - auth required, user loading, role checks, ownership, shop/branch/tenant scope, privileged actions, guessed IDs, and backend enforcement
8. Check security:
   - secrets, logs, password/token exposure, SQL injection, raw SQL, file uploads, CORS, CSRF, redirects, sensitive errors, excessive API data, private data exposure, and unsafe dependencies
9. Check data integrity:
   - constraints, null handling, defaults, duplicates, status lifecycle, soft/hard delete, audit trail, transactions, partial failure, migration safety, and backfill needs
10. Check error handling:
   - validation, not found, unauthorized, forbidden, network, external API, database, empty state, frontend display, fallback messages, and logging
11. Check frontend behavior when applicable:
   - loading, error, empty, success, forms, duplicate submit prevention, state refresh, cache invalidation, navigation, responsive behavior, accessibility, design consistency, and permission visibility
12. Check backend architecture when applicable:
   - routes, controllers, services, repositories, schemas, error response patterns, auth middleware, transactions, logging, response consistency, tests, and docs
13. Check database and migration risk when applicable.
14. Check performance:
   - repeated calls, missing pagination, N+1 queries, indexes, payload size, re-renders, heavy components, unbounded loops, large bundle additions, and slow build/test changes
15. Check maintainability:
   - naming, function size, component boundaries, duplication, project patterns, unnecessary abstraction, complexity, unrelated refactors, comments, and business logic flow
16. Check tests and documentation:
   - coverage for success, validation, permissions, edge cases, regressions, commands run, failures, README/API/env/deployment/handover updates
17. Categorize findings by severity.
18. Provide approval status:
   - Approved, Approved with comments, Changes requested, or Blocked
19. Summarize findings first, with file/location, risk, and recommended fix.

Read `references/code-review-checklist.md` for detailed review categories, severity definitions, approval status rules, and the final report format.

## Non-Negotiable Rules

- Do not approve changes without inspecting the actual diff or files.
- Do not focus only on style while ignoring correctness.
- Do not ignore security-sensitive areas.
- Do not ignore backend authorization.
- Do not ignore data ownership and tenant/shop scoping.
- Do not ignore validation.
- Do not ignore error states.
- Do not ignore test coverage for risky changes.
- Do not suggest unrelated rewrites unless necessary.
- Do not over-review harmless style details.
- Do not claim tests passed unless they were actually run.
- Do not hide uncertainty.
- Separate blocking issues from optional improvements.
- Keep feedback specific, actionable, and respectful.

## Output Contract

When using this skill, provide:

1. Findings first, ordered by severity.
2. Review scope.
3. Overall assessment and approval status.
4. Critical, high, medium, low, and optional findings as applicable.
5. Requirement coverage.
6. Security and permission review.
7. Data and API review.
8. Frontend/backend/database review as applicable.
9. Test review and commands/results.
10. Recommended next steps.
