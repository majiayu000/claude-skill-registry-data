---
name: java-development
description: Build, review, debug, and maintain production Java applications, libraries, services, and APIs. Use for Java, Spring Boot, Jakarta, Maven, Gradle, JUnit, concurrency, JVM performance, persistence, dependency injection, configuration, resilience, or Java security work.
---

# Java Development

Act as the Java engineer accountable for a service that must remain understandable, observable, and safe under load. Use explicit contracts, narrow interfaces, immutable data where practical, bounded resource use, and established framework conventions.

## Execution Workflow

1. **Inspect the build and runtime.** Read Maven/Gradle files, Java toolchain, module structure, dependency-management rules, test setup, framework conventions, configuration, packaging, and deployment path.
2. **Define the contract.** Establish inputs, validation, error mapping, transaction boundaries, authorization, compatibility needs, performance targets, and failure behavior.
3. **Implement in layers.** Keep transport, application orchestration, domain behavior, and infrastructure adapters distinct. Make dependency direction clear.
4. **Make operations bounded.** Configure timeouts, pools, concurrency, retries, transactions, pagination, and resource cleanup deliberately.
5. **Verify and hand off.** Run build, static analysis, focused tests, and relevant integration tests; describe configuration, migration, and operational impact.

## Step 0: Ground the Change Before Implementation

Before writing Java code, establish and state when non-obvious:

1. **Business outcome:** What observable behavior changes for which caller?
2. **Entry point:** Is it an HTTP endpoint, event consumer, scheduler, CLI, library API, or batch job?
3. **Contract:** Inputs, validation, output, error mapping, authorization, compatibility, and ownership.
4. **Dependencies:** Database, cache, queue, filesystem, identity provider, or remote service involved.
5. **Failure and operations:** Timeouts, retry, transaction, idempotency, capacity, logs/metrics, and rollback plan.
6. **Proof:** Unit, integration, build, and regression verification required.

Inspect `pom.xml` or Gradle build files, Java toolchain, dependency-management rules, application configuration, CI, test conventions, package layout, migrations, and adjacent production code. Follow the repository's framework choices; do not introduce a new web stack, persistence layer, or dependency-injection pattern for a single task.

## Plan Before Code

```markdown
## Java Change Plan

**Objective:** <observable behavior>
**Entry point / consumer:** <controller, listener, job, library API>
**Input and validation:** <DTO/command and constraints>
**Success and error contract:** <response/result and error codes>
**Layers affected:** <adapter, application service, domain, repository/client>
**Transactions and side effects:** <DB, remote calls, queue, files>
**Resilience:** <timeouts, retries, idempotency, concurrency>
**Verification:** <tests, build, static analysis, migration check>
```

Use the smallest architecture that makes responsibilities, testing, and failure boundaries clear. An abstraction is justified when it separates an external/nondeterministic dependency, supports a real second implementation, or expresses a stable domain capability—not because every class needs an interface.

## Layering and Contract Patterns

Use a directional flow such as:

```text
HTTP / message / CLI adapter
        -> application service (use case and transaction boundary)
        -> domain model and policies
        -> repository / remote-client adapters
```

- **Adapters/controllers:** authenticate, authorize, parse/validate input, invoke one use case, and map stable output. No business orchestration or raw persistence queries.
- **Application services:** coordinate one use case, transaction boundaries, idempotency, and dependencies. Do not expose framework request/response types through the domain.
- **Domain model:** enforce meaningful invariants and calculations. Keep it free of framework annotations or I/O where practical.
- **Infrastructure:** implement data/remote access, set timeouts, translate provider errors, and expose a narrow application-facing contract.

For a public API, define the DTO, success response, expected error code, status, and compatibility before implementation. Do not return entity objects, stack traces, driver error text, or unbounded collections.

## Validation and Error Mapping

Validate request/message/config input at the boundary and enforce deeper business invariants in domain/application code. Separate:

| Failure type | Treatment |
|---|---|
| Invalid syntax/shape | Stable validation response; do not retry |
| Unauthorized/forbidden | Do not reveal protected resource details |
| Missing/conflicting domain state | Stable application error or result |
| Transient dependency failure | Bounded retry/circuit policy where safe; surface a safe unavailable response |
| Programming defect | Log/trace centrally; fail safely; do not disguise as client error |

Preserve causes when translating exceptions. Catch only to recover, add context, translate at a boundary, or clean up. Avoid `catch (Exception)` as business flow and never silently return `null`, empty data, or success after an unexpected failure.

## Spring and Configuration Rules

- Use constructor injection and immutable dependencies. Avoid field injection, service locators, and mutable singleton state.
- Bind and validate configuration at startup with typed configuration properties. Document required production variables without committing values.
- Keep controllers thin and put cross-cutting concerns—error mapping, correlation IDs, security, validation, rate limits—at established framework boundaries.
- Respect proxy/transaction semantics: self-invocation, private methods, and remote calls inside transactions can invalidate assumptions.
- Implement readiness/health behavior that represents essential dependencies without exposing credentials, topology, or internal error detail.

## Persistence and Transaction Design

Before changing persistent behavior, identify schema ownership, migration rules, query pattern, expected cardinality, indexes, isolation/locking needs, and rollback compatibility.

- Write a versioned migration; do not rely on manual database changes.
- Parameterize queries and select only needed fields. Paginate all potentially unbounded reads.
- Check for N+1 reads and query count in list/detail workflows.
- Use database constraints for uniqueness and critical invariants. Application checks alone race under concurrency.
- Keep transactions short and local. Do not make HTTP calls, wait for queues, stream files, or perform slow CPU work while a transaction holds locks.
- For externally visible side effects, define ordering and recovery: outbox/event pattern, idempotency key, compensating action, or explicit reconciliation job.

## HTTP, Messaging, and Resilience

Every process boundary requires explicit limits:

- set connect, read, response, and pool-acquisition timeouts for remote clients;
- bound connection pools, executors, message batches, request/upload sizes, pagination, and queues;
- propagate correlation/tracing IDs using project conventions;
- retry only idempotent transient failures with capped exponential backoff and useful observability;
- use circuit breaking, bulkheads, or rate limits only when supported by an operational need and the repository’s platform;
- log structured event context and identifiers, never credentials, access tokens, raw sensitive payloads, or secrets.

## Concurrency and JVM Safety

Do not assume a singleton bean is thread-safe. Avoid shared mutable state; if it is necessary, document ownership and use a correct concurrency primitive. Do not block reactive/event-loop/request threads with slow I/O or long CPU work. Use the established execution model, bounded executors, and backpressure mechanisms.

Honor interruption: either propagate `InterruptedException` or restore the interrupt flag after cleanup. Close resources with try-with-resources or lifecycle hooks. Measure allocation, heap, thread, connection, queue, and database behavior before changing JVM flags, pool sizes, or caches.

## Test Strategy

Name the tests before implementation:

| Test | Proves |
|---|---|
| Domain unit test | Invariants and calculations are correct without framework boot |
| Application-service test | Use case, authorization, transaction/result behavior, and dependency failures |
| Adapter integration test | SQL/query mapping, serialization, security, or remote-client contract works |
| API/message test | Validation and stable error/success contract are correct |
| Regression test | The reported defect cannot recur |

Use the repository's JUnit/assertion/mocking stack. Keep tests isolated with controlled time, unique data, cleanup/rollback, and no live third-party dependencies in the default suite. Test the built artifact where framework wiring or packaging is a real risk.

## Build, Dependency, and Configuration Discipline

Treat Maven/Gradle metadata and service configuration as production code.

### Build rules

- Use the checked-in wrapper and declared toolchain. Do not rely on a globally installed Maven, Gradle, or newer JDK unless CI does too.
- Add a dependency only after checking existing platform/framework capability, maintenance status, license, CVE posture, transitive weight, and runtime compatibility.
- Use the repository dependency-management/BOM mechanism; do not pin a transitive version locally without a documented reason.
- Keep test-only dependencies out of production packaging. Do not commit generated build output unless the repository explicitly requires it.
- For a library, verify published artifact contents, public API compatibility, module metadata, and a consumer compile/run path.

### Configuration rules

- Bind configuration once into typed validated properties, not scattered `System.getenv` or `@Value` reads.
- Distinguish safe development defaults from mandatory production settings. Fail fast on missing critical config.
- Do not check in passwords, private URLs, tokens, keystores, or certificate material. Update templates/docs using placeholders only.
- Review feature flags for default, owner, telemetry, disable path, and removal date. A permanent flag is undeclared complexity.

## Security Review Gates

For a security-relevant Java change, explicitly check:

- [ ] Authentication establishes a verified identity, and authorization checks action plus resource/tenant ownership.
- [ ] Validation constrains request body, path/query values, message payloads, headers, uploads, and deserialized types.
- [ ] Queries are parameterized and ORM/query criteria cannot be controlled as raw expressions by users.
- [ ] Redirects, URLs, file paths, templates, expression evaluation, archives, and XML/deserialization are safe for untrusted input.
- [ ] Errors, logs, metrics, traces, audit records, and test fixtures exclude secrets and unnecessary personal data.
- [ ] Rate/size/time limits protect expensive operations, uploads, pagination, and externally-triggered work.
- [ ] Dependency updates and build plugins are compatible with project security policy.

Security is not complete because a controller has an authentication annotation. Check tenant isolation, object-level authorization, background jobs, message consumers, internal endpoints, and administrative flows separately.

## Performance and Capacity Review

Estimate or measure the worst credible behavior before shipping a hot path:

| Area | Questions to answer |
|---|---|
| Database | Query count, rows read, index use, lock duration, pagination, connection consumption? |
| Remote calls | Timeout, retry load, pool limit, fallback, fan-out, payload size? |
| JVM | Allocation, heap retention, thread/blocking behavior, GC pressure, executor queue? |
| API/job | Request size, concurrency, CPU cost, duplicate delivery, backpressure, rate limit? |
| Cache | Key cardinality, tenant/version isolation, TTL, invalidation, unavailable-cache behavior? |

Do not tune by guessing. Obtain a query plan, benchmark, profile, load-test, or production metric appropriate to the risk. State what evidence supports the design and what remains an assumption.

## Deployment and Migration Strategy

For a persistent/public change, plan the rollout—not merely compilation:

1. **Backward-compatible schema first:** add nullable/new fields, indexes, tables, or read capability before code relies on them.
2. **Deploy compatible readers/writers:** support old and new formats during transition; avoid a simultaneous migration assumption.
3. **Backfill safely:** batch, throttle, monitor, retry idempotently, and define completion/reconciliation.
4. **Enforce later:** remove old reads/writes and make constraints non-null/strict only after data is valid and old clients are gone.
5. **Observe and roll back:** define metrics/logs, feature-flag or disable route, and a rollback that does not corrupt newer data.

Never combine a destructive schema migration with code that assumes the new schema in one irreversible release unless downtime and recovery are explicitly authorized.

## Java Review Questions

### Correctness

- Are nullability, `Optional`, numeric precision, timezone, encoding, ordering, and collection mutability decisions explicit?
- Does the use case behave correctly under duplicate requests/messages and concurrent updates?
- Are transaction boundaries aligned with atomic business changes, not arbitrary method boundaries?
- Is a remote failure distinguished from a not-found/domain failure?

### Maintainability

- Does each class have one cohesive reason to change?
- Are framework annotations/objects contained at appropriate boundaries?
- Are exceptions and result types actionable for their callers?
- Is an abstraction serving a real external boundary, consumer, or substitution need?

### Operations

- Can an operator find the request/job/resource in logs and traces without seeing sensitive data?
- Does the operation have bounded memory, threads, connections, queue depth, retry pressure, and output size?
- Are health checks, metrics, alerting, migration, rollback, and configuration updates appropriate to the blast radius?

## Anti-Patterns to Reject

- A controller that performs authorization, business logic, persistence, and remote calls in one method.
- A `@Transactional` method that calls remote systems or performs long-running work while holding DB locks.
- A repository/list operation with no pagination, index consideration, or query-count check.
- `catch (Exception)` that turns unexpected faults into null, empty data, or a generic success response.
- A singleton bean with undocumented mutable request state.
- Unbounded executors, connection pools, queues, retries, or message batches.
- A schema change that requires a synchronized deploy or has no backfill/rollback story.
- A test suite that mocks every layer but never validates serialization, query behavior, security, or framework wiring.

## Required Output

```markdown
## Java Delivery Summary

### Scope and Contract
- Objective, entry point, and affected consumers:
- Input validation, authorization, success, and error behavior:

### Design
- Layers and key classes changed:
- Transaction, persistence, and external side effects:
- Timeouts, retries, idempotency, and observability:

### Verification
- Unit/integration/regression tests:
- Build and static-analysis commands run:
- Not run and why:

### Release Notes
- Configuration, migration, compatibility, rollout, and risk notes:
```

## Java Design Rules

- Compile and test with the declared Java toolchain. Do not use a locally newer API or language feature without deliberately updating the supported runtime.
- Prefer immutable value objects, records when supported, final fields, and constructors that establish valid state. Do not expose mutable collections.
- Design interfaces around real consumers; do not add an abstraction around every class or framework call.
- Use `Optional` for return values that may be absent, not fields, DTO serialization, or parameters. Never call `get()` without guaranteed presence.
- Validate at boundaries and encode invariants in domain types. Do not scatter null checks across business logic.
- Catch exceptions only to recover, translate at a boundary, or clean up. Preserve causes and do not expose internals to clients.

## Spring and Service Boundaries

- Keep controllers/adapters thin: parse and authorize input, call an application service, and map the result to transport output.
- Place transactions around cohesive application operations. Do not hold transactions during remote calls, long computation, streaming, or user interaction.
- Use constructor injection. Avoid field injection, service locators, and static mutable application state.
- Validate typed configuration at startup. Do not allow defaults that silently enable insecure production behavior.
- Apply authorization before sensitive operations. Treat deserialization, uploads, expressions, redirects, and headers as untrusted input.
- Expose health/readiness that reflects dependencies without leaking confidential detail.

## Persistence, HTTP, and Concurrency

- Parameterize queries, prevent N+1 access, select only needed fields, paginate unbounded collections, and make index implications visible.
- Define isolation and locking for contested writes. Use database constraints for critical invariants; application checks alone are race-prone.
- Set connect, read, and overall timeouts for remote clients. Bound pools, executors, queues, request bodies, and pagination.
- Retry only transient idempotent operations with capped backoff. Do not retry validation, authorization, or permanent client errors.
- Do not block request/event-loop threads with slow I/O, locks, or CPU work. Use the established execution model and bounded executors.
- Make shared mutable state explicit and synchronized or eliminate it. Respect interrupts and close streams, clients, transactions, and executors deterministically.

## Testing and Common Failure Modes

- Use JUnit and existing assertion/mocking libraries. Unit-test domain behavior; integration-test persistence, serialization, security, and framework wiring when risk warrants it.
- Keep tests isolated with unique data, rollback/cleanup, a controlled clock, and no live external services in the default suite.
- Common failures: transactions spanning remote calls, N+1 queries, unbounded executors, swallowed interrupts, leaking exception handlers, global mutable state, and configuration that only differs after deployment.

## Delivery Format

Provide contract and error behavior changed; layers affected; persistence/transaction effects; configuration, dependency, and migration changes; tests/build commands; and security or operational risks.

## Definition of Done

- [ ] Java toolchain, build system, dependency rules, framework conventions, and CI validation were inspected and respected.
- [ ] Objective, callers, input/output/error contract, dependencies, operational behavior, and verification plan are explicit.
- [ ] Inputs are validated, authorization occurs before sensitive work, and public errors are stable, actionable, and free of internal details.
- [ ] Adapter, application, domain, and infrastructure responsibilities have clear boundaries with no speculative layers.
- [ ] Transaction, idempotency, external side-effect ordering, timeout, retry, pool, queue, and pagination behavior is explicit where relevant.
- [ ] Persistence is parameterized, bounded, migration-backed, and evaluated for query count, indexes, locking, and concurrency correctness.
- [ ] Configuration is typed and validated at startup; logs/traces are useful and free of secrets or sensitive payloads.
- [ ] Concurrency avoids unsafe shared state, unbounded executors, blocking critical threads, and ignored interruption.
- [ ] Tests cover core behavior, validation, failure paths, persistence/security/framework risk, and the relevant regression.
- [ ] Build, static analysis, targeted/integration tests, migration checks, compatibility, rollout, and operational risks are reported.
