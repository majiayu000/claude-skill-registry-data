---
name: api-design
description: >
  Design clean and consistent APIs. Use when the user says "design an API",
  "API design review", "design these endpoints", "REST API for X", "GraphQL schema",
  "API contract", "how should this endpoint work", "review my API design",
  or wants to create or improve an API interface
  - even if they don't explicitly say "API design".
---

## Overview

Based on **"A Philosophy of Software Design"** by John Ousterhout. Ousterhout's key principle: modules should be deep - simple interface, powerful implementation. Applied to APIs: the surface area exposed to callers should be as small as possible, while the behavior provided should be as rich as possible. A leaky abstraction (where callers need to understand implementation details) is a design failure.

## Workflow

### Step 1: Define the API's job
Before designing any endpoint, state what the API enables:
- What is the caller trying to accomplish?
- What information does the caller have?
- What should the API hide from the caller?

Ousterhout: if callers need to know how the API works internally to use it correctly, the API is leaky.

### Step 2: Design resources (REST) or schema (GraphQL)
**REST:**
- Resources are nouns, not verbs: `/users`, `/orders` not `/getUsers`, `/createOrder`
- Use HTTP verbs for actions: GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove)
- Nest for ownership: `/users/{id}/orders` (orders owned by a user)
- Don't nest beyond 2 levels deep

**GraphQL:**
- Types model your domain, not your database schema
- Queries fetch data, mutations change it, subscriptions stream it
- Design the schema from the client's perspective: what does the UI need?

### Step 3: Design request and response contracts
For each endpoint:
```
Endpoint: [METHOD] /path/{param}
Purpose: [one sentence]
Auth: [required scope or token type]

Request:
  Path params: [required identifiers]
  Query params: [optional filters, pagination]
  Body: [JSON schema with required/optional fields]

Response (200):
  [JSON schema]

Errors:
  400 - [validation failure - which fields, why]
  401 - [unauthenticated]
  403 - [unauthorized - caller lacks permission]
  404 - [resource not found]
  409 - [conflict - e.g. duplicate]
  422 - [unprocessable entity - valid syntax, invalid semantics]
  500 - [internal error]
```

### Step 4: Apply consistency rules
Pick conventions and apply them everywhere:
- Naming: snake_case or camelCase for fields (pick one)
- Dates: ISO 8601 (`2026-03-03T14:30:00Z`)
- IDs: UUID or integer (pick one, apply everywhere)
- Pagination: cursor-based or page/limit (pick one)
- Errors: consistent error response shape `{ error: { code, message, details } }`

Inconsistency is the top complaint from API consumers.

### Step 5: Design for the caller's mental model
Ousterhout's information hiding principle: don't expose implementation artifacts.
- Don't expose database table names or internal IDs in API paths
- Don't return internal error codes that callers can't act on
- Don't require callers to make multiple requests for data they logically need together

### Step 6: Version the API
Every public API needs a versioning strategy before it ships:
- URL versioning: `/v1/users` (most common, most visible)
- Header versioning: `API-Version: 2026-01-01`
- Pick a strategy before v1 ships - changing it later breaks all callers

## Anti-Patterns

**1. Verbs in resource paths**
Bad: `POST /createUser`, `GET /getUserById`
Good: `POST /users`, `GET /users/{id}`

**2. Inconsistent error shapes**
Bad: Some endpoints return `{ error: "message" }`, others return `{ message: "error" }`.
Good: One error schema, applied everywhere.

**3. Leaking implementation details**
Bad: `/api/db/users_table/row/42`
Good: `/api/users/42`

**4. No versioning plan on day 1**
Bad: Ship v1 with no versioning, then break callers when you need to change the contract.
Good: Version from the first public release. Breaking changes require a new version.

## Quality Checklist

- [ ] Resources are nouns, HTTP verbs are the actions
- [ ] Request and response contracts documented for every endpoint
- [ ] All error codes documented with when each occurs
- [ ] Naming convention consistent across all endpoints (snake_case or camelCase)
- [ ] Dates in ISO 8601, IDs consistent type throughout
- [ ] No implementation details exposed to callers
- [ ] Versioning strategy defined before first public release
- [ ] Pagination strategy defined and consistent
