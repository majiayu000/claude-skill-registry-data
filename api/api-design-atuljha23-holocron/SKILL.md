---
name: api-design
description: REST and GraphQL API design conventions — resource modeling, pagination, error envelopes, versioning, idempotency. Use when adding, changing, or reviewing endpoints.
---

# API design

## REST

### Resource, not action
URLs name nouns. Actions are verbs.

Good: `POST /users/:id/password-reset`
Bad:  `POST /resetUserPassword?id=123`

### Status codes mean things
- `200` success with body
- `201` created (include `Location`)
- `204` success, no body
- `400` client sent something invalid (bad syntax, bad shape)
- `401` not authenticated
- `403` authenticated but not authorized
- `404` resource doesn't exist (or the caller isn't allowed to know it does)
- `409` conflict (version conflict, duplicate, precondition failed)
- `422` semantic validation failed (body parses but rules reject)
- `429` rate limited
- `5xx` server fault — internal detail logged, opaque to caller

### Error envelope
Pick one. Use it everywhere.

```json
{
  "error": {
    "code": "resource_not_found",
    "message": "User alice@example.com not found.",
    "requestId": "abc123"
  }
}
```

- `code` is machine-readable, stable, lowercase_snake.
- `message` is human-readable. Safe to surface.
- `requestId` lets the caller tell you what went wrong without you reading prod logs.

### Pagination
Cursor-based for anything you'll scale. Offset paging breaks under concurrent writes.

```
GET /messages?cursor=abc&limit=50
→ { items: [...], nextCursor: "xyz" }
```

### Idempotency
Any POST that has side-effects and will be retried needs an idempotency key:

```
POST /payments
Idempotency-Key: <uuid-v4>
```

Server stores the (key → response) for a reasonable TTL. Retries return the cached response, not a second charge.

### Versioning
Prefer additive changes. Add fields; don't remove or rename. When you must break, version:

- URL (`/v2/...`) — simple, explicit, slightly ugly
- Accept header (`Accept: application/vnd.foo.v2+json`) — prettier URLs, slightly opaque

Pick one per service. Never mix.

## GraphQL

### Nullability is a contract
`String!` says "this WILL be present". If you're not sure, it's `String` (nullable). A lie here cascades.

### Relay-style pagination
Connections, edges, pageInfo, cursors. Don't invent your own.

### One mutation per intent
`updateUser(input: { name, email, password })` is three different operations glued together. Split them.

### Errors as types
Return `{ user: User | UserNotFoundError | ValidationError }` unions where it matters. Generic `errors[]` at the top is for transport-level fault, not business rules.

## Across both

- **Typed shapes.** Schemas (OpenAPI / GraphQL / proto). Generate clients from them.
- **Rate limit** expensive or abuse-prone endpoints.
- **Observability.** Every request has a `requestId`. Log it. Return it on errors. Tie logs, metrics, and traces together with it.
- **Auth at the edge** — check in the handler or middleware the handler trusts. Never rely on the gateway alone.
