---
name: csharp-dotnet
description: Use when building on .NET 8+ with C# 12. Covers nullable reference types, records, async/await correctness, minimal APIs, dependency injection, and EF Core query performance.
metadata:
  category: languages
  version: 1.0.0
  tags: [csharp, dotnet, async, efcore, minimal-api]
---

# C# and .NET

## Purpose

Build .NET applications that are null-safe by contract, correctly asynchronous end to end, and free of the ORM traps that quietly turn one query into a thousand.

## When to Use

- Writing or reviewing C# on .NET 8 or later.
- Enabling nullable reference types on an existing project.
- Designing minimal APIs or ASP.NET Core services.
- Diagnosing async deadlocks or thread-pool starvation.
- Fixing EF Core N+1 queries and tracking overhead.

## Capabilities

- Nullable reference types, records, pattern matching, required members.
- Async correctness: `ConfigureAwait`, cancellation tokens, `IAsyncEnumerable`.
- Minimal APIs, endpoint filters, model validation, problem details.
- Dependency injection lifetimes and scope correctness.
- EF Core: projections, split queries, no-tracking reads, compiled queries.

## Inputs

- Solution or project files and target framework.
- Whether the project is a library, web API, or worker service.
- Data-access layer and database engine.

## Outputs

- Code compiling with `<Nullable>enable</Nullable>` and `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`.
- Async paths that flow a `CancellationToken` from request to database.
- EF Core queries with explicit projection and tracking behavior.

## Workflow

1. **Enable the gates** — Nullable reference types and warnings-as-errors, project-wide.
2. **Model** — Records for immutable values; `required` members instead of constructor sprawl.
3. **Thread cancellation** — Every async method takes a `CancellationToken` and passes it down.
4. **Shape the queries** — Project to DTOs; never materialize entities you will not mutate.
5. **Gate** — Build with warnings as errors, run analyzers, run the test suite.

## Best Practices

- Never call `.Result` or `.Wait()` on a Task. That is how deadlocks and starvation happen — async all the way down.
- Use `ConfigureAwait(false)` in library code; it is unnecessary in ASP.NET Core application code.
- Register `DbContext` as scoped. Injecting it into a singleton is a correctness bug, not a style issue.
- Read-only queries use `AsNoTracking()`. Tracking every row you only intend to display wastes memory and time.
- Return `Results.Problem(...)` / RFC 7807 payloads rather than bare status codes.
- Validate at the endpoint, not in the domain. The domain should be able to assume its inputs are valid.

## Examples

**Minimal API endpoint with cancellation and projection:**

```csharp
app.MapGet("/orders/{id:guid}", async (
    Guid id,
    AppDbContext db,
    CancellationToken ct) =>
{
    var order = await db.Orders
        .AsNoTracking()
        .Where(o => o.Id == id)
        .Select(o => new OrderSummary(
            o.Id,
            o.Customer.Name,
            o.Lines.Count,
            o.Lines.Sum(l => l.Price * l.Quantity)))
        .SingleOrDefaultAsync(ct);

    return order is null
        ? Results.Problem(statusCode: 404, title: "Order not found")
        : Results.Ok(order);
});
```

## Notes

- `IAsyncEnumerable<T>` streams results without buffering the full set — use it for large exports.
- EF Core's split-query mode avoids the cartesian explosion of multiple `Include`s, at the cost of extra round trips. Measure both.
- Source generators (e.g. `System.Text.Json`) remove reflection at startup and matter a great deal for AOT and cold-start latency.
