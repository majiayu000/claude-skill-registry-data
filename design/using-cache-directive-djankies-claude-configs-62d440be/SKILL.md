---
name: using-cache-directive
description: Teach Cache Components model with 'use cache' directive in Next.js 16. Use when implementing caching, optimizing performance, working with dynamic data, or migrating from Next.js 15 caching patterns.
allowed-tools: Read, Write, Edit, Glob, Grep, TodoWrite
version: 1.0.0
---

# Next.js 16 Caching with 'use cache' Directive

## Paradigm Shift: Dynamic by Default

For understanding how caching interacts with Server Components and their rendering lifecycle, use the REACT-COMPONENTS-server-components skill from the react-19 plugin.

Next.js 16 introduces a fundamental change in how caching works:

**Next.js 15 and Earlier:**
- Everything cached by default
- Opt-out with `dynamic = 'force-dynamic'`, `no-store`, or revalidate
- Complex mental model with surprising behaviors

**Next.js 16:**
- Everything dynamic by default
- Opt-in to caching with `'use cache'` directive
- Explicit and predictable caching behavior

This is the most significant paradigm shift in Next.js 16 and affects every application.

## The 'use cache' Directive

The `'use cache'` directive is a string that tells Next.js to cache the output of a file, component, or function.

### File-Level Caching

Cache an entire route or layout:

```typescript
'use cache'

export default async function ProductsPage() {
  const products = await db.query.products.findMany()
  return <ProductList products={products} />
}
```

### Component-Level Caching

Cache a specific component:

```typescript
async function ProductList() {
  'use cache'

  const products = await db.query.products.findMany()
  return (
    <div>
      {products.map(p => <ProductCard key={p.id} product={p} />)}
    </div>
  )
}
```

### Function-Level Caching

Cache the result of a function:

```typescript
async function getProducts() {
  'use cache'
  return db.query.products.findMany()
}

export default async function ProductsPage() {
  const products = await getProducts()
  return <ProductList products={products} />
}
```

## When to Use 'use cache'

Use the `'use cache'` directive when:

1. **Data Changes Infrequently**: Product catalogs, blog posts, documentation
2. **Expensive Operations**: Complex database queries, external API calls, computations
3. **High Traffic Pages**: Landing pages, marketing pages, public content
4. **Shared Data**: Data used across multiple routes or components

```typescript
async function getBlogPosts() {
  'use cache'
  return db.query.posts.findMany({
    where: { published: true },
    orderBy: { publishedAt: 'desc' }
  })
}
```

## When NOT to Use 'use cache'

Do NOT use `'use cache'` when:

1. **User-Specific Data**: User profiles, personalized content, authentication state
2. **Real-Time Data**: Live updates, activity feeds, chat messages
3. **Dynamic Parameters**: Content that varies by user, session, or request
4. **Write Operations**: Forms, mutations, actions

```typescript
export default async function UserDashboard() {
  const session = await auth()
  const user = await db.query.users.findFirst({
    where: { id: session.userId }
  })

  return <Dashboard user={user} />
}
```

## Cache Configuration

Configure cache behavior with the `cacheLife` and `cacheTag` options:

### Using cacheLife

Specify how long to cache:

```typescript
'use cache'
export const cacheLife = 'hours'

export default async function NewsPage() {
  const articles = await fetchNews()
  return <ArticleList articles={articles} />
}
```

Available presets:
- `'seconds'`: 1 second (real-time-ish)
- `'minutes'`: 5 minutes (frequent updates)
- `'hours'`: 1 hour (moderate updates)
- `'days'`: 1 day (infrequent updates)
- `'weeks'`: 1 week (rarely changes)
- `'max'`: 1 year (effectively static)

### Custom Cache Durations

Define custom cache profiles:

```typescript
'use cache'
export const cacheLife = {
  stale: 60,
  revalidate: 300,
  expire: 3600
}
```

- `stale`: Serve cached data for this many seconds
- `revalidate`: Revalidate in background after this many seconds
- `expire`: Hard expiration after this many seconds

### Using cacheTag

Tag caches for on-demand revalidation:

```typescript
'use cache'
export const cacheTag = 'products'

async function getProducts() {
  return db.query.products.findMany()
}
```

Then revalidate by tag:

```typescript
'use server'

import { revalidateTag } from 'next/cache'

export async function updateProduct(id: string, data: ProductInput) {
  await db.update(products).set(data).where(eq(products.id, id))
  revalidateTag('products')
}
```

## Anti-Patterns to Avoid

### 1. Don't Use unstable_cache

Next.js 15's `unstable_cache` is replaced by `'use cache'`:

```typescript
import { unstable_cache } from 'next/cache'

const getProducts = unstable_cache(
  async () => {
    return db.query.products.findMany()
  },
  ['products'],
  { revalidate: 3600 }
)
```

```typescript
async function getProducts() {
  'use cache'
  return db.query.products.findMany()
}
```

### 2. Don't Export revalidate from Components

Next.js 15's route segment config doesn't work with Cache Components:

```typescript
export const revalidate = 3600

export default async function Page() {
  const data = await fetch('...')
  return <div>{data}</div>
}
```

```typescript
'use cache'
export const cacheLife = 'hours'

export default async function Page() {
  const data = await fetch('...')
  return <div>{data}</div>
}
```

### 3. Don't Cache User-Specific Content

```typescript
'use cache'

export default async function Dashboard() {
  const session = await auth()
  const userData = await getUserData(session.userId)
  return <UserDashboard data={userData} />
}
```

```typescript
export default async function Dashboard() {
  const session = await auth()
  const userData = await getUserData(session.userId)
  return <UserDashboard data={userData} />
}
```

### 4. Don't Overuse File-Level Caching

```typescript
'use cache'

export default async function Page() {
  const session = await auth()
  const products = await getProducts()

  return (
    <div>
      <UserGreeting user={session.user} />
      <ProductList products={products} />
    </div>
  )
}
```

```typescript
async function CachedProductList() {
  'use cache'
  const products = await getProducts()
  return <ProductList products={products} />
}

export default async function Page() {
  const session = await auth()

  return (
    <div>
      <UserGreeting user={session.user} />
      <CachedProductList />
    </div>
  )
}
```

## Migration from Next.js 15

### Remove fetch Cache Options

```typescript
const data = await fetch('https://api.example.com/data', {
  cache: 'force-cache',
  next: { revalidate: 3600 }
})
```

```typescript
async function getData() {
  'use cache'
  return fetch('https://api.example.com/data')
}

const data = await getData()
```

### Replace Route Segment Config

```typescript
export const revalidate = 3600
export const dynamic = 'force-static'

export default async function Page() {
  return <div>...</div>
}
```

```typescript
'use cache'
export const cacheLife = 'hours'

export default async function Page() {
  return <div>...</div>
}
```

### Update unstable_cache Usage

```typescript
import { unstable_cache } from 'next/cache'

const getCachedPosts = unstable_cache(
  async () => db.query.posts.findMany(),
  ['posts'],
  { revalidate: 300 }
)
```

```typescript
async function getPosts() {
  'use cache'
  return db.query.posts.findMany()
}
```

## Best Practices

1. **Start Uncached**: Begin with dynamic behavior, add caching only where needed
2. **Cache at the Right Level**: Use function-level caching for shared data, component-level for UI chunks
3. **Use Cache Tags**: Enable on-demand revalidation for data that changes on specific events
4. **Monitor Cache Effectiveness**: Use Next.js analytics to see cache hit rates
5. **Test Cache Behavior**: Verify caching works as expected in production mode

## Common Patterns

### Cached Data Fetching Layer

```typescript
async function getProduct(id: string) {
  'use cache'
  return db.query.products.findFirst({
    where: eq(products.id, id)
  })
}

async function getProducts() {
  'use cache'
  return db.query.products.findMany()
}
```

### Cached Component with Dynamic Parent

```typescript
async function StaticProductGrid() {
  'use cache'
  const products = await getProducts()
  return <ProductGrid products={products} />
}

export default async function Page() {
  const session = await auth()

  return (
    <div>
      <UserNav user={session?.user} />
      <StaticProductGrid />
    </div>
  )
}
```

### Tagged Cache for Mutations

```typescript
'use cache'
export const cacheTag = 'inventory'

async function getInventory() {
  return db.query.inventory.findMany()
}
```

```typescript
'use server'

import { revalidateTag } from 'next/cache'

export async function updateInventory(data: InventoryUpdate) {
  await db.update(inventory).set(data)
  revalidateTag('inventory')
}
```

## Reference

For comprehensive examples and patterns, see:
- [cache-examples.md](./references/cache-examples.md) - Detailed examples for all caching scenarios
