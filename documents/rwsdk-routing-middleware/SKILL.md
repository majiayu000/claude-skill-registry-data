---
name: rwsdk-routing-middleware
description: Use when building rwsdk applications with route handling, middleware, authentication guards, HTTP method routing, context sharing, and type-safe link generation - covers defineApp, route patterns, interrupters, and Documents
---

# rwsdk Routing & Middleware

## Overview

rwsdk uses `defineApp()` to define request handling as an ordered array of middleware and route handlers. Routes match by pattern (static, parameter, wildcard), support HTTP method routing, and can use interrupters for authentication/validation. Middleware populates a shared context object available throughout the request lifecycle.

## When to Use

Use when:

- Building Cloudflare Workers apps with rwsdk
- Need request routing with middleware pipeline
- Want authentication guards per route
- Sharing data between middleware and handlers
- Need type-safe link generation
- Rendering React Server Components

Don't use when:

- Using different routing framework (Next.js, Remix)
- Simple Worker without routing needs (just use fetch handler)

## Quick Start Pattern

```typescript
import { defineApp } from 'rwsdk/worker';
import { route, render } from 'rwsdk/router';

export default defineApp([
  // 1. Middleware (runs before routing)
  sessionMiddleware,
  getUserMiddleware,

  // 2. Routes with interrupters
  route('/admin', [isAuthenticated, isAdmin, AdminPage]),
  route('/users/:id', UserProfilePage),

  // 3. Wrapped in Document
  render(Document, [route('/', HomePage), route('/about', AboutPage)]),
]);
```

**Execution order**: Middleware → Route matching → Interrupters → Handler

## Route Matching Patterns

| Pattern              | Example                                    | Match                   | Access Values                 |
| -------------------- | ------------------------------------------ | ----------------------- | ----------------------------- |
| **Static**           | `route("/about", ...)`                     | Exact path `/about`     | N/A                           |
| **Parameter**        | `route("/users/:id", ...)`                 | `/users/123`            | `params.id`                   |
| **Multi-param**      | `route("/users/:id/groups/:groupId", ...)` | `/users/123/groups/456` | `params.id`, `params.groupId` |
| **Wildcard**         | `route("/files/*", ...)`                   | `/files/any/path`       | `params.$0`                   |
| **Complex wildcard** | `route("/files/*/preview", ...)`           | `/files/docs/preview`   | `params.$0` (= "docs")        |

**Key behaviors**:

- Routes match in definition order (first match wins)
- Trailing slashes normalized automatically (`/about` = `/about/`)
- Parameters available in `params` object

## Request Handlers

**Two return types supported**:

### Response Object

```typescript
route('/api/users', ({ request, params, ctx }) => {
  return new Response(JSON.stringify(users), {
    headers: { 'Content-Type': 'application/json' },
  });
});
```

### JSX (React Server Components)

```typescript
route("/profile/:id", ({ params }) => {
  return <UserProfile userId={params.id} />;
});
```

**JSX is streamed**: Browser progressively renders before hydration.

## HTTP Method Routing

```typescript
route('/api/users', {
  get: () => new Response(JSON.stringify(users)),
  post: ({ request }) => new Response('Created', { status: 201 }),
  delete: () => new Response('Deleted', { status: 204 }),
  custom: {
    report: () => new Response('Report data'), // Custom methods
  },
});
```

**Automatic behaviors**:

- OPTIONS returns `204 No Content` with `Allow` header
- Unsupported methods return `405 Method Not Allowed`

**Disable auto-behaviors**:

```typescript
route('/api/users', {
  get: () => new Response('OK'),
  config: {
    disableOptions: true, // OPTIONS returns 405
    disable405: true, // Unsupported methods fall through to 404
  },
});
```

## Interrupters (Authentication Guards)

Interrupters are arrays of functions that execute in sequence. Return a Response to short-circuit:

```typescript
function isAuthenticated({ request, ctx }) {
  if (!ctx.user) {
    return new Response('Unauthorized', { status: 401 });
  }
  // Return nothing to continue
}

function isAdmin({ ctx }) {
  if (ctx.user.role !== 'admin') {
    return new Response('Forbidden', { status: 403 });
  }
}

defineApp([
  route('/admin', [isAuthenticated, isAdmin, AdminDashboard]),
  route('/profile', [isAuthenticated, UserProfile]),
]);
```

**Per-method interrupters**:

```typescript
route('/api/users', {
  get: [isAuthenticated, () => new Response(JSON.stringify(users))],
  post: [isAuthenticated, isAdmin, validateUser, createUserHandler],
});
```

## Middleware & Context

Middleware runs **before route matching** and populates the shared `ctx` object:

```typescript
import { defineApp } from "rwsdk/worker";

defineApp([
  // Middleware 1: Session
  async function sessionMiddleware({ request, ctx }) {
    ctx.session = await getSession(request);
  },

  // Middleware 2: User (depends on session)
  async function getUserMiddleware({ request, ctx }) {
    if (ctx.session?.userId) {
      ctx.user = await db.selectFrom("users")
        .where("id", "=", ctx.session.userId)
        .selectAll()
        .executeTakeFirst();
    }
  },

  // Routes can access ctx.user
  route("/dashboard", [
    ({ ctx }) => {
      if (!ctx.user) {
        return new Response("Unauthorized", { status: 401 });
      }
    },
    ({ ctx }) => <Dashboard user={ctx.user} />,
  ]),
]);
```

**Context flow**: Middleware populates → Interrupters check → Handlers use

## Documents (HTML Shell)

Documents define the HTML structure (`<html>`, `<head>`, `<body>`):

```typescript
import { render } from "rwsdk/router";

export const Document = ({ children }) => (
  <html lang="en">
    <head>
      <meta charSet="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <link rel="stylesheet" href="/styles.css" />
      <script type="module" src="/src/client.tsx"></script>
    </head>
    <body>
      <div id="root">{children}</div>
    </body>
  </html>
);

defineApp([
  render(Document, [
    route("/", HomePage),
    route("/about", AboutPage),
  ]),
]);
```

**Document applies to all nested routes** - wrap route arrays with `render()`.

## Request Info Object

Access request/response in server functions using `requestInfo`:

```typescript
import { requestInfo } from "rwsdk/worker";

export async function myServerFunction() {
  const { request, response, ctx, cf } = requestInfo;

  // Mutate response
  response.status = 404;
  response.headers.set("Cache-Control", "no-store");

  // Access context
  const user = ctx.user;

  // Access Cloudflare context
  const country = cf.country;

  return <NotFound />;
}
```

**Available properties**:

- `request`: Incoming HTTP Request object
- `response`: ResponseInit object (mutate for status/headers)
- `ctx`: Application context
- `rw`: rwsdk-specific context
- `cf`: Cloudflare Execution Context API

## Type-Safe Link Generation

Generate links with full type safety using `linkFor`:

```typescript
// src/lib/links.ts
import { linkFor } from 'rwsdk/router';

type App = typeof import('../../worker').default;

export const link = linkFor<App>();
```

**Usage** (in client or server code):

```typescript
import { link } from '@/lib/links';

// Static routes
const homeUrl = link('/');
const aboutUrl = link('/about');

// Dynamic routes with params
const userUrl = link('/users/:id', { id: '123' });
// Result: "/users/123"

const editUrl = link('/users/:id/edit', { id: userId });
// TypeScript ensures userId is provided
```

**Key benefits**:

- Type-only import (no Worker code in client bundles)
- TypeScript verifies route exists
- TypeScript ensures required params provided
- Autocomplete for all routes

## Common Mistakes

| Mistake                            | Fix                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------- |
| **Routes in wrong order**          | Put specific routes before wildcards: `/users/:id` before `/users/*`                  |
| **Missing return in interrupters** | Explicitly `return new Response(...)` to short-circuit, or return nothing to continue |
| **Middleware after routes**        | Middleware must come before route definitions in array                                |
| **Mutating request object**        | Request is immutable - use `ctx` for shared state                                     |
| **Forgetting params access**       | Use `params.id` not `request.params.id`                                               |
| **Not awaiting async middleware**  | Mark middleware functions as `async` if they use await                                |
| **linkFor without type import**    | Use `typeof import("...")` pattern for type-only reference                            |

## Request Handler Patterns

### API Routes (JSON)

```typescript
route('/api/todos', {
  get: async ({ ctx }) => {
    const todos = await db.selectFrom('todos').selectAll().execute();
    return new Response(JSON.stringify(todos), {
      headers: { 'Content-Type': 'application/json' },
    });
  },
  post: async ({ request, ctx }) => {
    const body = await request.json();
    await db.insertInto('todos').values(body).execute();
    return new Response('Created', { status: 201 });
  },
});
```

### Protected Routes

```typescript
function requireAuth({ ctx }) {
  if (!ctx.user) {
    return new Response('Unauthorized', { status: 401 });
  }
}

route('/settings', [requireAuth, SettingsPage]);
```

### Conditional Rendering

```typescript
route("/post/:slug", async ({ params, ctx }) => {
  const post = await db.selectFrom("posts")
    .where("slug", "=", params.slug)
    .selectAll()
    .executeTakeFirst();

  if (!post) {
    requestInfo.response.status = 404;
    return <NotFoundPage />;
  }

  return <PostPage post={post} />;
});
```

## Middleware Composition Pattern

```typescript
// Composable middleware
const withAuth = [sessionMiddleware, getUserMiddleware];
const withRateLimit = [rateLimitMiddleware];

defineApp([
  ...withAuth,
  ...withRateLimit,

  route('/', HomePage),
  route('/api/data', [isAuthenticated, DataHandler]),
]);
```

## Advanced: Multiple Documents

```typescript
defineApp([
  middleware,

  // Marketing site with marketing document
  render(MarketingDocument, [
    route('/', LandingPage),
    route('/pricing', PricingPage),
  ]),

  // App with app document (includes navigation)
  render(AppDocument, [
    route('/dashboard', DashboardPage),
    route('/settings', SettingsPage),
  ]),
]);
```

## Execution Flow Diagram

```
Request → Middleware 1 → Middleware 2 → Route Matching
                                              ↓
                                        Interrupter 1
                                              ↓
                                        Interrupter 2
                                              ↓
                                         Handler
                                              ↓
                                    Wrap in Document
                                              ↓
                                         Response
```

## Quick Reference Card

| Task                | Code                                           |
| ------------------- | ---------------------------------------------- |
| **Define app**      | `defineApp([...middleware, ...routes])`        |
| **Static route**    | `route("/path", handler)`                      |
| **Dynamic route**   | `route("/users/:id", handler)`                 |
| **Wildcard**        | `route("/files/*", handler)`                   |
| **HTTP methods**    | `route("/api", { get, post, delete })`         |
| **Guard route**     | `route("/admin", [isAuth, handler])`           |
| **Middleware**      | `function mid({ request, ctx }) { ctx.x = y }` |
| **Document**        | `render(Document, [routes])`                   |
| **Type-safe links** | `link("/users/:id", { id: "123" })`            |
| **Mutate response** | `requestInfo.response.status = 404`            |

## Performance Notes

- **Routes match sequentially**: Order matters for performance
- **Middleware runs on every request**: Keep lightweight
- **Context is per-request**: No shared state between requests
- **JSX streaming**: Progressive rendering before hydration
- **Type imports**: Zero runtime cost for `linkFor` type references
