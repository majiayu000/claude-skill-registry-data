---
name: api-smoke-testing
description: Start the dev server, discover API routes from the codebase, hit every endpoint, and report which ones return errors.
user-invocable: true
---

# API Smoke Testing

Verify all API endpoints return healthy responses by combining codebase analysis with HTTP requests.

## Workflow

### 1. Discover Routes

Search the codebase for API route definitions:

**Next.js (App Router):** `app/api/**/route.ts`
**Next.js (Pages Router):** `pages/api/**/*.ts`
**Express:** Look for `app.get(`, `app.post(`, `router.get(`, etc.
**Django:** Look for `urlpatterns` in `urls.py`
**FastAPI:** Look for `@app.get(`, `@app.post(`, decorators
**Rails:** Look for `routes.rb`

Build a list of endpoints with their HTTP methods.

### 2. Ensure Server is Running

Check terminal files for a running dev server. If none found, start one.

### 3. Hit Every Endpoint

For each route:

```bash
curl -s -o /dev/null -w "%{http_code}" -X <METHOD> http://localhost:<PORT><PATH>
```

For endpoints that require a body (POST/PUT/PATCH), send a minimal valid JSON:

```bash
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:<PORT><PATH> \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 4. Classify Results

| Status | Meaning |
|--------|---------|
| 200-299 | OK |
| 301/302 | Redirect (OK) |
| 400 | Bad request (expected for empty POST bodies) |
| 401/403 | Auth required (expected for protected routes) |
| 404 | Route not found (BUG — route exists in code but not served) |
| 500 | Server error (BUG) |
| 000/timeout | Server not responding (BUG) |

### 5. Report

```
API Smoke Test Results:
  Tested: 15 endpoints
  Passed: 12
  Auth required: 2 (GET /api/user, POST /api/settings)
  Errors:
    500 — POST /api/webhooks/stripe (TypeError: Cannot read property 'id' of undefined)
    404 — GET /api/v2/health (route defined but not mounted)
```

### 6. Fix Errors

For 500 errors, read the terminal output for the stack trace and fix the root cause. For 404s, check that the route file is in the correct location and properly exported.
