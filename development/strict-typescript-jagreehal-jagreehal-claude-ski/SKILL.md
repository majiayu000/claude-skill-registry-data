---
name: strict-typescript
description: "Enforce patterns with TypeScript beyond strict:true. Include noUncheckedIndexedAccess, erasableSyntaxOnly, ts-reset, and type-fest."
version: 1.0.0
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

## The Rules

1. **Enable noUncheckedIndexedAccess** - Handle missing array/object elements
2. **Enable exactOptionalPropertyTypes** - Optional means missing, not undefined
3. **Enable verbatimModuleSyntax** - Type-only imports stay type-only
4. **Enable erasableSyntaxOnly** - No enums, no parameter properties
5. **Install ts-reset** - Fix JSON.parse and other any leaks
6. **Use satisfies and as const** - Keep literal types, validate shapes
7. **Install Total TypeScript extension** - Better error messages in VS Code
