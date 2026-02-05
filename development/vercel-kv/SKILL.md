---
name: vercel-kv
description: |
  Integrate Redis-compatible Vercel KV for caching, session management, and rate limiting in Next.js applications. Powered by Upstash with strong consistency and TTL support.

  Use when implementing cache strategies, storing temporary data with expiration, building rate limiters, or troubleshooting missing environment variables, serialization errors, or rate limit issues.
---

# Vercel KV

**Last Updated**: 2025-11-28
**Version**: @vercel/kv@3.0.0 (Redis-compatible, powered by Upstash)

---

## Quick Start

```bash
# Create KV: Vercel Dashboard → Storage → KV
vercel env pull .env.local  # Creates KV_REST_API_URL and KV_REST_API_TOKEN
npm install @vercel/kv
```

**Basic Usage**:
```typescript
import { kv } from '@vercel/kv';

// Set with TTL (expires in 1 hour)
await kv.setex('session:abc', 3600, { userId: 123 });

// Get
const session = await kv.get('session:abc');

// Increment counter (atomic)
const views = await kv.incr('views:post:123');
```

**CRITICAL**: Always use namespaced keys (`user:123` not `123`) and set TTL for temporary data.

---

## Common Patterns

**Caching** (cache-aside):
```typescript
const cached = await kv.get(`post:${slug}`);
if (cached) return cached;

const post = await db.query.posts.findFirst({ where: eq(posts.slug, slug) });
await kv.setex(`post:${slug}`, 3600, post); // Cache 1 hour
return post;
```

**Rate Limiting**:
```typescript
async function checkRateLimit(ip: string): Promise<boolean> {
  const key = `ratelimit:${ip}`;
  const current = await kv.incr(key);
  if (current === 1) await kv.expire(key, 60); // 60s window
  return current <= 10; // 10 requests per window
}
```

**Session Management**:
```typescript
const sessionId = crypto.randomUUID();
await kv.setex(`session:${sessionId}`, 7 * 24 * 3600, { userId });
```

**Pipeline** (batch operations):
```typescript
const pipeline = kv.pipeline();
pipeline.set('user:1', data);
pipeline.incr('counter');
const results = await pipeline.exec(); // Single round-trip
```

**Key Naming**: Use namespaces like `user:123`, `post:abc:views`, `ratelimit:ip:endpoint`

---

## Critical Rules

**Always**:
- ✅ Set TTL for temporary data (`setex` not `set`)
- ✅ Use namespaced keys (`user:123` not `123`)
- ✅ Handle null returns (non-existent keys)
- ✅ Use pipeline for batch operations

**Never**:
- ❌ Forget to set TTL (memory leak)
- ❌ Store large values >1MB (use Vercel Blob)
- ❌ Use KV as primary database (it's a cache)
- ❌ Store non-JSON-serializable data (functions, BigInt, circular refs)

---

## Known Issues Prevention

This skill prevents **10 documented issues**:

### Issue #1: Missing Environment Variables
**Error**: `Error: KV_REST_API_URL is not defined` or `KV_REST_API_TOKEN is not defined`
**Source**: https://vercel.com/docs/storage/vercel-kv/quickstart
**Why It Happens**: Environment variables not set locally or in deployment
**Prevention**: Run `vercel env pull .env.local` and ensure `.env.local` is in `.gitignore`.

### Issue #2: JSON Serialization Error
**Error**: `TypeError: Do not know how to serialize a BigInt` or circular reference errors
**Source**: https://github.com/vercel/storage/issues/89
**Why It Happens**: Trying to store non-JSON-serializable data (functions, BigInt, circular refs)
**Prevention**: Only store plain objects, arrays, strings, numbers, booleans, null. Convert BigInt to string.

### Issue #3: Key Naming Collisions
**Error**: Unexpected data returned, data overwritten by different feature
**Source**: Production debugging, best practices
**Why It Happens**: Using generic key names like `cache`, `data`, `temp` across different features
**Prevention**: Always use namespaced keys: `feature:id:type` pattern.

### Issue #4: TTL Not Set
**Error**: Memory usage grows indefinitely, old data never expires
**Source**: Vercel KV best practices
**Why It Happens**: Using `set()` without `setex()` for temporary data
**Prevention**: Use `setex(key, ttl, value)` for all temporary data. Set appropriate TTL (seconds).

### Issue #5: Rate Limit Exceeded (Free Tier)
**Error**: `Error: Rate limit exceeded` or commands failing
**Source**: https://vercel.com/docs/storage/vercel-kv/limits
**Why It Happens**: Exceeding 30,000 commands/month on free tier
**Prevention**: Monitor usage in Vercel dashboard, upgrade plan if needed, use caching to reduce KV calls.

### Issue #6: Storing Large Values
**Error**: `Error: Value too large` or performance degradation
**Source**: https://vercel.com/docs/storage/vercel-kv/limits
**Why It Happens**: Trying to store values >1MB in KV
**Prevention**: Use Vercel Blob for files/images. Keep KV values small (<100KB recommended).

### Issue #7: Type Mismatch on Get
**Error**: TypeScript errors, runtime type errors
**Source**: Common TypeScript issue
**Why It Happens**: `kv.get()` returns `unknown` type, need to cast or validate
**Prevention**: Use type assertion with validation: `const user = await kv.get<User>('user:123')` and validate with Zod.

### Issue #8: Pipeline Errors Not Handled
**Error**: Silent failures, partial execution
**Source**: https://github.com/vercel/storage/issues/120
**Why It Happens**: Pipeline execution can have individual command failures
**Prevention**: Check results array from `pipeline.exec()` and handle errors.

### Issue #9: Scan Operation Inefficiency
**Error**: Slow queries, timeout errors
**Source**: Redis best practices
**Why It Happens**: Using `scan()` with large datasets or wrong cursor handling
**Prevention**: Limit `count` parameter, iterate properly with cursor, avoid full scans in production.

### Issue #10: Missing TTL Refresh
**Error**: Session expires too early, cache invalidates prematurely
**Source**: Production debugging
**Why It Happens**: Not refreshing TTL on access (sliding expiration)
**Prevention**: Use `expire(key, newTTL)` on access to implement sliding windows.

---

## Advanced Patterns

**Distributed Lock** (prevents race conditions):
```typescript
const lockKey = `lock:${resource}`;
const lockValue = crypto.randomUUID();

const acquired = await kv.setnx(lockKey, lockValue);
if (acquired) {
  await kv.expire(lockKey, 10); // TTL prevents deadlock
  try {
    await processOrders();
  } finally {
    const current = await kv.get(lockKey);
    if (current === lockValue) await kv.del(lockKey);
  }
}
```

**Leaderboard** (sorted sets):
```typescript
await kv.zadd('leaderboard', { score, member: userId.toString() });
const top = await kv.zrange('leaderboard', 0, 9, { rev: true, withScores: true });
const rank = await kv.zrevrank('leaderboard', userId.toString());
```
