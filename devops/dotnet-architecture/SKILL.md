---
name: dotnet-architecture
description: Decide the structure of an ASP.NET Core solution - project layout, feature slices vs layers, module seams, where business logic lives, data access shape, cross-cutting concerns (config, errors, observability, resilience, caching, background work, messaging), and when to split services. Use when starting a solution, adding a feature that doesn't fit the existing structure, introducing a new project or dependency, or reviewing architecture. For HTTP contracts use api-design; for shaping a module's interface use codebase-design; for recording decisions use domain-modeling.
---

# .NET Architecture (ASP.NET Core, .NET 10)

Follow the structure already in the codebase when it exists, even if these defaults differ; propose a change as an ADR instead of mixing styles. Use these defaults for new code or when the codebase has no settled pattern. Every layer, project, package, and abstraction must answer a present need; "we might swap the database" is not one.

## Platform baseline

- Target .NET 10 (LTS, supported to November 2028). .NET 11 is STS (GA November 2026); move to it only for a feature you need now, such as C# 15 union types or closed class hierarchies, and record that as an ADR.
- Pin the SDK in `global.json` with `rollForward: latestFeature`.
- Install `dotnet-ef` as a local tool (`dotnet new tool-manifest`, then `dotnet tool install dotnet-ef`) at the same version as the EF Core packages, so everyone and CI run the same tools. The startup project needs `Microsoft.EntityFrameworkCore.Design`.
- Use the `.slnx` solution format (the .NET 10 SDK default for `dotnet new sln`).
- Shared build settings go in `Directory.Build.props` at the repo root: `Nullable` enabled, `ImplicitUsings` enabled, `TreatWarningsAsErrors` true, `AnalysisLevel` latest. Package versions go in `Directory.Packages.props` with Central Package Management (`ManagePackageVersionsCentrally`); no `Version` attributes in project files.

## Solution shape

Pick the smallest shape that fits, and grow along this path only when the trigger appears:

| Shape | Projects | Use when | Grow when |
|---|---|---|---|
| Single project, feature folders | `MyApp.Api`, `MyApp.Api.Tests` | One team, one deployable, domain still being discovered. The default. | Distinct business areas start reaching into each other's data or internals |
| Modular monolith | `MyApp.Api` host + one project per module (`MyApp.Orders`, `MyApp.Billing`) + tests | Several business areas with real seams between them, still one deployable | A module needs independent deploys, scaling, or ownership by a separate team |
| Separate services | One deployable per service | Independent deploy/scale/team needs that the monolith blocks today | - |

- Don't start with microservices. Splitting is cheap from a modular monolith with clean seams and expensive from a tangled one.
- Clean Architecture's Domain/Application/Infrastructure/Api project split is not the default. Use it only when the domain model is large and invariant-heavy enough that compile-time isolation from infrastructure pays for the extra indirection; feature folders inside a module give most of the benefit.

## Feature slices

Organize by feature, not by technical type. A feature folder holds everything for one use case:

```
src/MyApp.Api/
  Program.cs
  Features/
    Orders/
      CreateOrder.cs        // request, response, validation, handler, endpoint mapping
      GetOrder.cs
      OrderEndpoints.cs     // MapGroup("/orders") and registration of the slice endpoints
      Order.cs              // entity, when only this feature area owns it
  Infrastructure/
    AppDbContext.cs
    Configurations/         // IEntityTypeConfiguration<T> per entity
  Common/                   // only code used by 3+ features
```

- Use minimal APIs with `MapGroup` per feature area and `TypedResults`. In a codebase already built on controllers, keep controllers rather than mixing styles.
- A slice may duplicate a little code from another slice; extract only on the third use, and only if the copies change for the same reason.
- Endpoints stay thin: bind, call the handler or service, map the result to a typed result. Business rules live in the handler, a service, or the entity.
- Handlers are plain classes registered in DI and injected into the endpoint. No mediator library by default: MediatR and MassTransit went commercial in 2025, and a mediator adds indirection without a present need. If pipeline behaviors (cross-cutting per handler) become a real need, write a small decorator or use an endpoint filter first.
- Map DTOs by hand with static methods or extension methods next to the slice. If mapping volume becomes a burden, use a source generator (Riok.Mapperly) rather than reflection-based mappers.

## Modules

When the solution becomes a modular monolith:

- Each module owns its tables, preferably in its own schema, and its own `DbContext`. No module queries another module's tables.
- Modules talk through a small public contract (interfaces and DTOs in the module project, or a `MyApp.Orders.Contracts` project), or through in-process events. Everything else is `internal`.
- Each module exposes one registration method (`services.AddOrdersModule(config)`, `app.MapOrdersEndpoints()`) called from the host.
- Enforce the seams with architecture tests (`TngTech.ArchUnitNET`) so they don't erode.

## Domain logic

- Put invariants on the entity: private setters, a constructor or factory that only builds valid instances, methods named for business operations (`order.Cancel(reason)`), not public property bags edited from outside.
- Use value objects (records, or EF Core complex types) for concepts with rules: `Money`, `EmailAddress`, `DateRange`.
- Keep simple CRUD simple: an entity with no invariants doesn't need a rich model.
- Expected failures (validation, not found, business rule violations) are return values that become ProblemDetails, not exceptions. Use a small result type or C# 15 unions once on .NET 11. Throw only for unexpected failures, and handle those centrally with `IExceptionHandler` and `AddProblemDetails()`.

## Data access

- `DbContext` is the unit of work and the repository. Inject it directly into handlers; don't wrap it in a generic repository.
- Add a specific repository only when the same non-trivial query or aggregate load is reused across several slices, or to hide a module's persistence from other modules.
- Entity configuration lives in `IEntityTypeConfiguration<T>` classes, applied with `ApplyConfigurationsFromAssembly`.
- Reads project to DTOs with `Select` and `AsNoTracking`; writes load the entity, call its methods, and `SaveChangesAsync` once per request.
- Bulk changes that need no domain logic use `ExecuteUpdateAsync` / `ExecuteDeleteAsync` instead of loading entities.
- Map value objects and nested data as complex types (`ComplexProperty`, with `.ToJson()` for a JSON column), not owned entities.
- Soft delete and multi-tenancy use named query filters (`HasQueryFilter("SoftDelete", ...)`), so a query can turn off one filter with `IgnoreQueryFilters(["SoftDelete"])` and keep the rest.
- Use optimistic concurrency tokens on entities edited concurrently. For slow or incorrect EF Core queries, use the `optimizing-ef-core-queries` skill from the `dotnet-data` plugin; for migrations, follow the `ef-migrations` rule.

## Cross-cutting concerns

| Concern | Default |
|---|---|
| Configuration | Options pattern: `AddOptions<T>().BindConfiguration("Section").ValidateDataAnnotations().ValidateOnStart()`. Secrets from user-secrets locally and a vault (e.g. Azure Key Vault) in deployed environments; never in `appsettings.json`. |
| Validation | Built-in minimal API validation: `builder.Services.AddValidation()` with DataAnnotations or `IValidatableObject`. Add FluentValidation only for rules DataAnnotations can't express cleanly. |
| Errors | `AddProblemDetails()`, `UseExceptionHandler()`, and an `IExceptionHandler` for unexpected exceptions. Log inside the handler: since .NET 10, exceptions it handles are no longer logged by default. Shapes per the `api-design` skill. |
| Observability | OpenTelemetry for traces, metrics, and logs (`AddOpenTelemetry().WithTracing(...).WithMetrics(...)`, exported via OTLP). Structured logging through `ILogger` with message templates; source-generated `[LoggerMessage]` on hot paths. Health checks: readiness (dependencies included) at `/health`, liveness (process only) at `/alive`. |
| Outbound HTTP | Typed clients via `AddHttpClient<T>()` plus `AddStandardResilienceHandler()` from `Microsoft.Extensions.Http.Resilience`. Never `new HttpClient()` per call. |
| Caching | `HybridCache` (`AddHybridCache()`) for in-process plus distributed caching with stampede protection. Output caching for whole GET responses. |
| Time and randomness | Inject `TimeProvider`; never call `DateTime.UtcNow` in business logic. |
| Background work | `BackgroundService` for in-process periodic or queue work, with a scoped `DbContext` created per iteration via `IServiceScopeFactory`. A scheduler (Quartz.NET, Hangfire) only for persisted schedules or retries across restarts. |
| Messaging | In-process events first. For a broker, use the official client (`Azure.Messaging.ServiceBus`, `RabbitMQ.Client`) or an MIT library (Wolverine, Rebus); MassTransit v9 needs a commercial license. Publish integration events through a transactional outbox so a message is never sent for a rolled-back change. |
| Auth | ASP.NET Core authentication and authorization policies; authorize at the endpoint group (`RequireAuthorization("policy")`), and check resource ownership in the handler. |

## Dependency injection

- Register by feature or module through extension methods, not one giant `Program.cs`.
- Constructor injection with primary constructors. Their parameters are mutable captures, not `readonly` fields: never reassign one, and assign it to a `private readonly` field when the class is large or the value must not change. No service locator (`IServiceProvider.GetService` in business code).
- Lifetimes: `DbContext` and anything holding it scoped; stateless services scoped or singleton; never inject a scoped service into a singleton.
- Interfaces only where there is more than one implementation or a test needs to replace something you don't own; a concrete class with one implementation needs no interface.

## Before finishing an architecture change

- [ ] It follows the existing structure, or the deviation is recorded as an ADR candidate
- [ ] Every new project, package, or abstraction is tied to a present need
- [ ] Module seams hold: no cross-module table access, internal by default
- [ ] Business rules live in handlers, services, or entities, not endpoints
- [ ] Configuration is validated on start; secrets are not in source
- [ ] New outbound calls have resilience; new background work creates its own scope
- [ ] Hard-to-reverse choices (solution shape, module split, messaging, database) are listed for the `domain-modeling` skill to record
