---
name: elysia
description: Elysia Bun-native, Eden Treaty, validation, WebSocket. Use when building Elysia apps.
---

## elysia

Build high-performance Bun apps with Elysia.

### Bun-Native Performance
- Built on Bun runtime for fast startup and low latency
- Zero-cost abstractions with compile-time optimizations
- Native Bun file I/O and SQLite support

### Eden Treaty
- End-to-end type safety between server and client
- `EdenTreaty` generates typed client from server instance
- Shared types without code generation

### Validation
- Built-in validation via Elysia.t (type system DSL)
- Supports all standard types: string, number, boolean, enum, array
- Custom error messages and validation transforms

### WebSocket & File Uploads
- Built-in WebSocket support via `app.ws()`
- File uploads via `@elysiajs/bun` form data
- Streaming responses for large payloads

### Rate Limiting & Auth
- @elysiajs/rate-limit for request throttling
- JWT auth via @elysiajs/jwt
- Cookie-based sessions with @elysiajs/cookie
- CORS configuration via @elysiajs/cors
