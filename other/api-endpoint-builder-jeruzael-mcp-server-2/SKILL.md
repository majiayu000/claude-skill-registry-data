---
name: api-endpoint-builder
description: Create or update backend API endpoints in a clean, consistent, secure, and testable way. Use when Codex needs to build endpoint behavior for bookings, orders, users, reports, auth, registration, notifications, inventory, payment tracking, admin tools, staff management, customer profiles, rider workflows, shop owner workflows, file uploads, dashboard summaries, search/filtering, status updates, approvals, external integrations, or webhooks with validation, authentication, authorization, database access, frontend contract updates, tests, and documentation.
---

# API Endpoint Builder

Use this skill when a task requires backend API behavior.

## Core Rule

Inspect existing API patterns before creating or modifying an endpoint. Follow the current route, validation, response, auth, error, database, test, and documentation style.

## Workflow

1. Understand the endpoint requirement:
   - purpose, actor, business action, request data, response data, permissions, related records, error cases, and consumer
2. Inspect existing API patterns:
   - routes, controllers, services, repositories, schemas/DTOs, response shape, error handling, auth, tests, docs
3. Design the endpoint contract:
   - method, path, params, body, response, status codes, auth, authorization, pagination/filtering/sorting
4. Define request data and validation rules.
5. Define response data and error responses.
6. Implement authentication using existing project mechanisms.
7. Implement authorization and ownership checks on the backend.
8. Place business logic in the correct layer.
9. Implement safe database access:
   - scoped queries, ownership filters, parameterization, pagination, transactions, null handling, constraints
10. Add safe logging only where useful.
11. Update API client, shared types, OpenAPI/contract, or frontend service files when needed.
12. Add or update endpoint tests where practical.
13. Update API documentation when the project has it.
14. Run relevant checks discovered from project scripts/docs.
15. Summarize the endpoint contract and verification result.

Read `references/endpoint-checklist.md` for contract templates, status code guidance, validation and permission checklists, testing guidance, and final report format.

## Non-Negotiable Rules

- Do not invent a new response format if the project already has one.
- Do not skip backend validation.
- Do not rely only on frontend validation.
- Do not skip backend authorization for protected data.
- Do not expose data across tenants, shops, customers, or roles.
- Do not use unsafe SQL string interpolation.
- Do not place complex business logic in route handlers when the project uses services.
- Do not return sensitive data unless explicitly required and safe.
- Do not ignore pagination for potentially large lists.
- Do not log secrets, passwords, tokens, payment details, or sensitive personal data.
- Do not claim the endpoint works unless verified or verification limits are clearly stated.

## Output Contract

When using this skill, provide:

1. Endpoint implemented or updated.
2. Purpose and endpoint contract.
3. Affected layers.
4. Validation and permission rules.
5. Database behavior.
6. Files changed.
7. Tests/checks or manual verification.
8. Risks and follow-up recommendations.
