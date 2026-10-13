---
name: next-cache-components
description: "Next.js 16+ Cache Components / Partial Prerendering (PPR) — mix static, cached, and dynamic content in a single route. Use when enabling cacheComponents, applying the 'use cache' directive, choosing cache profiles, or migrating from experimental.ppr. Explains the three content types: static (auto-prerendered), cached, and dynamic (Suspense)."
paths: ["next.config.*", "app/**"]
---

# Cache Components (Next.js 16+)

Cache Components enable Partial Prerendering (PPR) — mix static, cached, and dynamic content in a single route.

## Enable Cache Components

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

This replaces the old `experimental.ppr` flag.

## Three Content Types

With Cache Components enabled, content falls into three categories:

### 1. Static (Auto-Prerendered)
Synchronous code, imports, pure computations — prerendered at build time.

### 2. Cached (`use cache`)
Async data that doesn't need fresh fetches every request:
```typescript
async function BlogPosts() {
  'use cache'
  cacheLife('hours')
  const posts = await db.posts.findMany()
  return <PostList posts={posts} />
}
```

### 3. Dynamic (Suspense)
Runtime data that must be fresh — wrap in Suspense:
```typescript
import { Suspense } from 'react'

export default function Page() {
  return (
    <>
      <BlogPosts />  {/* Cached */}

      <Suspense fallback={<p>Loading...</p>}>
        <UserPreferences />  {/* Dynamic — streams in */}
      </Suspense>
    </>
  )
}
```

## use cache Directive

**File level:**
```typescript
'use cache'
export default async function Page() { /* entire page is cached */ }
```

**Component level:**
```typescript
export async function CachedComponent() {
  'use cache'
  // ...
}
```

**Function level:**
```typescript
export async function getData() {
  'use cache'
  return db.query('SELECT * FROM posts')
}
```

## Cache Profiles

**Built-in profiles:** `'default'`, `'minutes'`, `'hours'`, `'days'`, `'weeks'`, `'max'`

**Custom lifetime:**
```typescript
import { cacheLife } from 'next/cache'

async function getData() {
  'use cache'
  cacheLife('hours')  // or use cacheLife({ stale: 3600, revalidate: 7200, expire: 86400 })
  return fetch('/api/data')
}
```

## Cache Invalidation

**`cacheTag()`** — tag cached content for later invalidation:
```typescript
import { cacheTag } from 'next/cache'

async function getProducts() {
  'use cache'
  cacheTag('products', `product-${id}`)
  return db.products.findMany()
}
```

**`updateTag()`** — immediate invalidation within the same request (server action):
```typescript
'use server'
import { updateTag } from 'next/cache'
export async function updateProduct(id: string, data: FormData) {
  await db.products.update({ where: { id }, data })
  updateTag(`product-${id}`)  // Same request sees fresh data
}
```

**`revalidateTag()`** — background revalidation (stale-while-revalidate):
```typescript
'use server'
import { revalidateTag } from 'next/cache'
export async function createPost(data: FormData) {
  await db.posts.create({ data })
  revalidateTag('posts')  // Background — next request sees fresh data
}
```

## Runtime Data Constraint

**Cannot** access `cookies()`, `headers()`, or `searchParams` inside `use cache`.

**Solution — pass as arguments:**
```typescript
// Wrong — runtime API inside use cache
async function CachedProfile() {
  'use cache'
  const session = (await cookies()).get('session')?.value  // Error!
}

// Correct — extract outside, pass as argument
async function ProfilePage() {
  const session = (await cookies()).get('session')?.value
  return <CachedProfile sessionId={session} />
}

async function CachedProfile({ sessionId }: { sessionId: string }) {
  'use cache'
  const data = await fetchUserData(sessionId)
  return <div>{data.name}</div>
}
```

**Exception:** `'use cache: private'` allows runtime APIs for compliance requirements.

## Cache Key Generation

Keys are automatic based on:
- Build ID — invalidates all caches on deploy
- Function ID — hash of function location
- Serializable arguments — props become part of key
- Closure variables — outer scope values included

## Migration from Previous Versions

| Old | Replacement |
|---|---|
| `experimental.ppr` | `cacheComponents: true` |
| `dynamic = 'force-dynamic'` | Remove (default behavior) |
| `dynamic = 'force-static'` | `'use cache'` + `cacheLife('max')` |
| `revalidate = N` | `cacheLife({ revalidate: N })` |
| `unstable_cache()` | `'use cache'` directive |

**`unstable_cache` → `use cache` migration:**
- No manual cache keys — use cache auto-generates from arguments
- Replace `options.tags` with `cacheTag()` inside the function
- Replace `options.revalidate` with `cacheLife({ revalidate: N })` or built-in profile

## Limitations

- **Edge runtime not supported** — requires Node.js
- **Static export not supported** — needs server
- **Non-deterministic values** (`Math.random()`, `Date.now()`) execute once at build time

For request-time randomness outside cache, use `connection()`:
```typescript
import { connection } from 'next/server'
async function DynamicContent() {
  await connection()
  const id = crypto.randomUUID()  // Different per request
  return <div>{id}</div>
}
```

---

**Source:** https://officialskills.sh/vercel-labs/skills/next-cache-components