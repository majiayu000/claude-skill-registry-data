---
name: koa
description: Koa.js web framework. Use when building Node.js APIs with async middleware, koa-router, context object, error handling, body parsing, or CORS. Distinguish from Express when user needs modern async patterns.
---

## koa

Lightweight Node.js framework by Express team using async/await middleware and enhanced context.

### Core Concepts
- Async middleware: `app.use(async (ctx, next) => { ... })` with upstream/downstream execution via await next()
- Context object: `ctx` wraps Node `req`/`res` with helpers for body, params, cookies, and state
- Koa vs Express: no built-in routing, no middleware in req/res, no callback-based middleware
- Error handling: centralized `app.on('error')` listener or try/catch in async middleware

### Common Patterns
- koa-router: `router.get('/users/:id', handler)` with named params, nested routers, and HTTP verb methods
- Body parsing: `@koa/bodyparser` for JSON, form, and text payloads
- CORS: `@koa/cors` middleware with origin whitelist and credential support
- Static files: `@koa/static` for serving assets with caching headers

### Best Practices
- Top-level error middleware wrapping all downstream handlers with try/catch and structured JSON errors
- `ctx.state` for passing request-scoped data (auth user, request ID) between middleware
- Composition over mounting: compose small middleware functions rather than monolithic handlers
- Supertest with jest/ava for HTTP integration tests without binding to a port

### Common Code Patterns
- `ctx.body = { data: result }` for JSON responses with automatic content-type
- `ctx.throw(400, 'validation failed')` for HTTP error responses with message
