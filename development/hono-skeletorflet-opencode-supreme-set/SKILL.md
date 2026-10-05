---
name: hono
description: Hono multi-runtime, middleware, RPC, Zod validation. Use when building Hono apps.
---

## hono

Build multi-runtime web apps with Hono.

### Multi-Runtime
- Runs on Cloudflare Workers, Deno, Bun, Node.js, Lambda
- Runtime adapters auto-detected on import
- Same API across all platforms

### Routing & Middleware
- Express-style routing with `app.get()` / `app.post()`
- Wildcard and regex route patterns
- Built-in middleware: cors, etag, logger, jwt, bearer
- Custom middleware via `app.use()`

### RPC Mode
- `hc()` client for type-safe API calls
- Shared types between server and client
- Full end-to-end type safety without codegen

### Validation
- Zod integration via @hono/zod-validator
- JSON Schema validation with @hono/validator
- Input parsing for body, query, params, headers

### Best Practices
- Use HonoRequest instead of raw Request
- Error handling with app.onError()
- Serve static files via @hono/serve-static
- Deployment helpers for each runtime target
- JWT auth via @hono/jwt middleware
