---
name: strict-typescript
description: "Enforce patterns with TypeScript beyond strict:true. Include noUncheckedIndexedAccess, erasableSyntaxOnly, ts-reset, and type-fest. Advanced type patterns and ESLint enforcement."
version: 1.1.0
libraries: ["@total-typescript/ts-reset", "type-fest"]
---

# Enforcing Patterns with TypeScript

## Core Principle

`strict: true` is insufficient. Patterns without enforcement are just suggestions. TypeScript can enforce patterns at compile time.

## Required tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2024",
    "module": "ESNext",
    "moduleResolution": "bundler",

    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,

    "verbatimModuleSyntax": true,
    "erasableSyntaxOnly": true,

    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedSideEffectImports": true,

    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

## Key Flags Explained

### noUncheckedIndexedAccess

By default, `myArray[0]` is typed as the element type. This is a lie - it could be undefined.

```typescript
const users = ['Alice', 'Bob'];

// Without flag:
const first = users[0];  // string <- LIE!

// With flag:
const first = users[0];  // string | undefined <- TRUTH

if (first) {
  console.log(first.toUpperCase());  // Safe
}
```

### exactOptionalPropertyTypes

Ensures `{ id?: string }` means the key is MISSING, not `undefined`.

```typescript
type User = { id?: string };

// Without flag:
const user: User = { id: undefined };  // Allowed (causes bugs)

// With flag:
const user: User = { id: undefined };  // ERROR
const user: User = {};                 // OK - key is missing
```

### erasableSyntaxOnly (TS 5.8+)

Ensures code is compatible with native TypeScript runners (Node.js 22+, Bun, Deno):

```typescript
// FORBIDDEN - These emit JavaScript code
enum Status { Active, Inactive }
class User { constructor(public name: string) {} }

// REQUIRED - Erasable alternatives
const Status = { Active: 'active', Inactive: 'inactive' } as const;
type Status = (typeof Status)[keyof typeof Status];

class User {
  name: string;
  constructor(name: string) {
    this.name = name;  // Explicit assignment
  }
}
```

### verbatimModuleSyntax

Enforces `import type` for types - critical for the fn(args, deps) pattern:

```typescript
// CORRECT - Type-only import
import type { Database } from '../infra/database';

type GetUserDeps = { db: Database };

async function getUser(args, deps: GetUserDeps) {
  return deps.db.findUser(args.userId);  // Injected
}

// WRONG - Runtime import creates hidden dependency
import { db } from '../infra/database';

async function getUser(args) {
  return db.findUser(args.userId);  // Hard to test
}
```

### noUncheckedSideEffectImports

Catches ghost imports - side-effect imports that reference deleted files:

```typescript
import "./polyfills";  // ERROR if polyfills.ts doesn't exist
import "reflect-metadata";  // ERROR if package not installed
```

**Why this matters:**
- Side-effect imports run code but don't export anything
- Without this flag, TypeScript ignores them entirely
- Deleted or renamed files cause silent runtime failures
- This flag ensures all imports resolve correctly

## Fix Standard Library Leaks with ts-reset

`JSON.parse` returns `any` by default - bypasses all your validation!

```bash
npm install -D @total-typescript/ts-reset
```

Create `reset.d.ts`:

```typescript
import "@total-typescript/ts-reset";
```

Now:

```typescript
// Before ts-reset:
const data = JSON.parse(input);  // any <- DANGEROUS

// After ts-reset:
const data = JSON.parse(input);  // unknown <- MUST VALIDATE
const user = UserSchema.parse(data);  // Now typed
```

Also fixes:

```typescript
// Before:
[1, undefined, 2].filter(Boolean);  // (number | undefined)[]

// After:
[1, undefined, 2].filter(Boolean);  // number[]
```

## Type-Level Patterns

### satisfies Operator

```typescript
const routes = {
  home: { path: '/', handler: () => {} },
  about: { path: '/about', handler: () => {} },
} satisfies Record<string, Route>;

routes.typo;  // ERROR - Property 'typo' does not exist
routes.home;  // OK - Autocomplete works
```

### as const Assertions

```typescript
const ROLES = ['admin', 'user', 'guest'] as const;
type Role = (typeof ROLES)[number];  // "admin" | "user" | "guest"
```

## type-fest Utility Types

```bash
npm install type-fest
```

```typescript
import type { Simplify, SetRequired, PartialDeep, ReadonlyDeep } from 'type-fest';

// Flatten complex intersections for readable hovers
type UserWithPosts = Simplify<User & { posts: Post[] }>;

// Make specific optional keys required
type CreateUserArgs = SetRequired<Partial<User>, 'email' | 'name'>;

// Recursive Partial
type UserPatch = PartialDeep<User>;

// Recursive Readonly
type ImmutableUser = ReadonlyDeep<User>;
```

## Developer Experience

Complex type errors are a primary cause of pattern abandonment. Two tools help:

**[Total TypeScript VS Code Extension](https://www.totaltypescript.com/vscode-extension)**: Translates obtuse TypeScript errors into plain language directly in the IDE. Essential when working with complex generics like `createWorkflow` error unions.

**Type queries**: Use `// ^?` comments to show types inline in your editor:

```typescript
const user = { id: '123', role: 'admin' } as const;
//    ^? const user: { readonly id: "123"; readonly role: "admin"; }
```

This helps engineers understand complex generics and ensures code samples are truthful.

## The Native Compiler Future

As of late 2025, the TypeScript team is porting the compiler to native code (the "tsgo" project) to achieve up to 10x speedups. This native compiler uses multi-threading and optimized memory layouts.

**Why stricter flags matter for performance:** Flags like `verbatimModuleSyntax` and `erasableSyntaxOnly` reduce the "heuristics" the compiler needs to perform. When the compiler doesn't have to guess whether an import is type-only, or whether a feature needs transpilation, it can take faster code paths.

```typescript
// With verbatimModuleSyntax, the compiler knows immediately:
import type { User } from './types';  // Type-only, strip entirely
import { db } from './database';       // Runtime, keep as-is

// Without it, the compiler must analyze usage across the codebase
// to determine if an import is actually used at runtime
```

The flags we recommend aren't just about safety—they're also about performance. Stricter code is faster to compile because it's more explicit about intent.

## ESLint Enforcement

Ban unsafe patterns with tooling:

```javascript
// eslint.config.js
{
  extends: ['plugin:@typescript-eslint/strict-type-checked'],
  rules: {
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-unsafe-argument': 'error',
    '@typescript-eslint/no-unsafe-assignment': 'error',
    '@typescript-eslint/no-unsafe-call': 'error',
    '@typescript-eslint/no-unsafe-member-access': 'error',
    '@typescript-eslint/no-unsafe-return': 'error',
    '@typescript-eslint/consistent-type-assertions': ['error', { assertionStyle: 'never' }],
    '@typescript-eslint/no-non-null-assertion': 'error'
  }
}
```

## Type Narrowing (Never Use `as`)

### WRONG - Type Assertion

```typescript
const user = data as User;  // Lying to compiler
```

### CORRECT - Type Guard

```typescript
function isUser(x: unknown): x is User {
  return typeof x === 'object' && x !== null && 'id' in x;
}

if (isUser(data)) {
  data.id;  // Type-safe
}
```

### CORRECT - Discriminated Union

```typescript
type ApiResponse =
  | { status: 'success'; data: User }
  | { status: 'error'; message: string };

function handleResponse(response: ApiResponse) {
  if (response.status === 'success') {
    response.data;  // User, no assertion needed
  }
}
```

### CORRECT - Zod Validation

```typescript
const data: unknown = JSON.parse(input);
const user = UserSchema.parse(data);  // Throws if invalid, typed if valid
```

## Advanced Type Patterns

### Branded Types

Compile-time distinction between primitives:

```typescript
type UserId = string & { __brand: 'UserId' };
type PostId = string & { __brand: 'PostId' };

function getUser(id: UserId): User { }
function getPost(id: PostId): Post { }

const userId = 'abc' as UserId;
const postId = 'xyz' as PostId;

getUser(userId);  // OK
getUser(postId);  // ERROR - Type 'PostId' is not assignable to 'UserId'
```

### Template Literal Types

```typescript
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type Route = `/${string}`;
type Endpoint = `${HttpMethod} ${Route}`;

const endpoint: Endpoint = 'GET /users';  // OK
const invalid: Endpoint = 'FETCH /users'; // ERROR
```

### Conditional Types

```typescript
type ApiResponse<T> = T extends Error
  ? { success: false; error: T }
  : { success: true; data: T };

// ApiResponse<User> → { success: true; data: User }
// ApiResponse<Error> → { success: false; error: Error }
```

### Mapped Types with Key Remapping

```typescript
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type UserGetters = Getters<{ name: string; age: number }>;
// { getName: () => string; getAge: () => number }
```

## Build Performance

### Avoid Barrel Files

```typescript
// WRONG - Barrel file (index.ts re-exports)
// Slows tree-shaking, creates circular dependencies
export * from './user';
export * from './post';
export * from './comment';

// CORRECT - Direct imports
import { User } from './user';
import { Post } from './post';
```

### Profile with Diagnostics

```bash
tsc --extendedDiagnostics
```

### Project References for Monorepos

```json
// tsconfig.json
{
  "references": [
    { "path": "./packages/shared" },
    { "path": "./packages/api" }
  ]
}
```

## Build Tools

| Tool | Use For |
|------|---------|
| **Vite** | Modern dev server, HMR (apps) |
| **tsup/esbuild** | Ultra-fast transpilation (libraries) |
| **tsc** | Type checking (always, regardless of bundler) |

## The Rules

1. **Enable noUncheckedIndexedAccess** - Handle missing array/object elements
2. **Enable exactOptionalPropertyTypes** - Optional means missing, not undefined
3. **Enable verbatimModuleSyntax** - Type-only imports stay type-only
4. **Enable erasableSyntaxOnly** - No enums, no parameter properties
5. **Install ts-reset** - Fix JSON.parse and other any leaks
6. **Use satisfies and as const** - Keep literal types, validate shapes
7. **Install Total TypeScript extension** - Better error messages in VS Code
8. **Never use `any` or `as`** - Type guards and Zod instead
9. **ESLint strict-type-checked** - Enforce at build time
10. **Avoid barrel files** - Direct imports for build performance