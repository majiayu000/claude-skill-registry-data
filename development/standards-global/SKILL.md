---
name: standards-global
description: Global coding conventions and best practices for modern full-stack TypeScript development. Load when implementing any code to ensure consistent naming, error handling, file organization, type safety, and code style across the entire codebase.
---

# Global Standards

Universal coding conventions that apply to all code in modern TypeScript-first projects.

## When to Use

- Starting any implementation task
- Reviewing code for consistency
- Setting up new files or modules
- Onboarding new team members

## Resources

| Resource | Use When |
|----------|----------|
| [coding-conventions.md](resources/coding-conventions.md) | Naming, formatting, organization |
| [common-patterns.md](resources/common-patterns.md) | Reusable TypeScript patterns |
| [communication-style.md](resources/communication-style.md) | Documentation standards |

## Quick Reference

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files | `kebab-case` | `user-service.ts` |
| Functions | `camelCase` | `getUserById` |
| Types/Interfaces | `PascalCase` | `UserConfig` |
| Constants | `SCREAMING_SNAKE_CASE` | `MAX_RETRIES` |
| Booleans | `is`, `has`, `should`, `can` | `isLoading` |
| Hooks | `use` prefix | `useAuth` |
| Event handlers | `handle` prefix | `handleSubmit` |

### Type Safety

```typescript
// ✅ Use satisfies for type checking with inference
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
} satisfies Config;

// ✅ Discriminated unions for state
type AsyncState<T> = 
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// ❌ Never use any
function processData(data: any) { /* ... */ }
```

### Error Handling

```typescript
// Unified error hierarchy
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    public readonly isOperational: boolean = true,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, 'NOT_FOUND', 404, true, { resource, id });
  }
}

// Result pattern
type Result<T, E = AppError> = 
  | { success: true; data: T }
  | { success: false; error: E };
```

### Environment Variables

```typescript
// lib/env.server.ts - Server-only (NEVER import in client code)
import { z } from 'zod';

const serverEnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
});

export const serverEnv = serverEnvSchema.parse(process.env);

// lib/env.client.ts - Safe for client bundles
const clientEnvSchema = z.object({
  NEXT_PUBLIC_API_URL: z.string().url(),
});

export const clientEnv = clientEnvSchema.parse({
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
});
```

### Code Quality Rules

- **Maximum file length**: 300 lines
- **Maximum function length**: 50 lines
- **Maximum parameters**: 3 (use object if more)
- **No magic numbers**: Use named constants
- **No nested ternaries**: Use if/else or early returns

### Strict TypeScript

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true
  }
}
```

## Amp Tools to Use

- `finder` - Find existing patterns to follow
- `Read` - Check neighboring files for conventions
- `oracle` - Guidance on complex architectural decisions

## Related Skills

- `standards-frontend` - Frontend-specific patterns
- `standards-backend` - Backend-specific patterns  
- `standards-testing` - Testing conventions
