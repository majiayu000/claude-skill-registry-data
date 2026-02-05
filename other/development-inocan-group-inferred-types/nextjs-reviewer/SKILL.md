---
name: nextjs-reviewer
description: Review Next.js App Router code for optimal Partial Prerendering (PPR), caching strategy, Suspense boundaries, and React Query integration. Ensure adherence to Next.js 16+ Cache Components best practices.
---

# Next.js PPR & Caching Code Review Skill

## Purpose

Review Next.js App Router code for optimal Partial Prerendering (PPR), caching strategy, Suspense boundaries, and React Query integration. Ensure adherence to Next.js 16+ Cache Components best practices.

> **Documentation Version**: Based on Next.js 16.0.4 official documentation
> **Last Updated**: 2025-11-25
> **Source**: https://nextjs.org/docs/app/getting-started/partial-prerendering

## When to Use

- Before creating pull requests with Next.js components
- When implementing new data-fetching features
- During performance optimization reviews
- When adding or modifying Suspense boundaries
- After implementing caching strategies

## Prerequisites

- Next.js 16+ with `cacheComponents: true` in next.config
- App Router (not Pages Router)
- Understanding of Server Components vs Client Components

---

## Understanding the Two Cache Systems

> **📖 Reference**: [Cache Components - With runtime data](https://nextjs.org/docs/app/getting-started/partial-prerendering#with-runtime-data)

Before reviewing code, understand these two **completely different** caching mechanisms:

| Concept | React `cache()` | `'use cache'` directive |
|---------|-----------------|-------------------------|
| **Import** | `import { cache } from 'react'` | Directive: `'use cache'` |
| **Scope** | **Same-REQUEST** deduplication | **Cross-REQUEST** caching |
| **Duration** | Single render pass only | Minutes / hours / days |
| **Use Case** | `getCurrentUser()` called 5x = 1 actual call | Data cached for all users |
| **Works with cookies()** | ✅ Yes (wraps the function) | ❌ No (use `'use cache: private'`) |

### The Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: Layout/Page (STATIC SHELL)                                     │
│ ─────────────────────────────────────────────────────────────────────── │
│ • NO cookies(), NO headers(), NO runtime data                           │
│ • Prerendered at build time → instant delivery                          │
│ • Contains <Suspense> boundaries as deep as possible                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: Auth Boundary (DYNAMIC - inside Suspense)                      │
│ ─────────────────────────────────────────────────────────────────────── │
│ • Calls cookies() to get session token                                  │
│ • Uses getCurrentUser() wrapped with React cache() for dedup            │
│ • Handles redirect('/login') if not authenticated                       │
│ • Passes accessToken DOWN to cached components as prop                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: Cached Data (CACHED - 'use cache' with token as key)           │
│ ─────────────────────────────────────────────────────────────────────── │
│ • Receives accessToken as PROP (automatically becomes cache key)        │
│ • Uses 'use cache' + cacheLife() + cacheTag()                           │
│ • Fetches user-specific data using the token                            │
│ • Cached PER-USER across multiple requests                              │
└─────────────────────────────────────────────────────────────────────────┘
```

### Complete Auth + Caching Implementation

**Step 1: Auth Utilities (`auth/server.ts`)**

```typescript
import { cache } from 'react';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

// Internal: Read session from cookie (CANNOT be cached - runtime data)
async function getSessionFromCookie() {
  const cookieStore = await cookies();
  const session = cookieStore.get('github_session')?.value;
  return session ? decrypt(session) : null;
}

// ✅ Wrapped with React cache() for SAME-REQUEST deduplication
// If layout + page + 10 components call this = 1 actual cookie read
export const getCurrentUser = cache(async () => {
  const session = await getSessionFromCookie();
  if (!session) return null;
  return {
    accessToken: session.githubToken,
    userId: session.githubId,
    userName: session.userName,
  };
});

// ✅ Auth guard - redirects if not logged in
export async function requireAuth() {
  const user = await getCurrentUser();
  if (!user) {
    redirect('/login');
  }
  return user;
}
```

**Step 2: Layout (STATIC SHELL - no runtime data)**

```typescript
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  // ⚠️ NO cookies() here! Layout stays in static shell.
  return (
    <html>
      <body>
        <StaticHeader />   {/* ✅ Part of static shell */}
        <StaticSidebar />  {/* ✅ Part of static shell */}
        {children}
        <StaticFooter />   {/* ✅ Part of static shell */}
      </body>
    </html>
  );
}
```

**Step 3: Page with Suspense Boundaries (as deep as possible)**

```typescript
// app/pulls/page.tsx
import { Suspense } from 'react';

export default function PullsPage() {
  // ✅ Page itself is STATIC - no runtime data access here
  return (
    <div>
      <h1>Pull Requests</h1>  {/* ✅ Static shell */}

      {/* ✅ Suspense boundary as DEEP as possible */}
      <Suspense fallback={<PullsSkeleton />}>
        <AuthenticatedPullsList />
      </Suspense>
    </div>
  );
}
```

**Step 4: Auth Boundary Component (DYNAMIC)**

```typescript
// components/authenticated-pulls-list.tsx
import { requireAuth } from '@/auth/server';

// ⚠️ This component is DYNAMIC - accesses cookies via requireAuth
// ⚠️ MUST be wrapped in <Suspense> at usage site
export async function AuthenticatedPullsList() {
  // Step 1: Auth check (reads cookies, may redirect)
  const user = await requireAuth();

  // Step 2: Pass token to CACHED component (token = cache key)
  return <PullsListCached accessToken={user.accessToken} />;
}
```

**Step 5: Cached Data Component**

```typescript
// components/pulls-list-cached.tsx
import { cacheLife, cacheTag } from 'next/cache';

// ✅ This component is CACHED across requests
// ✅ accessToken is part of cache key - each user gets own cache
async function PullsListCached({ accessToken }: { accessToken: string }) {
  'use cache';
  cacheLife('minutes');        // 5 min stale, 1 min revalidate
  cacheTag('user-pulls');      // For on-demand invalidation

  // This fetch is cached per-user (keyed by accessToken prop)
  const client = createGitHubClient(accessToken);
  const pulls = await client.pulls.list();

  return (
    <ul>
      {pulls.map(pr => <PullRequestItem key={pr.id} pr={pr} />)}
    </ul>
  );
}
```

### Why This Pattern is Optimal

| Benefit | How It's Achieved |
|---------|-------------------|
| **Maximum static shell** | Layout, headers, titles prerendered instantly |
| **Suspense as deep as possible** | Only data sections stream; everything else instant |
| **No duplicate cookie reads** | `getCurrentUser()` with React `cache()` = 1 read per request |
| **Cross-request caching** | `'use cache'` with token key = per-user cache reuse |
| **Cache isolation** | Token as prop = automatic per-user cache keys |

### Critical Insight: Where Auth Happens

```typescript
// ❌ WRONG - Auth in layout blocks entire layout from prerendering
export default async function Layout({ children }) {
  const user = await getCurrentUser(); // cookies() blocks prerender!
  return <div>{children}</div>;
}

// ✅ CORRECT - Layout is static, auth is inside page's Suspense
export default function Layout({ children }) {
  return (
    <div>
      <StaticNav />
      {children}  {/* Pages put auth inside their own Suspense */}
    </div>
  );
}
```

### Decision Matrix: Which Cache to Use

| What You're Doing | Which Cache | Why |
|-------------------|-------------|-----|
| `getCurrentUser()` - reading cookies | React `cache()` | Same-request dedup; can't cache cookies cross-request |
| `getGitHubClient(token)` - creating client | React `cache()` | Same-request dedup; reuse client instance |
| `fetchUserRepos(token)` - API call with token | `'use cache'` | Cross-request cache; token is cache key |
| `fetchPublicRepo(owner, repo)` - public data | `'use cache'` | Cross-request cache; no auth needed |
| `fetchUserDashboard()` - needs cookies directly | `'use cache: private'` | Cross-request with cookie access |

---

## Review Checklist

### 1. PPR Pattern Implementation

> **📖 Reference**: [Cache Components](https://nextjs.org/docs/app/getting-started/partial-prerendering)

**The Core Concept:**

Cache Components lets you mix **static**, **cached**, and **dynamic** content in a single route:

| Content Type | When Used | How to Handle |
|--------------|-----------|---------------|
| **Static** | Synchronous I/O, pure computations | Auto-prerendered into static shell |
| **Cached** | Dynamic data without runtime context | Use `'use cache'` directive |
| **Dynamic** | Needs cookies, headers, searchParams | Wrap in `<Suspense>` boundaries |

**✅ CORRECT Pattern (Public/Shared Data):**

```typescript
// Outer component - accesses runtime data (stays dynamic)
export async function DataSection() {
  const user = await getCurrentUser(); // accesses cookies
  if (!user?.accessToken) redirect('/login');

  return <DataSectionCached accessToken={user.accessToken} />;
}

// Inner component - cached with 'use cache'
async function DataSectionCached({ accessToken }: { accessToken: string }) {
  'use cache';
  cacheLife('minutes');

  const client = getCachedAuthenticatedClient(accessToken);
  const data = await fetchData(client);
  return <UI data={data} />;
}

// ⚠️ CRITICAL: Usage site MUST wrap in Suspense
// app/page.tsx
export default function Page() {
  return (
    <Suspense fallback={<DataSkeleton />}>
      <DataSection />
    </Suspense>
  );
}
```

**❌ INCORRECT Pattern:**

```typescript
// ❌ Auth check blocks everything from being cached
export async function DataSection() {
  const user = await getCurrentUser(); // accesses cookies - blocks caching
  const client = getCachedAuthenticatedClient(user.accessToken);
  const data = await fetchData(client); // this could be cached but isn't
  return <UI data={data} />;
}
```

**Check for:**

- [ ] Runtime data access (cookies, headers, searchParams) isolated in outer wrapper
- [ ] Data fetching moved to inner cached component
- [ ] `'use cache'` directive at top of cached function/component
- [ ] `cacheLife()` called with appropriate duration
- [ ] Cache key includes all varying parameters (passed as props)
- [ ] **Outer component wrapped in `<Suspense>` at usage site**

---

### 1.5 PPR Pattern with Personalized Data (`use cache: private`)

> **📖 Reference**: [`use cache: private` directive](https://nextjs.org/docs/app/api-reference/directives/use-cache-private)

**When to Use**: For **user-specific** data where each user needs their own cache entry (dashboards, feeds, personalized recommendations).

**✅ CORRECT Pattern:**

```typescript
import { cookies } from 'next/headers';
import { cacheLife, cacheTag } from 'next/cache';
import { Suspense } from 'react';

// Usage - MUST wrap in Suspense (not prerendered)
export default function Page() {
  return (
    <Suspense fallback={<DashboardSkeleton />}>
      <UserDashboard />
    </Suspense>
  );
}

// Single function - no split needed with private cache!
async function UserDashboard() {
  'use cache: private';
  cacheLife({ stale: 60 }); // Minimum 30s required for runtime prefetch

  // Can access cookies directly
  const session = await cookies();
  const userId = session.get('userId')?.value;

  const data = await fetchUserSpecificData(userId);
  return <Dashboard data={data} />;
}
```

**Real-World Example (GitHub-style):**

```typescript
// User's personalized pull request dashboard
async function MyPullsPage() {
  'use cache: private';
  cacheLife('minutes'); // 5 min stale, 1 min revalidate

  const session = await cookies();
  const userId = session.get('userId')?.value;

  const myPrs = await db.pulls.findMany({
    where: {
      OR: [
        { authorId: userId },
        { assignees: { some: { id: userId } } },
      ],
    },
  });

  return <DashboardTable items={myPrs} />;
}
```

**Comparison: Public vs Private Caching**

| Feature | `'use cache'` (Public) | `'use cache: private'` (Private) |
|---------|------------------------|----------------------------------|
| **Use Case** | Shared across all users | Per-user personalized data |
| **Example** | `/vercel/next.js/issues` | `/pulls`, `/dashboard` |
| **Can access `cookies()`** | ❌ No | ✅ Yes |
| **Can access `headers()`** | ❌ No | ✅ Yes |
| **Can use `searchParams` prop** | ✅ Yes (as prop) | ✅ Yes (as prop or via access) |
| **Can access `connection()`** | ❌ No | ❌ **No** |
| **Prerendered in static shell** | ✅ Yes | ❌ No (personalized) |
| **Minimum `stale` time** | 30 seconds | **30 seconds** |
| **Cache scope** | Global (all users share) | Per-user (isolated) |

**Caching Strategy Decision Matrix**

| Page Type | Example Route | Directive | Revalidation Strategy |
|-----------|---------------|-----------|----------------------|
| **Public Static** | `/about`, Marketing | `'use cache'` | `cacheLife('weeks')` or `'days'` |
| **Public Dynamic** | `/vercel/next.js/issues` | `'use cache'` | `cacheTag('repo-issues')` |
| **User Private** | `/pulls`, `/dashboard` | `'use cache: private'` | `cacheLife('minutes')` + tags |
| **Real-time** | Comments, live feed | No directive | `<Suspense>` + streaming |

**Check for:**

- [ ] Personalized data uses `'use cache: private'`
- [ ] Private caches have `cacheLife` with `stale` >= 30 seconds
- [ ] Public shared data uses standard `'use cache'`
- [ ] Private cache components wrapped in `<Suspense>` at usage site
- [ ] `connection()` NOT used inside any cache directive

---

### 1.6 Async Dynamic APIs (Breaking Change)

> **📖 Reference**: [page.js - params and searchParams](https://nextjs.org/docs/app/api-reference/file-conventions/page)

**Next.js 15+ Breaking Change**: `params` and `searchParams` are now **Promises** and must be awaited.

**❌ WRONG (Next.js 14 and earlier - no longer works):**

```typescript
// This will cause runtime errors in Next.js 15+
export default function Page({ params }: { params: { slug: string } }) {
  const slug = params.slug; // ❌ ERROR: params is a Promise
  return <h1>{slug}</h1>;
}
```

**✅ CORRECT (Next.js 15+):**

```typescript
// Server Component - use async/await
export default async function Page({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const { slug } = await params;
  const { query } = await searchParams;
  return <h1>{slug} - {query}</h1>;
}

// Client Component - use React's use() hook
'use client';
import { use } from 'react';

export default function Page({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const { slug } = use(params);
  const { query } = use(searchParams);
  return <h1>{slug} - {query}</h1>;
}
```

**TypeScript Helper (Next.js 16+):**

```typescript
// Use PageProps helper for automatic typing from route literal
export default async function Page(props: PageProps<'/blog/[slug]'>) {
  const { slug } = await props.params;
  const query = await props.searchParams;
  return <h1>Blog Post: {slug}</h1>;
}
```

> **⚠️ PPR Impact**: Accessing `searchParams` triggers dynamic rendering. Always wrap components that access `searchParams` in `<Suspense>` boundaries to maximize the static shell.

**Check for:**

- [ ] All `params` accesses use `await` (Server Components) or `use()` (Client Components)
- [ ] All `searchParams` accesses use `await` or `use()`
- [ ] TypeScript types show `Promise<...>` not plain objects
- [ ] Components accessing `searchParams` are wrapped in `<Suspense>`
- [ ] Consider using `PageProps<'/route/[param]'>` helper for type safety

---

### 1.7 Proxy File Convention (Replaces middleware.ts)

> **📖 Reference**: [proxy.js](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)

**Next.js 16 Change**: `middleware.ts` is now `proxy.ts`. A codemod is available:

```bash
npx @next/codemod@latest middleware-to-proxy .
```

**Key Differences:**

| Feature | `middleware.ts` (deprecated) | `proxy.ts` (Next.js 16+) |
|---------|------------------------------|--------------------------|
| **Runtime** | Edge Runtime | Node.js Runtime |
| **Location** | Project root or `src/` | Project root or `src/` |
| **Purpose** | Request interception | Request interception + full Node.js APIs |
| **Capabilities** | Limited Edge APIs | Full Node.js APIs, DB access |

**Example `proxy.ts`:**

```typescript
// proxy.ts
import { NextRequest, NextResponse } from 'next/server';

export function proxy(request: NextRequest) {
  // Now runs on Node.js runtime - full access to Node APIs
  const response = NextResponse.next();

  // Authentication, logging, redirects, etc.
  if (!request.cookies.get('session')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return response;
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

**Check for:**

- [ ] Project uses `proxy.ts` instead of deprecated `middleware.ts`
- [ ] `matcher` config excludes metadata files if needed
- [ ] Proxy logic is modular (split into separate files, imported into `proxy.ts`)

---

### 2. Cache Strategy

> **📖 Reference**: [`cacheLife()` function](https://nextjs.org/docs/app/api-reference/functions/cacheLife)

**Preset Cache Profiles (ACCURATE VALUES):**

| Profile | `stale` | `revalidate` | `expire` | Use Case |
|---------|---------|--------------|----------|----------|
| `default` | 5 min | 15 min | 1 year | Standard content |
| `seconds` | 30 sec | **1 sec** | 1 min | Real-time data (aggressive!) |
| `minutes` | 5 min | **1 min** | 1 hour | Frequently updated |
| `hours` | 5 min | **1 hour** | 1 day | Multiple daily updates |
| `days` | 5 min | **1 day** | 1 week | Daily updates |
| `weeks` | 5 min | **1 week** | 30 days | Weekly updates |
| `max` | 5 min | **30 days** | 1 year | Rarely changes |

> **⚠️ Note**: All profiles have 5 min `stale` time (except `seconds` at 30s). The `revalidate` time is what varies significantly between profiles.

**Usage Examples:**

```typescript
// Frequently changing data (user activity, notifications)
'use cache';
cacheLife('minutes'); // 5 min stale, 1 min revalidate, 1 hour expire

// Moderate change frequency (user repos, profile data)
'use cache';
cacheLife('hours'); // 5 min stale, 1 hour revalidate, 1 day expire

// Rarely changing data (static content, config)
'use cache';
cacheLife('days'); // 5 min stale, 1 day revalidate, 1 week expire

// Custom inline profile
'use cache';
cacheLife({
  stale: 3600,      // 1 hour
  revalidate: 900,  // 15 minutes
  expire: 86400,    // 1 day
});
```

**Check for:**

- [ ] `cacheLife()` matches data freshness requirements
- [ ] Understand `'seconds'` profile is **very aggressive** (1s revalidate)
- [ ] High-frequency data uses `'minutes'` (1 min revalidate)
- [ ] Low-frequency data uses `'hours'`/`'days'`
- [ ] Cache tags used with `cacheTag()` for on-demand revalidation

---

### 3. Suspense Boundary Placement

> **📖 Reference**: [Cache Components - Defer rendering to request time](https://nextjs.org/docs/app/getting-started/partial-prerendering#defer-rendering-to-request-time)

**✅ CORRECT - Deep Suspense boundaries:**

```typescript
export default function Page() {
  return (
    <div>
      <StaticHeader /> {/* Part of static shell */}
      <Suspense fallback={<PullsSkeleton />}>
        <PullRequestsSection /> {/* Streams independently */}
      </Suspense>
      <Suspense fallback={<IssuesSkeleton />}>
        <IssuesSection /> {/* Streams independently */}
      </Suspense>
      <StaticFooter /> {/* Part of static shell */}
    </div>
  );
}
```

**❌ INCORRECT - Shallow Suspense (blocks too much):**

```typescript
export default function Page() {
  return (
    <Suspense fallback={<FullPageSkeleton />}>
      <StaticHeader />  {/* Unnecessarily blocked! */}
      <PullRequestsSection />
      <IssuesSection />
      <StaticFooter />  {/* Unnecessarily blocked! */}
    </Suspense>
  );
}
```

**Check for:**

- [ ] Suspense boundaries at deepest necessary points
- [ ] Static content **outside** Suspense (part of static shell)
- [ ] Each independent async section has its own Suspense
- [ ] Suspense `key` prop used when data depends on params: `key={query || 'default'}`
- [ ] Meaningful loading skeletons provided

---

### 4. React Query Integration Strategy

> **📖 Note**: React Query patterns are framework-agnostic. Next.js does not have official React Query docs - refer to [TanStack Query Documentation](https://tanstack.com/query/latest/docs/framework/react/guides/ssr).

**Decision Tree:**

```
┌─ Server Component?
│  ├─ Yes → Use 'use cache' + cacheLife (NOT React Query)
│  │
│  └─ No (Client Component) →
│     │
│     ├─ Need SSR data? → prefetchQuery + HydrationBoundary
│     │
│     └─ Client-only? → Standard useSuspenseQuery
```

**Server Components: Use `'use cache'` (NOT React Query)**

```typescript
// ✅ Server Components - Native Next.js caching
async function ServerData() {
  'use cache';
  cacheLife('hours');
  const data = await fetch('/api/data');
  return <UI data={data} />;
}
```

**Client Components with SSR: Prefetch + Hydration Pattern**

```typescript
// Server wrapper
import { getQueryClient } from '@/app/get-query-client';
import { dehydrate, HydrationBoundary } from '@tanstack/react-query';

async function DataWrapper({ userId }: { userId: string }) {
  const queryClient = getQueryClient();

  // ⚠️ CRITICAL: Don't await! Fire and forget.
  queryClient.prefetchQuery({
    queryKey: ['data', userId],
    queryFn: () => fetchData(userId),
  });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <DataClient userId={userId} />
    </HydrationBoundary>
  );
}
```

```typescript
// Client consumer
'use client';
import { useSuspenseQuery } from '@tanstack/react-query';

export function DataClient({ userId }: { userId: string }) {
  const { data } = useSuspenseQuery({
    queryKey: ['data', userId],
    queryFn: () => fetchData(userId),
  });

  return <UI data={data} />;
}
```

**Query Client Configuration:**

```typescript
// app/get-query-client.ts
import {
  QueryClient,
  defaultShouldDehydrateQuery,
  isServer,
} from '@tanstack/react-query';

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // Prevents refetch after hydration
      },
      dehydrate: {
        shouldDehydrateQuery: (query) =>
          defaultShouldDehydrateQuery(query) ||
          query.state.status === 'pending', // Include pending for PPR
        shouldRedactErrors: () => false,
      },
    },
  });
}

let browserQueryClient: QueryClient | undefined;

export function getQueryClient() {
  if (isServer) {
    return makeQueryClient(); // Always new on server
  }
  if (!browserQueryClient) {
    browserQueryClient = makeQueryClient(); // Singleton on client
  }
  return browserQueryClient;
}
```

**Check for:**

- [ ] Server Components use `'use cache'` (NOT React Query)
- [ ] `prefetchQuery` called **WITHOUT** `await`
- [ ] `HydrationBoundary` wraps client components
- [ ] `useSuspenseQuery` used (not `useQuery`)
- [ ] `staleTime: 60000` configured to prevent refetch
- [ ] `shouldDehydrateQuery` includes pending queries
- [ ] Browser QueryClient is singleton; Server is per-request

---

### 5. Request Deduplication

> **📖 Reference**: [React `cache()` for request memoization](https://react.dev/reference/react/cache)

**React's `cache()` wrapper:**

```typescript
import { cache } from 'react';

// ✅ Wrap fetchers with cache() for same-request deduplication
const getUserUncached = async (client: Client) => {
  const { data } = await usersGetAuthenticated({ client });
  return data;
};

export const getUser = cache(getUserUncached);
```

**Check for:**

- [ ] All data fetchers wrapped with React's `cache()`
- [ ] Cache wraps the implementation, not exported directly
- [ ] Used for same-request deduplication (layout + page + components)
- [ ] Works alongside `'use cache'` (different purposes)
- [ ] Auth helpers like `getCurrentUser()` wrapped with `cache()`

---

### 6. Common Anti-Patterns

> **📖 Reference**: [`use cache` - Constraints](https://nextjs.org/docs/app/api-reference/directives/use-cache#constraints)

**❌ Avoid these patterns:**

```typescript
// ❌ Using cookies() inside 'use cache' scope
async function BadCached() {
  'use cache';
  const cookieStore = await cookies(); // ERROR: Can't access runtime data
  return <div />;
}

// ✅ FIX OPTION 1: Use 'use cache: private' for personalized data
async function GoodCachedPrivate() {
  'use cache: private';
  cacheLife({ stale: 60 }); // Min 30s for prefetch

  const cookieStore = await cookies();
  const userId = cookieStore.get('userId')?.value;
  return <div>{userId}</div>;
}

// ✅ FIX OPTION 2: Split outer/inner for public shared data
export async function GoodCachedPublic() {
  const user = await getCurrentUser();
  return <CachedComponent userId={user.id} />;
}

async function CachedComponent({ userId }: { userId: string }) {
  'use cache';
  const data = await fetchData(userId);
  return <div>{data}</div>;
}

// ❌ Using connection() in any cache directive
async function BadConnection() {
  'use cache: private';
  await connection(); // ERROR: connection() not allowed in ANY cache directive
  return <div />;
}

// ❌ Shallow Suspense blocking static content
<Suspense fallback={<LoadingPage />}>
  <Header />           {/* Static but blocked! */}
  <DynamicContent />
</Suspense>

// ✅ FIX: Move static content outside
<Header />
<Suspense fallback={<LoadingContent />}>
  <DynamicContent />
</Suspense>
```

**Cache Key Behavior:**

> **📖 Reference**: [`use cache` - Cache keys](https://nextjs.org/docs/app/api-reference/directives/use-cache#cache-keys)

With `'use cache'`, cache keys **automatically** include:

1. **Build ID** - Unique per build
2. **Function ID** - Secure hash of function location and signature
3. **Serializable arguments** - Props (for components) or function arguments
4. **HMR refresh hash** (development only)

Closed-over values from parent scopes are automatically captured. **You don't need to manually configure cache keys** - just pass all varying parameters as props.

**Check for:**

- [ ] No `cookies()`/`headers()` inside `'use cache'` (use `'use cache: private'` instead)
- [ ] No `connection()` in ANY cache directive
- [ ] Auth checks separated from cached data (for public data patterns)
- [ ] searchParams accessed inside Suspense boundaries
- [ ] No shallow Suspense blocking static content
- [ ] All varying parameters passed as props

---

### 7. Build Output Verification

After implementing PPR, verify in build output:

```bash
bun run build
```

**Expected output:**

```
Route (app)
┌ ◐ /                    (Partial Prerender) ✅
├ ◐ /dashboard           (Partial Prerender) ✅
└ ○ /static              (Static)            ✅
```

**Symbols:**

- `◐` = Partial Prerender (PPR) - GOAL for dynamic pages
- `○` = Static - Good for truly static pages
- `ƒ` = Dynamic - Should be rare with PPR

**Check for:**

- [ ] Dynamic pages show `◐` symbol
- [ ] No unexpected `ƒ` (fully dynamic) routes
- [ ] API routes correctly marked as `ƒ`
- [ ] Build completes without "Uncached data" errors

---

### 8. Next.js MCP Runtime Validation

Use Next.js MCP tools to check for runtime issues:

```typescript
// 1. Discover running Next.js servers
mcp__next-devtools__nextjs_index()

// 2. Check for errors (use port from step 1)
mcp__next-devtools__nextjs_call({
  port: "3000",
  toolName: "get_errors"
})

// 3. Get route information
mcp__next-devtools__nextjs_call({
  port: "3000",
  toolName: "get_routes"
})
```

**Check for:**

- [ ] No runtime errors in browser sessions
- [ ] No "Uncached data accessed outside Suspense" errors
- [ ] No "cookies() during prerender" errors
- [ ] Routes properly registered

---

## Advanced Patterns

### 9. Cache Invalidation

> **📖 References**:
> - [`cacheTag()`](https://nextjs.org/docs/app/api-reference/functions/cacheTag)
> - [`updateTag()`](https://nextjs.org/docs/app/api-reference/functions/updateTag) - Server Actions only
> - [`revalidateTag()`](https://nextjs.org/docs/app/api-reference/functions/revalidateTag) - Server Actions + Route Handlers

**Two Invalidation Strategies:**

| Function | Where | Behavior | Use Case |
|----------|-------|----------|----------|
| `updateTag(tag)` | Server Actions only | **Immediate** - next request waits for fresh data | Read-your-own-writes |
| `revalidateTag(tag, profile)` | Server Actions + Route Handlers | **Stale-while-revalidate** - serves cached while fetching | Background refresh |

**`updateTag` - Immediate invalidation (read-your-own-writes):**

```typescript
import { cacheTag, updateTag } from 'next/cache';

// Component
async function Posts() {
  'use cache';
  cacheTag('posts');
  const posts = await fetchPosts();
  return <PostList posts={posts} />;
}

// Server Action - User sees their changes immediately
async function createPost(data: FormData) {
  'use server';
  await db.posts.create(data);
  updateTag('posts'); // Next request waits for fresh data
}
```

**`revalidateTag` - Stale-while-revalidate:**

```typescript
import { revalidateTag } from 'next/cache';

// Server Action OR Route Handler
async function refreshPosts() {
  'use server';
  await db.posts.create(data);
  revalidateTag('posts', 'max'); // ⚠️ Second argument REQUIRED
}
```

> **⚠️ BREAKING CHANGE**: `revalidateTag(tag)` without second argument is **deprecated**. Always use `revalidateTag(tag, 'max')` or specify a cache profile.

---

### 10. Optimistic Updates with useOptimistic

> **📖 Reference**: [React `useOptimistic` hook](https://react.dev/reference/react/useOptimistic)

```typescript
'use client';
import { useOptimistic, useTransition } from 'react';
import { useMutation } from '@tanstack/react-query';

export function MessageList({ messages }: { messages: Message[] }) {
  const [isPending, startTransition] = useTransition();
  const [optimisticMessages, addOptimistic] = useOptimistic(
    messages,
    (state, newMsg: Message) => [...state, newMsg]
  );

  const sendMutation = useMutation({
    mutationFn: (text: string) => api.sendMessage(text),
  });

  const handleSend = (text: string) => {
    const optimistic: Message = {
      id: `temp-${Date.now()}`,
      text,
      isPending: true,
    };

    startTransition(async () => {
      addOptimistic(optimistic);
      await sendMutation.mutateAsync(text);
    });
  };

  return (
    <ul>
      {optimisticMessages.map((msg) => (
        <li key={msg.id} className={msg.isPending ? 'opacity-50' : ''}>
          {msg.text}
        </li>
      ))}
    </ul>
  );
}
```

**Check for:**

- [ ] `useOptimistic` used for pending state
- [ ] `useTransition` wraps async mutation
- [ ] Optimistic items have temporary IDs
- [ ] Visual indicator for pending state
- [ ] Auto-rollback on error (built-in)

---

## Common Fixes

### Fix 1: Split Auth from Data Fetching

**Before:**

```typescript
export async function Component() {
  const user = await getCurrentUser();
  const data = await fetchData(user.accessToken);
  return <UI data={data} />;
}
```

**After:**

```typescript
export async function Component() {
  const user = await getCurrentUser();
  return <ComponentCached accessToken={user.accessToken} />;
}

async function ComponentCached({ accessToken }: { accessToken: string }) {
  'use cache';
  cacheLife('minutes');
  const data = await fetchData(accessToken);
  return <UI data={data} />;
}
```

### Fix 2: Deep Suspense Boundaries

**Before:**

```typescript
<Suspense fallback={<FullPageLoader />}>
  <Header />
  <Content />
  <Footer />
</Suspense>
```

**After:**

```typescript
<Header />
<Suspense fallback={<ContentLoader />}>
  <Content />
</Suspense>
<Footer />
```

### Fix 3: Add Cache to Data Fetching

**Before:**

```typescript
async function Component() {
  const data = await fetch('/api/data');
  return <UI data={data} />;
}
```

**After:**

```typescript
async function Component({ userId }: { userId: string }) {
  'use cache';
  cacheLife('hours');
  cacheTag(`user-${userId}-data`);
  const data = await fetch(`/api/data?user=${userId}`);
  return <UI data={data} />;
}
```

---

## Performance Metrics

After implementing PPR with proper caching:

**Expected improvements:**

- ✅ Time to First Byte (TTFB): < 200ms (static shell)
- ✅ First Contentful Paint (FCP): < 1s (static shell visible)
- ✅ Largest Contentful Paint (LCP): < 2.5s (with streaming)
- ✅ Reduced API calls: 50-90% reduction via caching
- ✅ Lower server load: Cached responses served without DB/API hits

**Monitor:**

- Build output for route types (◐ vs ○ vs ƒ)
- Runtime errors via Next.js MCP
- Cache hit rates in production
- API rate limit usage (should decrease)

---

## Documentation References

> **📚 CRITICAL**: All patterns in this skill are based on official Next.js 16.0.4+ documentation.

**Core Documentation:**
- [Cache Components / Partial Prerendering](https://nextjs.org/docs/app/getting-started/partial-prerendering)
- [`use cache` directive](https://nextjs.org/docs/app/api-reference/directives/use-cache)
- [`use cache: private` directive](https://nextjs.org/docs/app/api-reference/directives/use-cache-private)
- [`cacheLife()` function](https://nextjs.org/docs/app/api-reference/functions/cacheLife)
- [`cacheTag()` function](https://nextjs.org/docs/app/api-reference/functions/cacheTag)
- [`revalidateTag()` function](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)
- [`updateTag()` function](https://nextjs.org/docs/app/api-reference/functions/updateTag)
- [`cookies()` function](https://nextjs.org/docs/app/api-reference/functions/cookies)
- [`headers()` function](https://nextjs.org/docs/app/api-reference/functions/headers)
- [`connection()` function](https://nextjs.org/docs/app/api-reference/functions/connection)

**Query via MCP:**
```typescript
mcp__next-devtools__nextjs_docs({
  action: 'get',
  path: '/docs/app/getting-started/partial-prerendering',
})
```

---

## Summary Checklist

For every PR with data-fetching components:

**Core PPR Patterns:**

- [ ] Runtime data access (cookies, headers) isolated OR use `'use cache: private'`
- [ ] Public shared data uses `'use cache'` + `cacheLife()`
- [ ] Personalized data uses `'use cache: private'` + `cacheLife()` (min 30s stale)
- [ ] `connection()` NOT used inside any cache directive
- [ ] Cache keys include all varying parameters (as props - automatic)
- [ ] Suspense boundaries at deepest necessary points
- [ ] Static content **outside** Suspense (part of static shell)
- [ ] Components accessing runtime APIs wrapped in `<Suspense>` at usage
- [ ] Appropriate `cacheLife` profiles for data freshness
- [ ] React's `cache()` used for request deduplication
- [ ] Build output shows `◐` for dynamic pages
- [ ] No runtime errors

**Breaking Changes (Next.js 15+/16):**

- [ ] `params` and `searchParams` use `await` (Server) or `use()` (Client)
- [ ] TypeScript types show `Promise<...>` for params/searchParams
- [ ] Project uses `proxy.ts` instead of deprecated `middleware.ts`

**React Query Integration:**

- [ ] Server Components use `'use cache'` (NOT React Query)
- [ ] Client SSR uses prefetchQuery + HydrationBoundary
- [ ] `prefetchQuery` called WITHOUT await
- [ ] `useSuspenseQuery` used instead of `useQuery`
- [ ] QueryClient configured with `staleTime: 60000`

**Cache Invalidation:**

- [ ] `updateTag()` for immediate invalidation (Server Actions only)
- [ ] `revalidateTag(tag, profile)` for stale-while-revalidate (always pass profile!)
- [ ] Tags properly applied with `cacheTag()`

---

## Output Format

When reviewing code, provide:

1. **Summary:** Overall PPR readiness (Ready / Needs Work)
2. **Issues Found:** List specific anti-patterns with file:line
3. **Recommendations:** Concrete fixes with code examples
4. **Build Verification:** Check build output for route types
5. **Priority:** High/Medium/Low for each issue

**Example Output:**

```markdown
## PPR Code Review Summary

**Status:** Needs Work (3 issues found)

### High Priority Issues

1. **Auth check blocking cache** in `components/data-section.tsx:15`
   - Issue: `getCurrentUser()` called inside component that should be cached
   - Fix: Split into outer (dynamic) and inner (cached) components
   - Pattern: See Fix 1 above

2. **Missing cacheLife** in `components/posts.tsx:8`
   - Issue: `'use cache'` without `cacheLife()` call
   - Fix: Add `cacheLife('minutes')` or appropriate profile
   - Impact: Uses default profile (15 min revalidate)

### Medium Priority Issues

3. **Shallow Suspense boundary** in `app/page.tsx:25`
   - Issue: Static header/footer inside Suspense
   - Fix: Move static content outside Suspense
   - Impact: Delays static content unnecessarily

### Build Verification

✅ Build succeeds
✅ Routes show ◐ (Partial Prerender)
❌ 3 components need caching improvements

### Recommendations

Priority: Fix 1 first (blocking cache), then Fix 2 (missing cacheLife), then Fix 3 (Suspense).
```
