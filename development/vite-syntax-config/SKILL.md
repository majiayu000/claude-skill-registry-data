---
name: vite-syntax-config
description: >
  Use when creating or editing vite.config.ts, setting up project configuration,
  or configuring shared Vite options.
  Prevents misconfiguring defineConfig(), forgetting loadEnv() for env-dependent
  config, and using wrong shared option defaults.
  Covers defineConfig(), conditional and async config functions, loadEnv(),
  and all shared options (root, base, mode, define, plugins, publicDir, cacheDir,
  logLevel, clearScreen, envDir, envPrefix, appType, future).
  Keywords: vite, config, defineConfig, loadEnv, vite.config.ts, shared options, plugins.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-syntax-config

## Quick Reference

### Config File Resolution Order

Vite automatically resolves the config file from the project root in this order:

| File | Format |
|------|--------|
| `vite.config.js` | ES modules or CJS |
| `vite.config.ts` | TypeScript (transpiled automatically) |
| `vite.config.mjs` | ES modules (explicit) |
| `vite.config.mts` | TypeScript ES modules (explicit) |
| `vite.config.cjs` | CommonJS (explicit) |
| `vite.config.cts` | TypeScript CommonJS (explicit) |

### Shared Options Summary

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `root` | `string` | `process.cwd()` | Project root (where index.html lives) |
| `base` | `string` | `'/'` | Public base path for asset URLs |
| `mode` | `string` | `'development'` / `'production'` | Environment mode |
| `define` | `Record<string, any>` | -- | Global constant replacements |
| `plugins` | `(Plugin \| Plugin[])[]` | `[]` | Plugin array (falsy ignored, arrays flattened) |
| `publicDir` | `string \| false` | `'public'` | Static assets directory |
| `cacheDir` | `string` | `'node_modules/.vite'` | Pre-bundling cache location |
| `logLevel` | `'info' \| 'warn' \| 'error' \| 'silent'` | `'info'` | Console output verbosity |
| `customLogger` | `Logger` | -- | Custom logger instance |
| `clearScreen` | `boolean` | `true` | Clear terminal on server start |
| `envDir` | `string \| false` | `root` | Directory for .env files |
| `envPrefix` | `string \| string[]` | `'VITE_'` | Prefix for client-exposed env vars |
| `appType` | `'spa' \| 'mpa' \| 'custom'` | `'spa'` | Application type (controls HTML middleware) |
| `assetsInclude` | `string \| RegExp \| array` | -- | Additional static asset file types |
| `future` | `Record<string, 'warn' \| undefined>` | -- | Opt-in to future breaking changes |

### Critical Warnings

**NEVER** set `envPrefix` to `''` (empty string) -- this exposes ALL environment variables (including `DB_PASSWORD`, `SECRET_KEY`, etc.) to client-side code via `import.meta.env`.

**ALWAYS** use `defineConfig()` -- it provides full TypeScript IntelliSense and type checking for all config options, even in plain `.js` files.

**ALWAYS** use `JSON.stringify()` when setting string values in `define` -- values are used as raw code expressions, so bare strings cause syntax errors.

**NEVER** put sensitive data in `VITE_`-prefixed env variables -- they are embedded in the client bundle and visible to anyone.

---

## Config Patterns

### Basic Config with defineConfig()

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  root: './src',
  base: '/my-app/',
  plugins: [],
})
```

### Conditional Config (command/mode)

ALWAYS use a function export when config differs between `serve` (dev) and `build` (production):

```typescript
export default defineConfig(({ command, mode, isSsrBuild, isPreview }) => {
  if (command === 'serve') {
    return {
      // Dev-only config
    }
  } else {
    // command === 'build'
    return {
      // Production-only config
    }
  }
})
```

Parameters available in the function:
- `command`: `'serve'` (dev server) or `'build'` (production build)
- `mode`: `'development'`, `'production'`, or custom mode string
- `isSsrBuild`: `boolean` -- true during SSR builds
- `isPreview`: `boolean` -- true during `vite preview`

### Async Config

Use async config when you need to fetch data or run async operations before configuring:

```typescript
export default defineConfig(async ({ command, mode }) => {
  const data = await asyncFunction()
  return {
    // config using fetched data
  }
})
```

### Loading Environment Variables in Config

Environment variables are NOT available via `process.env` in the config file by default. ALWAYS use `loadEnv()` to access them:

```typescript
import { defineConfig, loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  // Load env from envDir (default: root). Third arg '' loads ALL env vars, not just VITE_-prefixed
  const env = loadEnv(mode, process.cwd(), '')
  return {
    define: {
      __APP_ENV__: JSON.stringify(env.APP_ENV),
    },
  }
})
```

`loadEnv(mode, envDir, prefixes)` parameters:
- `mode`: Which `.env.[mode]` file to load
- `envDir`: Directory containing `.env` files
- `prefixes`: String or array of prefixes to filter (default: `'VITE_'`). Use `''` to load all.

---

## Decision Trees

### Which Config Pattern to Use?

```
Need different config for dev vs build?
├── YES → Use conditional: defineConfig(({ command }) => { ... })
│         Need env vars in config?
│         ├── YES → Use loadEnv() inside the function
│         └── NO  → Return config object per command
├── NO, but need async operations?
│   └── YES → Use async: defineConfig(async () => { ... })
└── NO → Use static: defineConfig({ ... })
```

### Which appType to Use?

```
Building a Single Page Application (client-side routing)?
├── YES → appType: 'spa' (default, includes SPA fallback middleware)
├── NO, Multi-Page Application (separate HTML files)?
│   └── YES → appType: 'mpa' (HTML middleware, no SPA fallback)
└── NO, Custom server (Express, Fastify, etc.)?
    └── YES → appType: 'custom' (no HTML middleware at all)
```

---

## Transformer Options (v8+)

### oxc (replaces esbuild in v8)

Vite 8+ uses Oxc for JSX/TS transformation. Applied to `.ts`, `.jsx`, `.tsx` by default:

```typescript
export default defineConfig({
  oxc: {
    jsx: {
      runtime: 'classic',
      pragma: 'h',
      pragmaFrag: 'Fragment',
    },
  },
})
```

Set `oxc: false` to disable the Oxc transform entirely.

### esbuild (deprecated in v8)

In Vite 8+, `esbuild` config is converted internally to `oxc`. ALWAYS use the `oxc` option directly when targeting Vite 8+. For Vite 6/7, use `esbuild` as before.

---

## Custom Logger

Create a filtered logger to suppress specific warnings:

```typescript
import { createLogger, defineConfig } from 'vite'

const logger = createLogger()
const loggerWarn = logger.warn
logger.warn = (msg, options) => {
  if (msg.includes('vite:css') && msg.includes(' is empty')) return
  loggerWarn(msg, options)
}

export default defineConfig({
  customLogger: logger,
})
```

---

## Reference Links

- [references/config-options.md](references/config-options.md) -- Complete shared config options with types, defaults, and descriptions
- [references/examples.md](references/examples.md) -- Working code examples for conditional config, async config, loadEnv, and plugin arrays
- [references/anti-patterns.md](references/anti-patterns.md) -- Common configuration mistakes and how to avoid them

### Official Sources

- https://vite.dev/config/
- https://vite.dev/config/shared-options
- https://vite.dev/guide/
