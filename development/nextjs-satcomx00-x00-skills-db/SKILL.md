---
name: nextjs
description: Next.js 15 / React 19 state-of-the-art — App Router, async request APIs, use cache directive, Turbopack, Server Functions, Partial Prerendering, and production best practices.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 2.0.0
---

# nextjs

Next.js 15 / React 19 state-of-the-art — App Router, async request APIs, `use cache` directive, Turbopack, Server Functions, Partial Prerendering, and production best practices.

> Targets **Next.js 15+** with **React 19**. Older patterns (Pages Router, synchronous request APIs) are not covered here.

## Instructions

### Tooling & Project Setup

- Use **Turbopack** for local development — it is stable since Next.js 15 and faster than Webpack in virtually all cases:
  ```bash
  next dev --turbo
  ```
- Use `next.config.ts` (TypeScript) instead of `next.config.js` — full type safety for all config options
- Use the codemod CLI to upgrade between versions:
  ```bash
  npx @next/codemod@canary upgrade latest
  ```
- Enable the **React Compiler** (experimental) to auto-memoize components without manual `useMemo`/`useCallback`:
  ```ts
  // next.config.ts
  const nextConfig = {
    experimental: { reactCompiler: true },
  };
  ```

### App Router Conventions

Use the **App Router** (`app/`) exclusively. Understand the file conventions:

| File | Purpose |
|------|---------|
| `layout.tsx` | Shared UI wrapper; persists across navigation |
| `page.tsx` | Route segment UI |
| `loading.tsx` | Suspense boundary fallback for the segment |
| `error.tsx` | Error boundary (must be a Client Component) |
| `not-found.tsx` | Rendered when `notFound()` is called |
| `route.ts` | API route handler |
| `middleware.ts` | Edge function; runs before every matched request |
| `instrumentation.ts` | Server lifecycle hooks (stable in Next.js 15) |

**Server vs. Client Components:**
- All components are **Server Components by default** — zero JS bundle cost, direct DB/API access, secrets never reach the browser
- Add `'use client'` only for: event handlers, browser APIs, `useState`/`useEffect`, third-party client-only libraries
- Push `'use client'` boundaries as **far down** the tree as possible to minimise bundle size

```tsx
// Server Component — async/await directly, no useEffect
export default async function UserProfile({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params; // params is async in Next.js 15+
  const user = await db.user.findUnique({ where: { id } });
  if (!user) notFound();
  return <ProfileCard user={user} />;
}
```

### ⚠️ Async Request APIs (Next.js 15 Breaking Change)

`cookies()`, `headers()`, `draftMode()`, `params`, and `searchParams` are **now async** and must be awaited:

```ts
// ✅ Next.js 15+
import { cookies, headers } from 'next/headers';

export default async function Page({ params, searchParams }: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ q: string }>;
}) {
  const { slug } = await params;
  const { q } = await searchParams;
  const cookieStore = await cookies();
  const token = cookieStore.get('token');
  // ...
}
```

Run the official codemod to migrate automatically:
```bash
npx @next/codemod@canary next-async-request-api .
```

### Caching — New Model (`use cache`)

Next.js 15 ships two caching models. Use the **new model** for all new projects:

**Enable Cache Components in `next.config.ts`:**
```ts
const nextConfig = { cacheComponents: true };
export default nextConfig;
```

**`use cache` directive** — replaces the old implicit `fetch` caching:

```ts
// Data-level cache — reuse across multiple components
async function getProducts() {
  'use cache';
  return db.product.findMany();
}

// UI-level cache — cache an entire component's render
async function FeaturedBanner() {
  'use cache';
  const promo = await fetchPromo();
  return <Banner data={promo} />;
}
```

**Rules for `use cache`:**
- Arguments and closed-over values automatically form the cache key
- Cannot call `cookies()` or `headers()` inside a `use cache` scope — read them outside and pass as arguments
- For serverless environments the default LRU cache does not persist across invocations; use `'use cache: remote'` (Redis/KV) for shared runtime caching
- Revalidate with `revalidateTag()` / `revalidatePath()` on demand, or set a TTL via `cacheLife`:
  ```ts
  import { unstable_cacheLife as cacheLife } from 'next/cache';

  async function getStats() {
    'use cache';
    cacheLife('hours'); // built-in profiles: seconds | minutes | hours | days | weeks | max
    return fetchStats();
  }
  ```

**Legacy model (without `cacheComponents`):**
- `fetch` is **not cached by default** in Next.js 15 (opt in with `{ cache: 'force-cache' }`)
- `GET` Route Handlers are **not cached by default** (opt in with `export const dynamic = 'force-static'`)
- Use `unstable_cache` for non-`fetch` DB queries

### Rendering Strategies

| Strategy | Description | How |
|----------|-------------|-----|
| **Static** | Built at compile time; served from CDN | No request-time APIs; or `use cache` on the full page |
| **Dynamic** | Rendered per request | Use `cookies()`, `headers()`, or other request-time APIs |
| **Streaming** | Stream content progressively | `<Suspense>` boundaries around async Server Components |
| **PPR** (Partial Prerendering) | Static shell + dynamic holes per request | Opt in with `experimental.ppr: true`; wrap dynamic parts in `<Suspense>` |

PPR is the direction Next.js is headed — a single route delivers a static HTML shell instantly, then streams in dynamic personalised content:

```tsx
// next.config.ts
experimental: { ppr: 'incremental' }

// app/dashboard/page.tsx
export const experimental_ppr = true;

export default function Dashboard() {
  return (
    <main>
      <StaticNav />                          {/* included in static shell */}
      <Suspense fallback={<FeedSkeleton />}>
        <PersonalisedFeed />                 {/* streamed at request time */}
      </Suspense>
    </main>
  );
}
```

### Server Functions (Server Actions)

Server Functions (`'use server'`) are the primary mutation path — no separate API route needed for most operations:

```tsx
// app/actions/profile.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function updateProfile(_: unknown, formData: FormData) {
  const session = await getSession(); // validate auth first
  const name = formData.get('name') as string;
  await db.user.update({ where: { id: session.userId }, data: { name } });
  revalidatePath('/profile');
}

// Client usage with useActionState (React 19)
'use client';
import { useActionState } from 'react';
import { updateProfile } from '@/app/actions/profile';

export function ProfileForm() {
  const [state, action, isPending] = useActionState(updateProfile, null);
  return (
    <form action={action}>
      <input name="name" />
      <button disabled={isPending}>{isPending ? 'Saving…' : 'Save'}</button>
      {state?.error && <p role="alert">{state.error}</p>}
    </form>
  );
}
```

**Security:** Next.js 15 automatically generates unguessable endpoint IDs for Server Actions and tree-shakes unused ones from the client bundle. Still always validate session and authorise the action server-side.

### `after()` — Non-blocking Side Effects

Use `after()` to run work (logging, analytics, audit events) **after** the response is sent, without delaying it:

```ts
import { after } from 'next/server';

export async function POST(req: Request) {
  const data = await req.json();
  const result = await createOrder(data);

  after(async () => {
    await auditLog.record({ action: 'order.created', orderId: result.id });
    await analytics.track('order_created', { value: result.total });
  });

  return Response.json(result, { status: 201 });
}
```

### `instrumentation.ts` — Server Lifecycle Observability

Use `instrumentation.ts` at the project root to initialise telemetry once when the server starts:

```ts
// instrumentation.ts
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    const { NodeSDK } = await import('@opentelemetry/sdk-node');
    const sdk = new NodeSDK({ /* tracing config */ });
    sdk.start();
  }
}

export const onRequestError = async (err: unknown, request: Request) => {
  await errorReporter.capture(err, { url: request.url });
};
```

### Routing & Navigation

- Use `<Link>` for all internal navigation — prefetches on hover/visibility
- Use `<Form>` (`next/form`) for search/filter forms — navigates client-side without a full reload
- Use `useRouter().push()` for programmatic navigation in Client Components
- Use `redirect()` in Server Components / Server Functions
- **Parallel routes** (`@slot`) — render multiple pages in one layout (modals, split panes)
- **Intercepting routes** (`(.)segment`) — overlay a route on top of the current page (lightboxes)
- Protect routes in `middleware.ts` — runs at the Edge before the page renders

```ts
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';

export async function middleware(req: NextRequest) {
  const session = req.cookies.get('session')?.value;
  if (!session && req.nextUrl.pathname.startsWith('/dashboard')) {
    const url = req.nextUrl.clone();
    url.pathname = '/login';
    url.searchParams.set('callbackUrl', req.nextUrl.pathname);
    return NextResponse.redirect(url);
  }
}

export const config = { matcher: ['/dashboard/:path*', '/api/protected/:path*'] };
```

> **Node.js Middleware** (experimental in 15.2): if you need Node.js APIs in Middleware (file system, native modules), opt in with `experimental.nodeMiddleware: true` in `next.config.ts`.

### Performance

- **`next/image`**: mandatory for all images — automatic WebP/AVIF, lazy loading, prevents CLS
- **`next/font`**: self-hosted, zero layout shift, tree-shaken unused font subsets
- **`next/script`**: control loading strategy (`beforeInteractive`, `afterInteractive`, `lazyOnload`) for third-party scripts
- **Bundle analysis**: `ANALYZE=true next build` with `@next/bundle-analyzer`
- **React Compiler**: automatic memoisation (experimental) — removes most manual `useMemo`/`useCallback`
- **View Transitions** (experimental in 15.2): animate page/component transitions using the browser-native View Transitions API
  ```ts
  // next.config.ts
  experimental: { viewTransition: true }
  ```

### Environment Variables

- `NEXT_PUBLIC_*` — embedded in the browser bundle at build time; never put secrets here
- All other env vars — server-only; never sent to the client
- Type-safe validation at startup with `zod`:

```ts
// lib/env.ts
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  AUTH_SECRET: z.string().min(32),
  NEXT_PUBLIC_APP_URL: z.string().url(),
});

export const env = envSchema.parse(process.env);
```

- Use `server-only` package to hard-fail if a server module is accidentally imported client-side:
  ```ts
  import 'server-only'; // throws at build time if bundled for the client
  ```

### Error Handling

- Every route segment should have an `error.tsx` Client Component
- Use `notFound()` to render `not-found.tsx`
- Return typed result objects from Server Functions instead of throwing — use `useActionState` to display errors
- Use `onRequestError` in `instrumentation.ts` to capture all unhandled server errors in one place

### Metadata & SEO

- Define metadata in `layout.tsx` / `page.tsx` using the `metadata` export or `generateMetadata` function
- In Next.js 15.2+, `generateMetadata` is **streaming** — it no longer blocks the initial page render for end users (bots still receive blocking metadata)

```ts
export async function generateMetadata({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await getProduct(id);
  return {
    title: product.name,
    openGraph: { images: [product.imageUrl] },
  };
}
```

## Examples

```tsx
// app/dashboard/page.tsx — PPR + streaming + use cache
export const experimental_ppr = true;

import { Suspense } from 'react';
import { after } from 'next/server';

export default async function DashboardPage() {
  after(() => analytics.track('dashboard_viewed'));

  return (
    <main className="p-6">
      <h1>Dashboard</h1>
      {/* Static shell — rendered at build time */}
      <QuickStats />
      {/* Dynamic hole — streamed at request time */}
      <Suspense fallback={<FeedSkeleton />}>
        <ActivityFeed />
      </Suspense>
    </main>
  );
}

// Cached data fetch — revalidates every hour
async function getActivityFeed(userId: string) {
  'use cache';
  cacheLife('hours');
  return db.activity.findMany({ where: { userId }, orderBy: { createdAt: 'desc' }, take: 20 });
}
```

## References

- [Next.js 15 Release Notes](https://nextjs.org/blog/next-15)
- [Next.js 15.2 Release Notes](https://nextjs.org/blog/next-15-2)
- [Next.js Documentation](https://nextjs.org/docs)
- [`use cache` directive](https://nextjs.org/docs/app/api-reference/directives/use-cache)
- [Partial Prerendering](https://nextjs.org/docs/app/building-your-application/rendering/partial-prerendering)
- [`after()` API](https://nextjs.org/docs/app/api-reference/functions/after)
- [React 19 – `useActionState`](https://react.dev/reference/react/useActionState)
- [React Compiler](https://react.dev/learn/react-compiler)
- [Turbopack](https://turbo.build/pack/docs)
