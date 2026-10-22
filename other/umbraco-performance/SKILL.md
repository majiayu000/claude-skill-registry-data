---
name: umbraco-performance
description: >-
  Keeping a package fast on the sites that install it: the published cache over the services
  layer, tree traversal, caching lookups and clearing them, data type config and converter
  cache levels, output cache eviction, light hot paths, and backoffice screens that don't
  over-fetch. Use when writing, changing or reviewing code that runs per request, per save, per
  indexed item or at startup (property value converters, notification handlers, indexing),
  code that loops over every content item (a full rebuild, an import, a sync), or a list or
  search screen. Not for a site's own templates.

---

# Performance for Umbraco packages

A package's code runs on sites its author never sees: a 50-page brochure site and a
200,000-node multi-site install get the same DLL. Write for the big one. Every rule below
is a pattern that's harmless on the demo site and costly in production.

This skill covers code a package ships: property value converters, content finders,
Management API endpoints, notification handlers, indexers, background jobs, Delivery API
output, and backoffice extensions. A site's own templates and its tuning (cache seed counts,
turning output caching on, cache size limits) belong to the site owner. A package must
stay fast with the site's defaults, not depend on the owner changing them.

Verify version-specific APIs against the CMS source and docs for the major the project
targets (`umbraco-cms-source`, `umbraco-docs`). The published content cache was rebuilt in
v15, so caching advice written for v13 and earlier is often wrong now. Search changes in
v19: Umbraco Search (`Umbraco.Cms.Search`) replaces the built-in Examine indexes and their
hooks. It's also an add-on for v17 and v18, so check which one the site uses, not just the
major.

## *🎯 Why: Design for Change*

Slow code gets fixed by adding caches, and caches added late get bolted on in the wrong
place, with no plan for clearing them. Deciding up front where data is read from, and what
clears it, keeps a later speed fix a local change instead of a redesign.

## Read published content from the cache, not the services layer

The services layer (`IContentService`, `IMediaService`, `IRelationService` and friends)
reads and writes the database. It's for changing data, not reading it on a hot path. Package
code that runs per front-end or Delivery API request (a converter, a content finder, a
rendered component) reads from the published cache instead:

```csharp
// Hits the database on every call
var item = _contentService.GetById(key);

// Reads the published cache
var item = _publishedContentCache.GetById(key);
```

The published cache is lazy-loaded: an item is read from the database the first time it's
requested, then served from memory. A cold item costs a database call, which matters when
package code touches thousands of them (next section).

Source: [Common pitfalls](https://docs.umbraco.com/umbraco-cms/develop-with-umbraco/application-code/common-pitfalls),
[Cache seeding](https://docs.umbraco.com/umbraco-cms/extend-your-project/server-side-extensions/cache/cache-seeding).

## Don't walk the whole tree

`Descendants()` / `DescendantsOrSelf()` visit every node below the starting point and load
each one. From the root, that's the whole site. A filter after it still loads everything
first:

```csharp
// Loads every node in the site to find the products
var products = root
    .DescendantsOrSelf(_navigationQueryService, _publishedStatusFilteringService)
    .Where(x => x.ContentType.Alias == "product");
```

Since v15 this costs more than it used to: each `IPublishedContent` is rebuilt from the
cache when it's accessed, and items not yet cached come from the database. Package code that
walked a large tree comfortably on v13 has been reported many times slower on v15 to v17.
Test anything that traverses (sitemaps, feeds, link checkers, reports) against a large
content tree on the target major, with the site's default cache settings.

- Ask the navigation service tree questions. `IDocumentNavigationQueryService` (and its
  media counterpart) answers parent/child/descendant/ancestor questions from an in-memory
  structure of keys, without loading content. Filter by key and type there, then load only
  the items you need from the cache.
- Search the index, don't traverse. "Find every product with tag X" is a query, not a
  tree walk. On v19, or v17/v18 with the Umbraco Search add-on, get an `ISearcher` from
  `ISearcherResolver` and filter, sort and page in the query (`skip`/`take`). Without the
  add-on on v17/v18, query Examine.
- Work that must cover the whole tree (a full sitemap, an export) runs in a background
  job or on demand, and caches its result. It doesn't run per request.
- A descendant walk is fine when the subtree is small by design (a settings folder). Say so
  in a comment, so a reviewer doesn't have to guess.

Source: [Common pitfalls](https://docs.umbraco.com/umbraco-cms/develop-with-umbraco/application-code/common-pitfalls),
[Umbraco Search](https://docs.umbraco.com/umbraco-search),
CMS issues [#18869](https://github.com/umbraco/Umbraco-CMS/issues/18869) and
[#18892](https://github.com/umbraco/Umbraco-CMS/issues/18892).

## Navigation extensions: pass the services in

`Children()`, `Parent()`, `Ancestors()`, `Descendants()`, `Siblings()` and the rest of the
`IPublishedContent` navigation extensions (`Umbraco.Extensions`) are backed by the
navigation service. Each has an overload that takes the navigation service
(`IDocumentNavigationQueryService`, or `IMediaNavigationQueryService` for media) and
`IPublishedStatusFilteringService`. Package code calls those overloads, with both services
injected through the constructor:

```csharp
internal sealed class ProductListingService(
    IDocumentNavigationQueryService navigationQueryService,
    IPublishedStatusFilteringService publishedStatusFilteringService)
{
    public IEnumerable<IPublishedContent> GetProducts(IPublishedContent category)
        => category.Children(navigationQueryService, publishedStatusFilteringService)
            .Where(x => x.ContentType.Alias == "product");
}
```

The short forms without those parameters (`content.Children()`, mostly in
`FriendlyPublishedContentExtensions` in `Umbraco.Web.Common`) look both services up from
`StaticServiceProvider` on every call. That's a service-locator lookup per call, repeated in
every loop, plus a hidden dependency a unit test can't replace. A package project that only
references `Umbraco.Core` doesn't get most of them at all. They're for templates, not
package code.

The `IPublishedContent.Children` *property* is obsolete in v17 and removed in v18. Use the
extension method.

Source: `PublishedContentExtensions` and `FriendlyPublishedContentExtensions` in the CMS
source (17.7.1, 18.2.1, `v19/dev`); `IPublishedContent` at 17.7.1.

## Cache your own expensive lookups

Anything slow that package code repeats (a relation lookup, a call to an external API, a
computed aggregate) goes through Umbraco's `AppCaches`, not a static field or a private
`MemoryCache`:

- `AppCaches.RuntimeCache` (`IAppPolicyCache`) for values shared across requests, with an
  expiry.
- `AppCaches.RequestCache` for values reused within one request.

```csharp
var relations = _appCaches.RuntimeCache.GetCacheItem(
    $"MyPackage_ChildRelations_{key}",
    () => _relationService.GetByChildId(id, "umbDocument"),
    TimeSpan.FromMinutes(5));
```

- **Prefix every cache key** with your package name. The runtime cache is shared with core
  and every other package.
- **Decide what clears it, at design time.** An expiry alone means stale data for that
  long. If the data changes when your entity is saved, clear the key there. An integration
  test of that clearing needs `umbraco-dotnet-testing`, or it passes whatever the code does.
- **Clear it on every server.** On a load-balanced site the clear goes through a cache
  refresher (`umbraco-extensibility`'s catalogue, row 4).
- **Refresh many items in one call.** `DistributedCache.Refresh(refresherId, ids)` or
  `RefreshByPayload(refresherId, payloads)` with the whole set, not one call per item in a
  loop. Outside a web request (a background job, an import), each call is written to the
  database for the other servers straight away.
- **Never hold a request-scoped object in a singleton or static field.** `UmbracoHelper`,
  `IUmbracoContext` and anything resolved per request belong to one request. Kept longer,
  they pin memory and can serve one user's data to another.

Source: [Accessing the cache](https://docs.umbraco.com/umbraco-cms/extend-your-project/server-side-extensions/cache/application-cache),
[Common pitfalls](https://docs.umbraco.com/umbraco-cms/develop-with-umbraco/application-code/common-pitfalls),
`BatchedDatabaseServerMessenger` in the CMS source.

## Read data type configuration from its cache

Converters, value editors and data sources often need their data type's configuration. Read
it from `IDataTypeConfigurationCache` (`GetConfigurationAs<T>(dataTypeKey)`), not
`IDataTypeService`. The service goes to the repository and clones the result on every call,
and a value editor runs once per property, per variant, per load.

Source: CMS issue [#14936](https://github.com/umbraco/Umbraco-CMS/issues/14936) and
PR [#15731](https://github.com/umbraco/Umbraco-CMS/pull/15731).

## Property value converters: set the cache level

`GetPropertyCacheLevel` decides how often a converter runs. Pick it deliberately:

| Level | Converted again when | Use for |
|---|---|---|
| `Element` | the owning page or block changes | the default; values that only depend on their own data |
| `Elements` | any content changes | values that reference other content (pickers) |
| `None` | every read | almost never; it's a large cost on every read |

`PropertyValueConverterBase` returns `Snapshot`, which is obsolete and treated as `None`
by the current published cache. A converter that inherits the base class without
overriding `GetPropertyCacheLevel` runs its conversion on every read. Always override it.

A converter that also implements `IDeliveryApiPropertyValueConverter` sets two more:
`GetDeliveryApiPropertyCacheLevel` and `GetDeliveryApiPropertyCacheLevelForExpansion`
(which defaults to the first). The same table applies, and `Snapshot` means `None` here
too, even where a docs example uses it. Expanded output depends on each request's `expand`
and `fields`, so a cached copy is served to requests that asked for a different shape.
Override `GetDeliveryApiPropertyCacheLevelForExpansion` to return `None` rather than
inheriting the default; the built-in converters do the same through `Snapshot`. Never put per-request data (the current time, the
current user) in a converter's output: any cache level serves it stale, and it stops a site
using Delivery API output caching.

Source: [Property value converters](https://docs.umbraco.com/umbraco-cms/extend-your-project/backoffice-extensions/property-editors/property-value-converters),
[Custom property editors support](https://docs.umbraco.com/umbraco-cms/develop-with-umbraco/headless-and-apis/content-delivery-api/custom-property-editors-support);
`PublishedProperty.GetCacheValues` in `Umbraco.PublishedCache.HybridCache`.

## Output caching: evict when your data changes

From 17.4 (and every 18.x), a site can cache whole rendered pages and whole Delivery API
responses. The package doesn't turn this on, but has to work when the site does:

- **If package data feeds pages or API responses** and it changes outside a content
  publish (a product price, a review count from your own tables), evict what shows it:
  `IWebsiteOutputCacheManager` and `IDeliveryApiOutputCacheManager` evict by content key or
  by tag. Otherwise visitors see the old value until the cache expires.
- **If the package renders output that differs per visitor** (a member's name, a basket),
  mark that response as not cacheable. A cached copy of it is served to the next visitor.

Source: [Website output caching](https://docs.umbraco.com/umbraco-cms/develop-with-umbraco/caching/website-output-caching),
[Delivery API output caching](https://docs.umbraco.com/umbraco-cms/develop-with-umbraco/headless-and-apis/content-delivery-api/output-caching).

## Keep hot paths light

Some code runs far more often than it looks like it does:

- **Notification handlers** on save/publish run inside the editor's save. A bulk publish
  runs them once per item. Do slow work (external calls, reindexing your own data)
  after the save: record it and let a background job pick it up. An in-memory queue loses
  work on a restart.
- **Bulk operations** (an import, a sync, a migration over many items) run in one scope, so
  the work is one transaction and its notifications fire once, when the scope completes.
  `scope.Notifications.Suppress()` stops them entirely, which is only safe for data your
  package owns. Suppressing around content or media service calls leaves the published
  cache and search index stale until they're rebuilt.
- **Indexing code** runs once per item indexed, and a full rebuild runs it for every
  document and media item. With Umbraco Search, that's `IContentIndexer.GetIndexFieldsAsync`
  and `IPropertyValueHandler.GetIndexFields`. With Examine on v17/v18, it's
  `TransformingIndexValues` and similar events. For the Delivery API index, on any of them,
  it's `IContentIndexHandler.GetFieldValues`. A service lookup in there is one database
  call per item. Build fields from the content item you're handed. If you need related
  data, read it from the published cache or a cached lookup, not a service.
- **Startup** code runs on every app start, on every site that installs the package. Do
  work lazily, when it's first needed. Run one-time setup through a migration, which
  records that it ran, not a check on every boot.
- **Volatile data doesn't belong in content nodes.** Counters, form entries, logs and
  imported bulk data go in your own tables (`ef-core-data`). Content saves are slow by
  design: versioning, notifications, cache updates, reindexing.

Source: [Common pitfalls](https://docs.umbraco.com/umbraco-cms/develop-with-umbraco/application-code/common-pitfalls),
[ContentService notifications](https://docs.umbraco.com/umbraco-cms/extend-your-project/server-side-extensions/notifications/contentservice-notifications),
[Umbraco Search](https://docs.umbraco.com/umbraco-search).

## Management API endpoints: return what the list needs

- **Page anything that can grow.** A list endpoint takes `skip`/`take` and returns a total.
  Never return "all items" for the screen to page.
- **List-sized models.** A list returns what its columns show; the full model is for the
  detail endpoint.
- **No per-item URL building in lists.** Resolving a content URL is slow next to loading
  the item. Core moved URLs out of its own document response into a separate endpoint for
  this reason. Return keys, and let the screen ask for URLs where it shows them.

Source: CMS issue [#18910](https://github.com/umbraco/Umbraco-CMS/issues/18910).

## Backoffice extensions: don't over-fetch

- **Use the paging the screen already has.** Collection views have paging built in; wire
  them to the endpoint's `skip`/`take`.
- **Debounce search-as-you-type.** Use `debounce` from `@umbraco-cms/backoffice/utils`, so
  a search fires when typing pauses, not on every key press.
- **Fetch once, share it.** Two elements on one screen that need the same data read it from
  a shared context or repository, not one request each.
- **Don't refetch when an element reconnects.** Block editors' sorting removes and re-adds
  elements, so `connectedCallback` runs again on every drag. Server-rendered previews and
  other expensive fetches cache their result (for example by a hash of the value) and reuse
  it.

Source: Block Preview issue [#149](https://github.com/rickbutterfield/BlockPreview/issues/149).

## *Reviewing a diff for performance*

- A services-layer read (`IContentService`, `IMediaService`, `IDataTypeService`, ...) on a
  per-request, per-property or per-item path.
- `Descendants()`/`DescendantsOrSelf()` from a root or other large node, on a per-request
  path or without a comment saying why the subtree is small.
- A navigation extension (`Children()`, `Ancestors()`, ...) called without the injected
  navigation and published-status services, or the obsolete `.Children` property.
- A converter with no `GetPropertyCacheLevel` override, or any cache level (including the
  Delivery API one) set to `None` or `Snapshot` without a stated reason. The Delivery API
  expansion level is the exception: flag it when it's anything but `None` or `Snapshot`.
- A cache added with no rule for what clears it.
- A cache key without the package prefix.
- A request-scoped object stored in a singleton or static field.
- Package data shown on pages or in Delivery API responses, changed with no output cache
  eviction.
- A database or HTTP call inside a notification handler, a content indexer, a property
  value handler, an Examine event, or a loop over content.
- Bulk work outside a single scope, or `Suppress()` around content or media service calls.
- A list endpoint without paging, or with per-item URLs; a search box without a debounce;
  an expensive fetch in `connectedCallback` with no cache.
