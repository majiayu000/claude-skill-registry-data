---
name: cloudflare-api-orchestration
description: |
  Activates automatically when designing or implementing Cloudflare Workers APIs,
  orchestrating multi-provider API calls, implementing D1 database operations,
  or managing KV-based caching strategies.

  Ensures proper error handling, provider tagging, fallback chains, and
  orchestration patterns for BooksTrack backend infrastructure.

  Auto-activates on:
  - File patterns: *.worker.js, *-api.ts, *-service.ts in backend code
  - Keywords: "api orchestration", "multi-provider", "fallback chain", "D1 query"
  - Context: Cloudflare Workers development, API design discussions

allowed-tools: ["Read", "Grep", "Edit", "Write", "WebFetch"]
---

# Cloudflare API Orchestration Skill

This skill enforces BooksTrack-specific API orchestration patterns for Cloudflare Workers.

## Core Principles

### 1. Provider Orchestration (MANDATORY)

**NEVER make direct API calls without orchestration layer.**

**Correct pattern:**
```javascript
// orchestrator.js
export class APIOrchestrator {
  async searchBooks(query, options = {}) {
    const providers = [
      { name: 'google', fn: () => this.googleBooks.search(query) },
      { name: 'openlibrary', fn: () => this.openLibrary.search(query) }
    ];

    for (const provider of providers) {
      try {
        const result = await provider.fn();
        return {
          ...result,
          provider: `orchestrated:${providers.map(p => p.name).join('+')}`,
          cached: false
        };
      } catch (error) {
        console.warn(`Provider ${provider.name} failed:`, error);
        continue;
      }
    }

    // Final fallback to cache
    const cached = await this.kv.get(`book:${query}`);
    if (cached) {
      return {
        ...JSON.parse(cached),
        provider: 'cache:kv',
        cached: true
      };
    }

    throw new Error('All providers failed');
  }
}
```

**Wrong pattern (FORBIDDEN):**
```javascript
// ❌ Direct API call without orchestration
async function searchBooks(query) {
  const response = await fetch(`https://www.googleapis.com/books/v1/volumes?q=${query}`);
  return response.json(); // Missing provider tag, no fallback, no caching
}
```

### 2. Provider Tagging (REQUIRED)

**All responses MUST include provider metadata:**

```javascript
{
  data: { /* actual response */ },
  provider: "orchestrated:google+openlibrary", // Multi-provider
  cached: false,
  timestamp: Date.now()
}
```

**Tag formats:**
- `"orchestrated:google+openlibrary"` - Successful multi-provider aggregation
- `"google"` - Single provider (fallback failed or only one available)
- `"cache:kv"` - Retrieved from KV cache
- `"cache:d1"` - Retrieved from D1 database

### 3. Error Handling Patterns

**Implement graceful degradation:**

```javascript
try {
  // Primary provider
  const result = await primaryProvider.fetch();
  return { data: result, provider: 'primary', cached: false };
} catch (primaryError) {
  console.warn('Primary provider failed:', primaryError);

  try {
    // Secondary provider
    const result = await secondaryProvider.fetch();
    return { data: result, provider: 'secondary', cached: false };
  } catch (secondaryError) {
    console.warn('Secondary provider failed:', secondaryError);

    // Cache fallback
    const cached = await cache.get(key);
    if (cached) {
      return { data: cached, provider: 'cache:kv', cached: true };
    }

    // Final error with context
    throw new APIError('All providers exhausted', {
      primaryError,
      secondaryError,
      key
    });
  }
}
```

### 4. D1 Query Patterns

**Always use prepared statements:**

```javascript
// ✅ Correct - prepared statement
const result = await env.DB.prepare(
  'SELECT * FROM books WHERE isbn = ?'
).bind(isbn).first();

// ❌ Wrong - SQL injection vulnerability
const result = await env.DB.prepare(
  `SELECT * FROM books WHERE isbn = '${isbn}'`
).first();
```

**Batch operations for efficiency:**

```javascript
// ✅ Correct - batch insert
const stmt = env.DB.prepare('INSERT INTO books (isbn, title) VALUES (?, ?)');
const batch = books.map(book => stmt.bind(book.isbn, book.title));
await env.DB.batch(batch);

// ❌ Wrong - individual inserts (slow)
for (const book of books) {
  await env.DB.prepare('INSERT INTO books (isbn, title) VALUES (?, ?)')
    .bind(book.isbn, book.title)
    .run();
}
```

### 5. KV Caching Strategy

**Key naming convention:**
```
namespace:entity:id
```

**Examples:**
- `book:isbn:9780134685991`
- `search:query:swift+programming`
- `user:profile:user123`

**Caching pattern:**

```javascript
async function getCachedOrFetch(key, fetchFn, ttl = 3600) {
  // Try cache first
  const cached = await env.KV.get(key, { type: 'json' });
  if (cached) {
    return { ...cached, cached: true };
  }

  // Fetch from provider
  const fresh = await fetchFn();

  // Cache for TTL seconds
  await env.KV.put(key, JSON.stringify(fresh), {
    expirationTtl: ttl,
    metadata: { cached_at: Date.now() }
  });

  return { ...fresh, cached: false };
}
```

### 6. Rate Limiting

**Implement per-endpoint rate limits:**

```javascript
import { RateLimiter } from './rate-limiter';

const limiter = new RateLimiter({
  search: { requests: 100, window: 60 }, // 100 req/min
  details: { requests: 200, window: 60 }  // 200 req/min
});

async function handleSearch(request, env) {
  const clientId = request.headers.get('CF-Connecting-IP');

  if (!await limiter.check('search', clientId)) {
    return new Response('Rate limit exceeded', {
      status: 429,
      headers: {
        'Retry-After': '60',
        'X-RateLimit-Limit': '100',
        'X-RateLimit-Remaining': '0'
      }
    });
  }

  // Process request...
}
```

### 7. Circuit Breaker Pattern

**Prevent cascading failures:**

```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.failureCount = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.nextAttempt = Date.now();
  }

  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker OPEN');
      }
      this.state = 'HALF_OPEN';
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}
```

## BooksTrack-Specific Patterns

### Book Search API

```javascript
// Route: GET /api/v2/books/search?q=...
export async function handleBookSearch(request, env) {
  const url = new URL(request.url);
  const query = url.searchParams.get('q');

  if (!query) {
    return new Response(JSON.stringify({ error: 'Missing query parameter' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  const orchestrator = new APIOrchestrator(env);

  try {
    const result = await orchestrator.searchBooks(query);
    return new Response(JSON.stringify(result), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=3600',
        'X-Provider': result.provider
      }
    });
  } catch (error) {
    console.error('Search failed:', error);
    return new Response(JSON.stringify({
      error: 'Search failed',
      message: error.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
```

### Book Details API

```javascript
// Route: GET /api/v2/books/:isbn
export async function handleBookDetails(isbn, env) {
  // Try D1 first (authoritative source)
  const cached = await env.DB.prepare(
    'SELECT * FROM books WHERE isbn = ?'
  ).bind(isbn).first();

  if (cached) {
    return {
      ...cached,
      provider: 'cache:d1',
      cached: true
    };
  }

  // Fetch from providers
  const orchestrator = new APIOrchestrator(env);
  const result = await orchestrator.getBookByISBN(isbn);

  // Store in D1 for future requests
  await env.DB.prepare(
    'INSERT OR REPLACE INTO books (isbn, title, author, data) VALUES (?, ?, ?, ?)'
  ).bind(isbn, result.title, result.author, JSON.stringify(result)).run();

  return result;
}
```

## Anti-Patterns to Avoid

### ❌ Direct API Calls
```javascript
// DON'T DO THIS
const response = await fetch('https://api.example.com/books');
```

### ❌ Missing Provider Tags
```javascript
// DON'T DO THIS
return { data: books }; // Missing provider metadata
```

### ❌ Unhandled Errors
```javascript
// DON'T DO THIS
const result = await provider.fetch(); // No try-catch
```

### ❌ SQL Injection Vulnerabilities
```javascript
// DON'T DO THIS
await env.DB.prepare(`SELECT * FROM books WHERE title = '${title}'`).first();
```

### ❌ No Caching Strategy
```javascript
// DON'T DO THIS - always hitting live APIs
const result = await provider.fetch(); // No cache check
```

## Validation Checklist

When implementing or reviewing Cloudflare Workers APIs, verify:

- [ ] All API calls go through orchestration layer
- [ ] Responses include provider tags
- [ ] Fallback chains implemented (primary → secondary → cache)
- [ ] D1 queries use prepared statements
- [ ] KV keys follow naming convention
- [ ] Rate limiting configured for public endpoints
- [ ] Circuit breakers protect external services
- [ ] Error handling provides useful context
- [ ] Caching strategy reduces API calls
- [ ] Logging captures provider failures

## Integration with Code Review

This skill complements the `code-review-grok` subagent. When code review identifies orchestration violations, this skill provides the correct patterns to follow.

---

## Async API Development (v2.0.64)

**Complex API implementations can run in background:**

```javascript
// Launch complex endpoint implementation in background
Task({
  subagent_type: "cloudflare-specialist",
  prompt: "Implement /api/v3/books/search with full orchestration, caching, rate limiting",
  run_in_background: true
})

// Continue with other work (UI, tests)...

// Retrieve implementation when ready
TaskOutput({
  task_id: "agent_xyz123",
  block: true
})
```

**Background-friendly tasks:**
- Complex multi-provider orchestration
- D1 schema migrations
- KV→D1 data migrations
- Comprehensive API security audits

**Recommended Option Pattern (v2.0.62):**

When presenting API implementation choices:
```javascript
options: [
  {label: "Orchestrated (Recommended)", description: "Multi-provider with fallback"},
  {label: "Single provider", description: "Google Books only"},
  {label: "Cache-first", description: "D1/KV with lazy provider fetch"}
]
```

---

**Last Updated:** December 11, 2025
**Maintained by:** Claude Code PM System
**Related Agents:** cloudflare-specialist, code-review-grok
**Claude Code Version:** v2.0.65
