---
name: umbrella-dotnet-scaffold-api-server-models
description: 'Scaffold sealed API model records (request/response types) for a new feature, following the Umbrella shared-model, input-binding, immutability, and concurrency contracts.'
---

# Scaffold API Server Models

## Purpose

Create the API model records for a new feature — the request and response types used by API endpoints. These models are typically kept in a shared project (accessible by both server and client) and use C# records with data-annotation validation attributes.

This skill covers the model types only. For mapping entities to models using Mapperly, use the `umbrella-dotnet-scaffold-mapperly-factories` skill.

## Discovery (read these before writing anything)

1. Read 2-3 existing feature model folders in the shared models directory (e.g., `Web.Shared\Models\Api\`) to understand the naming conventions, which model types are used, and whether base class hierarchies are common.
2. Note whether the project uses `required` properties, `init` vs `set`, `abstract record` base types, and which validation attributes are standard (e.g., `[Required]`, `[ShortStringLength]`). Prefer the nearest established feature hierarchy over inventing an interface-based alternative.
3. Check whether the project has a constants file pattern per feature (e.g., `<Feature>Constants.cs`) for error message strings used in validation attributes.
4. Determine the friendly singular entity name used by grids and dialogs. The slim list record must declare it with a record-level `[Display(Name = "<Friendly Singular>")]` attribute.

---

## Model types reference

Choose only the types the feature needs. Skip types that do not apply.

| Type name | Interfaces | Purpose |
|---|---|---|
| `<Name>Model` | `IKeyedItem<int>`, `IReadOnlyConcurrencyStamp` | Full read model — returned by GET single |
| `Slim<Name>Model` | `IKeyedItem<int>` | Slim read model — used as the item in paginated list responses |
| `Create<Name>Model` | (none) | Create request body |
| `Update<Name>Model` | `IUpdateModel<int>` | Update request body — includes `Id` and `ConcurrencyStamp` |
| `Create<Name>ResultModel` | `ICreateResultModel<int>` | Create operation result |
| `Update<Name>ResultModel` | `IUpdateResultModel` | Update operation result — returns the new `ConcurrencyStamp` |
| `<Name>PaginatedResultModel` (optional) | extends `PaginatedResultModel<Slim<Name>Model>` | Feature-specific paginated response, only when the contract needs a named wrapper or extra properties |

**Choosing which model types to scaffold**

Match the models you create to the endpoints you intend to enable. Models for disabled endpoints (those using `object` or `NoOp*` in the controller) do not need to exist.

| Endpoints enabled | Model types to scaffold |
|---|---|
| Full CRUD | All six non-pagination model types in the table; add a named paginated wrapper only when the surrounding contract uses one |
| Read list only | `Slim<Name>Model`; optionally a named paginated wrapper |
| Read list + detail | `Slim<Name>Model`, `<Name>Model`; optionally a named paginated wrapper |
| Create only (e.g. analytics, session recording) | `Create<Name>Model`, `Create<Name>ResultModel` |
| Read list + create (no update, no detail) | `Slim<Name>Model`, `Create<Name>Model`, `Create<Name>ResultModel`; optionally a named paginated wrapper |
| Read list + detail + create (no update) | `Slim<Name>Model`, `<Name>Model`, `Create<Name>Model`, `Create<Name>ResultModel`; optionally a named paginated wrapper |

Every list endpoint needs `Slim<Name>Model` and a paginated contract. Prefer `PaginatedResultModel<Slim<Name>Model>` directly when that matches nearby controllers and services. Create a feature-specific derived record only when nearby features consistently name the wrapper or the response needs additional properties. If there is no list endpoint, neither form is needed.

---

**Interface property requirements — accessor rules:**

- `IKeyedItem<int>` → `int Id { get; }` — `init` is fine here
- `IReadOnlyConcurrencyStamp` → `string ConcurrencyStamp { get; }` → declare `required string ConcurrencyStamp { get; init; }`. This is the contract for read and result models.
- `IConcurrencyStamp` → `string ConcurrencyStamp { get; set; }` — mutable `set` required; `init` does NOT satisfy this interface. Use it **only** on EF/Dataverse entities and on `IUpdateModel<TKey>` request models that need the stamp assigned after construction.
- `ICreateResultModel<int>` → `int Id { get; }` → declare `required int Id { get; init; }`
- `IUpdateModel<int>` inherits `IKeyedItem<int>` + `IConcurrencyStamp` → needs `int Id { get; }` and `string ConcurrencyStamp { get; set; }`
- `IUpdateResultModel` inherits `IReadOnlyConcurrencyStamp` → declare `required string ConcurrencyStamp { get; init; }`

Result models are always populated by a mapper, never by the controller base, so their `Id` and `ConcurrencyStamp` are init-only. Reaching the stamp through the mutable `IConcurrencyStamp` on a read or result model blocks `init` and will trigger UA013.

---

## Record declaration and input-model style

All analyzer-matched model types use `record`. Concrete record classes are `sealed` by default; abstract records and record structs are exempt. Use `[UmbrellaAllowUnsealedModel("reason")]` only when a concrete model is intentionally inherited. Project type does not determine whether a model is `partial`; use `partial` only when a source generator actually needs to add an implementation.

The `[UmbrellaInputModel]`, `[UmbrellaAllowUnsealedModel]`, `[UmbrellaAllowNonRequiredProperty]` and `[UmbrellaAllowMutableProperty]` attributes used below are in the `Umbrella.Analyzers` namespace but ship in the **`Umbrella.Analyzers.Abstractions`** package. Before scaffolding, confirm the repository has the package as a global reference without `PrivateAssets` per `umbrella-dotnet-install-analyzers`. Do not work around an unresolved attribute by hand-declaring a local copy.

Mark only a concrete UI-bound or request-input model directly with `[UmbrellaInputModel]`; the marker is not inherited and is invalid on abstract types. It permits `set` and non-`required` input properties, but does not permit mutable collection contracts or missing getters. Do not add it by default to read or result models. A concrete input type that declares mutable trimmable string properties directly implements `IUmbrellaTrimmable`. Make that type `partial` when the installed trimming generator supplies the implementation; otherwise provide the interface implementation manually without forcing `partial`.

Read and result models normally remain immutable records with `required ... { get; init; }`. Do not mark them as input models merely because the same feature also has a Blazor form.

---

## Conditional validation

Before implementing `IValidatableObject` or a custom `ValidationAttribute` for a request/form rule, inspect the installed `Umbrella.DataAnnotations` package and nearby input models for an existing contingent validation attribute. Prefer the narrowest attribute that expresses the model-local condition, including `RequiredIf`, `RequiredIfNot`, `RequiredIfTrue`, `RequiredIfFalse`, `RequiredIfEmpty`, `RequiredIfNotEmpty`, `RequiredIfRegExMatch`, and `RequiredIfNotRegExMatch` where appropriate.

Reference dependent properties with `nameof(...)`, and use the feature's validation-message constants for `ErrorMessage` when that pattern exists:

```csharp
[RequiredIfNotEmpty(
    nameof(VideoThumbnailProviderFileName),
    ErrorMessage = IndustryConstants.VideoThumbnailAltTextRequiredErrorMessage)]
public string? VideoThumbnailAltText { get; set; }
```

Contingent attributes evaluate only the state present on the model being validated. If a rule depends on persisted entity state, values restored later by a controller/service lifecycle hook, external data, collections, or a condition the installed attributes cannot express, enforce that portion at the appropriate server boundary. Use `IValidatableObject` only when no existing attribute cleanly expresses a model-local rule.

---

## Base class hierarchies (use when models share fields)

When the full read, create, and update models share properties, put those properties and their validation attributes on a mutable abstract `<Name>ModelBase`. Add an abstract `CreateUpdate<Name>ModelBase : <Name>ModelBase` as the common Blazor form type. Do not replace this hierarchy with an `I<Name>InputModel`; the base records carry the shared implementation, validation, trimming contract, and form-binding surface.

Use `[UmbrellaAllowNonRequiredProperty]` and `[UmbrellaAllowMutableProperty]` with specific binding reasons on shared mutable base properties. Mark the abstract base `partial` and implement `IUmbrellaTrimmable` when its strings are handled by the trimming generator. Keep `[UmbrellaInputModel]` off abstract types; apply it directly only to a concrete input record that declares additional mutable properties requiring the marker.

**When to introduce bases:**
- Use `<Name>ModelBase` whenever the full read, create, and update records share editable properties.
- Use `CreateUpdate<Name>ModelBase` when one UI form binds both create and update records, even if it is currently an empty specialization.
- Use a result-model base only when create/update result records genuinely share returned properties.
- Prefer independent sealed records only when the models do not share implementation.

**Typical hierarchy (used when warranted):**

```
<Name>ModelBase (mutable abstract partial record, shared properties + validation)
├── sealed <Name>Model : <Name>ModelBase, IKeyedItem<int>, IReadOnlyConcurrencyStamp
└── CreateUpdate<Name>ModelBase (abstract record, common form type)
    ├── sealed Create<Name>Model : CreateUpdate<Name>ModelBase
    └── sealed Update<Name>Model : CreateUpdate<Name>ModelBase, IUpdateModel<int>

CreateUpdate<Name>ResultModelBase (abstract record)
├── sealed Create<Name>ResultModel : CreateUpdate<Name>ResultModelBase, ICreateResultModel<int>
└── sealed Update<Name>ResultModel : CreateUpdate<Name>ResultModelBase, IUpdateResultModel
```

Notes:
- `<Name>ModelBase` holds properties common to the full read, create, and update models. Its mutable accessors support Blazor binding, while analyzer suppressions document that concrete models populate them through binding or mapping.
- `CreateUpdate<Name>ModelBase` gives a combined manage page one concrete common contract without duplicating shared fields or introducing an input interface.
- Concrete create/update records own only fields unique to their operation, such as `Id`, `ConcurrencyStamp`, or `ReplaceExistingImage`.
- `Slim<Name>Model` usually does NOT inherit from `<Name>ModelBase` — it exists independently with only the fields needed in list views
- `CreateUpdate<Name>ResultModelBase` holds properties returned by both create and update results (e.g., `ConcurrencyStamp`, any computed properties like `ImageUrl`)
- A two-tier result base is only worth adding if there are genuinely shared result properties; if both results only return `ConcurrencyStamp`, a base is unlikely to add value

---

## Step 1 -- Create the model records

**Directory:** `Web.Shared\Models\Api\<Feature>\` (confirm with discovery)

**Abstract base (shared display + editable properties with validation):**

```csharp
using Umbrella.Analyzers;
using Umbrella.Utilities.Text;

namespace <AppName>.Web.Shared.Models.Api.<Feature>;

public abstract partial record <Name>ModelBase : IUmbrellaTrimmable
{
    [Required(ErrorMessage = "<Name>Constants.NameRequiredErrorMessage")]
    [MaxLength(200)]
    [UmbrellaAllowNonRequiredProperty("Shared base property is populated through binding by a concrete input model.")]
    [UmbrellaAllowMutableProperty("Shared base property supports binding by a concrete input model.")]
    public string Name { get; set; } = null!;
    // other shared read properties
}
```

**Shared create/update base (when one form handles both operations):**

```csharp
namespace <AppName>.Web.Shared.Models.Api.<Feature>;

public abstract record CreateUpdate<Name>ModelBase : <Name>ModelBase
{
}
```

**Full read model:**

```csharp
namespace <AppName>.Web.Shared.Models.Api.<Feature>;

public sealed record <Name>Model : <Name>ModelBase, IKeyedItem<int>, IReadOnlyConcurrencyStamp
{
    public required int Id { get; init; }
    public required string ConcurrencyStamp { get; init; }
    // Dynamic Image pairs populated by asynchronous enrichment, when used:
    // [UmbrellaAllowNonRequiredProperty("Populated after the generated mapping.")]
    // [UmbrellaAllowMutableProperty("Populated after the generated mapping.")]
    // public string? ImageUrl { get; set; }
    // [UmbrellaAllowNonRequiredProperty("Populated after the generated mapping.")]
    // [UmbrellaAllowMutableProperty("Populated after the generated mapping.")]
    // public string? ImageVersionToken { get; set; }
}
```

**Slim read model (for paginated list items):**

```csharp
namespace <AppName>.Web.Shared.Models.Api.<Feature>;

[Display(Name = "<Friendly Singular>")]
public sealed record Slim<Name>Model : IKeyedItem<int>
{
    public required int Id { get; init; }
    // only the fields shown in list views
}
```

**Create model:**

```csharp
namespace <AppName>.Web.Shared.Models.Api.<Feature>;

using Umbrella.Utilities.Text;

public sealed partial record Create<Name>Model : CreateUpdate<Name>ModelBase, IUmbrellaTrimmable
{
}
```

The shared base owns the common mutable properties and validation. The concrete create record remains empty unless create-only fields exist. The `partial` declaration assumes the trimming source generator supplies `IUmbrellaTrimmable`; follow the nearest established feature when the generator handles inherited properties.

**Update model:**

```csharp
namespace <AppName>.Web.Shared.Models.Api.<Feature>;

using Umbrella.Analyzers;
using Umbrella.Utilities.Text;

[UmbrellaInputModel]
public sealed partial record Update<Name>Model : CreateUpdate<Name>ModelBase, IUpdateModel<int>, IKeyedItem<int>, IUmbrellaTrimmable
{
    public required int Id { get; init; }
    [Required]
    public required string ConcurrencyStamp { get; set; }
    // add properties specific to update only (e.g., ReplaceExistingImage)
}
```

Note: on this **request** model `ConcurrencyStamp` must use `set` (not `init`), because `IUpdateModel<TKey>` inherits the mutable `IConcurrencyStamp` so a Blazor form can two-way bind it and re-stamp it after a save. Mark it `required` and add `[Required]` so client-side validation enforces it. Result models are the opposite — they use `init`, see below.

**Create result model:**

```csharp
namespace <AppName>.Web.Shared.Models.Api.<Feature>;

public sealed record Create<Name>ResultModel : ICreateResultModel<int>, IReadOnlyConcurrencyStamp
{
    public required int Id { get; init; }
    public required string ConcurrencyStamp { get; init; }
    // Dynamic Image pairs populated after saving, when used:
    // [UmbrellaAllowNonRequiredProperty("Populated after the file is saved.")]
    // [UmbrellaAllowMutableProperty("Populated after the file is saved.")]
    // public string? ImageUrl { get; set; }
    // [UmbrellaAllowNonRequiredProperty("Populated after the file is saved.")]
    // [UmbrellaAllowMutableProperty("Populated after the file is saved.")]
    // public string? ImageVersionToken { get; set; }
}
```

**Update result model:**

```csharp
namespace <AppName>.Web.Shared.Models.Api.<Feature>;

public sealed record Update<Name>ResultModel : IUpdateResultModel
{
    public required string ConcurrencyStamp { get; init; }
    // any other values the server recomputes on update
}
```

**Optional named paginated result model:**

```csharp
namespace <AppName>.Web.Shared.Models.Api.<Feature>;

public sealed record <Name>PaginatedResultModel : PaginatedResultModel<Slim<Name>Model>;
```

`PaginatedResultModel<T>` is a record in current Umbrella versions, so a derived named model must also be a record. Do not add this wrapper when the controller, data service, and client can use `PaginatedResultModel<Slim<Name>Model>` directly.

---

## `required` keyword guidance

Use `required` on public settable properties unless an analyzer-recognized contract or a justified suppression exempts them. Shared mutable properties on an abstract model base use `[UmbrellaAllowNonRequiredProperty]` and `[UmbrellaAllowMutableProperty]` because concrete models populate them through binding or mapping. `[UmbrellaInputModel]` permits additional properties declared directly by a concrete form/request model. For any other exceptional non-input property, use `[UmbrellaAllowNonRequiredProperty("reason")]`; do not omit `required` merely because a default initializer exists.

A property being nullable or frequently absent is **not** a reason to drop `required`. `public required string? Name { get; init; }` is valid and forces the mapper to make an explicit decision. Reserve `[UmbrellaAllowNonRequiredProperty]` for properties genuinely assigned after construction, and make the reason say what assigns them.

---

## Migrating an existing result model

Older result models were written as `public string ConcurrencyStamp { get; set; } = null!;` with `[UmbrellaAllowNonRequiredProperty("Populated after parameterless construction by the generic repository controller.")]`. That justification no longer holds: the controller base no longer constructs result models, so there is no parameterless-construction path and no `new()` constraint. To migrate:

1. `Update<Name>ResultModel` → `public required string ConcurrencyStamp { get; init; }`. Delete the suppression attribute and the `= null!` initialiser.
2. `Create<Name>ResultModel` → `public required TKey Id { get; init; }`, plus the same change for the stamp.
3. If a read or create-result model lists `IConcurrencyStamp` in its base list, change it to `IReadOnlyConcurrencyStamp`. Leaving the mutable interface in place keeps the setter slot and blocks `init`.
4. Leave `Update<Name>Model : IUpdateModel<TKey>` alone — its stamp keeps `{ get; set; }` for Blazor two-way binding and for the `updateModel.ConcurrencyStamp = result.Result.ConcurrencyStamp;` refresh after a save.
5. Any result-model property assigned by an `AfterCreateEntityAsync` / `AfterUpdateEntityAsync` override (e.g. `result.ImageUrl`) keeps `{ get; set; }` with `[UmbrellaAllowMutableProperty("reason")]`. Convert only `Id` and `ConcurrencyStamp`.
6. If a type genuinely cannot move, `[UmbrellaAllowMutableProperty("reason")]` suppresses the UA013 setter half.

Also remove any `, new()` constraint on `TCreateResultModel` / `TUpdateResultModel` in an app-specific controller base that wraps `UmbrellaGenericRepositoryApiController` — `required` members cannot satisfy `new()` (CS9040).

---

## Verification

1. Each model implements the correct interface(s) from the model types table.
2. Every concrete model record class is `sealed`, or carries a specific `[UmbrellaAllowUnsealedModel("reason")]`; abstract records and record structs are exempt.
3. `ICreateResultModel<int>` implementations have `required int Id { get; init; }` — not `set`.
4. Read and result models implement `IReadOnlyConcurrencyStamp` (directly or via `IUpdateResultModel`) and declare `required string ConcurrencyStamp { get; init; }` — not `set`. Only entities and concrete update-input models implement mutable `IConcurrencyStamp`.
5. A list endpoint uses `PaginatedResultModel<Slim<Name>Model>` directly or a justified sealed derived record; no unnecessary wrapper is introduced.
6. Properties shared by the full read, create, and update models live once on `<Name>ModelBase`, together with their validation attributes and justified mutable/non-required suppressions.
7. `Slim<Name>Model` does not inherit from the shared base and declares `[Display(Name = "<Friendly Singular>")]` on the record.
8. No abstract type carries `[UmbrellaInputModel]`; apply the marker directly only to concrete inputs that declare additional mutable properties requiring it.
9. A combined create/update UI uses `CreateUpdate<Name>ModelBase`; no `I<Name>InputModel` is introduced for shared form typing.
10. Every concrete type that declares mutable trimmable strings directly implements `IUmbrellaTrimmable`; only source-generated implementations force that type to be `partial`.
11. Collection properties expose read-only contracts unless an individual property has a justified `[UmbrellaAllowMutableProperty("reason")]`.
12. Conditional model-local rules use the narrowest available `Umbrella.DataAnnotations` contingent attribute; any `IValidatableObject` or custom validator has a rule that those attributes cannot express.
13. Read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build with the installed analyzers enabled.
