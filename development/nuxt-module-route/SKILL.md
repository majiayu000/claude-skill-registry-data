---
name: nuxt-module-route
description: Add a BFF route or a cached server import to the Nuxt half of @joinery/content or @joinery/i18n — the cached handler or function, the path and TTL consts, the module registration and the spec. Use when adding, changing or caching a server route or a Nitro auto-import inside a package's src/nuxt/runtime.
---

# Adding to a package's Nuxt module

The `*:new-vendor` skills stop at `src/core/`. This is the other half: the files that have to agree,
where the two that live outside `runtime/server/` are the ones that get missed.

The two modules expose their core differently, and the first decision is which shape you need:

| Shape | When | Example |
| --- | --- | --- |
| A cached **route** (`addServerHandler`) | The browser, or a framework loader that only speaks HTTP, needs the data, and it is meant to be public | [`@joinery/i18n`](../../../packages/i18n/src/nuxt): `/api/translations/:locale` |
| A cached **server import** (`addServerImports`) | Only the app's own server code reads it, and the app decides what reaches the browser | [`@joinery/content`](../../../packages/content/src/nuxt): `useContent(event)` |

Never add a public route just so the app's server can `$fetch` it in-process — that is a self-call
with a second set of paths, casts and status codes, and an endpoint nobody needed.
[`0031`](../../../docs/decisions/0031-content-server-accessor.md) is why content has no route.

## The files

```
src/nuxt/config.ts                              the path const (routes only), the TTL consts or defaults, the RuntimeConfig augmentation
src/nuxt/module.ts                              addServerHandler / addServerImports
src/nuxt/runtime/server/<name>.get.ts           a route: defineCachedEventHandler + getKey
src/nuxt/runtime/server/utils/<useName>.ts      an import: module-scope defineCachedFunction + getKey
…and a spec beside whichever you wrote
```

## 1. The path and the TTLs are consts, not literals

Everything that names a route imports it from `config.ts` — the module registering the handler and
whatever calls it. That is the only thing stopping the two from drifting.

```ts
export const TRANSLATIONS_API_PATH = "/api/translations";

export const TRANSLATIONS_MAX_AGE = 60 * 60;
export const TRANSLATIONS_STALE_MAX_AGE = 60 * 60 * 24;
```

`staleMaxAge` belongs on a `defineCachedEventHandler` only, which turns it into the
`stale-while-revalidate` of its `Cache-Control`. `defineCachedFunction` ignores it, so don't pass one.

Nitro reads cache options when the handler or function is defined, so a TTL cannot vary per call —
a genuinely different TTL means a different cached handler or function. Don't work around it with a
conditional inside `getKey`. A window an app should tune, such as a short one for local dev, is
module options instead: `@joinery/content` takes `content.cache` with defaults in `config.ts` and
reads it from `useRuntimeConfig()` once, at module scope.

## 2. Two places declare the runtime config

`module.ts` assigns it and `config.ts` augments the schema. Both, or the server code reads
`undefined`:

```ts
nuxt.options.runtimeConfig.content = resolvedOptions;
```

```ts
declare module "@nuxt/schema" {
    interface RuntimeConfig {
        content: ContentConfig
    }
}
```

Runtime reads it back through a cast: the augmentation only lands inside a Nuxt project, so compiled
standalone the value is `any`.

## 3. Register with the resolver, never a bare path

```ts
const resolver = createResolver(import.meta.url);

addServerHandler({
    route: `${TRANSLATIONS_API_PATH}/:locale`,
    method: "get",
    handler: resolver.resolve("./runtime/server/translations.get"),
});

addServerImports([{ name: "useContent", from: resolver.resolve("./runtime/server/utils/useContent") }]);
```

Validate what can fail the build in `setup` rather than on the first request — both modules reject
an unknown vendor name there.

## 4. The cache options, and the one rule inside them

```ts
const readList = defineCachedFunction(async (event: H3Event, resource: Resource, query: EntryQuery) => { … }, {
    name: "content-list",
    group: "content",
    ...cache.list,
    getKey: (event, resource, query) => contentKey(readVendor(event), resource, query),
});
```

**The key is built from the normalised input, never the raw one.** Defaults and the `MAX_PAGE` /
`MAX_PER_PAGE` / `MAX_SEARCH_LENGTH` ceilings are applied first, so `{}` and `{ page: 1 }` collapse
to one entry — and a crafted query cannot mint unbounded ones. A route does it inside `getKey`; a
server import does it before calling the cached function.
[`useContent.ts`](../../../packages/content/src/nuxt/runtime/server/utils/useContent.ts) and
[`contentKey.ts`](../../../packages/content/src/core/contentKey.ts) are the pattern.

Two things specific to `defineCachedFunction`, checked against nitropack 2.13:

- **Define it at module scope.** In-flight dedupe lives in a map inside each definition, so one
  defined per call never shares a pending upstream request.
- **Pass the event first.** Nitro's cache hands a stale refresh to `waitUntil` only when the first
  argument is an event. It also never runs `escapeKey` on a function's key, so the key must already
  be storage-safe — word characters only, as `contentKey` is.

## 5. Errors map at this edge and nowhere else

The core throws domain errors; this layer is the only place they become HTTP statuses.

| Helper | When |
| --- | --- |
| `rethrowAsHttpError(cause)` | anything the core already diagnosed — a non-domain error keeps its stack and reports as unhandled |
| `throwUnavailableError(cause, resource)` | a provider call that failed; an `UpstreamError` already carries its status and passes through untouched rather than flattening to 502 |

`statusMessage` reaches the client, so no message may repeat the vendor's URL or the transport's own
text. Both packages carry this pair verbatim — copy it, don't re-derive it.

## 6. The spec

Mock `nitropack/runtime` so the cache definition hands you its options back; that is how `getKey`
gets tested directly rather than through a live cache.
[`translations.get.spec.ts`](../../../packages/i18n/src/nuxt/runtime/server/translations.get.spec.ts)
is the shortest route example:

```ts
const nitro = vi.hoisted(() => ({ vendor: undefined, cache: undefined }));

vi.mock("nitropack/runtime", () => ({
    defineCachedEventHandler: (handler, options) => {
        nitro.cache = options;
        return handler;
    },
    useRuntimeConfig: () => ({ translations: { vendor: nitro.vendor } }),
}));
```

For a server import,
[`useContent.spec.ts`](../../../packages/content/src/nuxt/runtime/server/utils/useContent.spec.ts)
wraps the function so every call records the key it would be stored under. That pins that a refused
query mints no key at all. The rest follows the repo's spec conventions — see the `writing-tests`
skill.

## Building the transport

Both packages build the client from the vendor config, as
`new OfetchHttpClient(ofetch.create({ baseURL: vendor.baseURL }))`, and providers pass relative
paths. A route that builds it any other way, or hands a provider an absolute URL, breaks the
contract the two packages share.

## Verify

```sh
pnpm exec nx run-many -t lint typecheck test --projects @joinery/content @joinery/i18n
pnpm exec nx build @joinery/huella-legal  # registration only shows up once a real app installs the module
```

A route that 404s in the app, or a server import that is "not defined" there, but passes its spec,
is almost always step 3 — it was written and never registered.
