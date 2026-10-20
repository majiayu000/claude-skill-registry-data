---
name: clean-architecture
description: "Apply these opinionated .NET 8 architecture conventions whenever structuring or reviewing a backend service: clean architecture layering and which direction dependencies point, when CQRS with MediatR is worth it, cross-cutting concerns as pipeline behaviours, minimal APIs grouped by feature, keeping DbContext in Infrastructure, health checks and structured logging, WebApplicationFactory integration tests, and when AOT pays off."
---

# .NET Core Architecture

House architecture conventions for .NET 8 backend services. This covers how a service is _structured_; for language-level conventions see the `csharp` skill.

## Layering

Dependencies point inward only. Domain knows nothing about anything else, and Infrastructure is the one layer allowed to reference a database or an SDK — which is what lets the inner layers be tested without either.

```text
Domain          entities, value objects, domain events, interfaces  → no dependencies
Application     use cases, CQRS handlers, DTOs, validators          → Domain
Infrastructure  EF Core, external APIs, implementations of Domain interfaces → Domain + Application
Api             endpoints, DI wiring, middleware                    → all of the above
```

The test that keeps this honest: if `Domain` compiles with no package references beyond the BCL, the boundary is intact.

Entities enforce their own invariants: private setters, a private parameterless constructor for EF Core's materialiser, and a static factory that validates. Public setters mean any layer can put the entity into an invalid state, and then "the domain guarantees X" is just a comment.

```csharp
public class Product
{
    public string Name { get; private set; } = string.Empty;
    public decimal Price { get; private set; }

    private Product() { } // EF Core materialisation only

    public static Product Create(string name, decimal price) =>
        price <= 0
            ? throw new DomainException("Price must be greater than zero")
            : new Product { Name = name, Price = price };
}
```

## Conventions

- **CQRS with MediatR when reads and writes genuinely differ** — different models, different consistency, different scaling. On a CRUD service it is ceremony; adopt it because the domain asked for it, not by default.
- **Cross-cutting concerns go in pipeline behaviours**, not in handlers. Validation, logging, and transactions written once as a behaviour apply to every handler and can't be forgotten in a new one.
- **Minimal APIs grouped with `MapGroup`**, one file per feature area. A single `Program.cs` holding every endpoint stops being readable at about twenty routes.
- **Validation at the Application boundary** (FluentValidation in a behaviour), so the same rules apply no matter which entry point invoked the use case. Validation in the endpoint only guards HTTP.
- **DbContext stays in Infrastructure**, behind an interface the Application layer owns. Leaking `DbContext` into handlers ties your use cases to EF and makes them untestable without a provider.
- **Secrets never in `appsettings.json`** — user-secrets locally, environment or a vault in production. Anything committed is compromised, and rotating it means a redeploy.
- **Health checks (`/health/live`, `/health/ready`) and structured logging with correlation IDs** from the start. Retrofitting observability into a running incident is the wrong time to discover you have none. Keep the two probes genuinely different: readiness may check the database and downstream APIs, liveness must check only that the process itself is alive. A liveness probe that pings the database restarts every pod during a brief database blip, turning a recoverable dependency failure into a full outage.
- **Containers run as a non-root user.** Add a `USER` line — the default root container turns a process-level compromise into host-level reach, and it costs one line to prevent.
- **Integration tests over `WebApplicationFactory`** with a real database (Testcontainers). They exercise the DI graph, routing, serialisation, and EF mapping — the layers where mocked unit tests report success on a broken service.
- **AOT only where startup time or footprint justifies it.** It rules out runtime reflection, which quietly breaks some serialisers and DI patterns; verify the whole stack tolerates it before committing.
