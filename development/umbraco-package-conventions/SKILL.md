---
name: umbraco-package-conventions
description: >-
  Backend conventions for an Umbraco package: async naming, internal by default,
  Attempt-based results for routine failures, public-API backwards compatibility, and where
  extension methods live. Use when naming a method, choosing visibility, shaping a service's
  result, changing a public signature (including adding a dependency to a public class's
  constructor), or organizing extension methods. For
  extension mechanisms, see `umbraco-extensibility`.

---

# Umbraco package conventions

## *🎯 Why: Design for Change*

A package's own internal conventions — naming, layering, namespace organization, API stability
— don't touch its extension surface directly, but they're what makes the codebase predictable
enough that the *next* change (by you, or by a package consumer) doesn't require re-deriving
the rules from scratch each time.

## Async method naming: `[Action][Entity]Async`

| Component | Description | Examples |
|---|---|---|
| Action | Verb | `Get`, `Create`, `Update`, `Delete`, `Save`, `Find`, `List`, `Validate` |
| Entity | Noun | `Profile`, `Connection`, `Item`, `Context` |
| Async | Suffix | Always required |

Qualifiers come after the entity: `GetItemByAliasAsync`, `GetAllItemsAsync`. Existence
checks: `[Entity][Qualifier]ExistsAsync` (e.g. `ItemAliasExistsAsync`).

This is the dominant shape across real Umbraco service interfaces, though not universal —
treat it as a strong default, not a rule worth blocking a PR over on its own.

## Visibility: `internal` by default

Every `public` type or member is a contract. Once it ships, changing it falls under the
deprecation rules in "Public API backwards compatibility" below. So start everything
`internal`, and make it `public` only when it is one of these:

- **Public API**: something consumers are meant to call, plus the models they pass in or get
  back.
- **An extension point**: something others hook into, such as an interface to implement, a
  base class, a collection builder, or a notification and its payload.
- **Required by a base type or DI**: an override of a public member, or a type that the
  framework, the DI container or assembly scanning can only use when it's public.

Sharing code between your own assemblies isn't one of these. Keep it `internal` and add an
`InternalsVisibleTo` for the consuming assembly in the owning project. Visibility is also
per member: a notification class and its name can be public while the factory methods that
build it stay internal.

Before adding a `public` type or member, name which of the three it is. If you can't, it's
`internal`.

### Repositories: internal to the owning service

Repositories should be `internal` to the persistence assembly. Only the entity's own service
may touch its repository — controllers and other services go through the service layer:

```
Controller / other service ──▶ EntityService ──▶ EntityRepository (internal)
```

This keeps caching, validation, and business rules in one place (the service), and stops a
future refactor of the repository from becoming a breaking change for anyone but that one
service. Not a strict law — a repository can be `public` if something outside the normal
service layer (diagnostics, a health check) genuinely needs to reach it directly. Default to
`internal`; make a repository `public` only for a specific, nameable reason, not by omission.

## Routine failures: `Attempt<TResult, TStatus>`, like Umbraco's services

Umbraco's services report expected failures through the return type, not exceptions:
`IContentEditingService.CreateAsync` returns `Attempt<ContentCreateResult,
ContentEditingOperationStatus>`, and the Management API controller maps the status enum to a
response. A package service that can fail routinely (not found, invalid input, a duplicate)
should use the same shape: `Attempt<T, TStatus>` with the package's own operation-status
enum. Callers built on Umbraco already know how to branch on it, and a controller maps each
status to a `ProblemDetails` response in one place. Keep exceptions for programmer errors.

## Public API backwards compatibility

Never break a public method's signature outright. When a new version needs new parameters,
keep the old signature and have it **proxy** to the new one, resolving the new parameter via
DI/service location if it can't be threaded through the call site:

```csharp
// Simple case — the new parameter has a sensible static default, no DI needed:
[Obsolete("Use GetItemAsync(id, options) instead. Will be removed in v19.0.0.")]
public Task<Item> GetItemAsync(Guid id) => GetItemAsync(id, ItemOptions.Default);

public Task<Item> GetItemAsync(Guid id, ItemOptions options) { /* real implementation */ }

// Harder case — the new logic genuinely needs a dependency the old call site never had,
// and the old method can't take a new constructor parameter without breaking every existing
// caller's `new MyService(...)` call. Resolve it via the static service provider instead:
[Obsolete("Use CreateAsync(item, permissionChecker) instead. Will be removed in v19.0.0.")]
public Task<Item> CreateAsync(Item item) =>
    CreateAsync(item, StaticServiceProvider.Instance.GetRequiredService<IItemPermissionChecker>());

public Task<Item> CreateAsync(Item item, IItemPermissionChecker permissionChecker) { /* real implementation */ }
```

Resolve via `StaticServiceProvider.Instance.GetRequiredService<T>()` inside the obsolete
overload, rather than duplicating the implementation, only when a static default genuinely
isn't available — a compile-time default parameter is always simpler when one exists.

The same rule covers a public constructor, such as a Management API controller's or a
service's that consumers may construct themselves. Keep the old constructor, mark it
`[Obsolete]`, and chain it to the new one, resolving the new dependency through
`StaticServiceProvider`. Then put `[ActivatorUtilitiesConstructor]` on the new constructor.
With two public constructors and no marker, ASP.NET Core's `ActivatorUtilities` can't pick
one, and the controller fails at runtime on its first request, not at build time. Only a real
request through the demo site proves the right constructor is picked; a unit test calling
`new` directly doesn't.

```csharp
[ActivatorUtilitiesConstructor]
public ItemController(IItemService itemService, IItemPermissionChecker permissionChecker) { /* ... */ }

[Obsolete("Use the constructor taking IItemPermissionChecker. Will be removed in v19.0.0.")]
public ItemController(IItemService itemService)
    : this(itemService, StaticServiceProvider.Instance.GetRequiredService<IItemPermissionChecker>())
{ }
```

Give consumers a real deprecation window — state the target version in the `[Obsolete]`
message. The default target is the highest CMS major the package supports + 2. A package
supporting v17 and v18 that obsoletes a member in both targets v20, on both branches. Check
the project's `CLAUDE.md` first and follow whatever it actually states if it already commits
to a different number.

## Extension methods

Keep them in a single, predictable namespace (e.g. `<RootNamespace>.Extensions`), not
scattered next to whatever class happened to need one first. A consumer should be able to
guess where to look. (This is C#'s *extension method* language feature — an unrelated sense of
"extension" from `umbraco-extensibility`'s Umbraco extension points; don't confuse the two.)

## Multi-version support

If the package targets more than one Umbraco CMS major at once, that's a branching and
release-versioning question, not a package-convention one — see `git-workflow`'s "Umbraco
packages and version tracking" section for branch-per-major and version-alignment guidance.
This skill doesn't restate it.
