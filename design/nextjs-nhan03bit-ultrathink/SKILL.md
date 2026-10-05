---
name: nextjs
description: "Next.js 15 App Router deep dive — React Server Components, Server Actions, Suspense streaming SSR, Error Boundaries, parallel and intercepting routes, data prefetching, edge functions, Vercel deployment patterns, and performance best practices. Absorbs server-components, server-actions, suspense, error-boundary, parallel-routes, intercepting-routes, prefetch, edge-functions, vercel, vercel-react-best-practices."
layer: domain
category: frontend
triggers: ["@slot", "ErrorBoundary", "RSC", "React.lazy", "Suspense boundary", "app router", "bundle size", "cloudflare worker", "data preload", "edge computing", "edge config", "edge function", "edge middleware", "edge runtime", "edge-side", "error boundary", "error recovery", "error.tsx", "fallback ui", "form action", "generateStaticParams", "independent loading", "intercepted route", "intercepting routes", "lazy", "link prefetch", "loading fallback", "middleware", "modal route", "next.js", "next.js optimization", "next.js performance", "next/image", "next/link", "nextjs", "parallel route", "parallel routes", "photo modal", "prefetch", "prefetching", "preload", "react best practices", "react error boundary", "react performance", "react performance patterns", "revalidate", "revalidatePath", "revalidateTag", "route interception", "route prefetch", "rsc", "rsc payload", "server action", "server actions", "server client boundary", "server component", "server mutation", "server-only", "simultaneous rendering", "slot convention", "soft navigation modal", "stale while revalidate", "suspense", "suspense boundary", "use hook", "use server", "vercel", "vercel best practices", "vercel cron", "vercel deploy", "vercel edge", "vercel kv", "vercel middleware", "vercel.json"]
---

# nextjs

Next.js 15 App Router deep dive — React Server Components, Server Actions, Suspense streaming SSR, Error Boundaries, parallel and intercepting routes, data prefetching, edge functions, Vercel deployment patterns, and performance best practices. Absorbs server-components, server-actions, suspense, error-boundary, parallel-routes, intercepting-routes, prefetch, edge-functions, vercel, vercel-react-best-practices.


## Absorbs

- `server-components`
- `server-actions`
- `suspense`
- `error-boundary`
- `parallel-routes`
- `intercepting-routes`
- `prefetch`
- `edge-functions`
- `vercel`
- `vercel-react-best-practices`


## Core

# Next.js App Router & RSC Patterns

## Purpose

Provide expert guidance on Next.js 14+ App Router architecture, React Server Components, data fetching strategies, caching, and production deployment patterns. This skill focuses on the App Router paradigm and modern Next.js conventions.

## Key Patterns

### File System Routing

**Route Hierarchy:**

```
app/
  layout.tsx          # Root layout (wraps everything)
  page.tsx            # Home route /
  loading.tsx         # Suspense fallback for /
  error.tsx           # Error boundary for /
  not-found.tsx       # 404 for /
  global-error.tsx    # Root error boundary (replaces layout)

  dashboard/
    layout.tsx        # Nested layout for /dashboard/*
    page.tsx          # /dashboard
    loading.tsx       # Suspense for /dashboard

    settings/
      page.tsx        # /dashboard/settings

    [teamId]/
      page.tsx        # /dashboard/:teamId (dynamic)

    [...slug]/
      page.tsx        # /dashboard/* (catch-all)

  (marketing)/        # Route group (no URL impact)
    about/
      page.tsx        # /about
    pricing/
      page.tsx        # /pricing

  @modal/             # Parallel route (named slot)
    (.)photo/[id]/
      page.tsx        # Intercepted route

  api/
    route.ts          # API route /api
```

**Special Files Priority:** `layout > template > error > loading > not-found > page`

### Server vs Client Components

**Default: Server Components.** Only add `'use client'` when you need:
- Event handlers (`onClick`, `onChange`, etc.)
- State or effects (`useState`, `useEffect`, `useReducer`)
- Browser-only APIs (`window`, `localStorage`, `IntersectionObserver`)
- Custom hooks that use the above
- Third-party components that require client context

**Push client boundaries down:**

```tsx
// GOOD: Server component with small client island
// app/dashboard/page.tsx (Server Component)
import { getStats } from '@/lib/data';
import { StatsChart } from '@/components/stats-chart'; // client component

export default async function DashboardPage() {
  const stats = await getStats(); // runs on server, no waterfall
  return (
    <section className="py-16">
      <h1 className="text-2xl font-bold mb-8">Dashboard</h1>
      {/* Pass serializable data to client component */}
      <StatsChart data={stats} />
    </section>
  );
}

// components/stats-chart.tsx
'use client';
import { useState } from 'react';

export function StatsChart({ data }: { data: StatsData }) {
  const [range, setRange] = useState<'week' | 'month'>('week');
  // Interactive chart logic...
}
```

**BAD: Making entire page client-side:**

```tsx
// AVOID: Entire page as client component
'use client'; // This kills SSR benefits for the whole subtree
export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  useEffect(() => { fetch('/api/stats').then(/* waterfall! */) }, []);
}
```

### Data Fetching

**Server Components — fetch directly:**

```tsx
// Automatic request deduplication within a render pass
async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await fetch(`https://api.example.com/products/${id}`, {
    next: { revalidate: 3600 }, // ISR: revalidate every hour
  }).then(r => r.json());

  return <ProductDetail product={product} />;
}
```

**Parallel Data Fetching — avoid waterfalls:**

```tsx
// GOOD: Parallel fetches
async function DashboardPage() {
  const [user, stats, notifications] = await Promise.all([
    getUser(),
    getStats(),
    getNotifications(),
  ]);
  return (/* ... */);
}

// ALSO GOOD: Suspense streaming
async function DashboardPage() {
  const userPromise = getUser();
  const statsPromise = getStats();

  return (
    <div>
      <Suspense fallback={<UserSkeleton />}>
        <UserSection userPromise={userPromise} />
      </Suspense>
      <Suspense fallback={<StatsSkeleton />}>
        <StatsSection statsPromise={statsPromise} />
      </Suspense>
    </div>
  );
}
```

### Caching & Revalidation

**Cache Hierarchy (Next.js 15+):**

| Layer | Scope | Default | Control |
|-------|-------|---------|---------|
| Request Memoization | Single render pass | ON | `React.cache()` |
| Data Cache | Cross-request | OFF (Next 15) | `fetch({ next: { revalidate } })` |
| Full Route Cache | Static routes | ON for static | `export const dynamic` |
| Router Cache | Client-side | ON (reduced in 15) | `router.refresh()` |

**Revalidation Strategies:**

```tsx
// Time-based revalidation
export const revalidate = 3600; // Page-level: revalidate every hour

// On-demand revalidation via Server Action
'use server';
import { revalidatePath, revalidateTag } from 'next/cache';

export async function publishPost(id: string) {
  await db.post.update({ where: { id }, data: { published: true } });
  revalidatePath('/blog');           // Revalidate specific path
  revalidateTag('posts');            // Revalidate by cache tag
}

// Tag-based fetch caching
const posts = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'], revalidate: 3600 },
});
```

**Dynamic vs Static:**

```tsx
// Force dynamic rendering
export const dynamic = 'force-dynamic';

// Force static generation
export const dynamic = 'force-static';

// Generate static params for dynamic routes
export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map(post => ({ slug: post.slug }));
}
```

### Server Actions

```tsx
// app/actions.ts
'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
});

export async function createPost(prevState: ActionState, formData: FormData) {
  const parsed = CreatePostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  try {
    await db.post.create({ data: parsed.data });
    revalidatePath('/posts');
    return { success: true };
  } catch (e) {
    return { error: { _form: ['Failed to create post'] } };
  }
}
```

```tsx
// app/posts/new/page.tsx
'use client';

import { useActionState } from 'react';
import { createPost } from '@/app/actions';

export default function NewPostPage() {
  const [state, formAction, isPending] = useActionState(createPost, null);

  return (
    <form action={formAction} className="space-y-6 max-w-2xl">
      <div>
        <label htmlFor="title" className="block text-base font-medium mb-2">Title</label>
        <input
          id="title"
          name="title"
          className="w-full px-4 py-3 rounded-lg border transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2"
        />
        {state?.error?.title && (
          <p className="text-red-600 text-sm mt-1">{state.error.title[0]}</p>
        )}
      </div>
      <button
        type="submit"
        disabled={isPending}
        className="px-6 py-4 text-base rounded-lg bg-blue-600 text-white transition-all duration-200 hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50"
      >
        {isPending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  );
}
```

### Middleware

```tsx
// middleware.ts (root level)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Auth check
  const token = request.cookies.get('session')?.value;
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Add headers
  const response = NextResponse.next();
  response.headers.set('x-pathname', request.nextUrl.pathname);
  return response;
}

export const config = {
  matcher: [
    // Match all paths except static files and API
    '/((?!_next/static|_next/image|favicon.ico|api).*)',
  ],
};
```

### Metadata & SEO

```tsx
// Static metadata
export const metadata: Metadata = {
  title: 'My App',
  description: 'Description here',
  openGraph: { title: 'My App', description: '...' },
};

// Dynamic metadata
export async function generateMetadata(
  { params }: { params: Promise<{ slug: string }> }
): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      images: [post.coverImage],
    },
  };
}
```

### Image & Font Optimization

```tsx
import Image from 'next/image';
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

// Image with proper sizing
<Image
  src={product.image}
  alt={product.name}
  width={800}
  height={600}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  className="rounded-xl"
  priority={isAboveFold}
/>
```

## Best Practices

1. **Server Components by default** — Only add `'use client'` when browser APIs or interactivity are needed.
2. **Colocate data fetching** — Fetch data in the component that needs it. Request deduplication handles the rest.
3. **Stream with Suspense** — Wrap slow data sources in `<Suspense>` to stream HTML incrementally.
4. **Never fetch from client to your own API routes** — Use Server Actions or direct database access in Server Components.
5. **Use `loading.tsx`** — Provides instant loading states via Suspense.
6. **Validate Server Action inputs** — Always validate with Zod or similar. Never trust client data.
7. **Use `next/image`** — Automatic WebP/AVIF, lazy loading, and responsive sizing.
8. **Use `next/font`** — Zero layout shift, self-hosted font files.
9. **Prefer `revalidatePath`/`revalidateTag`** — Over `router.refresh()` for cache invalidation.
10. **Keep middleware lean** — It runs on every matched request. No heavy computation or database calls.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| `'use client'` at page level | Entire page loses SSR benefits | Push client boundary to smallest component |
| Fetching own API routes from RSC | Unnecessary network hop | Call database/service directly in RSC |
| Missing `loading.tsx` | White flash during navigation | Add loading files for major route segments |
| Sequential awaits in RSC | Waterfall data fetching | Use `Promise.all()` or parallel Suspense |
| Huge client bundles | Slow hydration | Dynamic import heavy components, keep client islands small |
| Not using `sizes` on Image | Full-size image downloaded on mobile | Always set responsive `sizes` prop |
| Mutating in GET handlers | Caching serves stale mutations | Use POST/PUT/DELETE or Server Actions for mutations |
| Accessing `searchParams` synchronously | Next.js 15 made params async | `await params` and `await searchParams` |
| No error boundaries | Entire page crashes on component error | Use `error.tsx` per route segment |
| Hardcoding secrets client-side | Security leak | Use `NEXT_PUBLIC_` prefix only for truly public values |


---

## From `server-components`

> React Server Components deep dive — RSC payload, streaming SSR, server/client boundaries, data patterns

# React Server Components

## Purpose

Provide expert guidance on React Server Components (RSC) architecture, including server/client boundary decisions, data fetching patterns, streaming SSR, RSC payload optimization, and common patterns for building performant applications with the App Router in Next.js 14+.

## Key Patterns

### Server vs Client Components

**Default to Server Components.** Only add `"use client"` when you need browser APIs, event handlers, or React state/effects.

| Feature | Server Component | Client Component |
|---------|-----------------|------------------|
| `async/await` for data | Yes | No (use hooks) |
| Database/file access | Yes | No |
| `useState`, `useEffect` | No | Yes |
| Event handlers (`onClick`) | No | Yes |
| Browser APIs (`window`, `localStorage`) | No | Yes |
| Bundle size impact | Zero JS sent | Adds to bundle |
| Re-renders on state change | No | Yes |

**Decision tree:**

```
Does it need useState/useEffect/event handlers?
  YES -> "use client"
  NO  -> Does it fetch data or access server resources?
    YES -> Server Component (default)
    NO  -> Server Component (default, still zero JS)
```

### Server/Client Boundary Architecture

Push `"use client"` boundaries as deep as possible in the component tree. Keep data fetching and layout in Server Components, and only wrap interactive leaf components as Client Components.

```tsx
// app/products/page.tsx -- Server Component (default)
import { Suspense } from "react";
import { ProductList } from "./product-list";
import { ProductFilters } from "./product-filters"; // "use client"
import { Skeleton } from "@/components/skeleton";

export default async function ProductsPage({
  searchParams,
}: {
  searchParams: Promise<{ category?: string; sort?: string }>;
}) {
  const params = await searchParams;

  return (
    <div className="flex gap-8">
      {/* Client Component for interactive filters */}
      <aside className="w-64">
        <ProductFilters
          initialCategory={params.category}
          initialSort={params.sort}
        />
      </aside>

      {/* Server Component with streaming */}
      <main className="flex-1">
        <Suspense fallback={<Skeleton count={12} />}>
          <ProductList
            category={params.category}
            sort={params.sort}
          />
        </Suspense>
      </main>
    </div>
  );
}
```

```tsx
// app/products/product-list.tsx -- Server Component
import { db } from "@/lib/db";

export async function ProductList({
  category,
  sort,
}: {
  category?: string;
  sort?: string;
}) {
  const products = await db.query.products.findMany({
    where: category ? eq(products.category, category) : undefined,
    orderBy: sort === "price" ? asc(products.price) : desc(products.createdAt),
  });

  return (
    <div className="grid grid-cols-3 gap-6">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

```tsx
// app/products/product-filters.tsx -- Client Component
"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useTransition } from "react";

export function ProductFilters({
  initialCategory,
  initialSort,
}: {
  initialCategory?: string;
  initialSort?: string;
}) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isPending, startTransition] = useTransition();

  function updateFilter(key: string, value: string) {
    const params = new URLSearchParams(searchParams.toString());
    if (value) {
      params.set(key, value);
    } else {
      params.delete(key);
    }
    startTransition(() => {
      router.push(`/products?${params.toString()}`);
    });
  }

  return (
    <div className={`p-6 rounded-xl shadow-sm ${isPending ? "opacity-60" : ""}`}>
      <select
        defaultValue={initialCategory}
        onChange={(e) => updateFilter("category", e.target.value)}
        className="px-4 py-3 rounded-lg border w-full transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2"
      >
        <option value="">All Categories</option>
        <option value="electronics">Electronics</option>
        <option value="clothing">Clothing</option>
      </select>
    </div>
  );
}
```

### Composition Pattern: Server Components as Children

Pass Server Components as `children` to Client Components to avoid pulling them into the client bundle.

```tsx
// app/layout.tsx -- Server Component
import { AuthProvider } from "./auth-provider"; // "use client"
import { Sidebar } from "./sidebar"; // Server Component

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <div className="flex">
        <Sidebar />
        <main className="flex-1">{children}</main>
      </div>
    </AuthProvider>
  );
}
```

```tsx
// app/auth-provider.tsx -- Client Component
"use client";

import { SessionProvider } from "next-auth/react";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  // children (including Server Components) are pre-rendered on the server
  // and passed as the RSC payload -- not re-rendered on the client
  return <SessionProvider>{children}</SessionProvider>;
}
```

### Data Fetching Patterns

**Pattern 1: Direct database access in Server Components**

```tsx
import { db } from "@/lib/db";

async function UserProfile({ userId }: { userId: string }) {
  const user = await db.query.users.findFirst({
    where: eq(users.id, userId),
    with: { posts: { limit: 10 } },
  });

  if (!user) notFound();

  return (
    <div className="p-6 rounded-xl shadow-sm">
      <h1 className="text-2xl font-bold">{user.name}</h1>
      <p className="text-base text-gray-600">{user.bio}</p>
    </div>
  );
}
```

**Pattern 2: Parallel data fetching**

```tsx
async function Dashboard() {
  const [stats, recentOrders, notifications] = await Promise.all([
    getStats(),
    getRecentOrders(),
    getNotifications(),
  ]);

  return (
    <div className="grid grid-cols-3 gap-6">
      <StatsCard stats={stats} />
      <OrderList orders={recentOrders} />
      <NotificationList notifications={notifications} />
    </div>
  );
}
```

**Pattern 3: Streaming with Suspense boundaries**

```tsx
async function Page() {
  return (
    <div>
      {/* Fast: renders immediately */}
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* Streams in when ready */}
      <Suspense fallback={<StatsSkeleton />}>
        <StatsSection />
      </Suspense>

      {/* Independent stream -- does not block above */}
      <Suspense fallback={<OrdersSkeleton />}>
        <RecentOrders />
      </Suspense>

      {/* Slow query streams last */}
      <Suspense fallback={<AnalyticsSkeleton />}>
        <AnalyticsChart />
      </Suspense>
    </div>
  );
}
```

### Server Actions

Server-side mutations callable from Client Components.

```tsx
// app/actions.ts
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { db } from "@/lib/db";
import { z } from "zod";

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
});

export async function createPost(formData: FormData) {
  const parsed = createPostSchema.safeParse({
    title: formData.get("title"),
    content: formData.get("content"),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  const post = await db.insert(posts).values(parsed.data).returning();

  revalidatePath("/posts");
  redirect(`/posts/${post[0].id}`);
}
```

```tsx
// app/posts/new/page.tsx -- Client Component using Server Action
"use client";

import { useActionState } from "react";
import { createPost } from "../actions";

export default function NewPostPage() {
  const [state, formAction, isPending] = useActionState(createPost, null);

  return (
    <form action={formAction} className="space-y-6 max-w-2xl">
      <div>
        <label htmlFor="title" className="block text-base font-medium mb-2">
          Title
        </label>
        <input
          id="title"
          name="title"
          className="px-4 py-3 rounded-lg border w-full transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2"
        />
        {state?.error?.title && (
          <p className="text-red-600 text-sm mt-1">{state.error.title}</p>
        )}
      </div>

      <div>
        <label htmlFor="content" className="block text-base font-medium mb-2">
          Content
        </label>
        <textarea
          id="content"
          name="content"
          rows={8}
          className="px-4 py-3 rounded-lg border w-full transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2"
        />
        {state?.error?.content && (
          <p className="text-red-600 text-sm mt-1">{state.error.content}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isPending}
        className="px-6 py-4 text-base rounded-lg bg-blue-600 text-white transition-all duration-200 hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50"
      >
        {isPending ? "Publishing..." : "Publish"}
      </button>
    </form>
  );
}
```

### Protecting Server-Only Code

Prevent accidental import of server code into Client Components.

```typescript
// lib/db.ts
import "server-only"; // Throws build error if imported in a Client Component

import { drizzle } from "drizzle-orm/neon-http";

export const db = drizzle(process.env.DATABASE_URL!);
```

```typescript
// lib/auth.ts
import "server-only";

import { cookies } from "next/headers";

export async function getSession() {
  const cookieStore = await cookies();
  const token = cookieStore.get("session")?.value;
  if (!token) return null;
  return verifyToken(token);
}
```

### RSC Payload Optimization

Keep the RSC payload small by avoiding passing large data through component props.

```tsx
// BAD: Entire product object serialized in RSC payload
async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await getProduct(id); // 50 fields
  return <ProductView product={product} />;
}

// GOOD: Only pass what the component needs
async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await getProduct(id);
  return (
    <ProductView
      name={product.name}
      price={product.price}
      image={product.image}
      description={product.description}
    />
  );
}
```

**Avoid serializing non-serializable values:**

```tsx
// BAD: Functions cannot be serialized across the server/client boundary
<ClientComponent onClick={() => console.log("click")} />

// GOOD: Use Server Actions for server-side logic
<ClientComponent action={serverAction} />

// GOOD: Handle events in the Client Component itself
<ClientComponent productId={product.id} />
```

## Best Practices

- **Default to Server Components** -- only add `"use client"` when you need interactivity, state, or browser APIs.
- **Push client boundaries down** -- wrap the smallest interactive subtree, not entire pages.
- **Use `server-only` package** to guard server code from accidental client import.
- **Fetch data in Server Components** directly -- no need for API routes or `useEffect` + `fetch`.
- **Use `Promise.all` for parallel fetches** -- do not `await` sequentially unless data depends on each other.
- **Wrap slow data fetches in `<Suspense>`** -- stream the shell immediately and fill in data as it resolves.
- **Pass Server Components as `children`** to Client Components to keep them out of the client bundle.
- **Validate Server Action inputs** with Zod -- never trust form data from the client.
- **Use `revalidatePath` or `revalidateTag`** after mutations to refresh cached data.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Adding `"use client"` to a page component | Entire page tree becomes client-rendered, losing RSC benefits | Keep page as Server Component; extract interactive parts into Client child components |
| Importing `useState` in a Server Component | Build error: hooks only work in Client Components | Move stateful logic to a `"use client"` child component |
| Passing functions as props across boundary | Serialization error: functions are not serializable | Use Server Actions (`"use server"`) or handle events inside the Client Component |
| Sequential `await` in Server Components | Waterfall: each fetch waits for the previous one | Use `Promise.all()` for independent data or Suspense for parallel streaming |
| Importing `server-only` modules in Client Components | Build error (good) or runtime error (bad without `server-only`) | Add `import "server-only"` to all files that use `process.env`, DB, cookies, etc. |
| Huge RSC payload | Slow initial load due to large serialized props | Only pass necessary fields; avoid serializing entire database rows |
| Not using Suspense boundaries | Entire page blocked until slowest query resolves | Wrap independent data sections in separate `<Suspense>` boundaries |
| Mutating data without revalidation | UI shows stale data after Server Action | Call `revalidatePath()` or `revalidateTag()` at the end of every mutation |


---

## From `server-actions`

> Next.js Server Actions — "use server", form actions, revalidation, optimistic updates with useOptimistic, progressive enhancement

# Server Actions Skill

## Purpose

Server Actions are Next.js's RPC mechanism: async functions on the server, callable from client components. They replace API routes for mutations, provide progressive enhancement, and integrate with React's concurrent features.

## Server Action with Validation

```typescript
// app/actions/posts.ts
'use server';

import { revalidateTag } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';

const createPostSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200),
  content: z.string().min(10, 'Content must be at least 10 characters'),
});

export type ActionState = {
  success: boolean;
  errors?: Record<string, string[]>;
  message?: string;
};

export async function createPost(prev: ActionState, formData: FormData): Promise<ActionState> {
  const parsed = createPostSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { success: false, errors: parsed.error.flatten().fieldErrors };

  const session = await getSession();
  if (!session?.user) return { success: false, message: 'Unauthorized' };

  try {
    await db.post.create({ data: { ...parsed.data, authorId: session.user.id } });
  } catch {
    return { success: false, message: 'Failed to create post' };
  }

  revalidateTag('posts');
  redirect('/posts');
}
```

## Form with useActionState

```typescript
'use client';

import { useActionState } from 'react';
import { createPost, type ActionState } from '@/app/actions/posts';

export function CreatePostForm() {
  const [state, formAction, isPending] = useActionState(createPost, { success: false });

  return (
    <form action={formAction} className="space-y-4">
      <div>
        <label htmlFor="title">Title</label>
        <input id="title" name="title" required className="w-full rounded-lg border px-4 py-3" />
        {state.errors?.title && <p className="text-sm text-red-600">{state.errors.title[0]}</p>}
      </div>
      <div>
        <label htmlFor="content">Content</label>
        <textarea id="content" name="content" required className="w-full rounded-lg border px-4 py-3" />
        {state.errors?.content && <p className="text-sm text-red-600">{state.errors.content[0]}</p>}
      </div>
      <button type="submit" disabled={isPending}
        className="rounded-lg bg-blue-600 px-6 py-4 text-white transition-all duration-200 hover:bg-blue-700 disabled:opacity-50">
        {isPending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  );
}
```

## Optimistic Updates

```typescript
'use client';

import { useOptimistic, useTransition } from 'react';
import { toggleLike } from '@/app/actions/likes';

export function LikeButton({ postId, liked, count }: LikeButtonProps) {
  const [isPending, startTransition] = useTransition();
  const [optimistic, setOptimistic] = useOptimistic(
    { liked, count },
    (current, newLiked: boolean) => ({
      liked: newLiked,
      count: current.count + (newLiked ? 1 : -1),
    })
  );

  return (
    <button onClick={() => startTransition(async () => {
      setOptimistic(!optimistic.liked);
      await toggleLike(postId);
    })} disabled={isPending}>
      {optimistic.liked ? 'Unlike' : 'Like'} ({optimistic.count})
    </button>
  );
}
```

## Revalidation Strategies

```typescript
'use server';
import { revalidatePath, revalidateTag } from 'next/cache';

revalidatePath('/posts');                    // Revalidate a specific page
revalidatePath('/posts/[slug]', 'page');     // Revalidate all post pages
revalidatePath('/', 'layout');               // Revalidate everything

revalidateTag('posts');                      // Tag-based (more precise)
revalidateTag(`post-${id}`);                 // Revalidate specific post data

// Tag fetches for invalidation
const posts = await fetch(url, { next: { tags: ['posts'] } });
```

## Best Practices

1. **Always validate inputs** with Zod — never trust client data
2. **Check auth inside the action**, not just in middleware
3. **Return structured errors** instead of throwing — enables field-level UI messages
4. **Use `revalidateTag`** over `revalidatePath` for precise invalidation
5. **Don't call `redirect()` inside try/catch** — redirect throws internally
6. **Use `useActionState`** over manual useState + startTransition for forms
7. **Keep actions in separate `'use server'` files** for clear boundaries


---

## From `suspense`

> React Suspense patterns including Suspense boundaries, React.lazy, loading.tsx in Next.js, use() hook, data fetching with Suspense, and streaming SSR

# React Suspense Skill

## Purpose

Suspense lets you declaratively specify loading states while components wait for async operations (code loading, data fetching). This skill covers Suspense boundaries, lazy loading, Next.js integration, and the `use()` hook for Suspense-compatible data fetching.

## Key Patterns

### Suspense Boundary Basics

```tsx
import { Suspense } from "react";

export default function Dashboard() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <Suspense fallback={<DashboardSkeleton />}>
        <DashboardContent />
      </Suspense>
    </div>
  );
}

function DashboardSkeleton() {
  return (
    <div className="animate-pulse space-y-4 py-16">
      <div className="h-8 w-1/3 rounded-lg bg-gray-200 dark:bg-gray-800" />
      <div className="h-32 rounded-xl bg-gray-200 dark:bg-gray-800" />
    </div>
  );
}
```

### React.lazy for Code Splitting

```tsx
import { lazy, Suspense } from "react";

// Only loaded when rendered
const HeavyChart = lazy(() => import("@/components/heavy-chart"));
const MarkdownEditor = lazy(() => import("@/components/markdown-editor"));

export default function AnalyticsPage() {
  return (
    <Suspense fallback={<div className="h-64 animate-pulse rounded-xl bg-gray-100" />}>
      <HeavyChart />
    </Suspense>
  );
}

// Named export lazy loading
const Settings = lazy(() =>
  import("@/components/settings").then((mod) => ({ default: mod.Settings }))
);
```

### Next.js loading.tsx (Automatic Suspense)

```tsx
// app/dashboard/loading.tsx — Next.js wraps page in Suspense automatically
export default function Loading() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600" />
    </div>
  );
}
```

### Nested Suspense Boundaries

```tsx
// Granular loading: each section loads independently
export default function Page() {
  return (
    <div className="space-y-8 py-16">
      <Suspense fallback={<HeaderSkeleton />}>
        <UserHeader />
      </Suspense>

      <div className="grid grid-cols-2 gap-6">
        <Suspense fallback={<CardSkeleton />}>
          <RecentActivity />
        </Suspense>
        <Suspense fallback={<CardSkeleton />}>
          <Stats />
        </Suspense>
      </div>
    </div>
  );
}
```

### The use() Hook (React 19+)

```tsx
// use() unwraps promises and integrates with Suspense
import { use, Suspense } from "react";

async function fetchUser(id: string) {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error("Failed to fetch user");
  return res.json() as Promise<{ name: string; email: string }>;
}

function UserProfile({ userPromise }: { userPromise: Promise<{ name: string; email: string }> }) {
  const user = use(userPromise);
  return (
    <div className="rounded-xl p-6 shadow-sm">
      <h2 className="text-xl font-semibold">{user.name}</h2>
      <p className="text-gray-600 dark:text-gray-400">{user.email}</p>
    </div>
  );
}

// Parent creates the promise, child consumes with use()
export default function Page({ params }: { params: { id: string } }) {
  const userPromise = fetchUser(params.id);
  return (
    <Suspense fallback={<ProfileSkeleton />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}
```

### Streaming SSR with Suspense (Next.js App Router)

```tsx
// Server Components + Suspense = streaming
// Each Suspense boundary streams its content as it resolves

// app/page.tsx (Server Component)
import { Suspense } from "react";

async function SlowData() {
  const data = await fetch("https://api.example.com/slow", { cache: "no-store" });
  const result = await data.json();
  return <pre>{JSON.stringify(result, null, 2)}</pre>;
}

export default function Page() {
  return (
    <main>
      <h1>Instant shell</h1>
      <Suspense fallback={<p>Loading data...</p>}>
        <SlowData />  {/* Streams in when ready */}
      </Suspense>
    </main>
  );
}
```

## Best Practices

- **Pair with Error Boundaries**: Every `<Suspense>` should have a sibling or parent `<ErrorBoundary>`.
- **Granular boundaries**: Wrap independent sections separately so fast content is not blocked by slow.
- **Meaningful skeletons**: Match the skeleton shape to the real content to reduce layout shift.
- **Lift promises up**: Create promises in parent, pass to child. This starts fetching before rendering.
- **Avoid Suspense waterfalls**: Do not nest async components sequentially. Fetch in parallel where possible.
- **loading.tsx per route**: In Next.js, each route segment can have its own loading state.

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Entire page shows spinner | Use nested Suspense boundaries for independent sections |
| Waterfall fetches | Start all fetches at the same level, pass promises down |
| Missing error handling | Add ErrorBoundary around Suspense boundaries |
| Layout shift on load | Use skeleton components that match final content dimensions |
| Lazy component flickers | Only lazy-load components that are large or conditionally rendered |


---

## From `error-boundary`

> React Error Boundaries including class-based ErrorBoundary, Next.js App Router error.tsx, fallback UI design, error recovery, retry patterns, and error reporting integration

# React Error Boundaries Skill

## Purpose

Prevent a single component crash from taking down the entire application. Error boundaries catch rendering errors, display fallback UI, enable recovery, and report errors to monitoring services.

## Error Boundary Types

| Type | Scope | File | Framework |
|------|-------|------|-----------|
| **Class ErrorBoundary** | Any component tree | Custom component | React 16+ |
| **error.tsx** | Route segment | `app/[route]/error.tsx` | Next.js App Router |
| **global-error.tsx** | Entire app (root layout) | `app/global-error.tsx` | Next.js App Router |
| **Suspense + ErrorBoundary** | Async boundaries | Composition | React 18+ |

## Key Patterns

### 1. Reusable Class-Based ErrorBoundary

```tsx
'use client';
import { Component, type ErrorInfo, type ReactNode } from 'react';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, reset: () => void) => ReactNode);
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.props.onError?.(error, errorInfo);
  }

  reset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      if (typeof this.props.fallback === 'function') {
        return this.props.fallback(this.state.error, this.reset);
      }
      return this.props.fallback ?? <DefaultFallback error={this.state.error} reset={this.reset} />;
    }
    return this.props.children;
  }
}

function DefaultFallback({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div role="alert" className="p-6 rounded-xl border border-red-200 bg-red-50">
      <h2 className="text-lg font-semibold text-red-800">Something went wrong</h2>
      <p className="mt-2 text-red-600">{error.message}</p>
      <button
        onClick={reset}
        className="mt-4 px-6 py-4 text-base rounded-lg bg-red-600 text-white
                   hover:bg-red-700 transition-all duration-200
                   focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-red-500"
      >
        Try again
      </button>
    </div>
  );
}
```

### 2. Next.js App Router error.tsx

```tsx
// app/dashboard/error.tsx -- catches errors in the dashboard route segment
'use client';

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Report to error monitoring
    reportError(error);
  }, [error]);

  return (
    <div role="alert" className="p-8 rounded-2xl border shadow-sm max-w-lg mx-auto mt-16">
      <h2 className="text-xl font-bold">Dashboard Error</h2>
      <p className="mt-2 text-gray-600">
        {error.digest
          ? 'An unexpected error occurred. Our team has been notified.'
          : error.message}
      </p>
      <button
        onClick={reset}
        className="mt-6 px-6 py-4 text-base rounded-lg bg-blue-600 text-white
                   hover:bg-blue-700 transition-all duration-200
                   focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
      >
        Try again
      </button>
    </div>
  );
}
```

### 3. Global Error Handler (Root Layout Crash)

```tsx
// app/global-error.tsx -- only catches errors in root layout
'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <div className="min-h-screen flex items-center justify-center p-8">
          <div className="p-8 rounded-2xl border shadow-sm max-w-md text-center">
            <h1 className="text-2xl font-bold">Something went wrong</h1>
            <p className="mt-4 text-gray-600">
              An unexpected error occurred. Please try refreshing the page.
            </p>
            <button
              onClick={reset}
              className="mt-6 px-6 py-4 text-base rounded-lg bg-blue-600 text-white
                         hover:bg-blue-700 transition-all duration-200
                         focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
            >
              Try again
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}
```

### 4. Retry with Exponential Backoff

```tsx
'use client';
import { useCallback, useState } from 'react';

function useRetryableQuery<T>(fetcher: () => Promise<T>, maxRetries = 3) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  const execute = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const result = await fetcher();
        setData(result);
        setRetryCount(0);
        setIsLoading(false);
        return result;
      } catch (err) {
        if (attempt === maxRetries) {
          setError(err instanceof Error ? err : new Error(String(err)));
          setRetryCount(attempt);
          setIsLoading(false);
          throw err;
        }
        // Exponential backoff: 1s, 2s, 4s
        await new Promise((r) => setTimeout(r, 1000 * Math.pow(2, attempt)));
      }
    }
  }, [fetcher, maxRetries]);

  return { data, error, isLoading, retryCount, execute };
}
```

### 5. Granular Boundaries with Suspense

```tsx
import { Suspense } from 'react';
import { ErrorBoundary } from './ErrorBoundary';

export default function Dashboard() {
  return (
    <div className="grid grid-cols-2 gap-6 py-16">
      {/* Each widget isolated -- one crash does not affect others */}
      <ErrorBoundary fallback={(err, reset) => <WidgetError error={err} reset={reset} />}>
        <Suspense fallback={<WidgetSkeleton />}>
          <RevenueChart />
        </Suspense>
      </ErrorBoundary>

      <ErrorBoundary fallback={(err, reset) => <WidgetError error={err} reset={reset} />}>
        <Suspense fallback={<WidgetSkeleton />}>
          <UserStats />
        </Suspense>
      </ErrorBoundary>

      <ErrorBoundary fallback={(err, reset) => <WidgetError error={err} reset={reset} />}>
        <Suspense fallback={<WidgetSkeleton />}>
          <RecentOrders />
        </Suspense>
      </ErrorBoundary>
    </div>
  );
}
```

## Error Reporting Integration

```typescript
// lib/error-reporting.ts
export function reportError(error: Error, context?: Record<string, unknown>) {
  // Sentry
  if (typeof window !== 'undefined' && window.Sentry) {
    window.Sentry.captureException(error, { extra: context });
  }

  // Fallback: POST to your own endpoint
  fetch('/api/errors', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: error.message,
      stack: error.stack,
      context,
      timestamp: new Date().toISOString(),
      url: typeof window !== 'undefined' ? window.location.href : undefined,
    }),
  }).catch(() => {});
}
```

## Best Practices

1. **Wrap every independent UI section** in its own ErrorBoundary -- sidebar, main content, widgets
2. **Always provide a reset/retry action** -- do not show dead-end error screens
3. **Use `error.digest`** in Next.js to distinguish server errors (hide details) from client errors
4. **Report errors to monitoring** in `componentDidCatch` or `useEffect` in error.tsx
5. **Combine ErrorBoundary + Suspense** for async components -- catch both loading and error states
6. **Show contextual fallbacks** -- a chart error should show a chart-sized placeholder, not a full-page error
7. **Do not catch errors in event handlers** with ErrorBoundary -- use try/catch instead

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| No ErrorBoundary at all | One bad component crashes the entire app | Add boundaries at route and widget level |
| Only a global boundary | Entire page replaced by error UI for a small widget crash | Use granular boundaries per section |
| ErrorBoundary around event handlers | Errors in onClick/onSubmit are not caught | Use try/catch inside event handlers |
| Forgetting `'use client'` on error.tsx | Next.js build error | error.tsx must be a Client Component |
| No error reporting | Errors happen silently in production | Integrate Sentry or custom error endpoint |


---

## From `parallel-routes`

> Next.js parallel routes — @slot conventions, simultaneous rendering, independent loading/error states, conditional slots, and modal patterns

# Skill: parallel-routes
> Layer: domain | Category: frontend

## Triggers
- parallel routes, @slot, simultaneous rendering, dashboard layout, split views, Next.js slots

## Links
- linksTo: intercepting-routes, nextjs-app-router
- linkedFrom: nextjs-app-router

## Overview

Parallel routes render multiple pages simultaneously within the same layout using **named slots**.
Slots are defined by the `@folder` convention and passed as props to the parent layout.

## Slot Convention

A slot is a directory prefixed with `@`. It does NOT create a URL segment.

```
app/
  layout.tsx          # receives @analytics and @team as props
  page.tsx
  @analytics/
    page.tsx
    loading.tsx       # independent loading state
    error.tsx         # independent error boundary
  @team/
    page.tsx
    loading.tsx
```

```tsx
// app/layout.tsx
export default function Layout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  team: React.ReactNode;
}) {
  return (
    <div className="grid grid-cols-2 gap-6 py-16">
      <main>{children}</main>
      <aside>{analytics}</aside>
      <section>{team}</section>
    </div>
  );
}
```

## default.tsx — Unmatched Route Fallback

When a slot has no matching route for the current URL, Next.js renders `default.tsx`.
Without it, unmatched slots return a 404 on hard navigation.

```tsx
// app/@analytics/default.tsx
export default function AnalyticsDefault() {
  return <p>Select a date range to view analytics.</p>;
}
```

**Rule**: every parallel slot should have a `default.tsx` unless you explicitly want a 404.

## Independent Loading and Error States

Each slot streams independently — one slot can show a skeleton while another is ready.

```tsx
// app/@analytics/loading.tsx
export default function AnalyticsLoading() {
  return <div className="animate-pulse h-64 rounded-xl bg-muted" />;
}

// app/@analytics/error.tsx
"use client";
export default function AnalyticsError({ reset }: { reset: () => void }) {
  return (
    <div className="p-6 rounded-xl border border-destructive">
      <p>Analytics failed to load.</p>
      <button onClick={reset} className="px-6 py-4 text-base rounded-lg">
        Retry
      </button>
    </div>
  );
}
```

## Conditional Rendering

Use auth or feature flags to swap which slot content renders.

```tsx
// app/layout.tsx
import { auth } from "@/lib/auth";

export default async function Layout({
  children,
  admin,
  user,
}: {
  children: React.ReactNode;
  admin: React.ReactNode;
  user: React.ReactNode;
}) {
  const session = await auth();
  return (
    <div className="py-16">
      {children}
      {session?.role === "admin" ? admin : user}
    </div>
  );
}
```

## Key Rules

1. Slots are **not** URL segments — `@analytics/page.tsx` maps to `/`, not `/analytics`.
2. Soft navigation preserves previously active slot state even if the URL doesn't match.
3. Hard navigation (full reload) requires `default.tsx` for unmatched slots.
4. Combine with intercepting routes for modal patterns that overlay parallel slots.
5. Each slot can define its own `loading.tsx`, `error.tsx`, `not-found.tsx`, and nested layouts.


---

## From `intercepting-routes`

> Next.js intercepting routes — (.) (..) (...) conventions, modal overlays, photo galleries, share-able modals, route interception patterns

# Skill: intercepting-routes
> Layer: domain | Category: frontend

## Triggers
- intercepting routes, modal route, photo gallery modal, (.) (..) (...), route interception, shareable modal URL

## Links
- linksTo: parallel-routes, nextjs-app-router
- linkedFrom: parallel-routes, nextjs-app-router

## Overview

Intercepting routes let you load a route from another part of your app within the current layout.
The canonical use case: clicking a photo in a feed opens a modal, but navigating directly to
`/photo/123` renders the full page. The URL is shareable either way.

## Convention Syntax

| Pattern  | Matches                                    | Analogy       |
|----------|--------------------------------------------|---------------|
| `(.)`    | Same level                                 | `./`          |
| `(..)`   | One level up                               | `../`         |
| `(..)(..)` | Two levels up                            | `../../`      |
| `(...)`  | App root                                   | `/`           |

**Important**: levels are based on route segments, not filesystem directories.

## File Structure — Modal Pattern

```
app/
  layout.tsx
  @modal/
    (.)photo/[id]/
      page.tsx          # intercepted: renders inside modal
    default.tsx         # renders nothing when no modal is active
  feed/
    page.tsx            # photo grid
  photo/[id]/
    page.tsx            # full page: direct navigation or refresh
```

## Combining with Parallel Routes

The `@modal` slot is a parallel route that intercepts `/photo/[id]`.

```tsx
// app/layout.tsx
export default function RootLayout({
  children,
  modal,
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
        {modal}
      </body>
    </html>
  );
}
```

```tsx
// app/@modal/default.tsx
export default function Default() {
  return null;
}
```

## Intercepted Route (Modal View)

```tsx
// app/@modal/(.)photo/[id]/page.tsx
import { Modal } from "@/components/modal";
import { getPhoto } from "@/lib/data";

export default async function PhotoModal({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const photo = await getPhoto(id);

  return (
    <Modal>
      <img
        src={photo.url}
        alt={photo.alt}
        className="rounded-xl max-h-[80vh] object-contain"
      />
      <p className="p-6 text-base">{photo.description}</p>
    </Modal>
  );
}
```

## Full Page Route (Direct Navigation)

```tsx
// app/photo/[id]/page.tsx
import { getPhoto } from "@/lib/data";

export default async function PhotoPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const photo = await getPhoto(id);

  return (
    <main className="py-16 max-w-4xl mx-auto">
      <img src={photo.url} alt={photo.alt} className="rounded-xl w-full" />
      <h1 className="text-2xl font-bold mt-6">{photo.title}</h1>
      <p className="text-base mt-4">{photo.description}</p>
    </main>
  );
}
```

## Reusable Modal Component

```tsx
"use client";
import { useRouter } from "next/navigation";

export function Modal({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
      onClick={() => router.back()}
    >
      <div
        className="p-8 rounded-2xl bg-white shadow-xl max-w-2xl w-full"
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </div>
    </div>
  );
}
```

## Key Rules

1. Interception only works on **soft navigation** (client-side `<Link>`). Hard refresh loads the actual route.
2. Always pair with a parallel `@slot` so the modal overlays without replacing page content.
3. Provide `default.tsx` in the slot to avoid 404 on unmatched states.
4. The `(..)` depth counts route segments, not filesystem folders — `@modal` is not a segment.
5. Use `router.back()` to dismiss the modal and restore the previous URL.


---

## From `prefetch`

> Data prefetching patterns — Next.js Link prefetch, route prefetching, preloading data, React Query prefetch, stale-while-revalidate

# Skill: prefetch
> Layer: domain | Category: frontend

## Triggers
- prefetch, preload data, prefetchQuery, router.prefetch, hover preload, stale-while-revalidate, link prefetch

## Links
- linksTo: react-query, nextjs-app-router, server-components
- linkedFrom: react-query, nextjs-app-router

## Overview

Data prefetching loads resources before the user needs them, eliminating perceived latency.
Strategies range from automatic link prefetching to manual hover-triggered data preloading.

## Next.js Link Prefetch

Next.js automatically prefetches `<Link>` routes when they enter the viewport.

```tsx
import Link from "next/link";

// Automatic: prefetches when link scrolls into view (production only)
<Link href="/dashboard">Dashboard</Link>

// Disable prefetch for rarely visited routes
<Link href="/settings" prefetch={false}>Settings</Link>

// Force full page prefetch (not just loading boundary)
<Link href="/dashboard" prefetch={true}>Dashboard</Link>
```

| `prefetch` value | Behavior                                               |
|------------------|--------------------------------------------------------|
| `undefined`      | Prefetches up to the nearest `loading.tsx` boundary     |
| `true`           | Prefetches the full page data                           |
| `false`          | No prefetching — fetches on click                       |

## router.prefetch()

Programmatically prefetch a route before navigation.

```tsx
"use client";
import { useRouter } from "next/navigation";

export function ProjectCard({ id }: { id: string }) {
  const router = useRouter();

  return (
    <div
      className="p-6 rounded-xl shadow-sm border transition-all duration-200 hover:shadow-md"
      onMouseEnter={() => router.prefetch(`/project/${id}`)}
      onClick={() => router.push(`/project/${id}`)}
    >
      <h3 className="text-base font-semibold">Project {id}</h3>
    </div>
  );
}
```

## React Query — prefetchQuery

Prefetch data into the query cache so it is instantly available when the component mounts.

```tsx
import { useQueryClient } from "@tanstack/react-query";
import { getProject } from "@/lib/api";

export function ProjectLink({ id }: { id: string }) {
  const queryClient = useQueryClient();

  const prefetch = () => {
    queryClient.prefetchQuery({
      queryKey: ["project", id],
      queryFn: () => getProject(id),
      staleTime: 60_000, // won't refetch if data is < 60s old
    });
  };

  return (
    <a
      href={`/project/${id}`}
      onMouseEnter={prefetch}
      onFocus={prefetch}
      className="px-6 py-4 text-base rounded-lg transition-all duration-200
                 hover:bg-muted focus-visible:ring-2 focus-visible:ring-offset-2"
    >
      View Project
    </a>
  );
}
```

## Server Component Preloading Pattern

Preload functions let you start fetching data at the top of a server component tree.

```ts
// lib/data.ts
import { cache } from "react";

export const getUser = cache(async (id: string) => {
  const res = await fetch(`https://api.example.com/users/${id}`);
  return res.json();
});

// Call early to start the fetch — the cache deduplicates
export const preloadUser = (id: string) => {
  void getUser(id);
};
```

```tsx
// app/user/[id]/page.tsx
import { preloadUser, getUser } from "@/lib/data";

export default async function UserPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  preloadUser(id); // starts fetch immediately

  // other async work can happen here...

  const user = await getUser(id); // resolves instantly if already fetched
  return <h1 className="text-2xl font-bold py-16">{user.name}</h1>;
}
```

## Stale-While-Revalidate

Show cached data immediately while revalidating in the background.

```tsx
const { data } = useQuery({
  queryKey: ["projects"],
  queryFn: fetchProjects,
  staleTime: 30_000,       // fresh for 30s
  gcTime: 5 * 60_000,      // keep in cache for 5min
  refetchOnWindowFocus: true,
});
```

## Key Rules

1. Prefetch on **hover and focus** — not just hover — for keyboard accessibility.
2. Set `staleTime` when prefetching with React Query to avoid immediate refetch on mount.
3. Use `React.cache()` for server component data deduplication across the tree.
4. Avoid prefetching large payloads unconditionally — use viewport or hover triggers.
5. `router.prefetch()` caches the RSC payload; combine with data prefetching for full coverage.
6. In production, Next.js `<Link>` prefetches automatically — disable for auth-gated routes.


---

## From `edge-functions`

> Edge computing — Vercel Edge Functions, Cloudflare Workers, edge middleware, geo-routing, edge config, runtime limitations

# Edge Functions Skill

## Purpose

Edge functions run at CDN nodes closest to the user with sub-50ms cold starts. Use for auth checks, redirects, A/B testing, geo-routing, and header manipulation.

## Edge vs Node.js Runtime

| Feature | Edge Runtime | Node.js Runtime |
|---------|-------------|-----------------|
| Cold start | < 50ms | 250ms+ |
| Node.js APIs | Subset (no `fs`, `net`) | Full |
| Database | HTTP clients only | TCP + HTTP |
| Max size | 1-4 MB | 50 MB+ |
| npm packages | Web-compatible only | All |

## Vercel Edge API Route

```typescript
// app/api/geo/route.ts
export const runtime = 'edge';

export async function GET(request: Request) {
  const country = request.headers.get('x-vercel-ip-country') ?? 'US';
  const city = request.headers.get('x-vercel-ip-city') ?? 'Unknown';
  return Response.json({ country, city, timestamp: Date.now() });
}
```

## Edge Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const country = request.geo?.country ?? 'US';

  // Geo-based redirect
  if (pathname === '/' && country === 'DE') {
    return NextResponse.redirect(new URL('/de', request.url));
  }

  // A/B testing
  if (!request.cookies.get('ab-bucket') && pathname === '/pricing') {
    const bucket = Math.random() < 0.5 ? 'control' : 'variant';
    const res = NextResponse.rewrite(new URL(`/pricing/${bucket}`, request.url));
    res.cookies.set('ab-bucket', bucket, { maxAge: 60 * 60 * 24 * 30 });
    return res;
  }

  // Security headers
  const response = NextResponse.next();
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  return response;
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
```

## Vercel Edge Config

```typescript
import { get } from '@vercel/edge-config';
export const runtime = 'edge';

export async function GET() {
  const maintenance = await get<boolean>('maintenance_mode');
  const flags = await get<Record<string, boolean>>('feature_flags');
  if (maintenance) return new Response('Under maintenance', { status: 503 });
  return Response.json({ flags });
}
```

## Edge-Compatible Database Access

```typescript
// Use HTTP-based clients (not TCP) at the edge
import { neon } from '@neondatabase/serverless';
export const runtime = 'edge';

export async function GET() {
  const sql = neon(process.env.DATABASE_URL!);
  const posts = await sql`SELECT * FROM posts WHERE published = true LIMIT 20`;
  return Response.json(posts);
}
```

## Cloudflare Workers

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const country = (request as any).cf?.country ?? 'US';
    const cached = await env.MY_KV.get('config', 'json');
    const result = await env.DB.prepare('SELECT * FROM posts LIMIT 10').all();
    return Response.json({ country, posts: result.results, config: cached });
  },
};
```

## Best Practices

1. **Keep bundles small** — 1-4 MB limits are strict
2. **Use HTTP database clients** (Neon serverless, PlanetScale) not TCP
3. **Use Edge Config** for feature flags (sub-ms reads)
4. **Scope middleware matchers** to exclude `_next/static`
5. **Test locally** with `vercel dev` or `wrangler dev`
6. **Don't assume global state** — edge functions are stateless between requests


---

## From `vercel`

> Vercel deployment, Edge Config, KV, Cron Jobs, Middleware, and platform-specific optimization

# Vercel Specialist

## Purpose

Optimize deployments, edge functions, middleware, cron jobs, and platform features on Vercel. This skill covers vercel.json configuration, Edge Config, Vercel KV, middleware patterns, preview deployments, and CI integration.

## Key Patterns

### vercel.json Configuration

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "regions": ["iad1", "sfo1"],
  "crons": [
    {
      "path": "/api/cron/cleanup",
      "schedule": "0 */6 * * *"
    },
    {
      "path": "/api/cron/sync",
      "schedule": "*/15 * * * *"
    }
  ],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store" }
      ]
    },
    {
      "source": "/(.*)\\.(.*)$",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ],
  "rewrites": [
    { "source": "/blog/:slug", "destination": "/api/blog/:slug" }
  ],
  "redirects": [
    { "source": "/old-page", "destination": "/new-page", "permanent": true }
  ]
}
```

### Middleware (Edge Runtime)

```typescript
// middleware.ts
import { NextRequest, NextResponse } from "next/server";

export const config = {
  matcher: [
    // Match all paths except static files and _next
    "/((?!_next/static|_next/image|favicon.ico|public/).*)",
  ],
};

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Geo-based routing
  const country = request.geo?.country || "US";

  // A/B testing with cookies
  const bucket = request.cookies.get("ab-bucket")?.value;
  if (!bucket) {
    const newBucket = Math.random() > 0.5 ? "a" : "b";
    const response = NextResponse.next();
    response.cookies.set("ab-bucket", newBucket, {
      httpOnly: true,
      maxAge: 60 * 60 * 24 * 30,
    });
    return response;
  }

  // Rate limiting header
  const ip = request.headers.get("x-forwarded-for") || "unknown";

  // Bot protection
  const ua = request.headers.get("user-agent") || "";
  if (isSuspiciousBot(ua)) {
    return new NextResponse("Forbidden", { status: 403 });
  }

  // Add custom headers
  const response = NextResponse.next();
  response.headers.set("x-country", country);
  return response;
}

function isSuspiciousBot(ua: string): boolean {
  const suspiciousPatterns = [/curl/i, /python-requests/i, /scrapy/i];
  return suspiciousPatterns.some((p) => p.test(ua));
}
```

### Vercel KV (Redis) Usage

```typescript
import { kv } from "@vercel/kv";

// Rate limiting
async function checkRateLimit(ip: string, limit: number, windowSec: number): Promise<boolean> {
  const key = `rate:${ip}`;
  const count = await kv.incr(key);

  if (count === 1) {
    await kv.expire(key, windowSec);
  }

  return count <= limit;
}

// Caching
async function getCachedData<T>(key: string, fetcher: () => Promise<T>, ttl: number): Promise<T> {
  const cached = await kv.get<T>(key);
  if (cached) return cached;

  const fresh = await fetcher();
  await kv.set(key, fresh, { ex: ttl });
  return fresh;
}

// Session storage
async function setSession(sessionId: string, data: object) {
  await kv.set(`session:${sessionId}`, data, { ex: 86400 });
}
```

### Edge Config (Feature Flags)

```typescript
import { get } from "@vercel/edge-config";

// Read feature flags at the edge (ultra-low latency)
export async function isFeatureEnabled(feature: string): Promise<boolean> {
  const flags = await get<Record<string, boolean>>("featureFlags");
  return flags?.[feature] ?? false;
}

// Maintenance mode check in middleware
export async function middleware(request: NextRequest) {
  const maintenance = await get<boolean>("maintenance");
  if (maintenance) {
    return NextResponse.rewrite(new URL("/maintenance", request.url));
  }
  return NextResponse.next();
}
```

### Cron Job Handler

```typescript
// app/api/cron/cleanup/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  // Verify the request is from Vercel Cron
  const authHeader = request.headers.get("authorization");
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const deleted = await cleanupExpiredSessions();
    return NextResponse.json({ success: true, deleted });
  } catch (error) {
    console.error("Cron cleanup failed:", error);
    return NextResponse.json({ error: "Cleanup failed" }, { status: 500 });
  }
}
```

## Best Practices

### Deployment
- Use preview deployments for every PR
- Set up GitHub integration for automatic deploys
- Use `VERCEL_ENV` to distinguish preview/production
- Configure environment variables per environment (preview, production)
- Use `vercel --prod` only from CI, not locally

### Performance
- Place compute in regions close to your database (set `regions` in vercel.json)
- Use Edge Runtime for latency-sensitive endpoints
- Use Edge Config for feature flags and config (reads in ~1ms)
- Use ISR (Incremental Static Regeneration) for semi-static pages
- Set appropriate `Cache-Control` headers for static assets

### Middleware
- Keep middleware lightweight (it runs on every matching request)
- Use `config.matcher` to limit which paths trigger middleware
- Avoid database calls in middleware; use Edge Config or KV instead
- Return early with `NextResponse.next()` for passthrough

### Cron Jobs
- Always verify the `CRON_SECRET` authorization header
- Keep cron handlers idempotent
- Log outcomes for debugging
- Use the Vercel dashboard to monitor cron execution history

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Middleware running on all paths | Use `config.matcher` to exclude static assets |
| Slow middleware with DB calls | Use Edge Config or Vercel KV instead |
| Missing CRON_SECRET verification | Always check auth header in cron endpoints |
| Environment variable mismatch | Set vars per environment in Vercel dashboard |
| Large serverless function bundles | Use dynamic imports, check with `@vercel/nft` |
| Region mismatch with database | Set `regions` in vercel.json near your DB |

## Examples

### OG Image Generation (Edge)

```typescript
// app/api/og/route.tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get("title") || "Default Title";

  return new ImageResponse(
    (
      <div style={{ display: "flex", fontSize: 48, background: "#000", color: "#fff", width: "100%", height: "100%", alignItems: "center", justifyContent: "center" }}>
        {title}
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
```

### Vercel CLI Deployment Script

```bash
#!/bin/bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Pull environment variables locally
vercel env pull .env.local

# Link to existing project
vercel link
```


---

## From `vercel-react-best-practices`

> React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements.

# Vercel React Best Practices

Comprehensive performance optimization guide for React and Next.js applications, maintained by Vercel. Contains 45 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring existing React/Next.js code
- Optimizing bundle size or load times

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)

- `async-defer-await` - Move await into branches where actually used
- `async-parallel` - Use Promise.all() for independent operations
- `async-dependencies` - Use better-all for partial dependencies
- `async-api-routes` - Start promises early, await late in API routes
- `async-suspense-boundaries` - Use Suspense to stream content

### 2. Bundle Size Optimization (CRITICAL)

- `bundle-barrel-imports` - Import directly, avoid barrel files
- `bundle-dynamic-imports` - Use next/dynamic for heavy components
- `bundle-defer-third-party` - Load analytics/logging after hydration
- `bundle-conditional` - Load modules only when feature is activated
- `bundle-preload` - Preload on hover/focus for perceived speed

### 3. Server-Side Performance (HIGH)

- `server-cache-react` - Use React.cache() for per-request deduplication
- `server-cache-lru` - Use LRU cache for cross-request caching
- `server-serialization` - Minimize data passed to client components
- `server-parallel-fetching` - Restructure components to parallelize fetches
- `server-after-nonblocking` - Use after() for non-blocking operations

### 4. Client-Side Data Fetching (MEDIUM-HIGH)

- `client-swr-dedup` - Use SWR for automatic request deduplication
- `client-event-listeners` - Deduplicate global event listeners

### 5. Re-render Optimization (MEDIUM)

- `rerender-defer-reads` - Don't subscribe to state only used in callbacks
- `rerender-memo` - Extract expensive work into memoized components
- `rerender-dependencies` - Use primitive dependencies in effects
- `rerender-derived-state` - Subscribe to derived booleans, not raw values
- `rerender-functional-setstate` - Use functional setState for stable callbacks
- `rerender-lazy-state-init` - Pass function to useState for expensive values
- `rerender-transitions` - Use startTransition for non-urgent updates

### 6. Rendering Performance (MEDIUM)

- `rendering-animate-svg-wrapper` - Animate div wrapper, not SVG element
- `rendering-content-visibility` - Use content-visibility for long lists
- `rendering-hoist-jsx` - Extract static JSX outside components
- `rendering-svg-precision` - Reduce SVG coordinate precision
- `rendering-hydration-no-flicker` - Use inline script for client-only data
- `rendering-activity` - Use Activity component for show/hide
- `rendering-conditional-render` - Use ternary, not && for conditionals

### 7. JavaScript Performance (LOW-MEDIUM)

- `js-batch-dom-css` - Group CSS changes via classes or cssText
- `js-index-maps` - Build Map for repeated lookups
- `js-cache-property-access` - Cache object properties in loops
- `js-cache-function-results` - Cache function results in module-level Map
- `js-cache-storage` - Cache localStorage/sessionStorage reads
- `js-combine-iterations` - Combine multiple filter/map into one loop
- `js-length-check-first` - Check array length before expensive comparison
- `js-early-exit` - Return early from functions
- `js-hoist-regexp` - Hoist RegExp creation outside loops
- `js-min-max-loop` - Use loop for min/max instead of sort
- `js-set-map-lookups` - Use Set/Map for O(1) lookups
- `js-tosorted-immutable` - Use toSorted() for immutability

### 8. Advanced Patterns (LOW)

- `advanced-event-handler-refs` - Store event handlers in refs
- `advanced-use-latest` - useLatest for stable callback refs

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

