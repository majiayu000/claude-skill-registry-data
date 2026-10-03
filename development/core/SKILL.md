---
name: backend-core-principles
description: Universal backend principles and architecture patterns language-agnostic. Core foundation for backend architects covering validation, error handling, database design, security, and maintainability across any framework or language.
license: MIT
metadata:
  author: Mastra
  version: "1.0.0"
---

# Universal Backend Core Principles

Fundamental backend architecture and design principles applicable across all frameworks, languages, and ORMs. These are the foundational rules that must guide any backend implementation.

## When to Apply

Use this skill as the foundation for every backend task:
- Writing new API endpoints or services
- Designing database schemas and migrations
- Implementing authentication and authorization
- Building middleware, interceptors, or request handlers
- Refactoring existing backend code
- Reviewing code for architecture and security issues
- Optimizing database queries and performance

This skill complements framework-specific skills (NestJS, Fastify, TypeORM, Prisma, etc.) which provide concrete implementation patterns for the framework in use.

## Core Principles by Category

### 1. Input Validation & Sanitization (CRITICAL)

**Principle**: Never trust user input. Validate and sanitize at the API boundary before any processing.

- All incoming data (query params, request body, headers) must be validated against a schema (DTO, interface, validation library)
- Validation must happen at the controller/handler layer, as early as possible
- Whitelist allowed fields; reject unknown fields explicitly
- Sanitize strings to prevent injection attacks (SQL, XSS, NoSQL injection)
- Use type coercion carefully; parse numbers and booleans explicitly
- Return clear validation error messages (include field name and constraint, not internals)
- Implement rate limiting at API boundaries to prevent abuse
- Example error response: `{ error: 'Validation failed', details: [{ field: 'email', message: 'Invalid email format' }] }`

### 2. Error Handling & Propagation (CRITICAL)

**Principle**: Never silently swallow errors. Handle and propagate errors with correct HTTP codes and context.

- All errors must be caught, logged, and mapped to appropriate HTTP status codes
- Do NOT expose internal error details (stack traces, database errors, file paths) to the client
- Log the full error with context (user ID, request ID, timestamp) for debugging
- Use correct HTTP status codes: 400 (validation/client error), 401 (auth required), 403 (forbidden), 404 (not found), 409 (conflict), 500 (server error), 503 (service unavailable)
- Errors must propagate up the stack; don't catch and ignore
- Implement a global error handler/middleware to catch unhandled exceptions
- Structure error responses consistently: `{ error: 'Error type', code: 'ERROR_CODE', message: 'User-friendly message', requestId: 'uuid' }`
- Example: database connection error should log full details but return `{ error: 'Service unavailable', code: 'DB_ERROR' }` to client

### 3. Database Connection Management (CRITICAL)

**Principle**: Database connections are a limited resource. Pool, reuse, and never create one per request.

- Always use connection pooling; never establish a new database connection per request
- Configure pool size based on expected concurrent load (default often 10-20, production 50-200)
- Set connection timeout and idle timeout to prevent resource leaks
- Implement health checks for database connections
- Never pass raw connection objects to services; abstract via repository pattern or query builder
- Log connection pool metrics (used, available, waiting) for monitoring
- Document pool configuration in environment/config file
- Example pattern: DataSource/Pool initialized once on startup, services inject the pool reference

### 4. Transactions & Data Consistency (CRITICAL)

**Principle**: Multiple related writes must happen atomically within transactions.

- Any operation that writes to multiple tables or multiple rows must use transactions
- Transactions must be explicit and scoped to the smallest unit that preserves consistency
- Set appropriate isolation levels (READ_COMMITTED is common; READ_SERIALIZABLE for strict requirements)
- Handle transaction rollbacks gracefully; don't assume all writes succeed
- Implement retry logic with exponential backoff for transient failures (e.g., deadlocks)
- Log transaction start, commit, and rollback for debugging
- Use optimistic locking (version fields) or pessimistic locking (row locks) to prevent race conditions
- Example: Creating an order with order items must happen in one transaction; both succeed or both rollback

### 5. Security: Secrets & Credentials (CRITICAL)

**Principle**: Secrets never appear in code, logs, or version control.

- All secrets (database passwords, API keys, tokens, encryption keys) must come from environment variables only
- Never hardcode secrets, even in examples or tests
- Do NOT log secrets; sanitize logs before writing
- Rotate secrets regularly via CI/CD or secrets management service
- Use different secrets per environment (dev, staging, production)
- Never store plaintext passwords; hash with bcrypt/Argon2 before storing
- Implement API key validation with rate limiting and scope-based access
- Example: ConfigService/Config module reads from env; services inject ConfigService
- Principle: If a secret is ever committed, treat repository as compromised

### 6. Structured Logging (HIGH)

**Principle**: Logs must be machine-readable, contextual, and help debug production issues.

- Log with structured format (JSON preferred): `{ timestamp, level, message, context, userId, requestId, duration, error }`
- Assign a request ID to every request; pass through all service calls for tracing
- Log at appropriate levels: DEBUG (detailed flow), INFO (state changes), WARN (recoverable issues), ERROR (failures requiring attention)
- Include context: who made the request (user ID), what operation, how long it took
- Never log sensitive data (passwords, tokens, PII beyond user ID)
- Use separate appenders for different log levels (info → file, errors → alerts)
- Implement log aggregation for production (ELK, Splunk, CloudWatch, etc.)
- Example: `{ level: 'info', timestamp: '2024-01-15T10:30:00Z', requestId: 'abc123', userId: 'user-456', operation: 'createOrder', duration: 120, message: 'Order created successfully' }`

### 7. API Design & Pagination (HIGH)

**Principle**: APIs must be consistent, predictable, and scalable.

- All list endpoints MUST support pagination (limit, offset or cursor-based)
- Default pagination: limit=20, max_limit=100; reject invalid limits
- Use cursor-based pagination for large datasets (more scalable than offset)
- Return pagination metadata: `{ items: [...], total, limit, offset, hasMore }`
- Use HTTP methods correctly: GET (retrieve), POST (create), PATCH (partial update), PUT (replace), DELETE (remove)
- Use consistent response format: `{ data: {...}, status: 'success', timestamp: '...' }` or errors: `{ error: '...', code: '...', timestamp: '...' }`
- Filter by indexed columns only; avoid full table scans on list endpoints
- Document all query parameters, required vs optional
- Implement proper caching headers (ETag, Last-Modified, Cache-Control)
- Example: `GET /api/users?limit=20&offset=0` returns `{ data: [...], pagination: { limit: 20, offset: 0, total: 500 } }`

### 8. Idempotency (HIGH)

**Principle**: Critical write operations must be safely retryable.

- Idempotent key: client provides unique ID (UUID or hash) for the operation
- Server stores the key and result; duplicate requests return cached result without side effects
- Apply to all POST/PUT operations that modify state or trigger external side effects (emails, payments)
- Idempotency key should be in request header: `Idempotency-Key: <UUID>`
- Cache idempotent responses for reasonable time window (e.g., 24 hours)
- Document which endpoints require idempotency key in API spec
- Example: Two requests with same Idempotency-Key must return same response and create only one order

### 9. Authentication & Authorization (HIGH)

**Principle**: All endpoints must verify the caller and enforce access policies.

- Implement token-based auth (JWT preferred for APIs)
- Store tokens securely: HTTP-only cookies or Authorization header (Bearer token)
- Set short expiry times for tokens (minutes to hours); use refresh tokens for longer sessions
- Validate token signature and expiry on every request
- Implement role-based access control (RBAC): roles → permissions → resources
- Check permissions at service layer, not just controller
- Never rely on client-side roles or IDs; always verify on server
- Implement audit logging for authentication failures and privilege escalations
- Example: Guard/Middleware validates JWT; Service checks user.role includes 'admin' before deleting resource

### 10. Separation of Concerns & Layering (HIGH)

**Principle**: Different responsibilities belong in different layers.

- **Controller/Handler Layer**: HTTP parsing, validation, authorization, response formatting
- **Service Layer**: Business logic, orchestration, transactions, domain rules
- **Repository/Data Layer**: Database queries, caching, connection management
- **Infrastructure Layer**: External services (email, payment, 3rd-party APIs), logging, config
- Don't mix layers: controllers don't query the database directly; services don't know about HTTP
- Each layer can be tested independently by mocking its dependencies
- Dependencies flow inward: Controller → Service → Repository → Database
- Implement dependency injection to decouple layers
- Example: Controller calls `userService.createUser(dto)`, service calls `userRepository.save(user)` and `emailService.sendWelcomeEmail(user)`

### 11. Caching Strategy (MEDIUM)

**Principle**: Cache frequently accessed data; invalidate when data changes.

- Cache read-heavy data (user profiles, configurations, reference data)
- Use appropriate TTLs based on data freshness requirements (seconds to hours)
- Implement cache invalidation: time-based (TTL) or event-based (on write, publish event)
- Multi-tier caching: in-memory (for process-local), Redis (for distributed)
- Cache key must include all query parameters to avoid collisions
- Monitor cache hit rate; low rates indicate poor cache strategy
- Example: Cache user profile for 5 minutes; on profile update, invalidate the key immediately
- Document cached data and TTLs in architecture docs

### 12. Database Query Optimization (MEDIUM)

**Principle**: Queries must be efficient; slow queries degrade user experience and increase costs.

- Always use indexes on columns used in WHERE, JOIN, and ORDER BY clauses
- Avoid N+1 queries: load related data with JOINs or batch queries, not separate requests
- Select only needed columns; avoid SELECT *
- Use LIMIT and pagination to avoid loading entire tables
- Monitor slow query logs; identify and optimize queries exceeding 100ms threshold
- Implement query timeouts to prevent runaway queries
- Use EXPLAIN/query plans to understand query performance
- Denormalize carefully when normalization costs too much in query complexity
- Example: Bad: Loop through users and query addresses per user (N+1). Good: JOIN users with addresses in one query.

### 13. Scalability & Performance (MEDIUM)

**Principle**: Design for growth; performance issues become cost issues.

- Use async/non-blocking operations for I/O (database, external APIs)
- Implement message queues (RabbitMQ, Kafka, SQS) for async work (emails, reports, heavy processing)
- Set HTTP timeouts; don't let requests hang indefinitely
- Batch operations where possible (bulk insert, bulk delete)
- Implement circuit breakers for external service calls
- Use content negotiation to support different response formats (JSON, XML, CSV)
- Monitor key metrics: response time, error rate, CPU, memory, database connections
- Example: Sending emails should enqueue message, not block the response; worker processes emails asynchronously

## Implementation Patterns

### Pattern: Repository/DAO Layer
Abstract database queries behind a repository interface. This allows:
- Swapping database implementation without changing services
- Unit testing services with mock repositories
- Centralizing query optimization
- Versioning complex queries

```
Service depends on RepositoryInterface
RepositoryInterface has: save(entity), findById(id), findAll(), delete(id)
Concrete repository implements queries using ORM or raw SQL
```

### Pattern: Dependency Injection
All dependencies (services, repositories, config) are injected, not created inside the class.
- Enables testing by injecting mocks
- Allows swapping implementations at runtime
- Container manages object lifecycle

### Pattern: Request Context
Wrap request data (user, ID, correlation ID, start time) in a context object. Pass context through all function calls.
- Enables logging with full context
- Allows middleware to attach user/tenant info without parameter passing
- Simplifies error tracking and debugging

### Pattern: Error Wrapper
Create domain-specific error classes that extend base Error. Include code, statusCode, and message.
- NotFoundError extends AppError with statusCode: 404
- ValidationError with details array for field errors
- Global handler catches and serializes to response

## Anti-Patterns to Avoid

- **God Service**: A service doing too much (users, auth, emails, payments). Split by domain.
- **Leaky Abstractions**: Repository that exposes SQL; ORM queries in service layer.
- **Silent Failures**: Catching errors without handling or logging.
- **Connection Per Request**: Creating new database connection for each request instead of pooling.
- **Hardcoded Secrets**: Database password, API keys in code or config files.
- **No Pagination**: List endpoint returning unbounded results; crashes on large datasets.
- **Tightly Coupled Tests**: Test depends on implementation details; breaks on refactoring.
- **Missing Transactions**: Multiple writes without transaction; data inconsistency on failure.
- **Unvalidated Input**: Trusting user input; SQL injection, XSS vulnerabilities.
- **No Error Context**: Errors logged without request ID, user, or operation context; hard to debug.

## Metrics & Monitoring

Track these metrics to ensure backend health:
- **API Response Time**: P50, P95, P99; target <200ms for user-facing APIs
- **Error Rate**: % of requests failing; alert if >1%
- **Database Connection Pool**: Used vs available; never exceed max
- **Cache Hit Rate**: % of cache hits; <50% indicates poor strategy
- **Slow Query Rate**: % of queries exceeding threshold
- **Unauthorized Request Rate**: Spike indicates attack or misconfiguration

Set up alerts for:
- Response time exceeds threshold
- Error rate spikes
- Database unavailable
- Connection pool exhausted
- Authentication/authorization failures

## Checklist for Backend Implementation

- [ ] All endpoints have input validation with DTOs/schemas
- [ ] All operations have error handling; no silent failures
- [ ] Database uses connection pooling, not per-request connections
- [ ] Write operations use explicit transactions
- [ ] No hardcoded secrets; all via environment variables
- [ ] Logging is structured and includes request ID/user context
- [ ] List endpoints have pagination (limit, offset/cursor)
- [ ] Critical write operations support idempotency keys
- [ ] All endpoints enforce authentication and authorization
- [ ] Code is organized in layers (controller, service, repository, infra)
- [ ] Database queries are indexed and optimized (no N+1)
- [ ] External service calls have timeouts and circuit breakers
- [ ] Monitoring and alerting configured for key metrics
- [ ] Documentation explains architecture, API contracts, and deployment

---

These principles are the foundation. Framework-specific skills (NestJS, Fastify, TypeORM, Prisma) show how to implement these principles in concrete code.
