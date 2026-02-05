---
name: esm-module-patterns
description: Modern ESM import/export patterns. Use when writing or reviewing module structure.
---

# ESM Module Patterns Skill

This skill covers modern ECMAScript Module (ESM) patterns for TypeScript projects.

## When to Use

Use this skill when:
- Setting up new TypeScript projects
- Converting CommonJS to ESM
- Designing module structure
- Reviewing import/export patterns

## Core Principle

**ESM ONLY** - No CommonJS (`require`/`module.exports`). All projects use native ES Modules.

## Package.json Configuration

```json
{
  "type": "module",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    }
  },
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "files": ["dist"]
}
```

## Import Patterns

### Named Imports (Preferred)

```typescript
// ✅ Named imports - clear and tree-shakeable
import { formatDate, parseDate } from './utils/date.js';
import { UserService, type User } from './services/user.js';

// ✅ Type-only imports
import type { Config } from './config.js';
```

### Default Imports

```typescript
// ✅ Default import for single main export
import express from 'express';
import React from 'react';

// ✅ Default with named
import fs, { promises as fsp } from 'node:fs';
```

### Namespace Imports

```typescript
// ✅ Namespace import when many exports needed
import * as utils from './utils/index.js';

utils.formatDate(date);
utils.parseDate(str);
```

### Dynamic Imports

```typescript
// ✅ Dynamic import for code splitting
const module = await import('./heavy-module.js');

// ✅ Conditional loading
if (process.env.NODE_ENV === 'development') {
  const devTools = await import('./dev-tools.js');
  devTools.enable();
}
```

## Export Patterns

### Named Exports (Preferred)

```typescript
// ✅ Named exports - explicit and tree-shakeable
export function formatDate(date: Date): string {
  return date.toISOString();
}

export interface User {
  id: string;
  name: string;
}

export const DEFAULT_TIMEOUT = 5000;
```

### Default Exports

```typescript
// ✅ Default export for main module entry
export default class ApiClient {
  // ...
}

// ✅ Default export for React components
export default function Button({ children }: ButtonProps) {
  return <button>{children}</button>;
}
```

### Re-exports

```typescript
// ✅ Re-export from barrel file (index.ts)
export { formatDate, parseDate } from './date.js';
export { User, UserService } from './user.js';
export type { Config } from './config.js';

// ✅ Re-export with rename
export { internalFunction as publicFunction } from './internal.js';

// ✅ Re-export all
export * from './utils.js';
export * as helpers from './helpers.js';
```

## File Extensions

**Always use `.js` extension in imports**, even for TypeScript files:

```typescript
// ✅ Correct - .js extension
import { helper } from './utils/helper.js';
import { User } from '../models/user.js';

// ❌ Wrong - no extension
import { helper } from './utils/helper';

// ❌ Wrong - .ts extension
import { helper } from './utils/helper.ts';
```

**Why `.js`?** TypeScript compiles `.ts` to `.js`, and Node.js ESM requires extensions.

## tsconfig.json for ESM

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "isolatedModules": true
  }
}
```

## Directory Structure

```
src/
├── index.ts              # Main entry point
├── types/
│   └── index.ts          # Type exports
├── utils/
│   ├── index.ts          # Barrel file
│   ├── date.ts
│   └── string.ts
├── services/
│   ├── index.ts          # Barrel file
│   ├── api.ts
│   └── auth.ts
└── models/
    ├── index.ts          # Barrel file
    └── user.ts
```

## Barrel Files (index.ts)

Use barrel files to simplify imports:

```typescript
// src/utils/index.ts
export { formatDate, parseDate } from './date.js';
export { capitalize, truncate } from './string.js';
export { debounce, throttle } from './async.js';
```

```typescript
// Consumer code
import { formatDate, capitalize, debounce } from './utils/index.js';
// or
import { formatDate, capitalize, debounce } from './utils/index.js';
```

## Node.js Built-in Modules

Use `node:` prefix for Node.js built-in modules:

```typescript
// ✅ With node: prefix
import fs from 'node:fs';
import path from 'node:path';
import { createServer } from 'node:http';

// ❌ Without prefix (works but not recommended)
import fs from 'fs';
```

## CommonJS Interop

When importing CommonJS modules:

```typescript
// ✅ Default import for CommonJS modules
import lodash from 'lodash';

// ✅ Named imports if supported
import { debounce } from 'lodash';

// ⚠️ May need default for some CJS modules
import pkg from 'some-cjs-package';
const { namedExport } = pkg;
```

## Anti-Patterns

### Mixed Module Systems

```typescript
// ❌ Never use require() in ESM
const fs = require('fs');

// ❌ Never use module.exports
module.exports = { foo };

// ❌ Never use __dirname/__filename directly
console.log(__dirname);
```

### ESM Replacements for CommonJS Globals

```typescript
// ✅ ESM way to get __dirname and __filename
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
```

### Circular Dependencies

```typescript
// ❌ Avoid circular imports
// a.ts
import { b } from './b.js';
export const a = b + 1;

// b.ts
import { a } from './a.js'; // Circular!
export const b = a + 1;

// ✅ Break cycle with third module or restructure
// shared.ts
export const base = 1;

// a.ts
import { base } from './shared.js';
export const a = base + 1;

// b.ts
import { base } from './shared.js';
export const b = base + 2;
```

## Type-Only Imports

Use `type` keyword for imports used only in type positions:

```typescript
// ✅ Type-only import - removed at compile time
import type { User, Config } from './types.js';

// ✅ Inline type import
import { createUser, type User } from './user.js';

// ✅ Type-only re-export
export type { User, Config } from './types.js';
```

## Best Practices Summary

1. **Always use `"type": "module"` in package.json**
2. **Use `.js` extension in all imports**
3. **Prefer named exports over default exports**
4. **Use `node:` prefix for Node.js built-ins**
5. **Use type-only imports for types**
6. **Create barrel files for clean API surface**
7. **Avoid circular dependencies**
8. **Never mix ESM and CommonJS**

## Code Review Checklist

- [ ] package.json has `"type": "module"`
- [ ] All imports use `.js` extension
- [ ] No `require()` or `module.exports`
- [ ] Node.js built-ins use `node:` prefix
- [ ] Type-only imports use `type` keyword
- [ ] No circular dependencies
- [ ] Barrel files export public API only
