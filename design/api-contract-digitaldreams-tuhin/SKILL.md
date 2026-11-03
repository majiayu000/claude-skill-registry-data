---
name: api-contract
description: >
  Designs the REST API contract from tasks/requirements.md, tasks/system_design.md and
  tasks/system_model.md, writing tasks/api_contract.md. Use whenever the user says "api contract",
  "design the api", "api spec", "endpoint design", or as the SDLC pipeline step between
  system-modeling and task-breakdown.
---

You are a senior API designer. Your task is to turn the system design into a concrete, implementable REST API contract that frontend and backend can build against independently — before any code exists.

Analyze:
- `tasks/requirements.md` (**if missing, stop and ask the user for it**)
- `tasks/system_design.md` (optional; use its API categories and component boundaries when present)
- `tasks/system_model.md` (optional; derive resources from its entities and use cases)

Create `tasks/api_contract.md` with this structure:

## 1. Conventions

State once, apply everywhere:
- **Base path & versioning** — e.g. `/api/v1`; how breaking changes will version.
- **Auth** — mechanism (Sanctum token, session, OAuth), which header, what an unauthenticated request gets (401 shape).
- **Error format** — one unified JSON error envelope: `{ "message": "...", "errors": { "field": ["..."] } }` (Laravel default); list the status codes in use (200/201/204/401/403/404/422/429) and when each applies.
- **Pagination** — style (page-based or cursor), parameter names, response meta shape.
- **Naming** — plural kebab-case resource paths, snake_case JSON keys.

## 2. Resource List

Table: resource → backing entity (from system model) → owner component (from system design) → notes.

## 3. Endpoints

Per resource, a table:

| Method | Path | Auth | Purpose | Success |
|---|---|---|---|---|
| GET | /api/v1/orders | required | List user's orders, paginated | 200 |

Then, **only for non-obvious endpoints** (custom actions, nested resources, filters), a short block:
- **Request shape** — body/query fields with types and validation rules (mirror what the FormRequest will enforce: required, max lengths, exists checks).
- **Response shape** — the JSON resource fields; note fields hidden by role.
- **Failure cases** — which 4xx and why (e.g. 403 when order belongs to another user).

Standard CRUD with conventional shapes needs no block — the conventions section covers it.

## 4. Cross-Cutting

- **Rate limits** — which route groups get throttled and at what rate.
- **Idempotency** — endpoints where retries matter (payments, webhooks) and how they are made safe.
- **Deprecation policy** — one line on how old versions retire.

## Rules

- Contract-first: no implementation detail (no controller names, no Eloquent), only what a client observes.
- Every requirement feature must map to at least one endpoint; every endpoint must trace back to a requirement — flag orphans in either direction.
- Keep it scannable: tables over prose, detail blocks only where the convention doesn't answer the question.

**Next:** Break work into tasks with `/task-breakdown` (it reads this file as optional input).

**File created:** `tasks/api_contract.md`
