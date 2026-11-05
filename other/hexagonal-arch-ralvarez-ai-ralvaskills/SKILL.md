---
name: hexagonal-arch
version: 1.1.0
description: Hexagonal architecture (ports & adapters) — dependencies point inward; domain declares ports, adapters implement them; domain never imports framework/DB/HTTP. Dependency graph is prescribed, folder layout is not. Use when designing service structure, placing interfaces, or evaluating seam cleanliness.
---

# Hexagonal Architecture — Ports & Adapters

The pattern, distilled: **the domain core knows nothing about the world**. Everything that touches the outside (HTTP, DB, queue, cron, third-party API) is an adapter. Adapters depend on the domain; the domain never depends on adapters. Pairs with [ddd-architect](../ddd-architect/SKILL.md) — DDD answers "what's in the domain"; hexagonal answers "where does the domain live and what touches it".

## 1. The pattern

Three layers, named by their role rather than their location:

- **Domain core** — entities, value objects, aggregates, domain services, business policies. Plain language types and functions. No imports from any framework, database driver, or HTTP library.
- **Ports** — interfaces declared *by the domain* describing what it needs from the outside (`UserRepo`, `EmailSender`, `PaymentGateway`). The names are domain-meaningful, not technology-meaningful (`UserRepo`, not `PostgresClient`).
- **Adapters** — concrete implementations of ports. Live outside the domain. One adapter per concrete technology: `PostgresUserRepo`, `SmtpEmailSender`, `StripePaymentGateway`. Also one per testing strategy: `InMemoryUserRepo`, `FakeEmailSender`.

The diagram is conventionally a hexagon (the "hex" in hexagonal) — the shape doesn't matter; the direction of arrows does.

## 2. Dependency direction — always inward

This is the single non-negotiable rule.

```
HTTP handler → application service → domain service → aggregate
                                                          ↑
                                            uses port:  UserRepo (interface)
                                                          ↑
                                                  implements:
                                            PostgresUserRepo (adapter)
```

- **Domain imports nothing outward.** No `import "net/http"`, no `from sqlalchemy ...`, no `from fastapi ...` in domain files. Static check: open any file in the domain package and grep its imports.
- **Adapters import the domain.** `PostgresUserRepo` imports `User` (the aggregate) and `UserRepo` (the port). The domain doesn't know `PostgresUserRepo` exists.
- **Application services orchestrate.** They depend on ports (interfaces) and call domain services; they're constructed with concrete adapters injected.
- **HTTP/CLI handlers depend on application services.** They translate from wire format to domain types and back, then delegate.

If you can't draw an arrow from any file in your codebase inward without crossing the rule, the architecture is hexagonal.

## 3. Where to put port definitions

Idioms differ; the rule is the same.

- **Go** — define the interface in the **consuming** package per [go-architect §4](../../languages/go-architect/SKILL.md#4-interfaces). The domain package declares `UserRepo`; the adapter package (`postgres`) implements it. Adapter imports domain; domain has no idea about adapter. Idiomatic and clean.
- **Python** — define `typing.Protocol` (structural typing) in the domain module per [python-architect §3](../../languages/python-architect/SKILL.md#3-interfaces--di). Same direction; no inheritance required. Adapters happen to satisfy the Protocol.
- **Other languages** — same principle: interface declared by the consumer (the domain); implementation lives with the adapter.

This is the inverted direction from what frameworks usually suggest ("define interfaces in their own `interfaces/` package"). The domain owns its contracts.

## 4. Primary vs secondary adapters

| | Primary (driving) | Secondary (driven) |
|---|---|---|
| Direction | World → application | Application → world |
| Examples | HTTP handlers, gRPC handlers, CLI commands, message-queue consumers, scheduled-job runners | DB repositories, HTTP clients to third parties, email senders, queue publishers, cache, file system |
| Initiates the call | Yes — receives external trigger | No — domain code calls them |
| Implements what | The application service or use-case entry point | A port the domain defined |

Both kinds of adapter are equally outside the domain. They differ only in who calls whom.

## 5. Testing benefits

- **Domain unit tests use no infrastructure.** Construct the domain types directly; assert on behavior. No DB, no HTTP server, no mocks of internal collaborators (per [tdd](../../workflows/tdd/SKILL.md)).
- **Swap adapters for fakes.** `InMemoryUserRepo` for tests; `PostgresUserRepo` in production. Tests don't need a real DB unless they're specifically integration-testing the adapter itself.
- **Adapter tests are integration tests** — they verify the adapter actually fulfills the port against the real technology (real Postgres, real SMTP server). One adapter, one integration test suite, narrow scope.
- **Application service tests use fake adapters + real domain.** Verify the orchestration without booting the full stack.

This is where hexagonal pays back. The cost (defining ports, separating layers) is paid up front; the savings (fast, focused tests; swap-out for new technology) compound forever.

## 6. Common mistakes

- **Anemic domain.** All "domain" types are bags of getters and setters; all logic lives in services that operate on them. The domain isn't really a domain — it's a DTO layer. Fix: move behavior onto entities and value objects.
- **Leaky port.** The port exposes infrastructure types: `UserRepo.FindWithJoin(...)` returning a SQL row, or `EmailSender.SendWithMimeType(...)` exposing email library types. Fix: rename the method, change the return type to domain types, add a translation step inside the adapter.
- **Adapters with business logic.** `PostgresUserRepo.PromoteToPremium(...)` decides what "premium" means. Fix: the rule lives in the domain (`User.PromoteToPremium()`); the adapter just persists the new state.
- **Single-adapter ports.** A port introduced "for future flexibility" with one implementation and no second adapter justified. Per [improve-codebase-architecture's DEEPENING.md](../../refactoring/improve-codebase-architecture/DEEPENING.md): *one adapter = hypothetical seam; two adapters = real seam*. If you only ever need one, the port is indirection without payoff. Inline it.
- **Reaching into infrastructure from the domain.** `User.save()` calling the DB. Fix: `User` is the data + behavior; `UserRepo.save(user)` does the persistence. The aggregate doesn't know how it gets persisted.
- **Treating "hexagonal" as a folder convention.** Renaming packages `domain/`, `application/`, `infrastructure/`, `interfaces/` doesn't make a codebase hexagonal. The dependency direction does. A flat folder structure can be hexagonal if the imports flow correctly; a deeply layered structure can be a mess if they don't.
- **Naming an adapter directory "ports."** A port is always an interface; an adapter is always a concrete implementation. If you split adapters into their own directories, name them after direction (`primary`/`secondary`, or `driving`/`driven`) — never reuse "ports" for an adapter folder just because that's where the outside world plugs in. An explicit primary port, when one is warranted (see §7 — usually only once a second caller needs to swap it), belongs with the layer that offers it (the application service), not with the adapter that calls into it.

## 7. When NOT to use it

- **Small services with one external dependency.** A CRUD service that talks to one DB and exposes HTTP doesn't need a defined port — the DB call is the use case. Adding a `UserRepo` interface with one implementation is ceremony.
- **Throwaway code.** Prototypes, scripts, spikes. The pattern's value compounds over months and years; over days it's pure cost.
- **Pure transformation services.** ETL, file converters, anything where "the domain" is data shapes and the application is wiring inputs to outputs. Functional decomposition is the right tool.
- **A facade over a single adapter.** If you'd write `UserRepo` and `PostgresUserRepo` and never have a second implementation (no fake, no test double — because you'll use a real test DB), the port is pointless. Use the concrete repo directly.

The rule from [improve-codebase-architecture](../../refactoring/improve-codebase-architecture/SKILL.md): *two adapters justify the seam; one adapter is hypothetical*. The `InMemoryUserRepo` you use in tests usually counts as the second.

## 8. Reference implementations

Go and Python examples — showing the domain core, port interface, application service, and adapter implementation — live in [RECIPES.md](RECIPES.md). The imports flow inward in both: adapter → domain, never the reverse.

## 9. Cross-skill ties

- **[ddd-architect](../ddd-architect/SKILL.md)** — what's in the domain (aggregates, value objects). Hexagonal is the container; DDD is the contents.
- **[go-architect §4](../../languages/go-architect/SKILL.md#4-interfaces)** / **[python-architect §3](../../languages/python-architect/SKILL.md#3-interfaces--di)** — the language idiom for defining ports.
- **[sql-architect](../../databases/sql-architect/SKILL.md)** — how secondary DB adapters are typically implemented (raw SQL via psycopg / sqlx).
- **[tdd](../../workflows/tdd/SKILL.md)** — testing benefits compound when adapters are swappable.
- **[improve-codebase-architecture](../../refactoring/improve-codebase-architecture/SKILL.md)** — uses the same vocabulary (modules, interfaces, seams); the "one adapter = hypothetical, two = real" rule applies to port introduction.
