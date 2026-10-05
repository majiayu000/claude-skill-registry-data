---
name: umbrella-dotnet-scaffold-service
description: 'Scaffold a logic service (interface, implementation, models) in the Core.Logic project, following the Umbrella ServiceBase pattern with Lazy<T> repo injection.'
---

# Scaffold Service

## Purpose

Add a new service to the `Core.<AppName>.Core.Logic` project for domain logic that goes beyond simple data access -- for example, AI integrations, external API calls, file processing orchestration, or complex calculations. Controllers call repositories directly for CRUD; this Logic project is for work that is genuinely more complex than that.

**Do not create per-entity wrapper services that only delegate to a repository** — that logic belongs in the controller (or its lifecycle hooks / controller service for Pattern 2). This rule overrides anything the Discovery step suggests: if the target project contains existing thin wrapper services, they are a legacy deviation, not a pattern to replicate.

## Layer boundary rule

> **Core.Logic must never reference Web-layer projects.**
>
> Service interfaces and implementations in `Core.Logic` must not import types from any `*.Web.Models`, `*.Web.Shared.Models`, or other Web-layer namespace. If a method needs custom input/output shapes, define them as plain `record` types in `Services\<Domain>\Models\` (Step 1). If the types you need currently live in a Web.Models project, that is a signal to create dedicated Core.Logic models — not to import from Web.

## Discovery (read these before writing anything)

1. Read 1-2 existing service implementations in `Core\<AppName>.Core.Logic\Services\` to understand the subfolder structure, constructor patterns, and method conventions.
2. Read the corresponding interfaces in their `Abstractions\` subfolder.
3. Read `Core\<AppName>.Core.Logic\IServiceCollectionExtensions.cs` to understand the DI registration structure.
4. Identify the layer-specific exception type (e.g., `<AppName>CoreLogicException` in `Core\<AppName>.Core.Logic\Exceptions\`).

---

## Folder structure

Services are grouped by domain under `Core\<AppName>.Core.Logic\Services\`:

```
Services\
  <Domain>\
    Abstractions\
      I<ServiceName>.cs
    Models\
      <ModelName>.cs        (only if the service has its own result/request models)
    <ServiceName>.cs
```

Examples: `Services\Careers\`, `Services\Industries\`. Use the entity or feature name as the domain folder.

---

## Step 1 -- Create result/request models (if needed)

Create model files in `Services\<Domain>\Models\` only if the service returns or accepts types that do not already exist in the domain or shared projects. Simple services that return existing entity types or primitives do not need model files.

Models are plain `record` or `class` types with no base class:

```csharp
namespace <AppName>.Core.Logic.Services.<Domain>.Models;

public sealed record <ModelName>(string Title, string Description);
```

---

## Step 2 -- Create the interface

**File location:** `Core\<AppName>.Core.Logic\Services\<Domain>\Abstractions\I<ServiceName>.cs`

```csharp
using <AppName>.Core.Logic.Services.<Domain>.Models;  // only if custom models are used

namespace <AppName>.Core.Logic.Services.<Domain>.Abstractions;

public interface I<ServiceName>
{
    Task<<ModelName>?> GetSomethingAsync(string input, CancellationToken cancellationToken = default);
    Task<IReadOnlyCollection<<ModelName>>> FindAllAsync(CancellationToken cancellationToken = default);
}
```

**Rules:**
- The interface is `public` (no base interface)
- Add explicit `using` directives for any model or enum types used in method signatures that are not covered by the project's global usings -- check existing interface files to see what is required
- `using` directives must not reference any namespace containing `.Web.` -- method signatures must only use types from `Core.Logic`, `Core.Domain`, `Core.Common`, or the BCL
- Every method is async with `CancellationToken cancellationToken = default` as the last parameter
- Return types follow the same conventions as repository interfaces: `Task<T?>` for single-or-null, `Task<IReadOnlyCollection<T>>` for lists

---

## Step 3 -- Create the implementation

**File location:** `Core\<AppName>.Core.Logic\Services\<Domain>\<ServiceName>.cs`

```csharp
using <AppName>.Core.Data.Repositories.Abstractions;
using <AppName>.Core.Logic.Exceptions;
using <AppName>.Core.Logic.Services.Abstractions;
using <AppName>.Core.Logic.Services.<Domain>.Abstractions;
using <AppName>.Core.Logic.Services.<Domain>.Models;

namespace <AppName>.Core.Logic.Services.<Domain>;

internal sealed class <ServiceName> : ServiceBase, I<ServiceName>
{
    private readonly Lazy<I<Entity>Repository> _<entity>Repository;
    private readonly IExternalService _externalService;

    public <ServiceName>(
        ILogger<<ServiceName>> logger,
        Lazy<I<Entity>Repository> <entity>Repository,
        IExternalService externalService)
        : base(logger)
    {
        _<entity>Repository = <entity>Repository;
        _externalService = externalService;
    }

    public async Task<<ModelName>?> GetSomethingAsync(string input, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        Guard.IsNotNullOrEmpty(input);

        try
        {
            // access repo via .Value
            var entity = await _<entity>Repository.Value.FindByXxxAsync(input, cancellationToken: cancellationToken);

            if (entity is null)
                return null;

            return new <ModelName>(entity.Title, entity.Description);
        }
        catch (Exception exc) when (Logger.WriteError(exc, new { input }))
        {
            throw new <AppName>CoreLogicException("There was a problem getting the <thing> with the specified input.", exc);
        }
    }
}
```

**Rules:**
- Always `internal sealed class` inheriting `ServiceBase` and the interface
- Constructor: `ILogger<T>` is the first parameter (passed to `: base(logger)`); remaining params are stored as `private readonly` fields
- Repositories are injected as `Lazy<IRepository>` and accessed via `.Value` inside methods
- Direct (non-repository) services are injected normally, not wrapped in `Lazy<T>`
- Add `using` directives for all namespaces that are not covered by the project's implicit or global usings -- follow the pattern of existing service files in the same project

---

## Step 4 -- Write service methods

Every method follows this structure:

```csharp
public async Task<T> DoWorkAsync(string input, CancellationToken cancellationToken = default)
{
    cancellationToken.ThrowIfCancellationRequested();
    Guard.IsNotNullOrEmpty(input);  // Guard.IsNotNull for non-string reference types; omit for value types

    try
    {
        // logic here -- call repos via .Value, call external services, build results
        return result;
    }
    catch (Exception exc) when (Logger.WriteError(exc, new { input }))
    {
        throw new <AppName>CoreLogicException("There was a problem doing the work.", exc);
    }
}
```

**Rules:**
- First line always: `cancellationToken.ThrowIfCancellationRequested();`
- Validate string inputs with `Guard.IsNotNullOrEmpty(param)` (Logic project uses `IsNotNullOrEmpty`, not `IsNotNullOrWhiteSpace` as in Data)
- The anonymous object in `Logger.WriteError` should contain the method's significant input parameters (omit `cancellationToken`)
- Re-throw as `<AppName>CoreLogicException`
- If integrating with an external API or service that may fail transiently, consider wrapping the call in a retry policy if one exists in the project (e.g., `AiPolicyHelper.RetryPolicy.ExecuteAsync(...)`)

---

## Step 5 -- Register in DI

**File:** `Core\<AppName>.Core.Logic\IServiceCollectionExtensions.cs`

Add one line in the `// Services` section, in alphabetical order:

```csharp
_ = services.AddScoped<I<ServiceName>, <ServiceName>>();
```

Services are always `AddScoped`. File handlers are `AddSingleton` -- but those are covered by a separate skill.

---

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Verification

1. Confirm the interface is `public`, has no base interface, and every method ends with `CancellationToken cancellationToken = default`.
2. Confirm the implementation is `internal sealed`, inherits `ServiceBase` and the interface, and `ILogger<T>` is the first constructor parameter passed to `: base(logger)`.
3. Confirm repositories are `Lazy<IRepository>` and accessed via `.Value` inside methods.
4. Confirm every method calls `cancellationToken.ThrowIfCancellationRequested()` first, validates string inputs with Guard, and re-throws as `<AppName>CoreLogicException`.
5. Confirm `AddScoped<I<ServiceName>, <ServiceName>>()` is present in `IServiceCollectionExtensions.cs`.
