---
name: dual-testing
version: 1.1.0
description: "Language-agnostic strategy for testing code at the boundary with external infrastructure (databases, APIs, queues): integration tests with real infrastructure (e.g. Testcontainers) prove the full chain works for happy paths; unit/slice tests with mocks prove error-handling and mapping logic (domain error to status, input validation, infra failure). Works in any language/framework — Go, .NET/C#, Java, Python, TypeScript and more — with concrete references for Go, .NET (ASP.NET Core) and Java (Spring Boot) and an explicit path to adapt when no reference matches your language. Apply when designing a test strategy, creating a handler/feature/worker that needs tests, or deciding what type of test a scenario needs. Triggers: 'dual testing', 'integration vs unit', 'testcontainers vs mocks', 'what type of test', 'where should this test go', 'error path coverage'. Does NOT trigger on writing individual test assertions or test naming conventions (use test-namer for those)."
---

# Dual Testing

A language-agnostic strategy for code at the boundary between your application and external infrastructure: **integration tests prove the full chain works for happy paths; unit/slice tests prove the error-handling and mapping logic.** It aligns with the Testing Honeycomb / Test Diamond philosophy — boundary code is dominated by interaction complexity, so lean on integration for wiring and on fast mock-based tests for the branchy error logic.

The strategy is the same in every language. Only the tooling changes. Concrete per-language references are listed at the bottom; if none matches your language, the **Adapt When No Reference Exists** algorithm tells you how to apply it anyway.

## Definitions

- **Integration test** — exercises the real application boundary plus a real external dependency (real database, broker, etc., typically via Testcontainers). Proves the wiring and the happy-path behavior end to end.
- **Unit/slice test** — the smallest test that still includes the mapping/adapter code (input validation, domain-error → outcome mapping), with the semantic dependencies mocked or faked. In some frameworks the mapping lives *outside* the handler class (an exception filter, `@ControllerAdvice`, error middleware), so the right test is a framework *slice* (in-process pipeline with the service mocked), not a pure class unit test.
- **The rule**: never duplicate happy paths in both layers. Integration proves the chain; unit/slice proves the mapping. Some overlap on boundary scenarios (e.g. not-found) is fine because they exercise different concerns.

## Decision List

Where a scenario belongs. The "outcome" is described generically — map it to your transport: HTTP status, gRPC status code, CLI exit code + stderr, or queue ack/nack/retry/dead-letter.

- **Happy path (successful create/read/update/delete)** — **Integration**: proves real wiring. Outcome: success (e.g. HTTP 2xx).
- **Handler input validation (bad/missing field)** — **Unit/slice**: pure mapping logic, no infra. Outcome: client error (e.g. HTTP 400).
- **Framework/middleware/filter validation (idempotency key, body binding, content negotiation)** — **Integration or slice that includes that pipeline**: the check runs before your handler.
- **Auth/authz policy (middleware-owned)** — **Integration/slice including the middleware**.
- **Resource not found** — **Both acceptable**: integration proves the chain, unit/slice proves the mapping. Outcome: not-found (e.g. HTTP 404).
- **Infrastructure/DB error** — **Unit/slice**: cannot force reliably with real infra. Outcome: server error (e.g. HTTP 500, or queue nack→retry/DLQ).
- **Circuit breaker open / resilience pattern** — **Unit/slice**: deterministic only via a mock. Outcome: unavailable (e.g. HTTP 503).
- **Timeout / cancellation** — **Unit/slice**: drive via a cancelled context/token.
- **Idempotency / deduplication** — **Integration**: requires real state.
- **Notifications / events emitted** — **Integration**: side effect of real infra.
- **Side effects in another store** — **Integration**: verifies the real effect.
- **Empty-collection serialization (`[]` not `null`)** — **Integration**: contract verified with real data.
- **Pure business/domain logic (defaults, calculations, optimistic-lock version handling)** — **Ordinary unit tests with real objects**, no mocks or infra needed.

Do not bake specific status numbers into the strategy. HTTP `499` in particular is client-closed-request (nginx-specific), not a portable code — keep such codes in a transport-specific note, never in the portable list.

## Testability Prerequisites (Principles)

Make the boundary mockable without coupling tests to infrastructure:

- **Depend on a narrow semantic port.** Each handler needs a small abstraction for the data operations it uses (a use-case / port / repository interface), not the DB driver. If the project already has service interfaces, ports, mediators or handlers, mock *those* — do not add a redundant per-controller interface.
- **No external I/O at construction.** A factory/constructor that wraps a connection must not ping or validate at construction time — unless the framework explicitly owns startup validation (e.g. a DI-container health check). This lets a test inject a broken or mock dependency and exercise the error path at request time.
- **Inject the port at the wiring point.** The setup/registration code takes the abstraction; inject the real implementation in production and integration tests, a mock in unit/slice tests.
- **Mock the semantic port, not the driver.** Mock domain methods (`ListItems`, `DeleteItem`); never mock `Query`/`Rows`/`Tx`. Driver-level mocks test SQL strings, not behavior, and are fragile.
- **Encapsulate a transaction in one method.** When a handler orchestrates begin → queries → commit, put the whole transaction in one port method returning a domain result or a domain error. The handler only maps result → outcome.
- **Error model — two idioms, one decision.** Distinguish business errors (→ not-found / client error) from infrastructure errors (→ server error). Languages that *return* errors use sentinels/typed errors (Go `errors.Is(err, ErrNotFound)`, Rust `Result`); languages that *throw* use typed exceptions (`NotFoundException`) caught at the mapping layer (`@ControllerAdvice`, exception filter, error middleware). The mapping decision is identical; only the mechanism differs — and because the mapping layer is often a separate class, the test that covers it is usually a slice test.

## Worker / Background-Job Variant

The same split applies to consumers and workers:

- One **integration** test drives a real message/job through the real dispatcher and real infra (happy path).
- **Unit/slice** tests mock the dispatch protocol to prove failure handling (retry, dead-letter, status transitions).
- Create a **fresh dispatcher/engine per test** when registration is one-shot — some dispatchers reject or panic on duplicate handler registration.
- Mock the **full dispatch protocol** the worker depends on (claim/next, resolve target, set status, succeed/fail).

## Recommendations

Trade-offs, not hard rules:

- **Fixed error strings on server errors** for contract-stable endpoints — do not leak internal error text. This keeps integration tests from coupling to internal messages.
- **Empty collections serialize as `[]`, not `null`** — verify in integration. (The language-specific mechanics, if any, live in the per-language reference.)
- **Update the dependency manifest/lockfile after adding a mocking library** (and any tidy/restore step), or CI may silently skip the new tests.

## When This Strategy Does NOT Apply

- **Pure functions** (no external dependencies) — output-based tests directly.
- **Domain logic** without infrastructure — unit tests with real objects, no mocks.
- **Utility code** — simple tests, no strategy needed.

The dual strategy is specifically for code that sits at the boundary between your application and external infrastructure (databases, APIs, message queues).

## Language References

**If a reference matches your language or framework, read only that reference before writing tests.** The core above tells you *what* belongs in each layer; the reference gives the idiomatic tooling, test shape, and language-specific gotchas — the core alone is not enough to get the idioms right.

- **Go** (Gin, pgx, testify, testcontainers-go) — [references/go.md](references/go.md)
- **.NET / C#** (ASP.NET Core; xUnit, Testcontainers for .NET, `WebApplicationFactory`, Moq) — [references/dotnet.md](references/dotnet.md)
- **Java** (Spring Boot; JUnit 5, Testcontainers `@ServiceConnection`, MockMvc, Mockito) — [references/java.md](references/java.md)

### Adapt When No Reference Exists

No reference for your language/framework? **Do not skip the strategy — adapt it.** Follow this algorithm:

1. Identify the **boundary adapter** (handler/controller/consumer) and its **transport contract** (HTTP/gRPC/CLI/queue).
2. Identify the **real external dependencies** (DB, cache, broker, external API).
3. Write **one happy-path test** through the real wiring and real infrastructure. Testcontainers has libraries for most languages (Java, .NET, Go, Node, Python, Rust, and more); otherwise use an equivalent ephemeral real dependency and state the confidence gap.
4. Put **each error-mapping branch** in the smallest unit/slice test that still includes the mapping code.
5. **Mock the semantic ports/use-cases** — never the DB driver or framework internals.
6. Keep the **Decision List** above. Only the tooling changes, not the strategy.

## Composing with Other Skills (Optional)

This skill is self-contained. If you also use them, these compose cleanly:

- `/test-namer` — how to name the test (this skill decides where it goes; test-namer decides what to call it).
- `/vertical-slice-architecture` — how to structure the feature directory.
- `/low-complexity` — keeps test functions readable.

None are required to apply dual testing.

## Checklist

For each new handler, feature, or worker:

- [ ] Each handler depends on a narrow semantic port (or reuses an existing one), not the DB driver
- [ ] The wiring point injects the port — real in prod/integration, mock in unit/slice
- [ ] Constructors/factories do no external I/O at construction (unless the framework owns startup validation)
- [ ] One integration test per happy path, through real wiring and real infrastructure
- [ ] One unit/slice test per error-mapping branch (validation, not-found, infra error, resilience), with the port mocked
- [ ] Happy paths are NOT duplicated in the unit/slice layer
- [ ] The matching language reference was read — or, if none exists, the 6-step adaptation was applied
