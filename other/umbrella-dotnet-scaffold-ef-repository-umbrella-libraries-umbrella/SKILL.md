---
name: umbrella-dotnet-scaffold-ef-repository
description: 'Scaffold a repository interface, implementation, IncludeMap, and DI registration for an existing EF Core entity, following Umbrella GenericDbRepository patterns.'
---

# Scaffold Repository

## Purpose

Add a repository interface, implementation class, optional IncludeMap static class, and DI registration for an existing EF Core entity, following the exact patterns used in the target repository.

## Discovery (read these before writing anything)

1. Read 2-3 existing repository implementations in `Core\<AppName>.Core.Data\Repositories\` to understand the query method and override conventions.
2. Read the corresponding interfaces in `Core\<AppName>.Core.Data\Repositories\Abstractions\` to see method signature patterns.
3. Read any existing IncludeMap files in `Core\<AppName>.Core.Data\Repositories\IncludeMaps\` -- only create one for the new entity if similar entities have them.
4. Read `Core\<AppName>.Core.Data\IServiceCollectionExtensions.cs` to understand the DI registration structure.
5. Identify the layer-specific exception type used by existing repositories (e.g., `<AppName>CoreDataException`).

---

## Step 1 -- Create the IncludeMap class

Only create this file if the entity has navigation properties (FK relations, collections) that callers may want to eagerly load. Skip this step for leaf entities with no navigations.

**File location:** `Core\<AppName>.Core.Data\Repositories\IncludeMaps\<EntityName>IncludeMaps.cs`

```csharp
#nullable disable
namespace <AppName>.Core.Data.Repositories.IncludeMaps;

public static class <EntityName>IncludeMaps
{
    public static IncludeMap<<EntityName>> All { get; } = new(x => x.Navigation1, x => x.Navigation2);
    public static IncludeMap<<EntityName>> Navigation1Only { get; } = new(x => x.Navigation1);
}
```

**Rules:**
- `#nullable disable` is required at the top of every IncludeMap file
- Name each property after the loading scenario or the navigation it loads (e.g., `SENDDetails`, `All`, `WithAuthor`)
- One property per logical loading scenario; if only one navigation exists, one property named after it is sufficient
- `IncludeMap<T>` takes `params Expression<Func<T, object?>>[]` -- pass navigations as lambda expressions

---

## Step 2 -- Create the interface

**File location:** `Core\<AppName>.Core.Data\Repositories\Abstractions\I<EntityName>Repository.cs`

```csharp
namespace <AppName>.Core.Data.Repositories.Abstractions;

public interface I<EntityName>Repository : IGenericDbRepository<<EntityName>>
{
    Task<<EntityName>?> FindByXxxAsync(string value, bool trackChanges = false, IncludeMap<<EntityName>>? map = null, CancellationToken cancellationToken = default);
}
```

**Rules:**
- No `using` directives -- all required types flow via global usings defined in the `.csproj`
- Inherits `IGenericDbRepository<<EntityName>>` -- this provides standard CRUD for free
- Add only query methods the entity genuinely needs beyond standard CRUD
- Standard tail parameters on every query method: `bool trackChanges = false, IncludeMap<<EntityName>>? map = null, CancellationToken cancellationToken = default`
- Omit `trackChanges` and `map` on methods that return non-entity projections (e.g., `IReadOnlyCollection<string>`, `bool`, `int`)
- Return types: `Task<<EntityName>?>` for single-or-null, `Task<IReadOnlyCollection<<EntityName>>>` for lists, `Task<bool>` for existence checks

---

## Step 3 -- Create the implementation

**File location:** `Core\<AppName>.Core.Data\Repositories\<EntityName>Repository.cs`

**Minimal pattern (no extra dependencies):**

```csharp
using Umbrella.Utilities.Dating.Abstractions;

namespace <AppName>.Core.Data.Repositories;

internal sealed class <EntityName>Repository : GenericDbRepository<<EntityName>, <AppName>DbContext>, I<EntityName>Repository
{
    public <EntityName>Repository(
        Lazy<<AppName>DbContext> dbContext,
        ILogger<<EntityName>Repository> logger,
        IDataLookupNormalizer lookupNormalizer,
        IUmbrellaDbContextHelper dbContextHelper,
        IEntityValidator entityValidator,
        IDateTimeProvider dateTimeProvider)
        : base(dbContext, logger, lookupNormalizer, dbContextHelper, entityValidator, dateTimeProvider)
    {
    }
}
```

**With extra service dependencies:**

```csharp
using Umbrella.Utilities.Dating.Abstractions;
using <Namespace.Of.ExtraService>;

namespace <AppName>.Core.Data.Repositories;

internal sealed class <EntityName>Repository : GenericDbRepository<<EntityName>, <AppName>DbContext>, I<EntityName>Repository
{
    private readonly IExtraService _extraService;

    public <EntityName>Repository(
        Lazy<<AppName>DbContext> dbContext,
        ILogger<<EntityName>Repository> logger,
        IDataLookupNormalizer lookupNormalizer,
        IUmbrellaDbContextHelper dbContextHelper,
        IEntityValidator entityValidator,
        IDateTimeProvider dateTimeProvider,
        IExtraService extraService)
        : base(dbContext, logger, lookupNormalizer, dbContextHelper, entityValidator, dateTimeProvider)
    {
        _extraService = extraService;
    }
}
```

**Rules:**
- `using Umbrella.Utilities.Dating.Abstractions;` is always required -- it contains `IDateTimeProvider`
- Add extra `using` directives only for services injected beyond the 6 base dependencies
- Always `internal sealed class` -- never `public`, never non-sealed
- Second generic parameter is the concrete DbContext class in this project (e.g., `<AppName>DbContext`)
- Base 6 dependencies in this exact order: `Lazy<TDbContext>`, `ILogger<TRepo>`, `IDataLookupNormalizer`, `IUmbrellaDbContextHelper`, `IEntityValidator`, `IDateTimeProvider`
- Extra dependencies go AFTER the 6 base params; pass only the 6 base params to `: base(...)`
- Store extra deps as `private readonly` fields

---

## Step 4 -- Write query methods

Every query method follows this pattern:

```csharp
public async Task<<EntityName>?> FindByXxxAsync(
    string value,
    bool trackChanges = false,
    IncludeMap<<EntityName>>? map = null,
    CancellationToken cancellationToken = default)
{
    cancellationToken.ThrowIfCancellationRequested();
    Guard.IsNotNullOrWhiteSpace(value);

    try
    {
        return await Items
            .TrackChanges(trackChanges)
            .IncludeMap(map)
            .SingleOrDefaultAsync(x => x.Field == value, cancellationToken);
    }
    catch (Exception exc) when (Logger.WriteError(exc, new { value, trackChanges, map }))
    {
        throw new <AppName>CoreDataException("There has been a problem getting the <entityName> with the specified <description>.", exc);
    }
}
```

**Rules:**
- First line always: `cancellationToken.ThrowIfCancellationRequested();`
- Validate string inputs immediately after with `Guard.IsNotNullOrWhiteSpace(param)`; use `Guard.IsNotNull(param)` for non-string reference types; no Guard call for value types
- Wrap every async query in `try/catch (Exception exc) when (Logger.WriteError(exc, new { ... }))` -- the catch block never executes, only the filter
- The anonymous object in `Logger.WriteError` should include the method's input parameters (omit `cancellationToken`)
- Re-throw as the layer-specific exception: `throw new <AppName>CoreDataException("...", exc);`
- Use `Items` as the query starting point -- this is a pre-filtered IQueryable from the base class
- Chain `.TrackChanges(trackChanges).IncludeMap(map)` on entity-returning methods; omit both on projection queries (e.g., `.Select(x => x.Name).ToListAsync(...)`)
- Use `Context.Value.Set<TOtherEntity>()` only when you genuinely need to query a different entity type

**Override methods (add only when the entity needs them):**

| Override | When to use |
|---|---|
| `SanitizeEntityAsync` | Normalize or compute derived fields before save (e.g., URL slugs, normalized lookup keys) |
| `ValidateEntityAsync` | Enforce uniqueness constraints or business rules beyond attribute validation |
| `BeforeContextSavingAsync` | Side effects just before EF SaveChanges |
| `BeforeContextDeletingAsync` | Side effects just before EF deletes the entity |
| `AfterContextSavedChangesAsync` | Post-save actions (e.g., queue background work, clear caches) |

Always call the base method first. For `ValidateEntityAsync`, add to the returned collection:

```csharp
protected override async Task SanitizeEntityAsync(<EntityName> entity, RepoOptions options, IEnumerable<RepoOptions>? childOptions, CancellationToken cancellationToken)
{
    await base.SanitizeEntityAsync(entity, options, childOptions, cancellationToken);
    entity.NameNormalized = _someService.Normalize(entity.Name);
}

protected override async Task<ICollection<ValidationResult>> ValidateEntityAsync(<EntityName> entity, RepoOptions options, IEnumerable<RepoOptions>? childOptions, CancellationToken cancellationToken)
{
    cancellationToken.ThrowIfCancellationRequested();
    var lstValidationResult = await base.ValidateEntityAsync(entity, options, childOptions, cancellationToken);

    if (await ExistsByNameAsync(entity.Name, entity.Id, cancellationToken))
        lstValidationResult.Add(new ValidationResult("The name must be unique.", new[] { nameof(entity.Name) }));

    return lstValidationResult;
}
```

Add `using System.ComponentModel.DataAnnotations;` to the implementation file if you override `ValidateEntityAsync`.

---

## Step 5 -- Register in DI

**File:** `Core\<AppName>.Core.Data\IServiceCollectionExtensions.cs`

Add one line in the `// Repositories` section of the `AddXxx(this IServiceCollection services)` method, in alphabetical order:

```csharp
_ = services.AddScoped<I<EntityName>Repository, <EntityName>Repository>();
```

---

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Verification

1. If an IncludeMap file was created, confirm it has `#nullable disable` and only references navigations that exist on the entity.
2. Confirm the interface inherits `IGenericDbRepository<<EntityName>>` with no extra `using` directives.
3. Confirm the implementation is `internal sealed`, the constructor passes exactly the 6 base params to `: base(...)`, and `using Umbrella.Utilities.Dating.Abstractions;` is present.
4. Confirm every query method starts with `cancellationToken.ThrowIfCancellationRequested()`, validates string params with Guard, and uses the try/catch pattern.
5. Confirm `_ = services.AddScoped<I<EntityName>Repository, <EntityName>Repository>();` is present in `IServiceCollectionExtensions.cs`.
