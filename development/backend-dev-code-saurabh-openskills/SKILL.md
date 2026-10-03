---
name: backend-dev
description: Production-grade backend development guidance — language and framework agnostic. Use when the user asks to build an API, design a backend service, create a database schema, implement authentication, write business logic, structure a backend project, or produce server-side code of any kind.
---

# Backend Development

Approach every backend task as a senior engineer who has been burned by shortcuts in production. You are not here to make something that works once — you are here to make something that works at 3am on a Saturday when no one is watching. Every decision defaults to correctness, observability, and maintainability over cleverness or speed.

---

## Step 0: Ground the Work Before Writing a Line

Before any code, establish:

1. **What is this service's single responsibility?** Name it in one sentence. If you can't, the scope needs splitting.
2. **What are the data boundaries?** What goes in, what comes out, what persists.
3. **What can fail?** External calls, DB writes, auth checks — enumerate failure points before coding happy paths.
4. **What does done look like?** Define the contract: endpoint, schema, or interface the caller expects.

State these four things explicitly to the user if the brief is ambiguous. Never silently assume.

---

## Execution Workflow

Before writing any implementation code, work through these steps in order:

1. **Understand the contract** — name the endpoint or function signature, its inputs, outputs, and error cases
2. **Map the layers** — decide what belongs in `api/`, `services/`, `repositories/`, and whether any new models or errors are needed
3. **Identify external dependencies** — list every DB call, external API, queue, or file system access the feature requires
4. **Enumerate failure modes** — for each dependency, ask: what happens if it is slow, returns nothing, or fails entirely?
5. **Define the tests first** — name the unit test cases before writing the implementation; if you cannot name them, the design is unclear
6. **Then implement** — follow the layer rules, apply the coding standards, handle every failure mode you named

Do not skip to implementation. A feature built on a vague contract costs more to fix than the time spent grounding it.

---

## Folder Structure

Always generate a clean, domain-driven folder structure. The structure must communicate the architecture at a glance. Follow this pattern regardless of language or framework:

```
project-root/
├── src/
│   ├── api/                  # Route handlers / controllers — thin layer only
│   │   └── v1/               # Versioned from day one
│   ├── services/             # Business logic — no framework code here
│   ├── repositories/         # All data access — DB queries live here only
│   ├── models/               # Domain entities and data types
│   ├── middleware/            # Auth, logging, rate limiting, error handling
│   ├── config/               # Environment config, constants, feature flags
│   ├── utils/                # Pure helper functions — stateless, no side effects
│   └── errors/               # Custom error classes and error codes
├── tests/
│   ├── unit/                 # One test file per source file
│   ├── integration/          # Tests that hit real DB / external services
│   └── fixtures/             # Shared test data and factories
├── migrations/               # Database migration files — versioned, never edited
├── scripts/                  # One-off ops scripts, seeding, utilities
├── docs/                     # API docs, ADRs, architecture diagrams
├── .env.example              # Template — never commit .env
├── Dockerfile                # Multi-stage, non-root user
├── docker-compose.yml        # Local dev environment
└── README.md                 # Setup, run, test — nothing else
```

**Rules:**
- `api/` handlers must be thin — validate input, call a service, return a response. No business logic.
- `services/` must be framework-agnostic — they should be callable from a test without spinning up a server.
- `repositories/` are the only place that know about the database. No raw queries elsewhere.
- Never cross layers — a `repository` never calls a `service`, a `model` never imports `middleware`.

---

## API Design

Every API must be designed contract-first. Define the interface before implementing it.

**Mandatory conventions:**
- Version from day one: `/api/v1/resource`
- Use correct HTTP methods: GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE (remove)
- Return consistent HTTP status codes — never return 200 for an error
- For new REST APIs, default to a consistent response envelope:
  ```json
  // Success
  { "data": { ... }, "meta": { ... } }

  // Error
  { "error": { "code": "RESOURCE_NOT_FOUND", "message": "...", "details": [...] } }
  ```
  Use this as the starting point unless the project has an established convention — consistency within a codebase matters more than the specific shape.
- Paginate all list endpoints — cursor-based preferred for large datasets, offset for simple cases
- Never expose stack traces or database errors in responses
- Every endpoint must have an OpenAPI/schema definition — auto-generate where possible

**Request handling checklist for every endpoint:**
- [ ] Validate and sanitize all input at the boundary before it touches any logic
- [ ] Authenticate — verify identity
- [ ] Authorize — verify permission for this specific resource
- [ ] Execute business logic via service layer
- [ ] Return typed, documented response

---

## Code Quality Standards

Every piece of generated backend code MUST follow these rules — no exceptions:

### Types & Contracts
- All function signatures must have explicit input and output types
- Define data contracts (schemas/interfaces/structs) for every external boundary: API input, API output, DB row, event payload
- No implicit any / untyped parameters — if a type is unknown, make it explicit and handle it

### Error Handling
- Never swallow errors silently — every caught error must be logged or re-thrown
- Use custom error classes with error codes, not raw strings
- Distinguish operational errors (invalid input, not found) from programmer errors (null dereference, wrong type)
- All async operations must have error handling — no unhandled promise rejections, no unchecked results
- Errors bubble up to a single top-level error handler that formats and logs them consistently

### Defensive Programming
- Validate all external input: API requests, environment variables, config values, message queue payloads
- Fail fast — check preconditions at the top of a function, not buried in the middle
- Never trust external data: third-party APIs, user uploads, webhook payloads

### Naming & Clarity
- Functions named as verbs: `getUserById`, `sendWelcomeEmail`, `calculateTax`
- Variables named as nouns: `userId`, `orderTotal`, `connectionPool`
- No abbreviations unless universally understood (`id`, `url`, `http`)
- One concept per function — if a function does two things, split it
- Comments explain *why*, not *what* — if the code needs a comment to explain what it does, rewrite the code

### Constants & Configuration
- No magic numbers or magic strings anywhere in business logic
- All configuration comes from environment variables — never hardcoded
- Group related constants into named objects/enums
- Every required environment variable must be validated on startup — crash early with a clear message rather than failing mysteriously later

---

## Database Rules

- **Migrations only** — never mutate a schema manually; every change is a versioned, reversible migration file
- **Indexes driven by query patterns** — add indexes for the queries you actually run; over-indexing slows writes; document the query that justifies each index in the migration comment
- **Transactions when atomicity is required** — wrap multi-step writes that must succeed or fail together in a transaction; not every multi-row operation needs one — use judgement
- **Soft deletes when the business requires it** — use `deleted_at` timestamps when audit history, undo, or compliance matters; hard deletes are correct when data has no retention requirement
- **Timestamps everywhere** — every table gets `created_at` and `updated_at` by default
- **Parameterized queries only** — never interpolate user input into a query string
- **Connection pooling** — configure min/max pool size; never open unbounded connections
- **Read replicas when scale requires it** — design repositories so read/write routing can be introduced later without touching service code; do not add the complexity before you need it

---

## SOLID and Dependency Design

Apply SOLID principles as engineering judgement, not as a checklist. The goal is code that is easy to change, easy to test, and honest about its dependencies.

- **Single Responsibility** — a module has one reason to change. A service that sends emails and processes payments will be painful to test and painful to change. Split them.
- **Open/Closed** — extend behaviour by adding code, not by editing existing logic. New payment providers, new notification channels, new export formats should slot in without touching working code.
- **Liskov Substitution** — any implementation of an interface must honour the contract of that interface. A mock in tests must behave like the real thing in the ways the caller depends on.
- **Interface Segregation** — callers should not depend on methods they do not use. A `UserRepository` interface used by the auth service should not expose bulk-export methods only the admin service needs.
- **Dependency Inversion** — high-level modules (services) depend on abstractions, not on concrete implementations (a specific DB client, a specific email provider). Wire concrete implementations at the composition root.
- **Composition Root** — all dependency wiring happens in one place at startup. Services do not construct their own dependencies. This makes the dependency graph readable and testable.

**Avoid over-engineering.** Do not introduce abstractions speculatively. Create an abstraction only when one of these is true:
- Multiple implementations exist now or are planned imminently
- The dependency crosses an external boundary (DB, HTTP, file system, queue)
- The dependency is nondeterministic (time, random, environment)
- It must be replaced in tests with a controlled substitute
- It represents a stable domain capability that multiple consumers will share

If none of these apply, use the concrete type directly.

---

## Reliability and External Dependencies

Every call that leaves the process boundary is a call that can fail, hang, or return inconsistent results. Design for this explicitly.

- **Timeouts** — set an explicit timeout on every outbound call; never rely on the remote end to close the connection
- **Retries with backoff** — retry transient failures (network errors, 429s, 503s) with exponential backoff and jitter; do not retry non-idempotent operations unless the operation is safe to repeat
- **Idempotency** — design write operations to be safely retryable; use idempotency keys for payment and order operations; ensure that processing a message twice produces the same outcome as processing it once
- **Message queues** — use queues to decouple producers from consumers and to absorb load spikes; consumers must be idempotent; dead-letter queues are mandatory for any queue used in production
- **Transactional outbox** — when a DB write and a message publish must happen together, write the event to an outbox table in the same transaction as the business data, then publish from the outbox asynchronously; this prevents silent message loss on process crash

---

## Authentication & Authorization

- Use short-lived access tokens + refresh token rotation as the default auth pattern
- Hash all passwords with a strong adaptive algorithm (bcrypt cost ≥ 12, or argon2id)
- Store tokens in httpOnly cookies for browser clients; never in localStorage
- Implement RBAC — every protected route checks both authentication (who are you?) and authorization (can you do this to this resource?)
- Verify resource ownership on every request — a user fetching `/orders/123` must own order 123
- Implement account lockout after repeated failed attempts
- Rotate secrets on a schedule; invalidate all sessions on password change
- Never log passwords, tokens, secrets, or PII in any log line — ever

---

## Unit Testing

Every service function, utility, and repository method gets a unit test. No exceptions.

**Structure of every test file:**
```
describe('<ModuleName>', () => {
  describe('<methodName>', () => {
    it('returns X when given valid input Y')
    it('throws ErrorCode.X when input is missing')
    it('calls dependency Z exactly once with correct args')
    it('does not call dependency Z when condition is false')
  })
})
```

**Rules:**
- Test behaviour, not implementation — test what a function does, not how it does it
- One assertion concept per test — a test that checks three things is three tests
- Mock all external dependencies (DB, HTTP, file system, clock) in unit tests — a unit test never hits the network or disk
- Use factories/builders for test data — never hardcode raw objects scattered across test files
- Test the sad path as rigorously as the happy path: invalid input, missing data, dependency failures, edge cases
- Every test must be independent — no shared mutable state between tests, no order dependency
- Aim for 80%+ line coverage on `services/` and `utils/`; 100% on critical auth and payment paths

**For every public function, generate tests that cover:**
- [ ] Happy path with valid input
- [ ] Missing required input
- [ ] Invalid type / format input
- [ ] Boundary values (empty string, zero, max int, null)
- [ ] Dependency throws an error
- [ ] Dependency returns empty / null
- [ ] Concurrent / race condition if applicable

---

## Integration Testing

- Integration tests live in `tests/integration/` and run against a real database (use containers or an in-memory equivalent)
- Test the full stack from HTTP request to DB response for critical paths
- Each integration test must clean up its own data — use transactions that rollback, or explicit teardown
- Test unhappy paths at the integration level too: DB constraint violations, duplicate keys, connection failures

---

## Security Checklist

Before marking any backend feature complete, verify:

- [ ] All inputs validated and sanitized at the API boundary
- [ ] SQL/NoSQL injection impossible (parameterized queries / ORM)
- [ ] Authentication required on all non-public endpoints
- [ ] Authorization checks resource ownership, not just role
- [ ] Sensitive data (passwords, tokens, keys) never logged or returned in responses
- [ ] Rate limiting applied to auth endpoints and expensive operations
- [ ] CORS configured to a whitelist, not `*` for credentialed requests
- [ ] Security headers set on all responses
- [ ] Dependencies audited for known vulnerabilities
- [ ] Secrets loaded from environment, not source code

---

## Observability

Every backend service must be observable from day one:

- **Structured logging** — every log line is a machine-readable JSON object with: `timestamp`, `level`, `message`, `correlationId`, `service`, and relevant context fields
- **Correlation IDs** — generate a unique ID per request at the entry point; thread it through every log line, every downstream call
- **Log levels used correctly**: `DEBUG` for dev-only detail, `INFO` for significant state changes, `WARN` for recoverable issues, `ERROR` for failures that need attention
- **Health endpoints** — every service exposes `/health` (liveness) and `/ready` (readiness) with no auth required
- **Key metrics to instrument**: request count, error rate, latency (p50/p95/p99), DB query time, external call duration
- **Never log PII** — mask emails, phone numbers, card numbers before they reach any log line

---

## Environment & Configuration

- Every environment variable required at startup must be listed in `.env.example` with a description comment
- Validate all required env vars on startup — if one is missing, crash immediately with a clear error naming the missing variable
- Separate config by environment: `development`, `test`, `staging`, `production`
- Never use production credentials in development or test environments
- Feature flags for anything that needs to be toggled without a deploy

---

## Docker & Local Dev

Every backend project ships with:

**Dockerfile (multi-stage):**
- Stage 1: install dependencies
- Stage 2: build / compile
- Stage 3: minimal runtime image, non-root user, only production artifacts

**docker-compose.yml:**
- App service
- Database service with a named volume
- Cache service (if applicable)
- Any other backing services (queue, search, etc.)
- Health checks on all services
- Environment variables loaded from `.env`

---

## Definition of Done

A backend feature is not done until:

- [ ] Folder structure follows the project convention
- [ ] All inputs validated at the API boundary
- [ ] Business logic isolated in the service layer
- [ ] Data access isolated in the repository layer
- [ ] All error cases handled and logged
- [ ] Unit tests written for all service and utility functions
- [ ] Integration test written for the critical path
- [ ] Security checklist passed
- [ ] OpenAPI / schema definition updated
- [ ] `.env.example` updated if new env vars added
- [ ] README updated if setup steps changed
- [ ] No secrets, no magic numbers, no TODO comments left in committed code
