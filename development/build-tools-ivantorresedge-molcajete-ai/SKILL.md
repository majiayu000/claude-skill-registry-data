---
name: build-tools
description: Build tool configuration for tsup, tsx, and bundlers. Use when setting up build pipelines.
---

# Build Tools Skill

This skill covers build tool configuration for TypeScript projects.

## When to Use

Use this skill when:
- Setting up build pipelines
- Configuring library bundling
- Running TypeScript directly
- Choosing between build tools

## Core Principle

**RIGHT TOOL FOR THE JOB** - Use tsup for libraries, tsx for scripts, Vite for apps.

## Tool Selection Guide

| Use Case | Recommended Tool |
|----------|------------------|
| Library/Package | tsup |
| CLI Application | tsup + tsx |
| Script Execution | tsx |
| React SPA | Vite |
| Full-Stack App | Next.js |

## tsup - Library Bundler

### Installation

```bash
npm install -D tsup
```

### Basic Configuration

```typescript
// tsup.config.ts
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,
  clean: true,
  splitting: false,
  sourcemap: true,
  minify: false,
  treeshake: true,
});
```

### Package.json for Library

```json
{
  "name": "my-library",
  "version": "1.0.0",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    }
  },
  "files": ["dist"],
  "scripts": {
    "build": "tsup",
    "dev": "tsup --watch"
  }
}
```

### Multiple Entry Points

```typescript
// tsup.config.ts
export default defineConfig({
  entry: {
    index: 'src/index.ts',
    utils: 'src/utils/index.ts',
    cli: 'src/cli.ts',
  },
  format: ['esm', 'cjs'],
  dts: true,
});
```

### CLI with Shebang

```typescript
// tsup.config.ts
export default defineConfig({
  entry: ['src/cli.ts'],
  format: ['esm'],
  banner: {
    js: '#!/usr/bin/env node',
  },
  clean: true,
});
```

## tsx - TypeScript Execution

### Installation

```bash
npm install -D tsx
```

### Usage

```bash
# Run TypeScript file directly
npx tsx src/script.ts

# Watch mode
npx tsx watch src/server.ts

# With Node.js flags
npx tsx --inspect src/debug.ts
```

### Package.json Scripts

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "start": "tsx src/index.ts",
    "script": "tsx scripts/migrate.ts"
  }
}
```

### tsconfig.json for tsx

```json
{
  "compilerOptions": {
    "module": "ESNext",
    "moduleResolution": "bundler",
    "esModuleInterop": true
  }
}
```

## TypeScript Compiler (tsc)

### Build Only (No Bundling)

```json
{
  "compilerOptions": {
    "outDir": "./dist",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

```json
{
  "scripts": {
    "build": "tsc",
    "build:watch": "tsc --watch"
  }
}
```

## Vite - Application Bundler

### Installation

```bash
npm create vite@latest
```

### Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    target: 'ES2022',
    sourcemap: true,
    outDir: 'dist',
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
```

### Library Mode

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import { resolve } from 'node:path';

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'MyLib',
      fileName: 'my-lib',
      formats: ['es', 'cjs'],
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
    },
  },
});
```

## Build Scripts

### Complete Build Pipeline

```json
{
  "scripts": {
    "prebuild": "npm run clean",
    "build": "tsup",
    "postbuild": "npm run type-check",
    "clean": "rm -rf dist",
    "type-check": "tsc --noEmit"
  }
}
```

### Watch Mode

```json
{
  "scripts": {
    "dev": "tsup --watch",
    "dev:run": "tsx watch src/index.ts"
  }
}
```

## Output Formats

### ESM (ES Modules)

```typescript
// Output: dist/index.js
export function hello() { }
```

### CJS (CommonJS)

```typescript
// Output: dist/index.cjs
module.exports.hello = function() { }
```

### Dual Package

```typescript
// tsup.config.ts
export default defineConfig({
  format: ['esm', 'cjs'],
  dts: true,
});
```

## Declaration Files

### Generate .d.ts

```typescript
// tsup.config.ts
export default defineConfig({
  dts: true, // Generate declaration files
});
```

### Separate Declaration Build

```json
{
  "scripts": {
    "build": "tsup && tsc --emitDeclarationOnly"
  }
}
```

## Source Maps

```typescript
// tsup.config.ts
export default defineConfig({
  sourcemap: true, // Generate source maps
});
```

## Tree Shaking

```typescript
// tsup.config.ts
export default defineConfig({
  treeshake: true, // Remove unused code
});
```

## Minification

```typescript
// tsup.config.ts
export default defineConfig({
  minify: true, // Minify output (production)
});
```

## External Dependencies

```typescript
// tsup.config.ts
export default defineConfig({
  external: ['react', 'react-dom'], // Don't bundle these
});
```

## Best Practices Summary

1. **Use tsup for libraries** - Simple, fast, handles dual packages
2. **Use tsx for scripts** - Direct execution without build
3. **Use Vite for apps** - Fast dev server, optimized builds
4. **Generate type declarations** - Always include .d.ts files
5. **Support both ESM and CJS** - Dual package format
6. **Enable source maps** - For debugging
7. **Tree shake in production** - Remove unused code

## Code Review Checklist

- [ ] Correct build tool selected for use case
- [ ] tsup.config.ts or vite.config.ts present
- [ ] Declaration files generated (dts: true)
- [ ] Both ESM and CJS formats for libraries
- [ ] Source maps enabled
- [ ] External dependencies configured
- [ ] Clean script removes old builds
