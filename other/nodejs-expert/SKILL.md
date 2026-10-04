---
name: nodejs-expert
description: Node.js backend expertise — architecture decisions, production patterns, Express/Fastify middleware, error handling, async patterns, security, and API design.
stacks:
  - nodejs-backend
  - backend
packages:
  - express
  - fastify
  - koa
  - hono
  - socket.io
  - stripe
  - pino
  - winston
  - nodemailer
  - elysia
  - "@directus/sdk"
  - directus
tags:
  - api
  - node
  - middleware
  - handler
  - listener
  - backend
---

## Use this skill when

- Building REST API or GraphQL server on Node.js
- Choosing a framework, runtime, or project architecture
- Designing middleware chains (auth, validation, logging)
- Implementing background processing (BullMQ, cron)
- Integrating databases (Prisma, TypeORM, raw SQL)
- Building WebSocket or SSE real-time features

## Do not use this skill when

- The task requires TypeScript architecture guidance specifically — use typescript-expert
- You are working in a non-Node.js runtime exclusively
- The task requires Nest.js-specific patterns — use nestjs-expert

## Instructions

1. Identify runtime targets and constraints (Node.js version, deployment environment)
2. Choose async patterns, module system, and framework based on context
3. Implement with robust error handling and centralized error middleware
4. Validate performance and security before shipping

## Capabilities

### Framework Selection (2025)
- **Hono** — edge/serverless (Cloudflare, Vercel), zero-dependency, ultra-fast cold starts
- **Fastify** — high performance API, 2-3x faster than Express, excellent TypeScript support
- **NestJS** — enterprise/team environments, structured DI, decorators
- **Express** — legacy/stable, maximum ecosystem, most middleware available
- **Next.js API Routes / tRPC** — full-stack with frontend

### Runtime Selection
- **Node.js** — general purpose, largest ecosystem
- **Bun** — performance-focused, built-in bundler
- **Deno** — security-first, built-in TypeScript

### Module System
- ESM (`import/export`) — preferred for new projects; better tree-shaking, async loading
- CommonJS (`require`) — legacy projects, wider npm package support
- Node.js 22+ supports `--experimental-strip-types` for running .ts files directly without build step

### Project Architecture
- Group by feature (auth/, users/, products/), not by layer — scales better in growing projects
- Layered architecture within each feature: Controller → Service → Repository
- Single source of truth for configuration via environment variables with typed config object

### Middleware Patterns
- Centralized error handler at the end of the middleware chain — ensures consistent error format
- Validation at the boundary (routes layer) — internal code trusts types
- Auth middleware extracts and verifies token, attaches user to request context

### Validation Libraries
- **Zod** — TypeScript-first, type inference from schema
- **Valibot** — smaller bundle size, tree-shakeable
- **ArkType** — performance-critical scenarios

### Database Patterns
- Single PrismaClient instance as module singleton — prevents connection pool exhaustion
- Transactions for multi-step operations that must be atomic
- Parameterized queries only — never string concatenation for SQL

### API Design
- Response format: `{ data: T }` for success, `{ error: { code, message, details? } }` for errors
- Pagination: offset for simple lists under 10K rows, cursor for feeds/logs/large tables
- HTTP status codes: 400 bad input, 401 no auth, 403 forbidden, 404 not found, 409 conflict, 422 business rules, 500 server error

### Async Patterns
- `async/await` for sequential operations
- `Promise.all` for parallel independent operations
- `Promise.allSettled` for parallel where some can fail
- `Promise.race` for timeout or first-response patterns
- CPU-bound work (crypto, image processing) → worker threads, not async

### Graceful Shutdown
- Register SIGTERM/SIGINT handlers
- Stop accepting new connections
- Drain in-flight requests
- Close database connections and cache clients
- Exit with appropriate code

### Retry Pattern
- Exponential backoff with configurable max retries
- Throw on final failure, not silently swallow

## Behavioral Traits
- Chooses framework based on project context, not habit
- Validates all inputs at the boundary layer
- Profiles before optimizing — avoids premature optimization
- Uses structured logging (pino) for machine-readable output
- Enforces TypeScript strict mode: no `any`, explicit return types for exports, `unknown` instead of `any`
- Prefers `satisfies` operator for type validation without widening

## Knowledge Base

### Security Checklist
- Input validation on all API endpoints
- Parameterized queries — no string concatenation for SQL
- Password hashing with bcrypt or argon2 (never MD5, SHA1)
- JWT verification: check signature AND expiry
- Rate limiting on public endpoints
- Security headers via Helmet.js
- HTTPS enforced in production
- CORS properly configured for expected origins
- Secrets in environment variables only
- Regular dependency audits

### Performance Considerations
- I/O-bound operations (DB queries, HTTP, filesystem) benefit from async patterns
- CPU-bound work blocks the event loop — delegate to worker threads
- Connection pooling is essential for database clients
- Avoid synchronous methods (`fs.readFileSync`, `crypto.pbkdf2Sync`) in request handlers

### Common Anti-Patterns
- Using Express for new edge/serverless projects — use Hono instead
- Synchronous operations in production request handlers
- Business logic in controllers — belongs in service layer
- Skipping input validation
- Hardcoding secrets in source files
- Blocking the event loop with CPU-intensive work

## Constraints
- TypeScript strict mode always: `strict: true`, no `any`, explicit return types for exported functions
- Never use synchronous file/crypto APIs in request handlers
- Never hardcode credentials, API keys, or connection strings
- Always handle async errors at appropriate boundaries — never leave unhandled promise rejections
- Configuration must come from environment variables, never from source files

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
