---
name: typedoc
description: Create and improve TypeScript project documentation using TypeDoc. Use when documenting TypeScript codebases, adding JSDoc comments, configuring TypeDoc, auditing documentation coverage, or generating API reference documentation for TypeScript projects.
---

# TypeDoc Documentation Skill

## Overview

This skill provides best practices for documenting TypeScript projects using TypeDoc, from writing effective JSDoc comments to configuring and generating comprehensive API documentation.

## Workflow Decision Tree

**When documenting TypeScript code:**

1. **Adding documentation to new code** → Follow JSDoc Comment Standards
2. **Auditing existing codebase** → Use Documentation Audit workflow
3. **Setting up TypeDoc** → Follow Configuration Setup
4. **Improving existing docs** → Review Common Patterns and apply to problem areas

## JSDoc Comment Standards

### Core Principles

Write documentation that adds value beyond what the code shows. Avoid stating the obvious.

**Good:** Explains why, edge cases, usage constraints
```typescript
/**
 * Validates user input against security rules and rate limits.
 * Throws RateLimitError if user exceeds 100 requests/minute.
 * @param input - Raw user input (not sanitized)
 * @returns Sanitized input safe for database queries
 */
function validateInput(input: string): string
```

**Avoid:** Repeating what TypeScript types already show
```typescript
/**
 * Validates input
 * @param input - The input
 * @returns A string
 */
function validateInput(input: string): string
```

### Essential Tags

Use these TypeDoc/JSDoc tags appropriately:

**@param** - Document each parameter (required for functions)
```typescript
/**
 * @param userId - Unique identifier from users table
 * @param options - Configuration overrides for query behavior
 */
async function fetchUser(userId: string, options?: QueryOptions)
```

**@returns** - Explain what's returned and when (required for non-void functions)
```typescript
/**
 * @returns User object if found, null if user doesn't exist
 * @throws DatabaseError if connection fails
 */
async function fetchUser(userId: string): Promise<User | null>
```

**@throws** - Document exceptions that callers should handle
```typescript
/**
 * @throws {ValidationError} When email format is invalid
 * @throws {ConflictError} When email already exists
 */
function registerUser(email: string, password: string)
```

**@example** - Show realistic usage (highly valuable)
```typescript
/**
 * @example
 * ```typescript
 * const user = await fetchUser('abc123');
 * if (user) {
 *   console.log(user.email);
 * }
 * ```
 */
```

**@deprecated** - Mark obsolete code with migration path
```typescript
/**
 * @deprecated Use fetchUserById() instead. Will be removed in v3.0.
 */
function getUser(id: string)
```

**@see** - Link to related functions or documentation
```typescript
/**
 * @see {@link validateUser} for validation rules
 * @see https://docs.example.com/auth for authentication flow
 */
```

**@remarks** - Add detailed explanations or important notes
```typescript
/**
 * @remarks
 * This function performs database migrations. Always backup before running.
 * Concurrent executions are prevented via row-level locks.
 */
```

### What to Document

**Always document:**
- Public APIs and exported functions/classes
- Complex business logic or algorithms
- Non-obvious behavior or edge cases
- Functions that throw errors
- Configuration objects with many options

**Usually document:**
- Interfaces and type aliases (brief description of purpose)
- Class methods (especially public ones)
- Callback parameters (explain when/how they're called)

**Sometimes skip:**
- Private implementation details (unless complex)
- Self-explanatory getters/setters
- Simple utility functions where name + types are sufficient

### Specific Patterns

**Classes and Constructors**
```typescript
/**
 * Manages WebSocket connections with automatic reconnection.
 * Handles connection pooling and implements exponential backoff.
 */
class ConnectionManager {
  /**
   * @param config - Connection settings
   * @param config.maxRetries - Maximum reconnection attempts (default: 5)
   * @param config.timeout - Connection timeout in milliseconds
   */
  constructor(config: ConnectionConfig) {}
}
```

**Interfaces and Types**
```typescript
/**
 * Configuration for database connection pooling.
 * @property maxConnections - Maximum concurrent connections (default: 10)
 * @property idleTimeout - Milliseconds before closing idle connections
 */
interface PoolConfig {
  maxConnections?: number;
  idleTimeout: number;
}
```

**Generic Functions**
```typescript
/**
 * Transforms array elements using provided mapper function.
 * @typeParam T - Input element type
 * @typeParam R - Output element type
 * @param items - Array to transform
 * @param mapper - Function to apply to each element
 * @returns New array with transformed elements
 */
function map<T, R>(items: T[], mapper: (item: T) => R): R[]
```

**Function Overloads**
```typescript
/**
 * Fetches data from API with flexible input formats.
 */
function fetch(url: string): Promise<Response>;
/**
 * @param config - Request configuration including headers and method
 */
function fetch(config: RequestConfig): Promise<Response>;
function fetch(urlOrConfig: string | RequestConfig): Promise<Response> {
  // Implementation
}
```

**Async Functions**
```typescript
/**
 * Fetches user data with automatic retry on transient failures.
 * @param userId - User identifier
 * @returns User data including profile and preferences
 * @throws {NotFoundError} When user doesn't exist
 * @throws {NetworkError} After 3 failed retry attempts
 */
async function fetchUser(userId: string): Promise<User>
```

**Enums**
```typescript
/**
 * Authentication states for user sessions.
 */
enum AuthState {
  /** User not logged in */
  Anonymous = 'ANONYMOUS',
  /** User logged in with credentials */
  Authenticated = 'AUTHENTICATED',
  /** Session expired, reauth required */
  Expired = 'EXPIRED'
}
```

## Configuration Setup

### Basic typedoc.json

Create `typedoc.json` in project root:

```json
{
  "$schema": "https://typedoc.org/schema.json",
  "entryPoints": ["./src/index.ts"],
  "out": "docs",
  "plugin": [],
  "excludePrivate": true,
  "excludeProtected": false,
  "excludeInternal": true,
  "readme": "README.md",
  "categorizeByGroup": true,
  "navigation": {
    "includeCategories": true,
    "includeGroups": true
  }
}
```

### Common Configuration Options

**entryPoints** - Starting files for documentation
- Single entry: `["./src/index.ts"]`
- Multiple modules: `["./src/api/index.ts", "./src/utils/index.ts"]`
- Glob patterns: `["./src/**/*.ts"]`

**excludePrivate/excludeProtected/excludeInternal** - Control visibility
- `excludePrivate: true` - Hide private members (recommended)
- `excludeInternal: true` - Hide `@internal` tagged items
- Keep protected members visible for inheritance docs

**categorizeByGroup** - Organize by `@group` tags
```typescript
/**
 * @group Authentication
 */
export function login() {}

/**
 * @group User Management
 */
export function createUser() {}
```

### Package.json Scripts

```json
{
  "scripts": {
    "docs": "typedoc",
    "docs:watch": "typedoc --watch",
    "docs:json": "typedoc --json docs.json"
  }
}
```

## Documentation Audit Workflow

When auditing a codebase for documentation coverage:

1. **Generate JSON output** to analyze programmatically:
```bash
npx typedoc --json docs.json
```

2. **Identify undocumented exports**:
   - Look for exported functions/classes without comments
   - Check for missing @param or @returns tags
   - Find functions that throw errors without @throws

3. **Prioritize documentation**:
   - Start with public API surface (exported items)
   - Focus on complex functions with multiple parameters
   - Document functions that throw errors or have side effects

4. **Common gaps to check**:
   - Generic type parameters without @typeParam
   - Callback parameters without explanation
   - Optional parameters without default value explanation
   - Return types that need context (e.g., null vs undefined)

## Advanced Patterns

### Module Organization

Use @module for file-level documentation:
```typescript
/**
 * Utilities for data validation and sanitization.
 * All functions in this module throw ValidationError on invalid input.
 * @module utils/validation
 */
```

### Cross-References

Link between related items:
```typescript
/**
 * Creates a new user account.
 * @see {@link validateEmail} - Email validation rules
 * @see {@link User} - The returned user type
 */
function createUser(email: string): User
```

### Inline Type Documentation

Document complex inline types:
```typescript
/**
 * @param options - Query configuration
 * @param options.sort - Sort field and direction (e.g., "name:asc")
 * @param options.filter - Filter criteria as key-value pairs
 */
function query(options: {
  sort?: string;
  filter?: Record<string, any>;
})
```

### Custom Tags

Define custom tags in typedoc.json for domain-specific needs:
```json
{
  "customTags": ["performance", "security"]
}
```

Use in code:
```typescript
/**
 * @performance O(n log n) time complexity
 * @security Sanitizes all user input
 */
function processData(data: string[])
```

## Quality Guidelines

### Write for Developers

Assume the reader knows TypeScript but not your domain:
- Explain business logic and "why"
- Document non-obvious behavior
- Highlight edge cases and gotchas
- Show realistic usage examples

### Keep It Current

- Update docs when changing function signatures
- Remove outdated examples
- Mark deprecated items immediately
- Version migration notes in @deprecated tags

### Consistency Matters

- Use consistent terminology across the codebase
- Follow a standard order: description → @param → @returns → @throws → @example
- Use active voice: "Returns the user" not "The user is returned"
