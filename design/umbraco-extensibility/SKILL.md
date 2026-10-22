---
name: umbraco-extensibility
description: >-
  Umbraco's extension mechanisms (Composers, collection builders, notification handlers,
  attribute discovery) and a catalogue of backend CMS extension points: property value
  converters, Management API endpoints, content finders, health checks, search indexing,
  package migrations, background jobs, and more. Use when making a feature extensible or
  choosing which extension point fits. Not for property editor UI, dashboards, sections or
  trees, which the official Backoffice Skills plugin covers.

---

# Extending Umbraco, not just building on top of it

## *🎯 Why: Design for Change*

Packages get extended by code you'll never see. Reuse Umbraco's own extension mechanisms so
the extension surface stays stable while the implementation changes; don't invent your own
DI/config/plugin system. For package conventions beyond extension points, see
`umbraco-package-conventions`.

## Composers — your package's DI entry point

A `Composer` (`IComposer`) registers a package into Umbraco's startup, auto-discovered via
assembly scanning. Keep one per package (or per logical concern in a large package). Keep it
thin: it wires things up, no logic.

```csharp
public class MyPackageComposer : IComposer
{
    public void Compose(IUmbracoBuilder builder)
    {
        builder.Services.AddSingleton<IMyPackageService, MyPackageService>();
        builder.MyPackageThings().Add<DefaultThing>();
    }
}
```

## Collection builders — how you make *your own* extension points

If other packages (or your own future features) need to plug in, expose a collection builder,
not a raw list or config flag. Umbraco uses the same mechanism for content finders, editors,
and notification handlers:

```csharp
public class MyPackageThingCollectionBuilder
    : OrderedCollectionBuilderBase<MyPackageThingCollectionBuilder, MyPackageThingCollection, IMyPackageThing>
{
    protected override MyPackageThingCollectionBuilder This => this;
}

public static class MyPackageBuilderExtensions
{
    public static MyPackageThingCollectionBuilder MyPackageThings(this IUmbracoBuilder builder)
        => builder.WithCollectionBuilder<MyPackageThingCollectionBuilder>();
}
```

Consumers then call `builder.MyPackageThings().Add<Custom>().InsertBefore<Custom, Default>()`.
Order via `Append()`/`InsertBefore<T>()`/`InsertAfter<T>()`, not an `Order` property on the
interface, so the registration site controls ordering, not each implementation.

## Attribute-based discovery, when the extension point is "plugins"

For pluggable implementations shipped as separate NuGet packages (providers, connectors,
adapters), prefer attribute + assembly-scan discovery over a config list the consumer must
update:

```csharp
[MyPackageProvider("cool-vendor", "Cool Vendor")]
public class CoolVendorProvider : MyPackageProviderBase { /* ... */ }
```

Then `dotnet add package My.Package.CoolVendor` is the whole integration step, with no code
change in the consuming project.

## Notification handlers, not raw event subscriptions

To react to content/media/member lifecycle events, implement `INotificationHandler<T>` and
register it via the composer, not a static event subscription. Handlers test in isolation and
don't leak subscriptions across restarts. Keep handlers light (`umbraco-performance`), and
put side effects only in handlers that run once, not on every server.

Not the same as the official Backoffice Extension Skills plugin's `umbraco-notifications`
skill: that covers backoffice toast messages (`UMB_NOTIFICATION_CONTEXT`), a frontend-only
concept that shares the name.

## Publish your own notifications at extension points

When a feature adds an extensible API or extension point, propose notifications for it in the
design. Don't wait to be asked, and don't cut them as "add later". They're cheap, and they're
the easiest way for someone to extend a feature without replacing a service or writing a
plugin. List the feature's lifecycle moments (selected, executing, executed, saved) and
propose one for each moment that adds value. Match the shape of the package's or Umbraco's
existing notifications.

Pick the kind by what the extender needs:

- **An "-ed" notification** (`ThingSavedNotification`) when they want to watch or react
  after the fact.
- **A cancelable "-ing" notification** (`ThingSavingNotification`) when they want to add to,
  change or block what happens. Several handlers can each add something, and any one can
  cancel.
- **A replaceable service or ordered collection** when they want to own the whole behavior,
  when there must be one answer, or when order matters. Notification handlers have no
  reliable order.

Skip a cancelable "-ing" notification when another mechanism already decides that outcome,
such as an ordered collection that picks the result. Two ways to decide the same thing will
conflict. Record that choice in `DECISION-LOG.md`.

If an "-ing" notification lets handlers change content you generate, such as text, pass it as
named parts that handlers add, remove or reorder. If handlers search and replace your raw
text, every wording change you make breaks someone.

## Catalogue: which CMS extension point for which job

Excludes what the official Backoffice Extension Skills plugin documents: the Lit/UUI element
and manifest for a backoffice-UI surface (`umbraco-property-editor-ui`, `umbraco-dashboard`,
`umbraco-sections`, `umbraco-tree`), and the C# property editor schema
(`umbraco-property-editor-schema`, covering `DataEditor`, `IConfigurationEditor`, and its own
value converter example). Property value converters stay here anyway, since you write one for
any property editor, built-in or custom.

Signatures can drift across Umbraco majors and this skill isn't version-pinned, so check
the CMS source at the target release (`umbraco-cms-source`) before trusting a base class or
attribute shape verbatim. The docs for that major (`umbraco-docs`) help find the right type. Full skeletons are in `references/`; read only the file you need.

| # | Extension point | Interface / base class | Registered via | Reach for it when |
|---|---|---|---|---|
| 1 | Property value converter | `IPropertyValueConverter` (+ `IDeliveryApiPropertyValueConverter`) | auto-discovered | a property's stored value needs a typed shape at runtime |
| 2 | Management API endpoint | `ManagementApiControllerBase` | versioned route attributes | the backoffice needs to call your package's data |
| 3 | Health check | `HealthCheck` | `[HealthCheck]` attribute | a site builder should be able to self-diagnose your package's config |
| 4 | Cache refresher | `ICacheRefresher` | auto-discovered | your package's own entities need to stay in sync across a load-balanced site |
| 5 | Content finder | `IContentFinder` | `ContentFindersCollection` | resolving custom/virtual URLs to content |
| 6 | URL segment provider | `IUrlSegmentProvider` | `UrlSegmentProviders().Insert<T>()` | generating those same custom URL segments |
| 7 | Search indexing | `IContentIndexer`, `IPropertyValueHandler` (Umbraco Search); `IValueSetBuilder` (Examine) | DI / auto-discovered; named options + composer | adding fields to indexed content, indexing a custom property editor's value, or indexing data that isn't content |¹
| 8 | Custom file system | `IFileSystem` | `builder.SetMediaFileSystem()` (or similar) | media/files live somewhere other than local disk |
| 9 | Package migration plan | `PackageMigrationPlan` + `AsyncPackageMigrationBase` | auto-discovered (or `builder.PackageMigrationPlans().Add<T>()`) | your package needs to import content/schema, or evolve it, across installs and upgrades |
| 10 | Recurring background job | `RecurringBackgroundJobBase` (or `IRecurringBackgroundJob` directly) | `builder.Services.AddRecurringBackgroundJob<T>()` | your package needs scheduled/periodic work (cleanup, sync, digest) without a separate host; for work that must happen once per site, `IDistributedBackgroundJob` (v17+) |
| 11 | Custom Management API authorization policy | `IAuthorizationRequirement` + `MustSatisfyRequirementAuthorizationHandler<T>` | `AddAuthorization` + `[Authorize(policyName)]` | a Management API endpoint (row 2) needs finer-grained access control than the built-in section/content policies |
| 12 | Delivery API query extension | `ISelectorHandler`, `IFilterHandler`, `ISortHandler`, `IContentIndexHandler` | auto-discovered | headless sites need to fetch, filter, or sort content by your package's data |

- **`references/content-and-routing.md`** — rows 1, 5, 6, 7.
- **`references/api-and-infrastructure.md`** — rows 2, 3, 4, 8, 9, 10, 11.
- **`references/delivery-api.md`** — row 1's Delivery API side, and row 12: what a package
  needs so a headless site can use it.

¹ v19 replaces the built-in Examine indexes and hooks with Umbraco Search, which is also an
add-on for v17 and v18. Which API applies depends on the stack the site runs, not just the
major; `content-and-routing.md` row 7 covers both.

## *Scope note*

This skill covers Umbraco's extension mechanisms and the backend-side CMS extension points
built on them, only.

- Async naming, visibility (internal by default), public-API backwards compatibility, and where extension
  methods live: `umbraco-package-conventions`.
- Extension points other products expose (a Commerce payment provider, a Forms workflow type, a
  Contentment data source): that package's own docs.
- What the official Backoffice Extension Skills plugin owns (`umbraco-property-editor-ui`,
  `umbraco-dashboard`, `umbraco-sections`, `umbraco-tree`, `umbraco-property-editor-schema`):
  left to that plugin, even where the code is plain C#.
- Name collisions: that plugin's `umbraco-notifications` and `umbraco-health-check` are
  frontend concepts (toast messages, a health check's backoffice manifest), distinct from this
  skill's `INotificationHandler<T>` and `HealthCheck` C# base class.
