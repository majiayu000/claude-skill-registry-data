---
name: cloudflare-workers
description: Optimize code for Cloudflare Workers free plan with 10ms CPU limit. Use when writing API routes, server code, middleware, or discussing performance optimization.
---

# Cloudflare Workers Optimization

## Constraints

- **10ms CPU limit** on free plan (not wall-clock time)
- No heavy computation in request handlers
- No blocking operations

## Patterns

### Prefer Streaming

```typescript
// Good: Stream response
return new Response(readableStream, {
  headers: { 'Content-Type': 'application/octet-stream' },
});

// Bad: Buffer entire response
const data = await fetchAllData();
return new Response(JSON.stringify(data));
```

### Delegate to Client

Move these to browser when safe:

- Image manipulation (canvas API)
- Complex calculations
- Data transformations
- Sorting/filtering large datasets

### Efficient Algorithms

- Use early returns
- Avoid nested loops on large datasets
- Use Map/Set for O(1) lookups
- Paginate database queries

### Async Patterns

```typescript
// Good: Parallel fetches
const [user, settings] = await Promise.all([getUser(id), getSettings(id)]);

// Bad: Sequential fetches
const user = await getUser(id);
const settings = await getSettings(id);
```

### Response Caching

```typescript
return new Response(body, {
  headers: {
    'Cache-Control': 'public, max-age=3600',
    'CDN-Cache-Control': 'max-age=86400',
  },
});
```

## Anti-patterns

- Synchronous crypto operations
- Large JSON parsing in hot paths
- Regex on untrusted input without limits
- Deep object cloning
