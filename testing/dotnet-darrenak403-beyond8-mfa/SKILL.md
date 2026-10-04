---
name: dotnet
description: .NET implementation details — C# patterns, ASP.NET Core Minimal API, EF Core, xUnit/Moq/FluentAssertions/Testcontainers, .NET Aspire orchestration, MassTransit/RabbitMQ events, FluentValidation. Activate for any C# code task, writing endpoints/services/entities/validators/tests, configuring Aspire, wiring MassTransit consumers, or reviewing .NET code.
---

# .NET — Clean Architecture Implementation

Load only the reference needed for the current task.

## Reference Map

| Task                                                    | When to load                 | File                                                             |
| ------------------------------------------------------- | ---------------------------- | ---------------------------------------------------------------- |
| Where does code go? What layer?                         | Any new feature or refactor  | [`references/architecture.md`](references/architecture.md)       |
| Writing C# — DI, async, records, patterns               | Writing or reviewing C# code | [`references/dotnet-patterns.md`](references/dotnet-patterns.md) |
| REST endpoints, routes, pagination, response envelope   | API design or new endpoint   | [`references/api-design.md`](references/api-design.md)           |
| Tests, TDD cycle, mocking, integration tests            | Writing or fixing tests      | [`references/testing.md`](references/testing.md)                 |
| Auth, JWT, secrets, input validation, SQL injection     | Security concerns            | [`references/security.md`](references/security.md)               |
| Aspire bootstrap, service discovery, typed HTTP clients | Aspire / microservice wiring | [`references/aspire.md`](references/aspire.md)                   |
| Events, consumers, MassTransit, RabbitMQ                | Event-driven inter-service   | [`references/events.md`](references/events.md)                   |
| EF Core queries, caching, async perf, output caching    | Performance optimization     | [`references/performance.md`](references/performance.md)         |

---

## Decision Tree

```
TASK?
│
├─ New feature / endpoint
│  ├─ Where does this code live?   → references/architecture.md
│  ├─ How to structure the API?    → references/api-design.md
│  └─ Service + C# patterns?       → references/dotnet-patterns.md
│
├─ Writing tests / TDD
│  └─ All test concerns            → references/testing.md
│
├─ Security concern
│  ├─ Secrets, auth, JWT, input    → references/security.md
│  └─ Endpoint auth rules          → references/security.md + references/api-design.md
│
├─ Microservice infrastructure
│  ├─ Aspire, service discovery    → references/aspire.md
│  └─ Events, consumers            → references/events.md
│
├─ Performance concern
│  ├─ Slow queries / N+1           → references/performance.md
│  ├─ Caching (memory / Redis)     → references/performance.md
│  └─ Async, ValueTask, parallel   → references/performance.md
│
└─ Code review / quality check
   ├─ Architecture violations?     → references/architecture.md
   ├─ C# anti-patterns?            → references/dotnet-patterns.md
   ├─ Performance issues?          → references/performance.md
   └─ Security issues?             → references/security.md
```

---

## Coverage

- **Clean Architecture** — Domain / Application / Infrastructure / Api / Common layers
- **C# patterns** — records, DI, async/await, Options, guard clauses, repository pattern
- **REST API** — Minimal API route groups, pagination, response envelope, soft delete
- **Testing** — TDD cycle, xUnit, FluentAssertions, Moq, Testcontainers, WebApplicationFactory
- **Security** — secrets, JWT, FluentValidation, SQL injection, auth, PII logging
- **Aspire** — service bootstrap, AppHost orchestration, service discovery, typed HTTP clients
- **Events** — MassTransit + RabbitMQ, event contracts, consumers, retry, idempotency
- **Performance** — EF Core query tuning, IMemoryCache, IDistributedCache, HTTP output caching, async patterns
