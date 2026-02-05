---
name: typescript-workflow
description: TypeScript/JavaScript project workflow guidelines using Bun package manager. Triggers on `.ts`, `.tsx`, `bun`, `package.json`, TypeScript. Covers bun run, bun install, bun add, tsconfig.json patterns, ESM/CommonJS modules, type safety, Biome formatting, naming conventions (PascalCase, camelCase, UPPER_SNAKE_CASE), project structure, error handling, environment variables, async patterns, and code quality tools. Activate when working with TypeScript files (.ts, .tsx), JavaScript files (.js, .jsx), Bun projects, tsconfig.json, package.json, bun.lock, or Bun-specific tooling.
---

# TypeScript/JavaScript Projects Workflow

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

Guidelines for working with TypeScript and JavaScript projects using Bun as the primary package manager with modern tooling and best practices.

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Lint + Format | Biome | `bun run biome check --apply .` |
| Type check | tsc | `bun run tsc --noEmit` |
| Dead code | ts-prune | `bun run ts-prune` |
| Test | Bun test | `bun test` |
| Coverage | c8 | `bun run c8 bun test` |

## CRITICAL: Bun Package Manager

**You MUST use Bun commands** for all package and runtime operations in Bun projects:

```bash
# Package management
bun install        # Install dependencies from package.json
bun add <package>  # Add production dependency
bun add --dev <package>  # Add development dependency
bun remove <package>  # Remove dependency

# Running code and scripts
bun run <script>   # Run script defined in package.json
bun <file.ts>      # Run TypeScript/JavaScript directly
bun run build      # Run build script

# Testing
bun test           # Run tests with Bun's native test runner

# Package info
bun list           # List installed packages
bun outdated       # Check for updates
```

**Benefits of Bun:**
- Native TypeScript support (no transpilation setup)
- Significantly faster than Node.js
- All-in-one tool (package manager, runtime, test runner)
- Smaller node_modules footprint
- Drop-in Node.js compatibility for most packages

## Module Systems

### ESM (ECMAScript Modules) - Preferred

**Default for Bun projects and modern TypeScript:**

```typescript
// Import named exports
import { UserService } from './services/user-service';
import { type User } from './types';

// Import default exports
import express from 'express';

// Import with alias
import * as helpers from './utils/helpers';

// Export named
export function getUserById(id: string): Promise<User> {
  // ...
}

// Export default
export default UserService;

// Re-export
export { type User } from './types';
export { UserService } from './services/user-service';
```

### CommonJS Fallback

Use only when necessary for legacy compatibility:

```javascript
// Require imports
const { UserService } = require('./services/user-service');
const express = require('express');

// Module exports
module.exports = UserService;
module.exports = { UserService, UserRepository };
```

### Mixed Module Usage

In `package.json`, specify module type:

```json
{
  "type": "module",
  "name": "my-app",
  "version": "1.0.0"
}
```

## TypeScript Configuration

### tsconfig.json Best Practices

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020"],
    "moduleResolution": "bundler",
    "strict": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "allowJs": false,
    "outDir": "./dist",
    "rootDir": "./src",
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@services/*": ["src/services/*"],
      "@models/*": ["src/models/*"]
    },
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### Key Options Explained

- **target:** ES2020 for modern environments, ES2015 for legacy support
- **module:** ESNext for Bun/bundlers, CommonJS for Node.js compatibility
- **moduleResolution:** bundler (for Bun/bundlers), node (for Node.js)
- **strict:** Enable all strict type checking
- **skipLibCheck:** Skip type checking of declaration files
- **baseUrl + paths:** Enable path aliases for cleaner imports
- **noUnusedLocals/Parameters:** Catch dead code

## Code Style and Formatting

### Biome (Preferred)

Biome is the RECOMMENDED all-in-one tool for linting and formatting. It replaces ESLint and Prettier with faster performance and unified configuration.

**Installation:**

```bash
bun add --dev @biomejs/biome
```

**Configuration (`biome.json`):**

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": {
        "noUselessSwitchCase": "error"
      },
      "style": {
        "noNonNullAssertion": "warn"
      }
    }
  },
  "javascript": {
    "formatter": {
      "semicolons": "always",
      "quoteStyle": "single",
      "trailingCommas": "es5"
    }
  }
}
```

**Usage:**

```bash
# Check and fix all issues
bun run biome check --apply .

# Format only
bun run biome format --write .

# Lint only
bun run biome lint .

# CI mode (check without fixing)
bun run biome check .
```

### Legacy: ESLint + Prettier

If a project uses ESLint/Prettier, migration to Biome is RECOMMENDED. For legacy support:

```bash
# ESLint
bun add --dev eslint
bun run eslint src/ --fix

# Prettier
bun add --dev prettier
bun run prettier --write src/
```

## Naming Conventions

### File Naming

- **Components:** PascalCase - `UserProfile.tsx`, `LoginForm.tsx`
- **Utilities/Helpers:** camelCase - `formatDate.ts`, `apiClient.ts`
- **Types/Interfaces:** PascalCase - `User.ts`, `ApiResponse.ts`
- **Constants:** UPPER_SNAKE_CASE - `API_ENDPOINTS.ts`, `CONFIG.ts`
- **Test files:** `.test.ts` or `.spec.ts` suffix - `user.service.test.ts`

### Code Naming

```typescript
// Classes/Types/Interfaces/Enums: PascalCase
class UserService { /* ... */ }
interface UserRepository { /* ... */ }
enum UserRole { Admin = 'ADMIN', User = 'USER' }

// Methods, properties, variables, functions: camelCase
getUserById(id: string): Promise<User>
const userData = {};

// Private members: camelCase with leading underscore
private _cache: Map<string, User> = new Map();

// Constants: UPPER_SNAKE_CASE
const MAX_RETRIES = 3;
const API_BASE_URL = 'https://api.example.com';

// React hooks: camelCase with use prefix
function useUserData(userId: string) { /* ... */ }
```

## Type Safety and Annotations

### Type Hints

- **Explicit types** for function parameters and return values
- **MUST NOT use `any`** - use `unknown` and type narrowing if needed
- **Avoid implicit `any`** - enable `noImplicitAny` in tsconfig.json

```typescript
// Function parameters and return types
function processUser(user: User): Promise<ProcessedUser> {
  // ...
}

// Arrow functions
const formatName = (first: string, last: string): string => {
  return `${first} ${last}`;
};

// Complex types
type ApiResponse<T> = {
  status: number;
  data: T;
  error?: string;
};

interface RequestHandler {
  handle(request: Request): Promise<Response>;
}
```

### Generics

```typescript
// Generic functions
function getById<T extends { id: string }>(items: T[], id: string): T | undefined {
  return items.find((item) => item.id === id);
}

// Generic classes
class Repository<T> {
  async getById(id: string): Promise<T | null> {
    // ...
  }
}

// Generic types
type Result<T, E = Error> = { success: true; data: T } | { success: false; error: E };
```

### Data Validation

Use **Zod** for runtime validation with type inference:

```typescript
import { z } from 'zod';

// Schema definition
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

// Type inference from schema
type User = z.infer<typeof UserSchema>;

// Runtime validation
function createUser(data: unknown): User {
  return UserSchema.parse(data);
}

// Safe parsing with error handling
const result = UserSchema.safeParse(data);
if (!result.success) {
  console.error(result.error.format());
}
```

## Project Structure

### Recommended Directory Layout

```
project/
├── src/
│   ├── main.ts              # Entry point
│   ├── types/               # Type definitions
│   ├── services/            # Business logic
│   ├── repositories/        # Data access layer
│   ├── models/              # Data models
│   ├── handlers/            # Request/event handlers
│   ├── middleware/          # Express/web middleware
│   ├── utils/               # Utility functions
│   └── config/              # Configuration
├── tests/                   # Unit and integration tests
├── dist/                    # Compiled output (gitignored)
├── package.json
├── tsconfig.json
├── biome.json
└── bun.lock
```

### Import Patterns

```typescript
// Absolute imports with path aliases
import { UserService } from '@services/user-service';
import type { User } from '@models/user';

// Relative imports within same feature
import { UserRepository } from '../repositories/user-repository';
import { validateUser } from '../utils/validators';

// Re-exports from index files
export { UserService, UserRepository } from './index';
```

## Error Handling

### Exception Best Practices

```typescript
// Define custom error classes
class AppError extends Error {
  constructor(message: string, public code: string, public statusCode = 500) {
    super(message);
    this.name = 'AppError';
  }
}

class ValidationError extends AppError {
  constructor(message: string, public field: string) {
    super(message, 'VALIDATION_ERROR', 400);
  }
}

class NotFoundError extends AppError {
  constructor(message: string) {
    super(message, 'NOT_FOUND', 404);
  }
}

// Result pattern for explicit error handling
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

async function safeFetchUser(id: string): Promise<Result<User, AppError>> {
  try {
    const user = await getUser(id);
    return { ok: true, value: user };
  } catch (error) {
    return { ok: false, error: error instanceof AppError ? error : new AppError('Unknown', 'UNKNOWN') };
  }
}
```

## Configuration Management

### Environment Variables

Use Zod for environment validation:

```typescript
// env.ts
import { z } from 'zod';

const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string(),
});

export default EnvSchema.parse(process.env);
```

## Common Async Patterns

```typescript
// Async/await with error handling
async function fetchUserData(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error('Failed to fetch');
    return response.json();
  } catch (error) {
    console.error('Error fetching user:', error);
    throw error;
  }
}

// Concurrent operations with Promise.all
async function loadDashboardData(): Promise<DashboardData> {
  const [users, products, stats] = await Promise.all([
    fetchUsers(),
    fetchProducts(),
    fetchStats(),
  ]);
  return { users, products, stats };
}
```

## Testing Integration

```typescript
import { describe, it, expect, beforeEach } from 'bun:test';
import { UserService } from '@services/user-service';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  it('should fetch user by id', async () => {
    const user = await service.getById('123');
    expect(user).toBeDefined();
    expect(user?.id).toBe('123');
  });
});
```

See **typescript-testing** skill for comprehensive testing patterns.

## Quick Reference

**Key Rules:**
- MUST use Bun commands in Bun projects
- MUST NOT use `any` - use `unknown` and type guards
- Use ESM (import/export) by default
- Enable strict TypeScript (`"strict": true`)
- Validate all external input with Zod
- Use custom error classes and Result types

## Out of Scope

- Next.js specifics → see `nextjs-workflow`
- React specifics → see `react-workflow`
- Database migrations → see `database-workflow`

---

**Note:** For project-specific TypeScript patterns, check `.claude/CLAUDE.md` in the project directory.
