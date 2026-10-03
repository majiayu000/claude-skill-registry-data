---
name: nuxt-ui-tools-query-prefetch
description: Use this skill when declaring or manually triggering route-level TanStack Query prefetches with nuxt-ui-tools. Covers page macros, staged dependencies, NuxtLink integration, and error-safe navigation behavior.
---

# nuxt-ui-tools Query Prefetch

Use this surface when a Nuxt page has data that should be warm before navigation.
The module registers the `defineQueryPrefetch(...)` page macro, executes it from
Nuxt route metadata, and connects it to Nuxt's `link:prefetch` hook.

## Declare a page prefetch

Write one top-level macro call in a page's `<script setup>`:

```vue
<script setup lang="ts">
const productQuery = (id: string) =>
  queryOptions({
    queryKey: ['products', id],
    queryFn: () => $fetch(`/api/products/${id}`),
  })

defineQueryPrefetch('products-id', ({ route }) => productQuery(String(route.params.id)))
</script>
```

The build transform moves the call into the page's `definePageMeta({
queryPrefetch })`. Keep it as a direct top-level statement, and keep an existing
`definePageMeta` call object-shaped. The transform rejects multiple macro calls,
multiple page-meta calls, page-meta spreads, and an existing `queryPrefetch`
property because silently choosing between definitions would make route data
unpredictable.

The destination route is resolved from the link, so query keys include the
destination's params and query string. With typed routes enabled, `route.params`
is narrowed from the route name; otherwise the macro accepts any route name.

## Stage dependent requests

Use `defineQueryPrefetchPlan()` when a later query needs data returned by an
earlier query. Queries declared in one stage run in parallel; stages run in
order:

```ts
defineQueryPrefetch('products-id', ({ route }) =>
  defineQueryPrefetchPlan()
    .stage({
      product: productQuery(String(route.params.id)),
    })
    .stage(({ product }) => ({
      recommendations: queryOptions({
        queryKey: ['recommendations', product.id],
        queryFn: () => $fetch(`/api/products/${product.id}/recommendations`),
      }),
    })),
)
```

Each query is deduplicated by TanStack Query's query key. Disabled entries
(`enabled: false`) are skipped, stale cache entries may be revalidated, and a
failed prefetch is isolated from navigation and from sibling queries. A failed
stage returns the context accumulated before the failure, so page queries remain
the correctness path.

## Trigger manually

Nuxt links invoke the same runtime through `link:prefetch`. For menus or other
interactions, call the auto-imported `prefetchPage` without navigating:

```vue
<UButton @mouseenter="prefetchPage('/products/42')">
  Preview product
</UButton>
```

`prefetchPage(...)` warms both declared queries and lazy route components. Calls
for the same internal destination share one in-flight promise; external URLs are
ignored. It is safe to call from client interactions, while the component preload
portion is skipped during SSR.

For direct package imports, use `nuxt-ui-tools/query-prefetch`.

## Prefetch a table route

Use `prefetchTable(...)` when the destination page renders a schema-driven table. It derives the
destination layout, pagination, sorting, search, and filter state from the route query, then stages
the same queries the runtime will consume:

```ts
defineQueryPrefetch('users', ({ route }) =>
  prefetchTable({
    route,
    schema: usersTableSchema(),
  }),
)
```

Schema context queries run first. The source, global facets, per-filter facets, and remote option
queries run next with that context. Page-context queries run last with the prefetched rows. TanStack
Query keys remain the cache identity, so mounting the destination table reuses fresh results.
