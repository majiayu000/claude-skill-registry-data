---
name: api-contract-review
description: Compare frontend API usage with backend endpoint definitions to find contract mismatches. Use when Codex needs to debug or review frontend-backend API alignment for failing screens, rejected form submissions, unexpected API data, changed backend responses, mobile/backend field mismatches, missing auth headers, status code handling, error response handling, pagination/filtering, date/time formatting, file uploads, shared types, or API docs before changing code.
---

# API Contract Review

Use this skill to verify whether frontend and backend agree on an API contract.

## Core Rule

Compare actual frontend code against actual backend code. Do not assume either side is wrong until both sides have been inspected.

## Workflow

1. Identify the API flow:
   - frontend screen/function, backend endpoint, user action, data sent, data expected, error behavior, actor/role
2. Inspect frontend API usage:
   - API client, fetch/Axios call, data-fetching hook, form handler, mobile service, types/interfaces, state updates, auth headers, error handling
3. Inspect backend API definition:
   - route, controller, service, schema/DTO, validation, auth middleware, authorization, database query, response formatter, tests, docs
4. Compare method and path.
5. Compare headers and authentication behavior.
6. Compare path/query parameters.
7. Compare request body or upload format.
8. Compare authorization and ownership rules.
9. Compare success response shape, field names, data types, nullability, pagination, dates, and enums.
10. Compare error response shape and status code handling.
11. Check shared contract sources if present:
   - OpenAPI, generated clients, shared TypeScript types, Zod schemas, Postman collections, API markdown docs
12. Produce a contract mismatch report with recommended changes and likely files affected.

Read `references/contract-review-template.md` for mismatch categories, checklist, and report format.

## Behavior Rules

- Identify exact mismatches, not vague "API mismatch" statements.
- Recommend the smallest safe alignment change.
- Do not change both frontend and backend unnecessarily.
- Do not ignore auth, authorization, nullability, error response, or date/time differences.
- Do not expose secrets while reviewing headers or config.
- If no formal contract exists, recommend one for important APIs.

## Output Contract

When using this skill, provide:

1. API flow reviewed.
2. Frontend expectation.
3. Backend implementation.
4. Contract match summary.
5. Mismatches table with severity and recommended fix.
6. Recommended frontend/backend/docs changes.
7. Files likely affected.
8. Testing checklist.
9. Risks and follow-up.
