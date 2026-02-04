---
name: migrating-async-request-apis
description: Teach async request APIs in Next.js 16 - params, searchParams, cookies(), headers(), draftMode() are now async. Use when migrating from Next.js 15, fixing type errors, or working with request data.
allowed-tools: Read, Write, Edit, Glob, Grep, TodoWrite
version: 1.0.0
---

# MIGRATION: Async Request APIs

## Purpose

Teach the breaking changes in Next.js 16 where request APIs are now async. This affects `params`, `searchParams`, `cookies()`, `headers()`, and `draftMode()` - all now return Promises and require `await`.

## When to Use

- Migrating from Next.js 15 to 16
- Fixing TypeScript errors about Promise types
- Working with route parameters, search params, or request headers
- Encountering "object is possibly undefined" errors
- Updating Server Components or API routes

## Breaking Changes Overview

### APIs Now Async

1. **Route Parameters (`params`)**
   - Pages: `params` prop is now a Promise
   - Layouts: `params` prop is now a Promise
   - Route Handlers: `params` argument is now a Promise

2. **Search Parameters (`searchParams`)**
   - Page `searchParams` prop is now a Promise

3. **Request APIs**
   - `cookies()` returns Promise
   - `headers()` returns Promise
   - `draftMode()` returns Promise

### Type Changes

```typescript
import { cookies, headers, draftMode } from 'next/headers';

type CookiesReturn = Promise<ReadonlyRequestCookies>;
type HeadersReturn = Promise<ReadonlyHeaders>;
type DraftModeReturn = Promise<{ isEnabled: boolean }>;
```

## Migration Patterns

### Pattern 1: Page Route Params

**Before (Next.js 15):**
```typescript
export default function Page({ params }: { params: { id: string } }) {
  return <div>User ID: {params.id}</div>;
}

export async function generateMetadata({ params }: { params: { id: string } }) {
  return { title: `User ${params.id}` };
}
```

**After (Next.js 16):**
```typescript
export default async function Page({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params;
  return <div>User ID: {id}</div>;
}

export async function generateMetadata({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params;
  return { title: `User ${id}` };
}
```

### Pattern 2: Search Parameters

**Before (Next.js 15):**
```typescript
export default function SearchPage({
  searchParams
}: {
  searchParams: { q?: string; page?: string }
}) {
  const query = searchParams.q || '';
  const page = Number(searchParams.page) || 1;

  return <SearchResults query={query} page={page} />;
}
```

**After (Next.js 16):**
```typescript
export default async function SearchPage({
  searchParams
}: {
  searchParams: Promise<{ q?: string; page?: string }>
}) {
  const params = await searchParams;
  const query = params.q || '';
  const page = Number(params.page) || 1;

  return <SearchResults query={query} page={page} />;
}
```

### Pattern 3: Cookies API

**Before (Next.js 15):**
```typescript
import { cookies } from 'next/headers';

export default function Component() {
  const cookieStore = cookies();
  const token = cookieStore.get('token');

  return <div>Token: {token?.value}</div>;
}
```

**After (Next.js 16):**
```typescript
import { cookies } from 'next/headers';

export default async function Component() {
  const cookieStore = await cookies();
  const token = cookieStore.get('token');

  return <div>Token: {token?.value}</div>;
}
```

### Pattern 4: Headers API

**Before (Next.js 15):**
```typescript
import { headers } from 'next/headers';

export default function Component() {
  const headersList = headers();
  const userAgent = headersList.get('user-agent');

  return <div>User Agent: {userAgent}</div>;
}
```

**After (Next.js 16):**
```typescript
import { headers } from 'next/headers';

export default async function Component() {
  const headersList = await headers();
  const userAgent = headersList.get('user-agent');

  return <div>User Agent: {userAgent}</div>;
}
```

### Pattern 5: Draft Mode

**Before (Next.js 15):**
```typescript
import { draftMode } from 'next/headers';

export default function Component() {
  const { isEnabled } = draftMode();

  return <div>Draft mode: {isEnabled ? 'on' : 'off'}</div>;
}
```

**After (Next.js 16):**
```typescript
import { draftMode } from 'next/headers';

export default async function Component() {
  const { isEnabled } = await draftMode();

  return <div>Draft mode: {isEnabled ? 'on' : 'off'}</div>;
}
```

### Pattern 6: Route Handlers

**Before (Next.js 15):**
```typescript
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const headersList = headers();
  const auth = headersList.get('authorization');

  return Response.json({ id: params.id, auth });
}
```

**After (Next.js 16):**
```typescript
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const [{ id }, headersList] = await Promise.all([
    params,
    headers()
  ]);
  const auth = headersList.get('authorization');

  return Response.json({ id, auth });
}
```

### Pattern 7: Layouts with Params

**Before (Next.js 15):**
```typescript
export default function Layout({
  children,
  params
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  return (
    <html lang={params.locale}>
      <body>{children}</body>
    </html>
  );
}
```

**After (Next.js 16):**
```typescript
export default async function Layout({
  children,
  params
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <html lang={locale}>
      <body>{children}</body>
    </html>
  );
}
```

## Common Migration Errors

### Error 1: Missing await

```typescript
const { id } = params;
```

**Fix:**
```typescript
const { id } = await params;
```

### Error 2: Non-async function

```typescript
export default function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
}
```

**Fix:**
```typescript
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
}
```

### Error 3: Wrong type annotation

```typescript
export default async function Page({ params }: { params: { id: string } }) {
  const { id } = await params;
}
```

**Fix:**
```typescript
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
}
```

### Error 4: Accessing properties directly

```typescript
const cookieStore = await cookies();
const allCookies = cookieStore.getAll();
```

**Fix (Same, but ensure await on cookies()):**
```typescript
const cookieStore = await cookies();
const allCookies = cookieStore.getAll();
```

## Performance Optimization

### Use Promise.all for Multiple Async Calls

**Inefficient (Sequential):**
```typescript
const { id } = await params;
const search = await searchParams;
const cookieStore = await cookies();
const headersList = await headers();
```

**Optimized (Parallel):**
```typescript
const [{ id }, search, cookieStore, headersList] = await Promise.all([
  params,
  searchParams,
  cookies(),
  headers()
]);
```

### When to Use Sequential vs Parallel

**Sequential (dependencies exist):**
```typescript
const { id } = await params;
const data = await fetchData(id);
```

**Parallel (no dependencies):**
```typescript
const [{ id }, cookieStore] = await Promise.all([
  params,
  cookies()
]);
```

## Type Safety

### Define Reusable Types

```typescript
type PageParams<T = {}> = Promise<T>;
type SearchParams = Promise<{ [key: string]: string | string[] | undefined }>;

type PageProps<T = {}> = {
  params: PageParams<T>;
  searchParams: SearchParams;
};

export default async function Page({ params, searchParams }: PageProps<{ id: string }>) {
  const { id } = await params;
  const search = await searchParams;

  return <div>{id}</div>;
}
```

### Type Guards with Promises

For advanced Promise type handling and type guards, see `@typescript/TYPES-type-guards` skill.

```typescript
function isValidId(id: string): id is string {
  return /^[a-z0-9]+$/i.test(id);
}

export default async function Page({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params;

  if (!isValidId(id)) {
    return <div>Invalid ID</div>;
  }

  return <div>Valid ID: {id}</div>;
}
```

## Special Cases

### Multi-Segment Routes

```typescript
export default async function Page({
  params
}: {
  params: Promise<{ category: string; product: string }>
}) {
  const { category, product } = await params;

  return (
    <div>
      <h1>Category: {category}</h1>
      <h2>Product: {product}</h2>
    </div>
  );
}
```

### Catch-All Routes

```typescript
export default async function Page({
  params
}: {
  params: Promise<{ slug: string[] }>
}) {
  const { slug } = await params;
  const path = slug.join('/');

  return <div>Path: {path}</div>;
}
```

### Optional Catch-All Routes

```typescript
export default async function Page({
  params
}: {
  params: Promise<{ slug?: string[] }>
}) {
  const { slug } = await params;

  if (!slug) {
    return <div>Home Page</div>;
  }

  return <div>Path: {slug.join('/')}</div>;
}
```

## References

For detailed migration examples, edge cases, and troubleshooting, see:

- [Detailed Async Patterns Reference](../../knowledge/async-patterns.md)
- Next.js 16 Migration Guide: https://nextjs.org/docs/app/building-your-application/upgrading/version-16
- `@typescript/TYPES-type-guards` for Promise type handling

## Migration Checklist

When migrating to async request APIs:

1. [ ] Update all `params` props to `Promise<T>` type
2. [ ] Update all `searchParams` props to `Promise<T>` type
3. [ ] Add `await` to all `cookies()` calls
4. [ ] Add `await` to all `headers()` calls
5. [ ] Add `await` to all `draftMode()` calls
6. [ ] Convert components to async where needed
7. [ ] Update type annotations
8. [ ] Use Promise.all for multiple async calls
9. [ ] Test all dynamic routes
10. [ ] Test all API routes
11. [ ] Verify TypeScript compilation
12. [ ] Run production build to catch errors

## Success Criteria

- No TypeScript errors related to Promise types
- All dynamic routes work correctly
- All API routes handle params properly
- Cookies, headers, and draft mode work as expected
- No runtime errors about "object is possibly undefined"
- Build completes successfully
