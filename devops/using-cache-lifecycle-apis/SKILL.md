---
name: using-cache-lifecycle-apis
description: Teach cache lifecycle APIs in Next.js 16 - cacheLife(), cacheTag(), updateTag(), refresh(), revalidateTag(). Use when managing cache invalidation, setting cache policies, or implementing cache tags.
allowed-tools: Read, Write, Edit, Glob, Grep, TodoWrite
version: 1.0.0
---

# Cache Lifecycle APIs in Next.js 16

Next.js 16 introduces comprehensive cache lifecycle APIs for fine-grained control over caching behavior. These APIs work together to manage cache policies, tagging, and invalidation across both private (CDN) and remote (server) caches.

## Core Lifecycle APIs

### cacheLife()

Sets cache duration profiles for fetch requests and route handlers. Replaces the need for manual revalidation intervals.

```typescript
import { unstable_cacheLife as cacheLife } from 'next/cache';

export async function GET() {
  'use cache';
  cacheLife('hours');

  const data = await fetch('https://api.example.com/data');
  return Response.json(data);
}
```

**Built-in Profiles:**

- `default`: 15 minutes stale, 1 day revalidate, 1 week expire
- `seconds`: 1 second stale, 10 seconds revalidate, 1 minute expire
- `minutes`: 5 minutes stale, 1 hour revalidate, 1 day expire
- `hours`: 5 minutes stale, 1 hour revalidate, 1 day expire
- `days`: 5 minutes stale, 12 hours revalidate, 7 days expire
- `weeks`: 5 minutes stale, 24 hours revalidate, 30 days expire
- `max`: 5 minutes stale, indefinite revalidate, indefinite expire

**Custom Profiles:**

```typescript
cacheLife({
  stale: 60,
  revalidate: 3600,
  expire: 86400,
});
```

**Multiple Profiles:**

```typescript
cacheLife('hours', 'days');
```

### cacheTag()

Associates cache entries with tags for targeted invalidation. Tags enable logical grouping of cached content.

```typescript
import { unstable_cacheTag as cacheTag } from 'next/cache';

export async function GET() {
  'use cache';
  cacheTag('products');

  const products = await db.query.products.findMany();
  return Response.json(products);
}
```

**Multiple Tags:**

```typescript
cacheTag('products', 'featured');
```

**Tag Naming Convention:**

- Use descriptive, hierarchical names: `user:123`, `posts:featured`
- Lowercase with hyphens or colons
- Avoid special characters

### updateTag() / revalidateTag()

Invalidates all cache entries associated with a tag. `revalidateTag()` has a new signature in Next.js 16.

**Breaking Change in Next.js 16:**

```typescript
import { revalidateTag } from 'next/cache';

export async function POST(request: Request) {
  const body = await request.json();

  await revalidateTag('products');

  return Response.json({ revalidated: true });
}
```

The new signature is async and returns a Promise. Previous versions were synchronous.

**Server Action Usage:**

```typescript
'use server';

import { revalidateTag } from 'next/cache';

export async function updateProducts() {
  await db.products.update();

  await revalidateTag('products');
  await revalidateTag('featured');
}
```

### refresh()

Forces immediate revalidation of the current page without invalidating tags.

```typescript
import { refresh } from 'next/cache';

export async function POST() {
  'use server';

  await db.update();

  refresh();

  return { success: true };
}
```

## Private vs Remote Caching

### Private Caching (CDN)

Caches at the edge closest to users. Controlled by Cache-Control headers.

```typescript
export async function GET() {
  'use cache';
  cacheLife('hours');

  return Response.json(data, {
    headers: {
      'Cache-Control': 'private, max-age=3600',
    },
  });
}
```

**Use Cases:**
- User-specific content
- Authenticated data
- Regional content

### Remote Caching (Server)

Caches on the Next.js server or shared infrastructure. Controlled by cacheLife() and tags.

```typescript
export async function GET() {
  'use cache';
  cacheLife('days');
  cacheTag('public-data');

  return Response.json(data);
}
```

**Use Cases:**
- Public data
- Shared across users
- Database query results

### Hybrid Strategy

Combine both for optimal performance:

```typescript
export async function GET(request: Request) {
  'use cache';
  cacheLife('hours');
  cacheTag('products');

  const userId = request.headers.get('x-user-id');
  const products = await getProducts(userId);

  return Response.json(products, {
    headers: {
      'Cache-Control': 'private, s-maxage=3600, stale-while-revalidate=86400',
    },
  });
}
```

## Cache Invalidation Strategies

### On-Demand Invalidation

Invalidate immediately when data changes:

```typescript
'use server';

import { revalidateTag } from 'next/cache';

export async function createProduct(formData: FormData) {
  await db.products.create({
    name: formData.get('name'),
  });

  await revalidateTag('products');
  await revalidateTag('homepage');
}
```

### Scheduled Invalidation

Use cacheLife() with appropriate profiles for periodic updates:

```typescript
export async function GET() {
  'use cache';
  cacheLife('hours');

  const stats = await getAnalytics();
  return Response.json(stats);
}
```

### Granular Invalidation

Tag different aspects of data for targeted updates:

```typescript
export async function getProduct(id: string) {
  'use cache';
  cacheTag(`product:${id}`, 'products', 'catalog');

  return db.query.products.findFirst({ where: { id } });
}

export async function updateProduct(id: string, data: any) {
  'use server';

  await db.products.update({ where: { id }, data });

  await revalidateTag(`product:${id}`);
}
```

### Cascading Invalidation

Invalidate related caches together:

```typescript
export async function deleteProduct(id: string) {
  'use server';

  const product = await db.products.findUnique({ where: { id } });

  await db.products.delete({ where: { id } });

  await Promise.all([
    revalidateTag(`product:${id}`),
    revalidateTag('products'),
    revalidateTag(`category:${product.categoryId}`),
    revalidateTag('search-results'),
  ]);
}
```

## Complete Example: E-commerce Product Management

```typescript
import {
  unstable_cacheLife as cacheLife,
  unstable_cacheTag as cacheTag,
  revalidateTag,
} from 'next/cache';

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  'use cache';
  cacheLife('hours');
  cacheTag(`product:${params.id}`, 'products');

  const product = await db.query.products.findFirst({
    where: { id: params.id },
    with: { reviews: true, category: true },
  });

  return Response.json(product, {
    headers: {
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
    },
  });
}

export async function PUT(
  request: Request,
  { params }: { params: { id: string } }
) {
  const body = await request.json();

  const product = await db.products.update({
    where: { id: params.id },
    data: body,
  });

  await Promise.all([
    revalidateTag(`product:${params.id}`),
    revalidateTag('products'),
    revalidateTag(`category:${product.categoryId}`),
  ]);

  return Response.json({ success: true, product });
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  const product = await db.products.findUnique({
    where: { id: params.id },
  });

  await db.products.delete({ where: { id: params.id } });

  await Promise.all([
    revalidateTag(`product:${params.id}`),
    revalidateTag('products'),
    revalidateTag(`category:${product.categoryId}`),
    revalidateTag('search-results'),
    revalidateTag('homepage'),
  ]);

  return Response.json({ success: true });
}
```

## Best Practices

1. **Profile Selection**: Use built-in profiles for consistency
2. **Tag Hierarchy**: Create logical tag groupings for efficient invalidation
3. **Async Handling**: Always await revalidateTag() calls
4. **Tag Reuse**: Apply same tags to related cached content
5. **Private Data**: Use private Cache-Control for user-specific content
6. **Granular Tags**: Combine specific and general tags for flexibility
7. **Error Handling**: Wrap invalidation in try-catch blocks
8. **Performance**: Batch revalidateTag() calls with Promise.all()

## Query Optimization for Cached Data

When caching database queries, optimize query selection and pagination to prevent performance issues:

- If optimizing field selection in cached Prisma queries, use the optimizing-query-selection skill from prisma-6 for select() patterns preventing over-fetching
- If implementing pagination in cached Prisma endpoints, use the implementing-query-pagination skill from prisma-6 for cursor vs offset pagination patterns
- If implementing query result caching with Redis, use the implementing-query-caching skill from prisma-6 for cache key generation, invalidation strategies, and TTL management

## Common Patterns

### Time-Based + Tag-Based Caching

```typescript
export async function GET() {
  'use cache';
  cacheLife('days');
  cacheTag('blog-posts');

  const posts = await db.query.posts.findMany();
  return Response.json(posts);
}
```

### User-Scoped Caching

```typescript
export async function GET(request: Request) {
  'use cache';
  const userId = request.headers.get('x-user-id');
  cacheTag(`user:${userId}`);
  cacheLife('minutes');

  const data = await getUserData(userId);

  return Response.json(data, {
    headers: { 'Cache-Control': 'private, max-age=300' },
  });
}
```

### Background Revalidation

```typescript
export async function webhookHandler(request: Request) {
  const event = await request.json();

  if (event.type === 'product.updated') {
    await revalidateTag(`product:${event.productId}`);
    await revalidateTag('products');
  }

  return Response.json({ received: true });
}
```

## Migration Notes

When upgrading from Next.js 15 to 16:

1. Update all `revalidateTag()` calls to handle Promises:
   ```typescript
   revalidateTag('tag');
   ```
   becomes:
   ```typescript
   await revalidateTag('tag');
   ```

2. Replace manual revalidation with cacheLife():
   ```typescript
   export const revalidate = 3600;
   ```
   becomes:
   ```typescript
   cacheLife('hours');
   ```

3. Use cacheTag() instead of custom headers for invalidation

4. Import APIs from 'next/cache' with unstable_ prefix where required
