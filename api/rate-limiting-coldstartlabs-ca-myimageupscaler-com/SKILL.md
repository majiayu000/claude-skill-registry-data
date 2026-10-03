---
name: rate-limiting
description: Implement and optimize rate limiting for APIs and routes. Use when protecting endpoints, preventing abuse, or managing resource usage across different user tiers.
---

# Rate Limiting Implementation Guide

## Overview

Rate limiting protects your API from abuse, ensures fair resource usage, and prevents denial of service attacks. This skill covers implementing rate limiting with sliding window algorithms, tier-based limits, and edge deployment patterns.

## Core Concepts

### Sliding Window Algorithm

The sliding window algorithm provides smooth rate limiting by tracking request timestamps within a moving time window.

```typescript
interface IRateLimitEntry {
  timestamps: number[];
}

interface IRateLimitResult {
  success: boolean;
  remaining: number;
  reset: number;
}

function createRateLimiter(limit: number, windowMs: number) {
  const store = new Map<string, IRateLimitEntry>();

  // Cleanup old entries periodically
  setInterval(
    () => {
      const now = Date.now();
      const fiveMinutesAgo = now - 5 * 60 * 1000;

      for (const [key, entry] of store.entries()) {
        entry.timestamps = entry.timestamps.filter(t => t > fiveMinutesAgo);
        if (entry.timestamps.length === 0) {
          store.delete(key);
        }
      }
    },
    5 * 60 * 1000
  );

  return async (identifier: string): Promise<IRateLimitResult> => {
    const now = Date.now();
    const windowStart = now - windowMs;

    let entry = store.get(identifier);
    if (!entry) {
      entry = { timestamps: [] };
      store.set(identifier, entry);
    }

    // Remove timestamps outside current window
    entry.timestamps = entry.timestamps.filter(t => t > windowStart);

    // Check if limit exceeded
    if (entry.timestamps.length >= limit) {
      const oldestTimestamp = entry.timestamps[0];
      const resetTime = oldestTimestamp + windowMs;

      return {
        success: false,
        remaining: 0,
        reset: resetTime,
      };
    }

    // Add current timestamp
    entry.timestamps.push(now);

    return {
      success: true,
      remaining: limit - entry.timestamps.length,
      reset: now + windowMs,
    };
  };
}
```

### Rate Limit Configurations

Different endpoints and user tiers require different limits:

```typescript
// Base rate limiters
export const rateLimit = {
  limit: createRateLimiter(50, 10 * 1000), // 50 requests per 10 seconds
};

export const publicRateLimit = {
  limit: createRateLimiter(10, 10 * 1000), // 10 requests per 10 seconds
};

export const upscaleRateLimit = {
  limit: createRateLimiter(5, 60 * 1000), // 5 requests per minute
};

// Tier-based rate limiters
export const tierRateLimits = {
  free: createRateLimiter(10, 60 * 1000), // 10 requests per minute
  starter: createRateLimiter(30, 60 * 1000), // 30 requests per minute
  hobby: createRateLimiter(60, 60 * 1000), // 60 requests per minute
  pro: createRateLimiter(120, 60 * 1000), // 120 requests per minute
  enterprise: createRateLimiter(500, 60 * 1000), // 500 requests per minute
};
```

## Middleware Patterns

### IP-Based Rate Limiting

For public endpoints and anonymous users:

```typescript
import { NextRequest, NextResponse } from 'next/server';

export function getClientIp(req: NextRequest): string {
  // Cloudflare-specific header (most reliable on Cloudflare)
  const cfConnectingIp = req.headers.get('cf-connecting-ip');
  if (cfConnectingIp) return cfConnectingIp;

  // Standard forwarded header
  const xForwardedFor = req.headers.get('x-forwarded-for');
  if (xForwardedFor) {
    const firstIp = xForwardedFor.split(',')[0]?.trim();
    if (firstIp) return firstIp;
  }

  // Alternative header
  const xRealIp = req.headers.get('x-real-ip');
  if (xRealIp) return xRealIp;

  return 'unknown';
}

export async function applyPublicRateLimit(
  req: NextRequest,
  res: NextResponse
): Promise<NextResponse | null> {
  const ip = getClientIp(req);
  const { success, remaining, reset } = await publicRateLimit.limit(ip);

  const rateLimitHeaders = createRateLimitHeaders(10, remaining, reset);

  if (!success) {
    return NextResponse.json(
      {
        error: 'Too many requests',
        details: {
          retryAfter: Math.ceil((reset - Date.now()) / 1000),
        },
      },
      {
        status: 429,
        headers: rateLimitHeaders,
      }
    );
  }

  // Add headers to successful response
  Object.entries(rateLimitHeaders).forEach(([key, value]) => {
    if (key !== 'Retry-After') {
      res.headers.set(key, value);
    }
  });

  return null;
}
```

### User-Based Rate Limiting

For authenticated users with different tiers:

```typescript
interface IRateLimitHeaders {
  'X-RateLimit-Limit': string;
  'X-RateLimit-Remaining': string;
  'X-RateLimit-Reset': string;
  'Retry-After': string;
}

export function createRateLimitHeaders(
  limit: number,
  remaining: number,
  reset: number
): IRateLimitHeaders {
  return {
    'X-RateLimit-Limit': limit.toString(),
    'X-RateLimit-Remaining': remaining.toString(),
    'X-RateLimit-Reset': new Date(reset).toISOString(),
    'Retry-After': Math.ceil((reset - Date.now()) / 1000).toString(),
  };
}

export async function applyUserRateLimit(
  userId: string,
  userTier: string,
  res: NextResponse
): Promise<NextResponse | null> {
  // Get rate limiter based on user tier
  const tierLimiter = tierRateLimits[userTier] || tierRateLimits.free;
  const tierLimits = {
    free: 10,
    starter: 30,
    hobby: 60,
    pro: 120,
    enterprise: 500,
  };

  const limit = tierLimits[userTier] || tierLimits.free;
  const { success, remaining, reset } = await tierLimiter(userId);

  const rateLimitHeaders = createRateLimitHeaders(limit, remaining, reset);

  if (!success) {
    return NextResponse.json(
      {
        error: 'Rate limit exceeded',
        details: {
          tier: userTier,
          limit,
          reset: new Date(reset).toISOString(),
          retryAfter: Math.ceil((reset - Date.now()) / 1000),
        },
      },
      {
        status: 429,
        headers: rateLimitHeaders,
      }
    );
  }

  // Add headers to successful response
  Object.entries(rateLimitHeaders).forEach(([key, value]) => {
    if (key !== 'Retry-After') {
      res.headers.set(key, value);
    }
  });

  return null;
}
```

### Route Middleware Integration

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { applyPublicRateLimit } from '@lib/middleware/rateLimit';

export async function middleware(req: NextRequest) {
  const res = NextResponse.next();

  // Apply rate limiting to API routes
  if (req.nextUrl.pathname.startsWith('/api/')) {
    const rateLimitResponse = await applyPublicRateLimit(req, res);
    if (rateLimitResponse) {
      return rateLimitResponse;
    }
  }

  return res;
}
```

## API Route Protection

### Individual Route Protection

```typescript
// app/api/upscale/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getAuthenticatedUser } from '@server/middleware/getAuthenticatedUser';
import { applyUserRateLimit, upscaleRateLimit } from '@lib/middleware/rateLimit';

export async function POST(req: NextRequest) {
  const res = NextResponse.next();

  // Check authentication
  const user = await getAuthenticatedUser(req);
  if (!user) {
    return NextResponse.json({ error: 'Authentication required' }, { status: 401 });
  }

  // Apply user-based rate limit
  const userRateLimitResponse = await applyUserRateLimit(user.id, user.subscription.tier, res);
  if (userRateLimitResponse) {
    return userRateLimitResponse;
  }

  // Apply additional upscale-specific rate limit
  const upscaleResponse = await upscaleRateLimit.limit(user.id);
  if (!upscaleResponse.success) {
    return NextResponse.json(
      {
        error: 'Upscale rate limit exceeded',
        details: {
          reset: new Date(upscaleResponse.reset).toISOString(),
        },
      },
      {
        status: 429,
        headers: createRateLimitHeaders(5, upscaleResponse.remaining, upscaleResponse.reset),
      }
    );
  }

  // Process the request...
  return res;
}
```

## Tier-Based Rate Limiting

### Configuration with Subscription Tiers

```typescript
// shared/config/rate-limit.config.ts
import { SUBSCRIPTION_CONFIG } from './subscription.config';

export const RATE_LIMIT_CONFIG = {
  // Default limits per minute
  defaultLimits: {
    free: 10, // 10 requests per minute
    starter: 30, // 30 requests per minute
    hobby: 60, // 60 requests per minute
    pro: 120, // 120 requests per minute
    enterprise: 500, // 500 requests per minute
  },

  // Endpoint-specific multipliers
  endpointMultipliers: {
    '/api/upscale': 0.5, // Half the normal limit
    '/api/analyze-image': 1.5, // 1.5x the normal limit
    '/api/models': 2.0, // 2x the normal limit
  },

  // Time windows (in milliseconds)
  windows: {
    default: 60 * 1000, // 1 minute
    strict: 60 * 1000, // 1 minute
    lenient: 60 * 1000 * 5, // 5 minutes
  },

  // Special routes with custom limits
  customLimits: {
    '/api/upscale': {
      free: 5,
      starter: 15,
      hobby: 30,
      pro: 60,
      enterprise: 250,
      window: 60 * 1000, // 1 minute
    },
    '/api/webhooks/stripe': {
      // Higher limits for webhooks to handle bursts
      free: 100,
      starter: 500,
      hobby: 1000,
      pro: 2000,
      enterprise: 5000,
      window: 60 * 1000, // 1 minute
    },
  },
};

export function getRateLimitForTier(
  tier: string,
  endpoint?: string
): { limit: number; window: number } {
  // Check for custom endpoint limits
  if (endpoint && RATE_LIMIT_CONFIG.customLimits[endpoint]) {
    const custom = RATE_LIMIT_CONFIG.customLimits[endpoint];
    return {
      limit: custom[tier] || custom.free,
      window: custom.window,
    };
  }

  // Apply endpoint multiplier
  let baseLimit = RATE_LIMIT_CONFIG.defaultLimits[tier] || RATE_LIMIT_CONFIG.defaultLimits.free;

  if (endpoint && RATE_LIMIT_CONFIG.endpointMultipliers[endpoint]) {
    baseLimit = Math.floor(baseLimit * RATE_LIMIT_CONFIG.endpointMultipliers[endpoint]);
  }

  return {
    limit: baseLimit,
    window: RATE_LIMIT_CONFIG.windows.default,
  };
}
```

## Edge Deployment Patterns

### Cloudflare Workers Adaptation

For edge deployment with Cloudflare Workers, adapt the rate limiting for 10ms CPU limits:

```typescript
// Cloudflare Workers optimized rate limiting
export class EdgeRateLimiter {
  private kv: KVNamespace;
  private durableObjectId: string;

  constructor(kv: KVNamespace, durableObjectId: string) {
    this.kv = kv;
    this.durableObjectId = durableObjectId;
  }

  async limit(identifier: string, limit: number, window: number): Promise<IRateLimitResult> {
    // Use Durable Objects for distributed rate limiting
    const id = this.durableObjectId;
    const stub = this.durableObjects.get(id);

    return stub.fetch(
      new Request('https://rate-limit', {
        method: 'POST',
        headers: {
          identifier: identifier,
          limit: limit.toString(),
          window: window.toString(),
        },
      })
    );
  }
}

// Durable Object for rate limiting
export class RateLimitDurableObject {
  private storage: DurableObjectStorage;
  private state: {
    [identifier: string]: {
      timestamps: number[];
      lastCleanup: number;
    };
  } = {};

  constructor(state: DurableObjectState) {
    this.storage = state.storage;
  }

  async fetch(request: Request): Promise<Response> {
    const identifier = request.headers.get('identifier');
    const limit = parseInt(request.headers.get('limit') || '10');
    const window = parseInt(request.headers.get('window') || '60000');

    const now = Date.now();
    const windowStart = now - window;

    // Load or initialize state
    if (!this.state[identifier]) {
      const stored = await this.storage.get(identifier);
      this.state[identifier] = stored || {
        timestamps: [],
        lastCleanup: now,
      };
    }

    const entry = this.state[identifier];

    // Periodic cleanup
    if (now - entry.lastCleanup > 5 * 60 * 1000) {
      entry.timestamps = entry.timestamps.filter(t => t > windowStart);
      entry.lastCleanup = now;
      await this.storage.put(identifier, entry);
    }

    // Filter timestamps
    entry.timestamps = entry.timestamps.filter(t => t > windowStart);

    // Check limit
    if (entry.timestamps.length >= limit) {
      const oldestTimestamp = entry.timestamps[0];
      const resetTime = oldestTimestamp + window;

      return Response.json({
        success: false,
        remaining: 0,
        reset: resetTime,
      });
    }

    // Add timestamp
    entry.timestamps.push(now);
    await this.storage.put(identifier, entry);

    return Response.json({
      success: true,
      remaining: limit - entry.timestamps.length,
      reset: now + window,
    });
  }
}
```

### KV-Based Rate Limiting

For simpler edge rate limiting using Cloudflare KV:

```typescript
// KV-based rate limiting (simpler but less precise)
export class KVRateLimiter {
  private kv: KVNamespace;

  constructor(kv: KVNamespace) {
    this.kv = kv;
  }

  async limit(identifier: string, limit: number, window: number): Promise<IRateLimitResult> {
    const now = Date.now();
    const windowStart = now - window;
    const key = `rate_limit:${identifier}:${Math.floor(now / window)}`;

    const current = await this.kv.get(key);
    const count = parseInt(current || '0');

    if (count >= limit) {
      const resetTime = Math.ceil(now / window) * window + window;

      return {
        success: false,
        remaining: 0,
        reset: resetTime,
      };
    }

    // Increment counter
    const newCount = count + 1;
    await this.kv.put(key, newCount.toString(), {
      expirationTtl: Math.ceil(window / 1000),
    });

    return {
      success: true,
      remaining: limit - newCount,
      reset: Math.ceil(now / window) * window + window,
    };
  }
}
```

## Testing Strategies

### Unit Testing Rate Limiters

```typescript
// tests/unit/rate-limit.test.ts
import { describe, test, expect, beforeEach, vi } from 'vitest';
import { createRateLimiter } from '../../server/rateLimit';

describe('Rate Limiting', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  test('should allow requests within limit', async () => {
    const limiter = createRateLimiter(5, 1000); // 5 requests per second
    const identifier = 'test_user';

    for (let i = 0; i < 5; i++) {
      const result = await limiter(identifier);
      expect(result.success).toBe(true);
      expect(result.remaining).toBe(5 - i - 1);
    }
  });

  test('should block requests exceeding limit', async () => {
    const limiter = createRateLimiter(3, 1000);
    const identifier = 'test_user';

    // Use up the limit
    for (let i = 0; i < 3; i++) {
      await limiter(identifier);
    }

    // Next request should be blocked
    const result = await limiter(identifier);
    expect(result.success).toBe(false);
    expect(result.remaining).toBe(0);
  });

  test('should reset after window expires', async () => {
    const limiter = createRateLimiter(2, 1000); // 2 requests per second
    const identifier = 'test_user';

    // Use up the limit
    await limiter(identifier);
    await limiter(identifier);

    // Should be blocked
    let result = await limiter(identifier);
    expect(result.success).toBe(false);

    // Advance time by window
    vi.advanceTimersByTime(1000);

    // Should be allowed again
    result = await limiter(identifier);
    expect(result.success).toBe(true);
    expect(result.remaining).toBe(1);
  });

  test('should handle multiple identifiers independently', async () => {
    const limiter = createRateLimiter(2, 1000);

    // User 1 uses their limit
    await limiter('user1');
    await limiter('user1');

    // User 2 should still have their full limit
    const result = await limiter('user2');
    expect(result.success).toBe(true);
    expect(result.remaining).toBe(1);
  });
});
```

### Integration Testing with API Routes

```typescript
// tests/api/rate-limiting.api.spec.ts
import { test, expect } from '@playwright/test';
import { ApiClient } from '../helpers';

test.describe('API Rate Limiting', () => {
  test('should rate limit public endpoints by IP', async ({ request }) => {
    const api = new ApiClient(request);

    // Make requests up to the limit
    const responses = [];
    for (let i = 0; i < 12; i++) {
      // Exceeds 10 request limit
      const response = await api.get('/api/models');
      responses.push(response);
    }

    // First 10 should succeed
    for (let i = 0; i < 10; i++) {
      await responses[i].expectStatus(200);
    }

    // Subsequent requests should be rate limited
    for (let i = 10; i < 12; i++) {
      await responses[i].expectStatus(429);
      await responses[i].expectErrorCode('TOO_MANY_REQUESTS');
    }
  });

  test('should apply tier-based rate limiting for authenticated users', async ({ request }) => {
    const api = new ApiClient(request);

    // Create users with different tiers
    const freeUser = await api.createUser({ tier: 'free' });
    const proUser = await api.createUser({ tier: 'pro' });

    // Test free user limit
    const freeApi = api.withAuth(freeUser.token);
    let successCount = 0;

    for (let i = 0; i < 15; i++) {
      const response = await freeApi.get('/api/models');
      if (response.status() === 200) successCount++;
    }

    expect(successCount).toBeLessThanOrEqual(10); // Free tier limit

    // Test pro user limit
    const proApi = api.withAuth(proUser.token);
    successCount = 0;

    for (let i = 0; i < 130; i++) {
      const response = await proApi.get('/api/models');
      if (response.status() === 200) successCount++;
    }

    expect(successCount).toBeLessThanOrEqual(120); // Pro tier limit
  });
});
```

## Performance Optimization

### Memory Management

```typescript
// Optimized rate limiting with memory cleanup
export class OptimizedRateLimiter {
  private store = new Map<string, IRateLimitEntry>();
  private cleanupInterval: NodeJS.Timeout;

  constructor() {
    // Clean up old entries every 5 minutes
    this.cleanupInterval = setInterval(
      () => {
        this.cleanup();
      },
      5 * 60 * 1000
    );
  }

  private cleanup() {
    const now = Date.now();
    const fiveMinutesAgo = now - 5 * 60 * 1000;

    for (const [key, entry] of this.store.entries()) {
      // Filter old timestamps
      entry.timestamps = entry.timestamps.filter(t => t > fiveMinutesAgo);

      // Remove empty entries
      if (entry.timestamps.length === 0) {
        this.store.delete(key);
      }
    }
  }

  destroy() {
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
    }
  }
}
```

### Concurrent Request Handling

```typescript
// Handle concurrent requests safely
export class ConcurrentSafeRateLimiter {
  private locks = new Map<string, Promise<void>>();

  async limit(identifier: string, limit: number, window: number): Promise<IRateLimitResult> {
    // Wait for any existing operation on this identifier
    if (this.locks.has(identifier)) {
      await this.locks.get(identifier);
    }

    // Create a new lock for this operation
    const lockPromise = this.performLimiting(identifier, limit, window);
    this.locks.set(identifier, lockPromise);

    try {
      return await lockPromise;
    } finally {
      this.locks.delete(identifier);
    }
  }

  private async performLimiting(
    identifier: string,
    limit: number,
    window: number
  ): Promise<IRateLimitResult> {
    // Implement the actual rate limiting logic here
    // This ensures only one operation runs per identifier at a time
    const now = Date.now();
    // ... rate limiting implementation
  }
}
```

## Best Practices

### 1. Layered Rate Limiting

Apply multiple layers of rate limiting for comprehensive protection:

```typescript
// Apply multiple rate limits in sequence
export async function applyLayeredRateLimit(req: Request, user: IUser) {
  // 1. Global IP-based limit
  const ipLimit = await applyPublicRateLimit(req);
  if (ipLimit) return ipLimit;

  // 2. User-based limit
  const userLimit = await applyUserRateLimit(user.id, user.tier);
  if (userLimit) return userLimit;

  // 3. Endpoint-specific limit
  const endpointLimit = await applyEndpointLimit(req.url, user);
  if (endpointLimit) return endpointLimit;

  return null; // All checks passed
}
```

### 2. Graceful Degradation

Handle rate limit failures gracefully:

```typescript
export async function safeRateLimit(identifier: string): Promise<IRateLimitResult> {
  try {
    return await rateLimit.limit(identifier);
  } catch (error) {
    // Log error but allow request through
    console.error('Rate limiting error:', error);

    return {
      success: true,
      remaining: 100, // Generous fallback
      reset: Date.now() + 60000,
    };
  }
}
```

### 3. Monitoring and Alerting

Monitor rate limit violations:

```typescript
export class RateLimitMonitor {
  private violations = new Map<string, number>();

  async logViolation(identifier: string, endpoint: string, tier?: string) {
    const key = `${identifier}:${endpoint}`;
    const count = (this.violations.get(key) || 0) + 1;
    this.violations.set(key, count);

    // Alert on repeated violations
    if (count === 5) {
      await this.sendAlert({
        type: 'RATE_LIMIT_VIOLATION',
        identifier,
        endpoint,
        tier,
        violationCount: count,
      });
    }

    // Cleanup old violations
    this.cleanupViolations();
  }
}
```

### 4. Cache Headers

Add cache headers to rate limited responses:

```typescript
export function createRateLimitResponse(limit: number, remaining: number, reset: number) {
  return NextResponse.json(
    {
      error: 'Rate limit exceeded',
      retryAfter: Math.ceil((reset - Date.now()) / 1000),
    },
    {
      status: 429,
      headers: {
        'X-RateLimit-Limit': limit.toString(),
        'X-RateLimit-Remaining': remaining.toString(),
        'X-RateLimit-Reset': new Date(reset).toISOString(),
        'Retry-After': Math.ceil((reset - Date.now()) / 1000).toString(),
        'Cache-Control': 'no-cache, no-store, must-revalidate',
      },
    }
  );
}
```

## Migration Path

### From In-Memory to Edge Storage

```typescript
// Abstract rate limiter interface
interface IRateLimiter {
  limit(identifier: string, limit: number, window: number): Promise<IRateLimitResult>;
}

// In-memory implementation (development)
class InMemoryRateLimiter implements IRateLimiter {
  private store = new Map<string, IRateLimitEntry>();

  async limit(identifier: string, limit: number, window: number): Promise<IRateLimitResult> {
    // In-memory implementation
  }
}

// Edge implementation (production)
class EdgeRateLimiter implements IRateLimiter {
  private kv: KVNamespace;

  async limit(identifier: string, limit: number, window: number): Promise<IRateLimitResult> {
    // Edge KV implementation
  }
}

// Factory function
export function createRateLimiter(): IRateLimiter {
  if (process.env.NODE_ENV === 'production' && process.env.CLOUDFLARE_WORKER) {
    return new EdgeRateLimiter(/* KV namespace */);
  }

  return new InMemoryRateLimiter();
}
```

### Gradual Rollout

```typescript
// Feature flag for edge rate limiting
export class HybridRateLimiter {
  private inMemory: InMemoryRateLimiter;
  private edge: EdgeRateLimiter;
  private edgeEnabled: boolean;

  constructor(edgeEnabled: boolean = false) {
    this.inMemory = new InMemoryRateLimiter();
    this.edge = new EdgeRateLimiter();
    this.edgeEnabled = edgeEnabled;
  }

  async limit(identifier: string, limit: number, window: number): Promise<IRateLimitResult> {
    if (this.edgeEnabled) {
      try {
        return await this.edge.limit(identifier, limit, window);
      } catch (error) {
        // Fallback to in-memory
        console.error('Edge rate limiting failed, falling back:', error);
        return await this.inMemory.limit(identifier, limit, window);
      }
    }

    return await this.inMemory.limit(identifier, limit, window);
  }

  enableEdge() {
    this.edgeEnabled = true;
  }
}
```
