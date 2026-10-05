---
name: umbrella-dotnet-scaffold-ef-entity
description: 'Scaffold a new EF Core entity: entity class in Core.Domain, configuration method in DbContext. Follows Umbrella patterns and is front-end agnostic.'
---

# Scaffold Entity

## Purpose

Create a new EF Core entity class and register it in the DbContext, following the exact patterns used in the target repository.

## Discovery (read these before writing anything)

1. List the files in `Core\<AppName>.Core.Domain\Entities\` to understand the naming and folder conventions.
2. Read 2-3 existing entity files that are similar in complexity to the one being created.
3. Read the DbContext file (`Core\<AppName>.Core.Data\<AppName>DbContext.cs`) -- specifically `OnModelCreating` and the existing `Add*` private static methods -- to understand registration order and configuration patterns.
4. Read the Domain project `.csproj` to identify available string-length attributes and which Umbrella packages are referenced.

---

## Step 1 -- Create the entity class

**File location:** `Core\<AppName>.Core.Domain\Entities\<EntityName>.cs`

**Rules:**
- Namespace: `namespace <AppName>.Core.Domain.Entities;`
- Declare as `public partial class` -- always `partial`, never omit this (required for Umbrella source generation: EF Core interceptors and audit infrastructure)
- Always include `public int Id { get; set; }` as the primary key
- Choose the correct audit interfaces (see Interface Reference below)
- String properties: always annotate with `[ShortStringLength]`, `[MediumStringLength]`, or `[LongStringLength]` from `<AppName>.Shared.Common.Attributes`
- Required string properties: use `= null!` null-forgiving operator (`public string Name { get; set; } = null!;`)
- Optional string properties: use nullable type (`public string? Description { get; set; }`)
- Foreign keys: non-nullable `int` for required FK (`public int CareerId { get; set; }`), nullable `int?` for optional FK
- Navigation properties: always nullable (`public Career? Career { get; set; }`)
- Collection navigation properties: `List<T>?` with nullable annotation (`public List<CareerDetail>? Details { get; set; }`)
- DateTime properties: `DateTime` (UTC, never local); optional DateTime uses `DateTime?`
- Enum properties: use the strongly-typed enum type from `<AppName>.Shared.Common.Enumerations`
- `using` directives: add only what is needed; check existing entities of the same kind for the exact imports

**Minimal example (ICreatedDateAuditEntity):**
```csharp
using <AppName>.Shared.Common.Attributes;
using Umbrella.DataAccess.Abstractions;

namespace <AppName>.Core.Domain.Entities;

public partial class <EntityName> : IEntity<int>, ICreatedDateAuditEntity
{
    public int Id { get; set; }
    public DateTime CreatedDateUtc { get; set; }

    [ShortStringLength]
    public string Name { get; set; } = null!;
}
```

---

## Step 2 -- Register in the DbContext

**File:** `Core\<AppName>.Core.Data\<AppName>DbContext.cs`

**Changes required:**

1. Add a call to `Add<EntityName>(builder);` inside `OnModelCreating`, grouped with logically related entities and in alphabetical order within that group.
2. Add a new private static method at the bottom of the method block, following the same expression-body style as existing methods:

```csharp
private static void Add<EntityName>(ModelBuilder builder)
    => builder.Entity<<EntityName>>(builder =>
    {
        // configuration here -- see Step 3
    });
```

**Do NOT add a `DbSet<T>` property.** The base `UmbrellaIdentityDbContext` exposes entity sets without explicit `DbSet` declarations.

---

## Step 3 -- Write the configuration method

Choose the correct setup calls based on which interfaces the entity implements. Always assign discards (`_ =`) for every builder call.

### Primary key

Use `SetupNonClusteredPrimaryKey()` when a clustered index will be placed on a FK column (which is the common case). Omit it only when the primary key itself should be the clustered index (rare).

```csharp
_ = builder.SetupNonClusteredPrimaryKey();
```

### Audit properties

Call each method that corresponds to an interface the entity implements. Always use discards.

| Entity implements | Configuration call |
|---|---|
| `ICreatedDateAuditEntity` | `_ = builder.SetupCreatedDateUtcAuditProperty();` |
| `IUpdatedDateAuditEntity` | `_ = builder.SetupUpdatedDateUtcAuditProperty();` |
| `ICreatedUserAuditEntity<int>` | `_ = builder.SetupCreatedByIdAuditProperty<<EntityName>, AppUser, int>();` |
| `IUpdatedUserAuditEntity<int>` | `_ = builder.SetupUpdatedByIdAuditProperty<<EntityName>, AppUser, int>();` |
| `IConcurrencyStamp` | `_ = builder.SetupConcurrencyToken();` |

When the entity implements all four audit interfaces (i.e. `IAuditEntity<int, int>` or the equivalent combination of `ICreatedDateAuditEntity` + `IUpdatedDateAuditEntity` + `ICreatedUserAuditEntity<int>` + `IUpdatedUserAuditEntity<int>`), replace the four individual date/user calls with the single combined helper:

```csharp
_ = builder.SetupAuditProperties<<EntityName>, AppUser, int>();
```

### Optional DateTime properties

```csharp
_ = builder.Property(x => x.ReadDateUtc).EnsureUtc();
```

### Relationships

```csharp
// Required FK -> Cascade
_ = builder.HasOne(x => x.Career!).WithMany().HasForeignKey(x => x.CareerId).OnDelete(DeleteBehavior.Cascade);

// Required FK -> Restrict (use when the parent should not be deleted while children exist)
_ = builder.HasOne(x => x.Sender!).WithMany().HasForeignKey(x => x.SenderId).OnDelete(DeleteBehavior.Restrict);

// Optional FK -> SetNull
_ = builder.HasOne(x => x.Category!).WithMany().HasForeignKey(x => x.CategoryId).OnDelete(DeleteBehavior.SetNull);
```

### Owned collections (JSON storage)

```csharp
_ = builder.OwnsMany(x => x.Sections, x => x.ToJson());
```

### Indexes

Always add an index on every FK column. Choose clustered carefully -- each table can have only one clustered index.

```csharp
// Clustered on a single FK (most common for child entities)
_ = builder.HasIndex(x => x.ParentId).IsClustered();

// Clustered composite (use when entity is always queried by both FKs together)
_ = builder.HasIndex(x => new { x.UserId, x.CareerId }).IsClustered();

// Unique clustered composite
_ = builder.HasIndex(x => new { x.UserId, x.CareerId }).IsClustered().IsUnique();

// Filtered index for nullable FK
_ = builder.HasIndex(x => x.OptionalParentId)
    .HasFilter("[OptionalParentId] IS NOT NULL")
    .HasDatabaseName("IX_<EntityName>_OptionalParent");

// Unique non-clustered
_ = builder.HasIndex(x => x.Name).IsUnique();
```

---

## Interface reference

| Interface | Properties required | Use when |
|---|---|---|
| `IEntity<int>` | `Id` | All entities -- always include this |
| `ICreatedDateAuditEntity` | `CreatedDateUtc` | Track when the entity was created |
| `IUpdatedDateAuditEntity` | `UpdatedDateUtc` | Track when the entity was last updated |
| `ICreatedUserAuditEntity<int>` | `CreatedById` | Track which user created the entity |
| `IUpdatedUserAuditEntity<int>` | `UpdatedById` | Track which user last updated the entity |
| `IAuditEntity<int, int>` | `Id` + all four above | Shorthand combining `IEntity` + all four date and user audit interfaces |
| `IConcurrencyStamp` | `ConcurrencyStamp` | Entity is mutable and requires optimistic concurrency control |
| `IAppTenantEntity` | `AppTenantId` | Entity belongs to a specific application tenant (multi-tenant scenarios) |

**Common combinations:**

| Pattern | Interfaces |
|---|---|
| Append-only log/event | `IEntity<int>` + `ICreatedDateAuditEntity` |
| Append-only with user | `IEntity<int>` + `ICreatedDateAuditEntity` + `ICreatedUserAuditEntity<int>` |
| Mutable, date audit only | `IEntity<int>` + `ICreatedDateAuditEntity` + `IUpdatedDateAuditEntity` + `IConcurrencyStamp` |
| Full audit | `IAuditEntity<int, int>` + `IConcurrencyStamp` |

`IAuditEntity<int, int>` is a composite -- do not also add the individual date/user interfaces alongside it, as they are already included.

---

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Verification

After writing the files:

1. Check the entity class compiles -- look for missing `using` directives by comparing with a similar existing entity.
2. Check `OnModelCreating` -- confirm the new `Add<EntityName>(builder)` call is present and the private static method exists.
3. Confirm no `DbSet<T>` property was added.
4. Confirm every string property has a length attribute.
5. Confirm every navigation property is nullable.
6. Confirm every FK column has an index in the configuration method.
