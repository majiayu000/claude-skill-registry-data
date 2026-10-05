---
name: umbrella-dotnet-scaffold-mapperly-factories
description: 'Scaffold Mapperly mapper classes that map between EF Core entities and API model records, or between client-side model types, following the Umbrella source-generated catalog pattern.'
---

# Scaffold Mapperly Factories

## Purpose

Create Mapperly mapper classes for either:

- **Server-side** (`Web.Server.ModelFactories`): entity ↔ API model (GET, POST, PUT endpoints).
- **Client-side** (`Web.Client.Data`): API model → update model (to populate the edit form) and update-result model → update model (to refresh the form after save without a full page reload).

Mappers plug into the `UmbrellaMapper` infrastructure via a **source-generated catalog**. The `Umbrella.Generators.Mapperly` package scans the assembly at compile time, discovers all mapper classes, and emits a `{AssemblyName}UmbrellaMapperlyCatalog` class. That catalog is then passed to `AddUmbrellaUtilitiesMappingMapperly` at startup. No per-mapper DI registration is needed.

## Discovery (read these before writing anything)

1. Read 2–3 existing mapper files in the target project (server: `Web.Server.ModelFactories\Mappings\Api\`; client: `Web.Client.Data\Mappings\Api\`) to understand naming conventions and how manual properties are handled.
2. Check the project `.csproj` for `Umbrella.Generators.Mapperly` and global usings for `Riok.Mapperly.Abstractions` and `Umbrella.Utilities.Mapping.Mapperly.Abstractions`.
3. Check the consuming project's `Program.cs` for `AddUmbrellaUtilitiesMappingMapperly(...)` to understand which catalog(s) are already registered.
4. Check the consuming project's `IServiceCollectionExtensions.cs` for `[assembly: UmbrellaMapperlyCatalogReference(...)]`.
5. Before choosing an asynchronous file-enrichment mapping, verify that the feature-specific file-handler interface, implementation, and DI registration already exist. If they do not, stop mapper generation and use `umbrella-dotnet-scaffold-file-handler` first; do not invent an unresolved handler reference or expand this mapping-only task into file infrastructure.

---

## How UmbrellaMapper discovers mappers

When you reference `Umbrella.Generators.Mapperly` in a project, the incremental source generator runs at compile time. It scans the assembly for non-abstract types implementing any of the six mapper interfaces and emits a catalog class:

- **Class name:** `{AssemblyName}UmbrellaMapperlyCatalog` — dots in the assembly name become underscores.
  - Example: `IndyRecords.Web.Server.ModelFactories` → `IndyRecords_Web_Server_ModelFactoriesUmbrellaMapperlyCatalog`
- **Namespace:** `Umbrella.Generated.Mapping.Mapperly`

The catalog exposes a `static Instance` property and implements `IUmbrellaMapperlyCatalog`. At startup, the consuming project registers it:

```csharp
builder.Services.AddUmbrellaUtilitiesMappingMapperly(
    Umbrella.Generated.Mapping.Mapperly.MyApp_Web_Server_ModelFactoriesUmbrellaMapperlyCatalog.Instance);
```

The Roslyn analyzer (`UMA001`/`UMA002`) validates `IUmbrellaMapper` call sites using the `[assembly: UmbrellaMapperlyCatalogReference(typeof(...))]` attribute on the consuming project — if a `MapAsync` call has no registered mapping, it emits an error at compile time.

**Consequence:** mapper classes can be public or internal, but must be accessible from the generated catalog. Keep them top-level (or otherwise accessibly nested), non-abstract, and `partial` when decorated with `[Mapper]`; UMA003 reports invalid declarations. When a mapper has no reason to be public, prefer `internal sealed partial class` so consumer CA1852 rules are satisfied. Do not emit a bare `internal partial class`; retain public accessibility only when it is part of the intended API.

---

## Interface reference

### Server-side (entity ↔ API model)

| Interface | Method signature | Use for |
|---|---|---|
| `IUmbrellaMapperlyNewInstanceMapper<TSource, TDest>` | `TDest Map(TSource source)` | Entity → model (GET single / POST/PUT result) |
| `IUmbrellaMapperlyNewCollectionMapper<TSource, TDest>` | `IReadOnlyCollection<TDest> MapAll(IEnumerable<TSource> source)` | Entity → model collection (GET list) |
| `IUmbrellaMapperlyExistingInstanceMapper<TSource, TDest>` | `void Map(TSource source, TDest destination)` | Request model → entity (PUT update) |
| `IUmbrellaMapperlyNewInstanceAsyncMapper<TSource, TDest>` | `ValueTask<TDest> MapAsync(TSource source, CancellationToken cancellationToken)` | New-instance mapping that requires asynchronous enrichment |
| `IUmbrellaMapperlyNewCollectionAsyncMapper<TSource, TDest>` | `ValueTask<IReadOnlyCollection<TDest>> MapAllAsync(IEnumerable<TSource> source, CancellationToken cancellationToken)` | Collection mapping that requires asynchronous enrichment |
| `IUmbrellaMapperlyExistingInstanceAsyncMapper<TSource, TDest>` | `ValueTask MapAsync(TSource source, TDest destination, CancellationToken cancellationToken)` | Existing-instance mapping that requires asynchronous enrichment |

### Client-side (model → model, in `Web.Client.Data`)

| Interface | Method signature | Use for |
|---|---|---|
| `IUmbrellaMapperlyNewInstanceMapper<ManageModel, UpdateModel>` | `UpdateModel Map(ManageModel source)` | Populate edit form from loaded `ManageModel` |
| `IUmbrellaMapperlyExistingInstanceMapper<UpdateResultModel, UpdateModel>` | `void Map(UpdateResultModel source, UpdateModel destination)` | Refresh edit form (e.g. concurrency stamp) after successful save — avoids full page reload |

A class can implement any combination of interfaces on the same source/destination pair. It cannot implement the same interface twice with different type arguments — use a separate class with a numbered suffix in that case.

**Choosing which mapper interfaces to implement**

Only create mappings for model types that exist. Skip any direction for which no corresponding model exists.

| Endpoint / model | Mapper interface to implement |
|---|---|
| GET single (`<Name>Model`) | `IUmbrellaMapperlyNewInstanceMapper<Entity, <Name>Model>` |
| GET list (`Slim<Name>Model`) | `IUmbrellaMapperlyNewCollectionMapper<Entity, Slim<Name>Model>` |
| POST request (`Create<Name>Model → Entity`) | `IUmbrellaMapperlyNewInstanceMapper<Create<Name>Model, Entity>` |
| POST result (`Entity → Create<Name>ResultModel`) | `IUmbrellaMapperlyNewInstanceMapper<Entity, Create<Name>ResultModel>` (separate class) |
| PUT request (`Update<Name>Model → Entity`) | `IUmbrellaMapperlyExistingInstanceMapper<Update<Name>Model, Entity>` |
| PUT result (`Entity → Update<Name>ResultModel`) | `IUmbrellaMapperlyNewInstanceMapper<Entity, Update<Name>ResultModel>` (separate class) |
| Edit form populate | `IUmbrellaMapperlyNewInstanceMapper<<Name>Model, Update<Name>Model>` (in Client.Data) |
| Edit form refresh after save | `IUmbrellaMapperlyExistingInstanceMapper<Update<Name>ResultModel, Update<Name>Model>` (in Client.Data) |

For any entity-to-model row above—including create and update result mappings—replace the synchronous interface with `IUmbrellaMapperlyNewInstanceAsyncMapper<TSource, TDest>` when the destination contains a file URL/version-token pair or another value requiring asynchronous enrichment. The file-handler preflight still applies. Do not leave image-bearing result mappings synchronous merely because the table shows their non-enriched default form.

---

## Step 1 -- Create the mapper file

### Server-side mapper

**File location:** `Web.Server.ModelFactories\Mappings\Api\<Feature>Mappers.cs`

**Minimal mapper (all properties auto-mapped):**

```csharp
using <AppName>.Core.Domain.Entities;
using <AppName>.Web.Shared.Models.Api.<Feature>;

namespace <AppName>.Web.Server.ModelFactories.Mappings.Api;

[Mapper]
public partial class <Name>Mapper :
    IUmbrellaMapperlyNewInstanceMapper<<Name>Entity, <Name>Model>,
    IUmbrellaMapperlyNewCollectionMapper<<Name>Entity, Slim<Name>Model>,
    IUmbrellaMapperlyNewInstanceMapper<Create<Name>Model, <Name>Entity>,
    IUmbrellaMapperlyExistingInstanceMapper<Update<Name>Model, <Name>Entity>
{
    public partial <Name>Model Map(<Name>Entity source);
    public partial IReadOnlyCollection<Slim<Name>Model> MapAll(IEnumerable<<Name>Entity> source);

    // Keep only the discovered repository-managed targets that exist on this entity.
    [MapperIgnoreTarget(nameof(<Name>Entity.Id))]
    [MapperIgnoreTarget(nameof(<Name>Entity.CreatedDateUtc))]
    [MapperIgnoreTarget(nameof(<Name>Entity.CreatedById))]
    [MapperIgnoreTarget(nameof(<Name>Entity.UpdatedDateUtc))]
    [MapperIgnoreTarget(nameof(<Name>Entity.UpdatedById))]
    [MapperIgnoreTarget(nameof(<Name>Entity.ConcurrencyStamp))]
    public partial <Name>Entity Map(Create<Name>Model source);

    [MapperIgnoreTarget(nameof(<Name>Entity.CreatedDateUtc))]
    [MapperIgnoreTarget(nameof(<Name>Entity.CreatedById))]
    [MapperIgnoreTarget(nameof(<Name>Entity.UpdatedDateUtc))]
    [MapperIgnoreTarget(nameof(<Name>Entity.UpdatedById))]
    public partial void Map(Update<Name>Model source, <Name>Entity destination);
}
```

Audit the actual entity hierarchy before keeping those ignore attributes. They document targets managed by the repository/controller lifecycle rather than the request mapper; remove any attribute for a member the entity does not declare, and add any equivalent application-owned lifecycle target. Do not accept RMG012 warnings as harmless.

For relationship inputs, allow Mapperly to map a scalar foreign-key property when the request model and entity expose the same member, and ignore the corresponding navigation property on the request-to-entity mapping. Do not resolve and assign the navigation solely to verify that the key exists. Prevalidate the related entity only when the endpoint contract deliberately promises a domain-specific `400` or `404`, or when a domain rule cannot be enforced by the persistence constraint.

Do not make an update result image-bearing merely because the update changes an image foreign key. Preserve the discovered API contract: command results normally carry only values the client must refresh immediately, such as a concurrency stamp, while read-only URL, version-token, alt-text, and navigation-derived values belong on the read model. Add asynchronous result enrichment only when the client explicitly requires those values in the update response.

**Mapper with properties needing asynchronous manual values (for example versioned file URLs):**

This form requires an existing feature file handler. Complete the discovery preflight above before emitting it.

```csharp
using <AppName>.Core.Domain.Entities;
using <AppName>.Core.Logic.FileSystem.Abstractions;
using <AppName>.Web.Shared.Models.Api.<Feature>;

namespace <AppName>.Web.Server.ModelFactories.Mappings.Api;

[Mapper]
public partial class <Name>Mapper :
    IUmbrellaMapperlyNewInstanceAsyncMapper<<Name>Entity, <Name>Model>,
    IUmbrellaMapperlyNewCollectionAsyncMapper<<Name>Entity, Slim<Name>Model>
{
    private readonly ILogger<<Name>Mapper> _logger;
    private readonly I<Name>FileHandler _fileHandler;

    public <Name>Mapper(ILogger<<Name>Mapper> logger, I<Name>FileHandler fileHandler)
    {
        _logger = logger;
        _fileHandler = fileHandler;
    }

    public async ValueTask<<Name>Model> MapAsync(<Name>Entity source, CancellationToken cancellationToken)
    {
        cancellationToken.ThrowIfCancellationRequested();
        Guard.IsNotNull(source);

        try
        {
            var model = MapInternal(source);
            UmbrellaVersionedUrl? image = await _fileHandler
                .GetVersionedWebFilePathAsync(source.Id, source.ImageProviderFileName, cancellationToken)
                .ConfigureAwait(false);

            model.ImageUrl = image?.Url;
            model.ImageVersionToken = image?.VersionToken;

            return model;
        }
        catch (Exception exc) when (_logger.WriteError(exc, new { source.Id, source.ImageProviderFileName }))
        {
            throw;
        }
    }

    [MapperIgnoreTarget(nameof(<Name>Model.ImageUrl))]
    [MapperIgnoreTarget(nameof(<Name>Model.ImageVersionToken))]
    private partial <Name>Model MapInternal(<Name>Entity source);

    public async ValueTask<IReadOnlyCollection<Slim<Name>Model>> MapAllAsync(
        IEnumerable<<Name>Entity> source,
        CancellationToken cancellationToken)
    {
        cancellationToken.ThrowIfCancellationRequested();
        Guard.IsNotNull(source);

        try
        {
			<Name>Entity[] entities = [.. source];
			Slim<Name>Model[] models = [.. entities.Select(MapSlimInternal)];
			Task<UmbrellaVersionedUrl?>[] imageTasks =
			[
				.. entities.Select(entity => _fileHandler.GetVersionedWebFilePathAsync(
					entity.Id,
					entity.ImageProviderFileName,
					cancellationToken))
			];
			UmbrellaVersionedUrl?[] images = await Task.WhenAll(imageTasks).ConfigureAwait(false);

			for (int index = 0; index < models.Length; index++)
			{
				models[index].ImageUrl = images[index]?.Url;
				models[index].ImageVersionToken = images[index]?.VersionToken;
			}

            return models;
        }
        catch (Exception exc) when (_logger.WriteError(exc, new { source }))
        {
            throw;
        }
    }

    [MapperIgnoreTarget(nameof(Slim<Name>Model.ImageUrl))]
    [MapperIgnoreTarget(nameof(Slim<Name>Model.ImageVersionToken))]
    private partial Slim<Name>Model MapSlimInternal(<Name>Entity source);
}
```

Use the async mapper interfaces whenever enrichment performs I/O. Assign each Dynamic Image URL and matching version token in the same flow. For collection wrappers, map each element through an attributed single-item partial method; Mapperly method-level ignore attributes on a collection-returning method do not suppress unmapped targets on its element mapping. Resolve independent lookups concurrently only for bounded materialized collections, such as one paginated result, and preserve entity/model ordering; do not start unbounded work over arbitrary streams. Authored public mapper bodies activate UA008/UA016, so inject an `ILogger`, put guards/cancellation before the outer `try`, and log meaningful state. Pure bodyless partial mappings need neither a logger nor a wrapper.

**Multiple mapper classes (when the same interface can't be implemented twice):**

```csharp
[Mapper]
public partial class <Name>Mapper2 : IUmbrellaMapperlyNewInstanceMapper<<Name>Entity, Create<Name>ResultModel>
{
    public partial Create<Name>ResultModel Map(<Name>Entity source);
}

[Mapper]
public partial class <Name>Mapper3 : IUmbrellaMapperlyNewInstanceMapper<<Name>Entity, Update<Name>ResultModel>
{
    public partial Update<Name>ResultModel Map(<Name>Entity source);
}
```

### Client-side mapper (in `Web.Client.Data\Mappings\Api\`)

```csharp
using <AppName>.Web.Shared.Models.Api.<Feature>;

namespace <AppName>.Web.Client.Data.Mappings.Api;

[Mapper]
public partial class <Name>Mapper :
    IUmbrellaMapperlyNewInstanceMapper<<Name>Model, Update<Name>Model>,
    IUmbrellaMapperlyExistingInstanceMapper<Update<Name>ResultModel, Update<Name>Model>
{
    public partial Update<Name>Model Map(<Name>Model source);
    public partial void Map(Update<Name>ResultModel source, Update<Name>Model destination);
}
```

The first interface populates the edit form when loading an existing record. The second refreshes the form (especially `ConcurrencyStamp`) after a successful save, without a full page reload.

---

## Step 2 -- Verify source generator package in the mapper project

Open the `.csproj` for the mapper project and confirm:

```xml
<ItemGroup>
  <PackageReference Include="Umbrella.Generators.Mapperly" Version="..." />
  <PackageReference Include="Umbrella.Utilities.Mapping.Mapperly" Version="..." />
</ItemGroup>
<ItemGroup>
  <Using Include="Riok.Mapperly.Abstractions" />
  <Using Include="Umbrella.Utilities.Mapping.Mapperly.Abstractions" />
</ItemGroup>
```

If `Umbrella.Generators.Mapperly` is missing, add it (match the version of `Umbrella.Utilities.Mapping.Mapperly`). The generator emits the catalog class — without it, nothing is discovered.

---

## Step 3 -- Register the catalog in the consuming project's Program.cs

The consuming project (Web Server or Web Client) must pass the generated catalog instance to `AddUmbrellaUtilitiesMappingMapperly`. The generated class lives in namespace `Umbrella.Generated.Mapping.Mapperly` and its name is the assembly name with dots replaced by underscores, suffixed with `UmbrellaMapperlyCatalog`.

```csharp
// Web Server Program.cs — server-side catalog from ModelFactories assembly
builder.Services.AddUmbrellaUtilitiesMappingMapperly(
    Umbrella.Generated.Mapping.Mapperly.<AppName>_Web_Server_ModelFactoriesUmbrellaMapperlyCatalog.Instance);

// Web Client Program.cs — client-side catalog from Client.Data assembly
builder.Services.AddUmbrellaUtilitiesMappingMapperly(
    Umbrella.Generated.Mapping.Mapperly.<AppName>_Web_Client_DataUmbrellaMapperlyCatalog.Instance);
```

If both catalogs are already registered (i.e. you are adding mappers to an existing assembly), no change is needed here.

---

## Step 4 -- Add the assembly attribute for the Roslyn analyzer

The consuming project's `IServiceCollectionExtensions.cs` must carry a `[assembly: UmbrellaMapperlyCatalogReference(typeof(...))]` attribute pointing to its generated catalog. This is what enables the UMA001/UMA002 diagnostic rules to validate `IUmbrellaMapper` call sites at compile time.

```csharp
// In Web.Server/IServiceCollectionExtensions.cs
using Umbrella.Utilities.Mapping.Mapperly.Abstractions;

[assembly: UmbrellaMapperlyCatalogReference(typeof(Umbrella.Generated.Mapping.Mapperly.<AppName>_Web_Server_ModelFactoriesUmbrellaMapperlyCatalog))]

namespace <AppName>.Web.Server;

public static class IServiceCollectionExtensions { ... }
```

```csharp
// In Web.Client/IServiceCollectionExtensions.cs
using Umbrella.Utilities.Mapping.Mapperly.Abstractions;

[assembly: UmbrellaMapperlyCatalogReference(typeof(Umbrella.Generated.Mapping.Mapperly.<AppName>_Web_Client_DataUmbrellaMapperlyCatalog))]

namespace <AppName>.Web.Client;

public static class IServiceCollectionExtensions { ... }
```

**Important:** the attribute lives in the consuming project (the one calling `AddUmbrellaUtilitiesMappingMapperly`), not in the mapper project itself. Web client and web server have separate catalogs and separate assembly attributes.

Note: the source generator also auto-emits a `[assembly: UmbrellaMapperlyCatalogReference]` attribute in the mapper project itself (pointing back to its own catalog). This is separate from — and in addition to — the manually-added attribute in the consuming project. When grepping for `UmbrellaMapperlyCatalogReference` you will see two occurrences per catalog: one in the generated `.g.cs` file in the mapper project, and one in the consuming project's `IServiceCollectionExtensions.cs`. The consuming-project attribute is the one the analyzer uses to validate call sites there.

If the attribute is already present in the consuming project, no change is needed — the analyzer will automatically pick up any new mappers that the source generator adds to the catalog.

---

## Rules

- Use an accessible `partial class`; top-level `public` and `internal` mapper types are supported. Follow the target project's visibility convention.
- `[Mapper]` attribute on the class triggers Mapperly source generation for `partial` methods.
- `partial` methods with no body are auto-implemented by Mapperly. Methods with a body are manual overrides.
- `[MapperIgnoreTarget(nameof(Prop))]` goes on the private `partial` method (the one Mapperly implements), not on the class.
- When you write a public wrapper that calls a private `partial` method, add cancellation/argument validation before its outer `try`, inject an `ILogger`, and apply state-aware exception logging. Prefer an async mapper interface when the wrapper performs I/O.
- All mapper classes for one feature go in one file named `<Feature>Mappers.cs`.
- No per-mapper DI registration is needed — the generated catalog handles all registrations.
- The generated catalog class name is `{AssemblyName_Dots_Replaced_By_Underscores}UmbrellaMapperlyCatalog` in namespace `Umbrella.Generated.Mapping.Mapperly`.

---

## Verification

1. All `[Mapper]` classes are accessible `partial` classes; public and internal top-level types are valid.
2. Every `partial` method either has no body (Mapperly generates it) or has a body for manual post-mapping logic.
3. `[MapperIgnoreTarget(nameof(Prop))]` is placed on the private `partial` method.
4. Authored public wrapper methods validate before the outer `try`, have logger access, log useful state, and use async interfaces for asynchronous enrichment.
5. The mapper project has `Umbrella.Generators.Mapperly` in its `.csproj` with global usings for `Riok.Mapperly.Abstractions` and `Umbrella.Utilities.Mapping.Mapperly.Abstractions`.
6. The consuming project's `Program.cs` passes the generated catalog to `AddUmbrellaUtilitiesMappingMapperly(...)`.
7. The consuming project's `IServiceCollectionExtensions.cs` has `[assembly: UmbrellaMapperlyCatalogReference(typeof(...))]` pointing to the generated catalog.
8. Web client and web server have separate catalogs — each registered and attributed independently.
9. Read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build with UA/UMA/UWDI analyzers enabled where applicable.
10. Async file-enrichment mappers reference an existing, DI-registered feature file handler; a missing handler is routed to `umbrella-dotnet-scaffold-file-handler` before mapper work begins.
