---
name: package-exports
description: Configure package.json exports and understand import resolution in the Orient monorepo. Use when confused about dist vs source imports, configuring package exports, fixing module resolution errors, or creating barrel files. Covers exports field patterns, development vs production resolution, and re-export strategies.
---

# Package Exports & Import Patterns

## Quick Reference

```bash
# Test package exports work correctly
pnpm --filter @orient/core test

# Check what a package exports
cat packages/core/package.json | jq '.exports'

# Verify dist exists before importing
ls packages/core/dist/
```

## The Golden Rule: Source vs Dist

| Context                         | Import From           | Why                |
| ------------------------------- | --------------------- | ------------------ |
| **Inside same package**         | Source (`./file.js`)  | Direct file access |
| **Cross-package (production)**  | Dist (`@orient/pkg`)  | Built output       |
| **Cross-package (development)** | Source via path alias | TypeScript paths   |

**Never** import from another package's `dist/` directory directly:

```typescript
// ❌ WRONG - importing dist directly
import { Service } from '../../../dist/services/service.js';
import { Service } from '@orient/core/dist/index.js';

// ✅ CORRECT - use package name (resolves to dist via exports)
import { Service } from '@orient/core';

// ✅ CORRECT - use local re-export
import { Service } from './services/index.js';
```

## package.json Exports Field

The `exports` field defines how your package can be imported:

### Basic Export Pattern

```json
{
  "name": "@orient/core",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.js",
      "default": "./dist/index.js"
    }
  }
}
```

### Subpath Exports

For packages with multiple entry points:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./config": {
      "types": "./dist/config/index.d.ts",
      "import": "./dist/config/index.js"
    },
    "./logger": {
      "types": "./dist/logger/index.d.ts",
      "import": "./dist/logger/index.js"
    }
  }
}
```

This enables:

```typescript
import { loadConfig } from '@orient/core'; // Main export
import { Config } from '@orient/core/config'; // Subpath export
import { createLogger } from '@orient/core/logger'; // Subpath export
```

### Export Order Matters

Node.js uses the **first matching condition**:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts", // TypeScript reads this first
      "import": "./dist/index.js", // ESM import
      "require": "./dist/index.cjs", // CommonJS require
      "default": "./dist/index.js" // Fallback
    }
  }
}
```

## Development Resolution with Path Aliases

During development, TypeScript uses path aliases from root `tsconfig.json`:

```json
{
  "compilerOptions": {
    "paths": {
      "@orient/core": ["./packages/core/src/index"],
      "@orient/database": ["./packages/database/src/index"]
    }
  }
}
```

This means:

- **Development**: `@orient/core` → `packages/core/src/index.ts`
- **Production**: `@orient/core` → `packages/core/dist/index.js`

## Re-Export Patterns (Barrel Files)

### Standard Re-Export

```typescript
// packages/core/src/index.ts

// Named exports
export { loadConfig } from './config/index.js';
export { createLogger, createServiceLogger } from './logger/index.js';

// Type exports (important for consumers)
export type { Config, LogLevel } from './types/index.js';

// Default export
export { default as CoreModule } from './CoreModule.js';
```

### Re-Exporting from Dependencies

When re-exporting from workspace dependencies:

```typescript
// packages/agents/src/index.ts

// Re-export from workspace dependency
export { MessageDatabase } from '@orient/database-services';

// Or selective re-export
import { MessageDatabase } from '@orient/database-services';
export { MessageDatabase };
```

### Avoiding Re-Export Issues

```typescript
// ❌ Can cause issues with CJS modules
export * from './some-module.js';

// ✅ Explicit named exports are safer
export { SpecificClass, specificFunction } from './some-module.js';
```

## Common Errors & Solutions

### "Cannot find module '@orient/package'"

1. **Build the package first**:

   ```bash
   pnpm --filter @orient/package build
   ```

2. **Check exports match dist structure**:

   ```bash
   ls packages/package/dist/
   cat packages/package/package.json | jq '.exports'
   ```

3. **Verify workspace dependency**:
   ```json
   {
     "dependencies": {
       "@orient/package": "workspace:*"
     }
   }
   ```

### "Module has no exported member"

The export exists in source but not in the barrel file:

```typescript
// Check src/index.ts includes the export
export { MissingClass } from './MissingClass.js';
```

### Import Works in IDE but Fails at Runtime

TypeScript uses path aliases (source), but runtime uses package exports (dist):

1. Ensure package is built
2. Check exports field matches what you're importing
3. Subpath imports need explicit exports

### Circular Import Error

Usually caused by re-export chains:

```typescript
// Package A re-exports from B
export { Something } from '@orient/B';

// Package B re-exports from A
export { Other } from '@orient/A'; // Circular!
```

Solution: Import from the source package directly.

## Testing Package Exports

Add a contract test to verify exports work:

```typescript
// tests/contracts/core.contract.test.ts
import { describe, it, expect } from 'vitest';

describe('@orient/core exports', () => {
  it('should export loadConfig', async () => {
    const { loadConfig } = await import('@orient/core');
    expect(typeof loadConfig).toBe('function');
  });

  it('should export from subpath', async () => {
    const { Config } = await import('@orient/core/config');
    expect(Config).toBeDefined();
  });
});
```

## Files Field for Publishing

Control what gets published to npm:

```json
{
  "files": ["dist", "README.md"]
}
```

This excludes `src/`, tests, and config files from the package.

## Checklist for New Exports

When adding a new export to a package:

- [ ] Add export to `src/index.ts`
- [ ] If subpath export, add to `package.json` exports
- [ ] Rebuild the package
- [ ] Add contract test for the export
- [ ] Update consumers to use the new export
