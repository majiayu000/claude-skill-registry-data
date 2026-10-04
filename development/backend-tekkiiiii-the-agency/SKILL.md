---
name: backend
description: >
  Designs, builds, and reviews backend systems: APIs, databases, server-side logic, authentication, file handling, webhooks, and microservices. Triggers when the user asks to build an API, design a database schema, write server-side code, set up authentication, handle file uploads, build webhooks, design microservices, optimize queries, or work with Node.js, Python, Go, Java, or any server-side technology. Also triggers proactively when reviewing backend code for performance, scalability, or correctness issues — including N+1 queries, missing indexes, connection pool exhaustion, and missing pagination. Key capabilities: layered architecture patterns (routes/controllers/services/repositories), REST design with correct HTTP status codes, UUID-based public IDs with created_at/updated_at timestamps, JWT auth with short-lived access tokens + httpOnly refresh cookies, bcrypt password hashing at cost factor 12+, centralized error handling, structured JSON logging, parameterized queries only, and background job patterns. Ideal for backend engineers building from scratch or debugging existing systems. Also for: architecture reviews, query optimization, security audits on auth flows, and API contract design.
---

# Backend Development Skill

## Before Building — Clarify:
1. **Framework/Language**: Node.js (Express/Fastify/Hono), Python (FastAPI/Django), Go, Java Spring?
2. **Database**: Relational (PostgreSQL/MySQL) or NoSQL (MongoDB/Redis)?
3. **Auth method**: JWT, sessions, OAuth, API keys?
4. **Deployment target**: Serverless, containers, VPS?
5. **Scale expectations**: Requests/sec, data volume?

## API Design Principles

### REST Best Practices
- Use nouns for resources, verbs for HTTP methods
- `GET /users/:id` not `GET /getUser`
- Consistent response envelope:
```json
{
  "data": {},
  "error": null,
  "meta": { "page": 1, "total": 100 }
}
```
- Use correct HTTP status codes (200, 201, 400, 401, 403, 404, 422, 500)
- Version your API: `/api/v1/...`

### Request Validation
- Validate and sanitize ALL inputs before processing
- Return descriptive 422 errors with field-level messages
- Use Zod (TS), Pydantic (Python), or class-validator

## Database Patterns

### Schema Design
- Use UUIDs over sequential IDs for public-facing IDs
- Always include `created_at`, `updated_at` timestamps
- Index foreign keys and frequently queried columns
- Soft deletes with `deleted_at` when data history matters

### Query Optimization
- Avoid N+1 queries — use JOINs or eager loading
- Use `EXPLAIN ANALYZE` to debug slow queries
- Paginate all list endpoints (cursor-based for large datasets)
- Cache expensive queries with Redis (TTL based on data freshness)

## Authentication & Sessions
- Hash passwords with bcrypt (cost factor 12+)
- JWT: short-lived access tokens (15min) + refresh tokens (7-30 days)
- Store refresh tokens in httpOnly cookies, not localStorage
- Always validate token on protected routes middleware-level

## Error Handling
- Centralized error handler middleware
- Never expose stack traces in production responses
- Log errors with context (user ID, request ID, timestamp)
- Use structured logging (JSON) for easy querying

## Code Structure (Node.js example)
```
src/
├── routes/        # Route definitions only
├── controllers/   # Request/response handling
├── services/      # Business logic
├── repositories/  # Database queries
├── middleware/    # Auth, validation, logging
├── models/        # DB schemas/types
└── utils/         # Shared helpers
```

## Performance Checklist
- [ ] Database connections pooled (not opened per request)
- [ ] Async/await used correctly (no blocking the event loop)
- [ ] Background jobs offloaded to queue (Bull, Celery, etc.)
- [ ] Rate limiting on public endpoints
- [ ] Response compression enabled (gzip/brotli)
- [ ] Health check endpoint at `GET /health`

## Security Reminders
- Parameterized queries always (no string concatenation in SQL)
- CORS configured restrictively
- Helmet.js or equivalent security headers
- Secrets in environment variables, never in code