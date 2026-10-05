---
name: umbrella-dotnet-migrate-automapper-to-mapperly
description: 'Migrate AutoMapper Profile classes to Mapperly source-generated mappers, following the Umbrella catalog pattern. Covers ForMember translation, AfterMap, Ignore, flattening detection, DI rewiring, and AutoMapper removal.'
---

# Migrate AutoMapper to Mapperly

## Purpose

Replace AutoMapper `Profile` classes with Mapperly source-generated mapper classes, wired into the `UmbrellaMapper` catalog infrastructure. The end state is identical to what `umbrella-dotnet-scaffold-mapperly-factories` would produce from scratch — read that skill for the target file shape, interface reference, catalog naming, and assembly-attribute requirements. This skill covers only the *migration diff*: translating AutoMapper patterns to their Mapperly equivalents, rewiring DI, and removing all AutoMapper artefacts.

---

## Discovery (read these before writing anything)

1. List all files inheriting `AutoMapper.Profile` across the solution. They may be in a dedicated `Mappings/` folder or scattered.
2. For each `CreateMap<TSource, TDest>()` pair, note all customisations: `ForMember`, `AfterMap`, `ReverseMap`, `.ForAllMembers`.
3. Find every `IMapper` and `IUmbrellaMapper` injection site — constructors, field declarations, and service-scope lookups.
4. Find the `AddAutoMapper(...)` call in the mapper project's `IServiceCollectionExtensions.cs`.
5. Find `AddUmbrellaUtilitiesMappingAutoMapper()` and/or `AddUmbrellaUtilitiesMappingMapperly(...)` in the consuming project's `Program.cs`. If `AddUmbrellaUtilitiesMappingMapperly` is already present, note it — you must extend that single call, not add a second one (see Step 4).

---

## Pre-flight: convention-based flattening

AutoMapper auto-flattens by naming convention: a destination property `CustomerName` is silently populated from `source.Customer.Name` even with no `ForMember`. Mapperly does not do this.

For every `CreateMap<TSource, TDest>()` that has no `ForMember` covering a given destination property, compare property names between source and destination. If a destination property has no direct name match on the source, check whether it could be a flattened path (e.g., `CustomerName` → `Customer.Name`). If so, add `[MapProperty(new[] { "Customer", "Name" }, "CustomerName")]` to the `partial` method, or use a manual wrapper. Do not leave it silent — Mapperly will produce `default(T)` for unmatched properties.

---

## AutoMapper → Mapperly conversion reference

### Interface selection

See `umbrella-dotnet-scaffold-mapperly-factories` for the full interface table. Quick reference:

| AutoMapper intent | Mapperly interface |
|---|---|
| `CreateMap<S,D>()` — returns new instance | `IUmbrellaMapperlyNewInstanceMapper<S, D>` |
| `CreateMap<S,D>()` — maps a collection | `IUmbrellaMapperlyNewCollectionMapper<S, D>` |
| `CreateMap<S,D>()` — updates an existing object (`_mapper.Map(src, existing)`) | `IUmbrellaMapperlyExistingInstanceMapper<S, D>` |
| Same interface twice on one class | Split into `<Name>Mapper2`, `<Name>Mapper3` in the same file |

`ReverseMap()` has no Mapperly equivalent. Create explicit interfaces or classes for each direction. For reverse unflattening into a required nested target, do not assume `[MapProperty]` can construct and satisfy that nested object: use a guarded manual wrapper when generated mapping reports required-member or nested-target diagnostics.

### ForMember patterns

**Property rename:**
```csharp
// AutoMapper
.ForMember(d => d.UserName, o => o.MapFrom(s => s.Email));

// Mapperly
[MapProperty(nameof(Source.Email), nameof(Dest.UserName))]
public partial Dest Map(Source source);
```

**Ignore a destination property:**
```csharp
// AutoMapper
.ForMember(d => d.Children, o => o.Ignore());

// Mapperly — attribute on the partial method
[MapperIgnoreTarget(nameof(Dest.Children))]
public partial Dest Map(Source source);

// For ExistingInstance:
[MapperIgnoreTarget(nameof(Dest.Children))]
public partial void Map(Source source, Dest destination);
```

**Computed value (non-trivial lambda expression):**

A direct member-access rename such as `s => s.Email` follows the `[MapProperty]` rule above. Other `MapFrom` expressions—arithmetic, method calls, conditionals, concatenation, or lambdas that use the destination—have no direct Mapperly attribute equivalent; write a manual public wrapper plus private `MapInternal`.

An authored public mapper body activates UA008/UA016. Inject `ILogger<TMapper>` into that mapper and retain it in `_logger`; the examples below include the required outer logging shape. Bodyless partial mappings do not require a logger:

```csharp
// AutoMapper
.ForMember(d => d.Initials, o => o.MapFrom(
    (src, dest) => (src.FirstName[0].ToString() + src.LastName[0].ToString()).ToUpperInvariant()
));

// Mapperly
public Dest Map(Source source)
{
    Guard.IsNotNull(source);

    try
    {
        var model = MapInternal(source);
        // record type — use with:
        model = model with { Initials = (source.FirstName[0].ToString() + source.LastName[0].ToString()).ToUpperInvariant() };
        // class type — assign directly:
        // model.Initials = ...;
        return model;
    }
    catch (Exception exc) when (_logger.WriteError(exc, new { source.FirstName, source.LastName }))
    {
        throw;
    }
}

[MapperIgnoreTarget(nameof(Dest.Initials))]
private partial Dest MapInternal(Source source);
```

Check whether the destination type is a `record` (use `with`) or a `class` (assign directly) by reading the model file.

When multiple destination properties require computed values, list all `[MapperIgnoreTarget]` attributes on the private method and compute all of them in the public wrapper body.

**Custom transform helper on the Profile class:**

Some profiles define a `static` or `protected static` helper method used inside a `MapFrom`. Move that method to the mapper class:

```csharp
// AutoMapper profile
protected static int TransformTimeType(InterruptionTimeType t) => t switch { ... };
.ForMember(d => d.TimeFrameType, o => o.MapFrom(src => TransformTimeType(src.TimeType)));

// Mapperly
private static int TransformTimeType(InterruptionTimeType t) => t switch { ... };

public Dest Map(Source source)
{
    Guard.IsNotNull(source);

    try
    {
        var model = MapInternal(source);
        model = model with { TimeFrameType = TransformTimeType(source.TimeType) };
        return model;
    }
    catch (Exception exc) when (_logger.WriteError(exc, new { source.TimeType }))
    {
        throw;
    }
}

[MapperIgnoreTarget(nameof(Dest.TimeFrameType))]
private partial Dest MapInternal(Source source);
```

### AfterMap patterns

**AfterMap (destination side — new instance):**
```csharp
// AutoMapper
.AfterMap((src, dest) =>
{
    var days = src.Days.OrderBy(x => x.Date).ToArray();
    dest.StartDate = days.First().Date;
    dest.EndDate   = days.Last().Date;
});

// Mapperly
public Dest Map(Source source)
{
    Guard.IsNotNull(source);

    try
    {
        var model = MapInternal(source);
        var days = source.Days.OrderBy(x => x.Date).ToArray();
        model = model with { StartDate = days.First().Date, EndDate = days.Last().Date };
        return model;
    }
    catch (Exception exc) when (_logger.WriteError(exc, new { source.Days }))
    {
        throw;
    }
}

[MapperIgnoreTarget(nameof(Dest.StartDate))]
[MapperIgnoreTarget(nameof(Dest.EndDate))]
private partial Dest MapInternal(Source source);
```

**AfterMap on ExistingInstance (void mapping):**
```csharp
// AutoMapper
.AfterMap((src, dest) => dest.HasItems = src.Items?.Any() ?? false);

// Mapperly
public void Map(Source source, Dest destination)
{
    Guard.IsNotNull(source);
    Guard.IsNotNull(destination);

    try
    {
        MapInternal(source, destination);
        destination.HasItems = source.Items?.Any() ?? false;
    }
    catch (Exception exc) when (_logger.WriteError(exc, new { source.Items }))
    {
        throw;
    }
}

[MapperIgnoreTarget(nameof(Dest.HasItems))]
private partial void MapInternal(Source source, Dest destination);
```

**AfterMap that modifies the SOURCE object (side-effect pattern):**

If the original `AfterMap` sets a property on the *source* object (first parameter) rather than the destination, do not silently replicate or silently drop it. Flag it:

```
// MIGRATION NOTE: original AfterMap modified the source object — confirm with the developer
// whether (a) this should set a property on the destination, or (b) it can be dropped.
```

---

## Step 1 — Create mapper files

Group related AutoMapper profiles by entity/feature and write one `<Feature>Mappers.cs` file per group, following `umbrella-dotnet-scaffold-mapperly-factories` for file location and naming. Apply the conversion reference above for each `CreateMap` pair.

All rules from `umbrella-dotnet-scaffold-mapperly-factories` apply to generated mappings: use an accessible `partial class`, preferring `internal sealed partial class` when the mapper is not an intentional public API; put `[Mapper]` on each class that contains Mapperly-generated partial methods; place `[MapperIgnoreTarget]` on the specific public or private partial mapping method whose target owns the ignored member; and apply validation plus state-aware logging to every public wrapper with a body. A fully manual Umbrella mapper-interface implementation with no generated partial methods does not need `[Mapper]` or `partial`. Use the async mapper interfaces when migrated enrichment performs I/O.

---

## Step 2 — Update the mapper project .csproj

Remove AutoMapper:
```xml
<!-- Remove -->
<PackageReference Include="AutoMapper" Version="..." />
<PackageReference Include="AutoMapper.Extensions.Microsoft.DependencyInjection" Version="..." />
<PackageReference Include="Umbrella.Utilities.Mapping.AutoMapper" Version="..." />
```

Add Mapperly (match the version already in the solution — check a sibling project or `Directory.Packages.props`):
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

---

## Step 3 — Simplify the mapper project's IServiceCollectionExtensions

Remove the `AddAutoMapper(assemblies)` call. The source-generated catalog replaces assembly scanning — no per-mapper registration is needed. Delete the extension method if its only purpose was `AddAutoMapper`; otherwise keep it and remove only that line.

---

## Step 4 — Update Program.cs in the consuming project

Replace `AddUmbrellaUtilitiesMappingAutoMapper()` with `AddUmbrellaUtilitiesMappingMapperly(...)`.

**Critical:** `AddUmbrellaUtilitiesMappingMapperly` uses `ReplaceSingleton` internally. Calling it twice means the second call overwrites the first catalog. All catalogs must be in a single call:

```csharp
// No existing Mapperly catalog:
builder.Services.AddUmbrellaUtilitiesMappingMapperly(
    Umbrella.Generated.Mapping.Mapperly.<AppName>_Web_Server_ModelFactoriesUmbrellaMapperlyCatalog.Instance);

// Existing catalog already present — extend it, don't add a second call:
builder.Services.AddUmbrellaUtilitiesMappingMapperly(
    Umbrella.Generated.Mapping.Mapperly.<AppName>_BlazorComponentsUmbrellaMapperlyCatalog.Instance,
    Umbrella.Generated.Mapping.Mapperly.<AppName>_Web_Server_ModelFactoriesUmbrellaMapperlyCatalog.Instance);
```

Note: duplicate `(TSource, TDest)` mappings across catalogs throw `InvalidOperationException` at startup. If any type pair overlaps between an existing catalog and the new one, resolve the duplication before merging.

Remove the call to the mapper project's extension method (e.g. `AddHawcroftModelFactories()`) if it now only contained `AddAutoMapper`.

---

## Step 5 — Add the assembly attribute

Follow `umbrella-dotnet-scaffold-mapperly-factories` Step 4. The `[assembly: UmbrellaMapperlyCatalogReference(typeof(...))]` attribute goes in every assembly that directly calls `IUmbrellaMapper`, including test or secondary consumer projects; referencing it only from the primary app does not satisfy UMA validation in another compilation.

---

## Step 6 — Update IMapper injection sites

If the project injects `IMapper` directly (not through `IUmbrellaMapper`), update every constructor parameter and field:

```csharp
// Before
private readonly IMapper _mapper;
// After
private readonly IUmbrellaMapper _mapper;
```

Update service-scope lookups too:
```csharp
// Before
IMapper mapper = serviceScope.ServiceProvider.GetRequiredService<IMapper>();
// After
IUmbrellaMapper mapper = serviceScope.ServiceProvider.GetRequiredService<IUmbrellaMapper>();
```

If the project already uses `IUmbrellaMapper` throughout (e.g. via Umbrella base controllers), no changes are needed at injection sites.

---

## Step 7 — Delete AutoMapper artefacts

1. Delete all `Profile` class files. Preserve a pre-existing application extension method when it remains an intentional hook after `AddAutoMapper` is removed; delete only infrastructure that truly became unused because of the migration.
2. Remove `AutoMapper`, `AutoMapper.Extensions.Microsoft.DependencyInjection`, and `Umbrella.Utilities.Mapping.AutoMapper` NuGet references from every project file.
3. Remove any `using AutoMapper;` directives that are no longer needed.

---

## Rules

- Read `umbrella-dotnet-scaffold-mapperly-factories` before writing any mapper files — all its rules apply here.
- `[MapperIgnoreTarget]` goes on the private `partial` method, never on the public method or the class.
- A direct member-access `MapFrom` rename becomes `[MapProperty]`; other expression bodies (arithmetic, method calls, conditionals, extension methods) become manual wrappers.
- `ReverseMap()` has no Mapperly equivalent — each direction needs its own interface or class.
- All catalogs must be in a single `AddUmbrellaUtilitiesMappingMapperly(...)` call — never add a second call.
- Do not replicate a side-effect `AfterMap` (one modifying the source object) without a developer decision.

---

## Verification

1. `dotnet build` produces no mapping-related errors.
2. No `Profile` class files remain.
3. No `AutoMapper`, `AutoMapper.Extensions.Microsoft.DependencyInjection`, or `Umbrella.Utilities.Mapping.AutoMapper` package references remain in any `.csproj`.
4. No `IMapper` injections remain — all sites use `IUmbrellaMapper`.
5. All classes containing generated partial mappings are accessible `[Mapper]` partial types; fully manual mapper-interface implementations need neither marker.
6. `[MapperIgnoreTarget]` is on the private `MapInternal` partial method only.
7. Authored public wrapper methods validate before the outer `try`, have logger access, and use state-aware exception logging; bodyless partial declarations remain logger-free.
8. `Program.cs` has a single `AddUmbrellaUtilitiesMappingMapperly(...)` call containing all catalogs.
9. The consuming project's `IServiceCollectionExtensions.cs` has `[assembly: UmbrellaMapperlyCatalogReference(typeof(...))]`.
10. Asynchronous enrichment uses the corresponding async mapper interface and propagates its cancellation token.
11. Read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build with UA/UMA/UWDI analyzers enabled where applicable.
12. Every direct `IUmbrellaMapper` consumer assembly, including tests, references the generated catalog needed for its mappings.
