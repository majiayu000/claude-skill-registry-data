---
name: vite-syntax-env-vars
description: >
  Use when configuring environment variables, using .env files, creating custom modes,
  or debugging env variable issues.
  Prevents exposing secrets by omitting the VITE_ prefix and misconfiguring .env file precedence.
  Covers import.meta.env built-ins, .env file loading order, VITE_ prefix requirement,
  dotenv-expand, custom modes, NODE_ENV vs mode, ImportMetaEnv TypeScript, HTML %VAR%, and loadEnv().
  Keywords: import.meta.env, .env, VITE_ prefix, loadEnv, custom mode, NODE_ENV, ImportMetaEnv.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-syntax-env-vars

## Quick Reference

### Built-in Constants (import.meta.env)

| Property | Type | Description |
|----------|------|-------------|
| `import.meta.env.MODE` | `string` | Current mode (`"development"`, `"production"`, or custom) |
| `import.meta.env.BASE_URL` | `string` | Base URL from `base` config option |
| `import.meta.env.PROD` | `boolean` | `true` when running in production |
| `import.meta.env.DEV` | `boolean` | `true` when running in development (ALWAYS inverse of `PROD`) |
| `import.meta.env.SSR` | `boolean` | `true` when running server-side |

### .env File Loading Order (Priority: Low to High)

| Priority | File | Loaded When | Gitignored |
|----------|------|-------------|------------|
| 1 (lowest) | `.env` | All modes | No |
| 2 | `.env.local` | All modes | Yes |
| 3 | `.env.[mode]` | Matching mode only | No |
| 4 | `.env.[mode].local` | Matching mode only | Yes |
| 5 (highest) | OS environment variables | Always | N/A |

OS environment variables ALWAYS take highest priority and NEVER get overwritten by `.env` files.

### Critical Warnings

> **NEVER** set `envPrefix` to `''` (empty string). This exposes ALL environment variables to client-side code, including secrets like `DB_PASSWORD`, `AWS_SECRET_KEY`, and session tokens. This is a critical security vulnerability.

> **NEVER** put secrets in `VITE_`-prefixed variables. Any variable with the `VITE_` prefix is embedded in the client bundle and visible to anyone inspecting the browser source. Use server-side environment variables or a backend API for secrets.

### VITE_ Prefix Rule

Only variables prefixed with `VITE_` are exposed to client code via `import.meta.env`:

```
VITE_API_URL=https://api.example.com   # Exposed: import.meta.env.VITE_API_URL
VITE_APP_TITLE=My App                  # Exposed: import.meta.env.VITE_APP_TITLE
DB_PASSWORD=secret123                  # NOT exposed: import.meta.env.DB_PASSWORD === undefined
SECRET_KEY=abc                         # NOT exposed: import.meta.env.SECRET_KEY === undefined
```

ALWAYS use the `VITE_` prefix for any variable that needs to reach client-side code.

---

## Decision Trees

### Which env approach to use?

```
Need env variable in CLIENT-SIDE code?
├── Yes → Prefix with VITE_ and access via import.meta.env.VITE_*
│         Is it a secret (API key, password, token)?
│         ├── Yes → STOP. NEVER put secrets in VITE_* vars.
│         │         Use a backend proxy or server-side API instead.
│         └── No → Safe to use VITE_* prefix
└── No → Need it in vite.config.ts?
    ├── Yes → Use loadEnv(mode, envDir, prefixes) to load it
    └── No → Use standard process.env (Node.js server-side only)
```

### Which .env file to use?

```
Variable needed in ALL environments?
├── Yes → Put in .env
│         Is it sensitive/local-only?
│         ├── Yes → Put in .env.local (gitignored)
│         └── No → Put in .env (committed)
└── No → Put in .env.[mode] (e.g., .env.staging, .env.production)
          Is it sensitive/local-only?
          ├── Yes → Put in .env.[mode].local (gitignored)
          └── No → Put in .env.[mode] (committed)
```

---

## NODE_ENV vs Mode

These are two DIFFERENT concepts. NEVER confuse them.

| Command | NODE_ENV | Mode | .env files loaded |
|---------|----------|------|-------------------|
| `vite` (dev server) | `"development"` | `"development"` | `.env`, `.env.development` |
| `vite build` | `"production"` | `"production"` | `.env`, `.env.production` |
| `vite build --mode staging` | `"production"` | `"staging"` | `.env`, `.env.staging` |
| `vite build --mode development` | `"production"` | `"development"` | `.env`, `.env.development` |
| `NODE_ENV=development vite build` | `"development"` | `"production"` | `.env`, `.env.production` |

Key distinction:
- **NODE_ENV** is set by the Vite command (`vite` = development, `vite build` = production) and controls `import.meta.env.PROD`/`DEV`
- **Mode** controls which `.env.[mode]` files are loaded and sets `import.meta.env.MODE`
- The `--mode` flag changes mode WITHOUT changing NODE_ENV
- ALWAYS use `--mode` for custom environments (staging, test, QA)

---

## Config Options

### envDir

- **Type**: `string | false`
- **Default**: `root` (project root)
- Directory to load `.env` files from
- Set to `false` to disable `.env` file loading entirely

### envPrefix

- **Type**: `string | string[]`
- **Default**: `"VITE_"`
- Controls which env variables are exposed to `import.meta.env`
- ALWAYS keep a meaningful prefix — NEVER set to empty string

```typescript
export default defineConfig({
  envPrefix: ['VITE_', 'PUBLIC_'],  // Expose both VITE_* and PUBLIC_* vars
})
```

### loadEnv()

Use `loadEnv()` to access env variables inside `vite.config.ts`:

```typescript
import { defineConfig, loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  // Load env files from cwd, only VITE_-prefixed vars
  const env = loadEnv(mode, process.cwd())

  // Load ALL env vars (including non-prefixed)
  const allEnv = loadEnv(mode, process.cwd(), '')

  return {
    define: {
      __APP_ENV__: JSON.stringify(allEnv.APP_ENV),
    },
  }
})
```

**Signature**: `loadEnv(mode: string, envDir: string, prefixes?: string | string[])`
- `mode`: The mode to load (e.g., `'development'`, `'production'`, `'staging'`)
- `envDir`: Directory containing `.env` files
- `prefixes`: Filter by prefix. Default `'VITE_'`. Pass `''` to load all variables.

---

## Variable Expansion (dotenv-expand)

Vite uses `dotenv-expand` to expand variables within `.env` files:

```bash
BASE_URL=https://example.com
API_URL=$BASE_URL/api         # https://example.com/api
ESCAPED=test\$BASE_URL        # test$BASE_URL (literal dollar sign)
UNDEFINED=$NONEXISTENT        # "" (empty string)
```

Use `\$` to escape a literal dollar sign. Undefined variables expand to empty string.

---

## TypeScript IntelliSense

ALWAYS define custom env variables in a type declaration file for full IntelliSense:

```typescript
// src/vite-env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  readonly VITE_API_URL: string
  readonly VITE_ENABLE_ANALYTICS: string
  // Add all custom VITE_* variables here
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

NEVER omit the `/// <reference types="vite/client" />` triple-slash directive — it provides types for all built-in constants (MODE, BASE_URL, PROD, DEV, SSR).

---

## HTML Env Replacement

Use `%ENV_VAR%` syntax in `index.html` to inject env variables:

```html
<title>%VITE_APP_TITLE%</title>
<p>Running in %MODE% mode</p>
<link rel="icon" href="%BASE_URL%favicon.ico" />
```

- All `import.meta.env` properties are available (built-in + VITE_-prefixed)
- Non-existent variables are silently ignored (no error, no replacement)
- This replacement happens at build time — values are statically embedded

---

## Reference Links

- [references/config-options.md](references/config-options.md) -- envDir, envPrefix, loadEnv signature, .env loading precedence details, mode config
- [references/examples.md](references/examples.md) -- Complete .env file examples, TypeScript IntelliSense setup, HTML replacement, custom modes, loadEnv patterns
- [references/anti-patterns.md](references/anti-patterns.md) -- Common environment variable mistakes and security pitfalls

### Official Sources

- https://vite.dev/guide/env-and-mode
- https://vite.dev/config/shared-options#envdir
- https://vite.dev/config/shared-options#envprefix
