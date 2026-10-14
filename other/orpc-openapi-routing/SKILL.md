---
name: oRPC OpenAPI Routing
description: Configure procedure routing with HTTP methods, paths, and response statuses.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Routing

> Applies only when using [OpenAPIHandler](/docs/openapi/openapi-handler).

## Basic Routing

By default oRPC uses `POST`, builds paths from router keys, and returns `200` on success.

```ts
os.route({ method: 'GET', path: '/example', successStatus: 200 })
os.route({ method: 'POST', path: '/example', successStatus: 201 })
```

> `.route` can be called multiple times; each call spread-merges with existing.

## Path Parameters

```ts
os.route({ path: '/example/{id}' })
  .input(z.object({ id: z.string() }))

os.route({ path: '/example/{+path}' }) // Matches slashes
  .input(z.object({ path: z.string() }))
```

## Route Prefixes

```ts
const router = os.prefix('/planets').router({
  list: listPlanet,
  find: findPlanet,
  create: createPlanet,
})
```

> Prefix applies only to procedures with a `path`.

## Lazy Router

When combining a lazy router with OpenAPIHandler, a prefix is required:

```ts
const router = {
  planet: os.prefix('/planets').lazy(() => import('./planet'))
}
```

> If using [contract-first](/docs/contract-first/define-contract), the prefix requirement doesn't apply.

> Don't use `lazy` helper from `@orpc/server` here — it can't apply route prefixes.

## Initial Configuration

```ts
const base = os.$route({ method: 'GET' })
```
