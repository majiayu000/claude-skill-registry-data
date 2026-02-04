---
name: code-guidelines
description: Apply this repository's coding conventions and patterns. Use when writing or reviewing code in this codebase to ensure consistency with established patterns for DI, logging, error handling, testing, and documentation. Auto-trigger when implementing features, fixing bugs, or reviewing code changes.
---

# Code Guidelines

Follow the patterns established in this repository. Reference `code-guidelines.md` at project root for the authoritative source.

## Core Patterns

### Dependency Injection

Prefer constructor/function injection for side effects:
- DB connections, loggers, auth, clock, external clients
- Wire at edges (app startup, router factories)
- Avoid global singleton imports from deep modules
- Tests supply fakes/in-memory implementations without patching

```typescript
// Good: injectable
function createUserService(db: Database, logger: Logger) {
  return { ... }
}

// Bad: global import
import { db } from '../db'
```

### Error Handling

Use `neverthrow` Result types for expected failures. See `docs/neverthrow.md`.

```typescript
// Good: explicit Result
function findUser(id: string): ResultAsync<User, NotFoundError | DbError>

// Bad: throwing for control flow
function findUser(id: string): Promise<User> // throws on not found
```

Error conventions:
- Model expected failures as custom errors (`NotFoundError`, `UnauthorizedError`)
- Normalize unknown catches with `typedError()`
- Map internal errors to transport errors intentionally
- Never leak internals to clients

### Logging

Use structured logging with pino. See `docs/logging.md`.

```typescript
logger.info("user created", { userId: user.id, email: user.email })
```

Logging rules:
- Log at boundaries (request → router → service)
- Never log secrets (tokens, passwords, cookies)
- Use appropriate levels: error, warn, info, debug

### Testing

See `docs/testing.md` and `docs/vitest_config.md`.

- Use DI to inject test dependencies
- Prefer real DB for integration tests (testcontainers)
- Use fakes when faster/clearer
- Make tests deterministic (no timing, randomness, shared state)

### API Design

Use oRPC for type-safe APIs. See `docs/orpc.md`.

- Define contracts in routers
- Validate inputs with schemas
- Return typed Results

## Documentation

See `docs/` for detailed guides:
- `auth.md` - Authentication patterns
- `config.md` - Configuration management
- `db.md` - Database conventions
- `orpc.md` - API design with oRPC
- `neverthrow.md` - Error handling with Result types
- `testing.md` - Testing strategies
- `tech_choices.md` - Technology decisions

## When Writing Code

1. Check existing patterns in similar files
2. Use DI for testability
3. Handle errors explicitly with Result types
4. Add structured logging at boundaries
5. Write tests that use DI
6. Update docs if changing workflows

## LLM Usage

When using AI assistance:
- Treat output as untrusted input
- Run `pnpm typecheck` and `pnpm test`
- Verify security implications
- Watch for: validation gaps, error handling, logging secrets, SQL issues

