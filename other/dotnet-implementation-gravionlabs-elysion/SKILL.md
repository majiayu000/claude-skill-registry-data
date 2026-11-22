---
name: dotnet-implementation
description: 'C#/.NET implementation and test rules extending `implementation`. Use when writing or changing C# code.'
---

The official `dotnet` plugin skills (dependency `dotnet/skills`) cover general C#/.NET style. Only project conventions follow.

## Conventions

- `dotnet build` with Central Package Management; nullable enabled
- Naming: `_camelCase` fields; files `{ClassName}.cs`
- File-scoped namespaces; global usings for `System.*` in one file
- DI: constructor injection only, prefer primary constructors
- `record` types for DTOs, `init` setters for models
- Solution: code in `src/`, versions in `Directory.Packages.props`
- Library code: `ConfigureAwait(false)` on every `await`; app code: optional
- I/O methods accept `CancellationToken cancellationToken = default` and pass it through
- Logging: `ILogger<T>` with structured templates, never `Console.WriteLine`
- XML docs on public API; `<summary>` is one sentence starting with a third-person verb
- Upgrades: bump versions centrally in `Directory.Build.props` / `Directory.Packages.props`; no prerelease unless requested; build and test after each step
- **Aspire**: only when `detect-techstack` reports `frameworks: ["aspire"]`, load `dotnet-aspire`

## Format

- Extensions: `.cs`
- Format: `dotnet format --include {files}`
- Check (read-only): `dotnet format --verify-no-changes --include {files}`
- Run after green tests, before the commit: `pwsh <implementation dir>/scripts/Format-Changed.ps1 -Language dotnet` (`-Check` for the check commands; not-configured, override: references/format.md of `implementation`)

## EF Core

- Fluent API in `IEntityTypeConfiguration<T>`, not data annotations
- Always configure string max length
- Never edit a generated migration; add a new one

## Tests

Runner, layout, naming, structure and mocking live in `dotnet-test`.

## Review rules

- 🔴 Lint run (`Format-Changed.ps1 -Lint -Language dotnet`, analyzer) exits non-zero: error-level findings; 🟡 warning-level findings
- No `.Result`, `.Wait()`, or `async void` (except event handlers)
- `CancellationToken` propagated through async call chains
- Nullable reference types respected; no swallowed exceptions
- `record` for DTOs; dependencies injected via interfaces
- Tests follow `dotnet-test` conventions

## Minimal APIs

House convention: endpoints are organized with Carter modules, not scattered `app.MapGet` calls in `Program.cs`:

```csharp
public class <Feature>Module : ICarterModule
{
    public void AddRoutes(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/<feature>").WithTags("<Feature>");
        group.MapGet("/", Handle).WithName("<Name>").WithOpenApi();
    }
}
```

- Register with `builder.Services.AddCarter()` and `app.MapCarter()`
- Typed request/response records; OpenAPI metadata (`.WithSummary()`, `.Produces<T>()`, `.ProducesProblem()`)
- Return `TypedResults`, not `Results.Ok(...)`; validate input (FluentValidation or Data Annotations)
