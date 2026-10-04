---
name: remix
description: "Covers Remix / React Router v7: nested routes with parallel data loading, loaders and actions (server-side data fetching and mutations), progressive enhancement via <Form> (works without JavaScript), clientLoader/clientAction for client-side caching, defer() for streaming slow data with <Suspense> and <Await>, per-route ErrorBoundary and HydrateFallback, useFetcher for non-navigation mutations, Vite integration, route configuration (explicit routes.ts and file-system conventions), type generation (Route.* types), deployment adapters (Node, Cloudflare, Express, Deno), and migration from Remix v2 to React Router v7. Use for \"Remix\", \"remix\", \"React Router v7\", \"react-router\", \"loader\", \"action Remix\", \"nested routes Remix\", \"useFetcher\", \"progressive enhancement Remix\" questions."
license: MIT
---

# Remix / React Router v7

This skill covers Remix / React Router v7. Remix v2 rebranded to React Router v7 in late 2024 -- same team, same runtime model, same API.

It covers:

- Nested routes: route tree, parallel loader execution, code splitting, `<Outlet />`
- Loaders: server-side GET data fetching, `params`, `request`, throwing Response for errors
- Actions: server-side POST/PUT/DELETE mutations, FormData, redirect after success (PRG)
- Progressive enhancement: `<Form>` works as plain HTML without JS; AJAX with JS
- Streaming: `defer()` with `<Suspense>` and `<Await>` for slow data
- Client loaders/actions: `clientLoader`, `clientAction`, `HydrateFallback`
- Error boundaries: per-route `ErrorBoundary`, `isRouteErrorResponse`, error isolation
- Data hooks: `useLoaderData`, `useActionData`, `useRouteLoaderData`, `useFetcher`, `useNavigation`
- Route configuration: explicit `routes.ts`, file-system conventions via `@react-router/fs-routes`
- Vite integration: `reactRouter()` plugin, HMR, code splitting, type generation
- Deployment adapters: Node.js, Cloudflare Workers, Express, Deno
- Migration: Remix v2 to React Router v7 (package renames, config, type generation)

## How to Approach Tasks

When you receive a request:

1. **Classify** the request type:
   - **Data loading** -- Load `references/patterns/data-loading.md`
   - **Forms / mutations** -- Load `references/patterns/forms.md`
   - **Migration** -- Load `references/patterns/migration.md`
   - **Architecture / Design** -- Load `references/architecture.md`
   - **Best practices** -- Load `references/best-practices.md`
   - **Troubleshooting** -- Load `references/diagnostics.md`
   - **Configuration** -- Reference `assets/react-router.config.ts` or `assets/routes.ts`

2. **Identify context** -- Determine if the user is on Remix v2 or React Router v7. The API is identical; only package names and config file names changed.

3. **Load context** -- Read the relevant reference file.

4. **Analyze** -- Apply Remix-specific reasoning. Remix favors Web standards (Request, Response, FormData, Headers). Avoid recommending client-side state management for data that belongs in loaders/actions.

5. **Recommend** -- Provide actionable guidance. Prefer `<Form>` over `fetch`, loaders over `useEffect`, and actions over client-side mutation.

6. **Verify** -- Suggest validation steps (Network tab, `useNavigation().state`, ErrorBoundary testing).

## Core Expertise

### Nested Routes

React Router v7 builds a route tree from `app/routes.ts`. Every route module can export `loader`, `action`, `ErrorBoundary`, `HydrateFallback`, and a default component. Parent layouts render `<Outlet />` for children.

```typescript
// app/routes.ts
import { type RouteConfig, route, index, layout, prefix } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("about", "routes/about.tsx"),
  layout("routes/_auth.tsx", [
    route("login", "routes/login.tsx"),
    route("register", "routes/register.tsx"),
  ]),
  ...prefix("products", [
    index("routes/products.index.tsx"),
    route(":id", "routes/products.$id.tsx"),
  ]),
] satisfies RouteConfig;
```

Key behaviors: each route owns its own data, error, and loading state. A child error does not unmount siblings. All loaders on the matched branch fire simultaneously (parallel). Each route is a separate Vite chunk.

### Loaders (GET)

```typescript
export async function loader({ params, request }: LoaderFunctionArgs) {
  const product = await db.product.findUnique({ where: { id: params.id } });
  if (!product) throw new Response("Not Found", { status: 404 });
  return { product };
}

export default function ProductPage() {
  const { product } = useLoaderData<typeof loader>();
  return <h1>{product.name}</h1>;
}
```

### Actions (POST/PUT/DELETE)

```typescript
export async function action({ request, params }: ActionFunctionArgs) {
  const formData = await request.formData();
  const name = String(formData.get("name"));
  await db.product.update({ where: { id: params.id }, data: { name } });
  return redirect(`/products/${params.id}`);
}
```

### Progressive Enhancement

```tsx
<Form method="post">
  <input name="email" type="email" />
  <button type="submit">Subscribe</button>
</Form>
```

Without JS: plain HTML form POST. With JS: fetch-based, no full reload.

### Streaming with defer()

```typescript
export async function loader() {
  const fastData = await getFastData();
  const slowPromise = getSlowData();       // NOT awaited
  return defer({ fastData, slowPromise });
}

export default function Page() {
  const { fastData, slowPromise } = useLoaderData<typeof loader>();
  return (
    <>
      <h1>{fastData.title}</h1>
      <Suspense fallback={<p>Loading...</p>}>
        <Await resolve={slowPromise}>
          {(data) => <ReviewList reviews={data} />}
        </Await>
      </Suspense>
    </>
  );
}
```

### Per-Route Error Boundaries

```tsx
export function ErrorBoundary() {
  const error = useRouteError();
  if (isRouteErrorResponse(error)) {
    return <h1>{error.status} -- {error.data}</h1>;
  }
  if (error instanceof Error) return <p>{error.message}</p>;
  throw error;
}
```

### useFetcher (Non-Navigation Mutations)

```tsx
function LikeButton({ postId }: { postId: string }) {
  const fetcher = useFetcher();
  return (
    <fetcher.Form method="post" action={`/posts/${postId}/like`}>
      <button>{fetcher.state !== "idle" ? "Saving..." : "Like"}</button>
    </fetcher.Form>
  );
}
```

## Common Pitfalls

**1. Missing action export for POST forms**
`<Form method="post">` triggers the route's action. If no action is exported, you get 405 Method Not Allowed.

**2. Missing name attributes on inputs**
FormData requires `name` attributes. Unnamed inputs are not included.

**3. No redirect after successful action**
Always redirect after mutation (PRG pattern) to prevent double-submission on browser back.

**4. useLoaderData returns undefined**
Reading the wrong route's data. Use `useRouteLoaderData("routes/parent")` for parent data.

**5. defer values never resolve**
Missing `<Suspense>` + `<Await>` wrapper around deferred data.

**6. Root ErrorBoundary missing full HTML**
The root `ErrorBoundary` must render a complete `<html>` document since no layout wraps it.

**7. Stale data after mutation**
Loaders automatically re-run after actions on the same route. If data appears stale, check that the action returns a redirect.

**8. clientLoader.hydrate without HydrateFallback**
Setting `hydrate = true` without exporting `HydrateFallback` causes a flash of missing content.

## Reference Files

- `references/architecture.md` -- Nested routes, loaders/actions, progressive enhancement
- `references/best-practices.md` -- Data flow, form handling, error boundaries, deployment
- `references/diagnostics.md` -- Route errors, hydration issues, migration problems

## Configuration References

- `assets/react-router.config.ts` -- Annotated config
- `assets/routes.ts` -- Route configuration patterns

## Pattern Guides

- `references/patterns/data-loading.md` -- Loaders, defer, clientLoader
- `references/patterns/forms.md` -- Actions, Zod validation, progressive enhancement
- `references/patterns/migration.md` -- Remix v2 to React Router v7
