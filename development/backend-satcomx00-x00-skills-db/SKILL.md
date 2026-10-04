---
name: backend
description: Backend and API design patterns — RESTful and GraphQL API conventions, error handling, pagination, authentication patterns, and database best practices.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
---

# backend

Backend and API design patterns — RESTful and GraphQL API conventions, error handling, pagination, authentication patterns, and database best practices.

## Instructions

Apply these backend practices when building services and APIs:

## Guidelines

### Type Safety

- **Type-safe schemas for every route**: define request and response types with Zod (TypeScript) or Pydantic (Python); validate before any business logic runs
- **Typed database models**: use an ORM with typed models (Prisma, Drizzle, SQLAlchemy); never return raw untyped query results
- **Validated environment variables**: parse and validate all `process.env` / `os.environ` values at application boot using a typed schema — fail fast if required vars are missing or invalid
- **No `any` in controller, service, or repository layers** — every function must have explicit parameter and return types

### Error Handling

- Every route handler must be wrapped in error-catching middleware or use typed `Result`/`Either` types
- Database errors must be caught and converted to domain errors before reaching the controller
- Never expose internal error details (stack traces, DB query strings) to API consumers
- Always return a `traceId` in error responses for debuggability

### Async / Performance

- All I/O operations (DB, HTTP, file) must be async — no synchronous blocking calls in request handlers
- Set explicit timeouts on all outbound HTTP calls and DB queries
- Use connection pooling for database connections; never create a new connection per request

### Security Baseline

- Validate and sanitise every request field — reject unknown fields (strict schema parsing)
- Rate-limit all public endpoints
- Never log request bodies that may contain credentials or PII

---

### RESTful API Design

**Resource naming — use nouns, not verbs:**
```
GET    /users           → list users
POST   /users           → create a user
GET    /users/:id       → get a user
PATCH  /users/:id       → partially update a user
PUT    /users/:id       → replace a user
DELETE /users/:id       → delete a user
GET    /users/:id/posts → list a user's posts
```

**HTTP status codes:**
| Situation | Code |
|-----------|------|
| OK / resource returned | 200 |
| Created | 201 |
| No content (DELETE) | 204 |
| Bad request (validation) | 400 |
| Unauthenticated | 401 |
| Forbidden | 403 |
| Not found | 404 |
| Conflict (duplicate) | 409 |
| Unprocessable entity | 422 |
| Server error | 500 |

**Versioning:** prefix routes with `/v1/`, `/v2/` etc. Never break a published API version.

### Error Response Format

Return consistent, machine-readable errors:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "email", "message": "Must be a valid email address" }
    ],
    "traceId": "abc123"
  }
}
```

Always include a `traceId` for debuggability in production.

### Pagination

Use cursor-based pagination for large or real-time datasets; offset for simple cases:

**Cursor-based (preferred):**
```json
{
  "data": [...],
  "pagination": {
    "hasNextPage": true,
    "endCursor": "eyJpZCI6MTAwfQ=="
  }
}
```

**Offset-based:**
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "perPage": 20,
    "total": 543
  }
}
```

### Authentication Patterns

- **JWT (stateless)**: use short-lived access tokens (15 min) + refresh tokens (7 days stored in `HttpOnly` cookie)
- **Session-based**: server stores session; send `HttpOnly; Secure; SameSite=Strict` cookie
- **API keys**: for machine-to-machine; hash the key in the DB (never store plaintext)
- **OAuth 2.0 / OIDC**: for third-party login; delegate to an identity provider

Validate tokens on every request. Never trust client-supplied user IDs without re-verifying the token.

### Database Best Practices

**Schema design:**
- Use UUIDs (v4 or v7) for primary keys in distributed systems
- Add `created_at` and `updated_at` timestamps to every table
- Use soft deletes (`deleted_at`) for data that needs audit trails
- Index foreign keys and any column used in frequent WHERE/ORDER BY clauses

**Query discipline:**
- Use an ORM or query builder — avoid raw string SQL except for complex reports
- Always paginate queries that can return unbounded rows
- Avoid N+1: use eager loading (`.include()`, `JOIN`, `dataloader`)
- Wrap related mutations in a transaction

**Migrations:**
- Use a migration tool (Flyway, Liquibase, Prisma Migrate, Alembic)
- Migrations must be backward-compatible with the previous deployment (expand-contract pattern)
- Never edit a committed migration — create a new one

### Service Layer Pattern

Organise code in layers:
```
Controller (HTTP) → Service (business logic) → Repository (data access)
```

- Controllers validate input and map HTTP ↔ domain
- Services contain all business rules; no HTTP/DB concerns
- Repositories encapsulate all DB queries; return domain objects

### Background Jobs

- Use a queue (BullMQ, Celery, Sidekiq) for work that shouldn't block an HTTP response
- Jobs must be idempotent — safe to retry
- Implement exponential backoff with jitter for retries
- Dead-letter queue for failed jobs after max retries

## Examples

```ts
// Controller: validate input, delegate to service
app.post('/users', async (req, res) => {
  const parsed = createUserSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(422).json({ error: parsed.error.format() });
  }
  const user = await userService.create(parsed.data);
  res.status(201).json(user);
});

// Service: business logic only
class UserService {
  async create(data: CreateUserDto) {
    const existing = await this.userRepo.findByEmail(data.email);
    if (existing) throw new ConflictError('Email already registered');
    return this.userRepo.create({ ...data, passwordHash: await hash(data.password) });
  }
}
```

## References

- [REST API Design Best Practices](https://blog.stoplight.io/rest-api-standards)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [Cursor-based Pagination](https://relay.dev/graphql/connections.htm)
- [The Twelve-Factor App](https://12factor.net/)
- [Prisma ORM](https://www.prisma.io/)
