---
name: vite-agents-project-scaffolder
description: >
  Use when generating a new Vite project from scratch, adding Vite to an
  existing app, or scaffolding a production-ready Vite setup.
  Prevents missing vite-env.d.ts, incorrect plugin selection, and incomplete
  environment variable configuration.
  Covers vite.config.ts generation, TypeScript setup (tsconfig.json,
  vite-env.d.ts), package.json with scripts, index.html entry point, source
  directory structure, .env setup, and React/Vue/Svelte/vanilla support.
  Keywords: scaffold, project setup, vite.config.ts, tsconfig, React, Vue,
  Svelte, TypeScript, package.json, create-vite.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-agents-project-scaffolder

## Quick Reference

### Scaffolding Decision Tree

```
What framework?
├── React
│   ├── Need Babel plugins (relay, styled-components)? → @vitejs/plugin-react
│   └── No special Babel needs? → @vitejs/plugin-react-swc (ALWAYS prefer — 20x faster)
├── Vue
│   └── ALWAYS → @vitejs/plugin-vue
├── Svelte
│   └── ALWAYS → @sveltejs/vite-plugin-svelte
└── Vanilla TypeScript
    └── No plugin needed
```

### What Vite Version?

| Version | Transform Engine | Bundler | Config Key |
|---------|-----------------|---------|------------|
| Vite 6/7 | esbuild | Rollup | `esbuild` |
| Vite 8+ | Oxc | Rolldown | `oxc` |

**ALWAYS** check the installed Vite version before generating config. Vite 8 uses `oxc` and `build.rolldownOptions`; Vite 6/7 uses `esbuild` and `build.rollupOptions`.

### Generated File Inventory

| File | Purpose | Framework-Specific |
|------|---------|-------------------|
| `vite.config.ts` | Build tool configuration | Yes (plugin differs) |
| `tsconfig.json` | TypeScript compiler options | Yes (JSX settings) |
| `tsconfig.node.json` | Node-targeted TS config for vite.config.ts | No |
| `src/vite-env.d.ts` | Vite client type declarations | No |
| `package.json` | Dependencies and scripts | Yes (deps differ) |
| `index.html` | Application entry point | Yes (root element, script src) |
| `src/main.tsx` / `src/main.ts` | Application bootstrap | Yes (framework entry) |
| `src/App.tsx` / `src/App.vue` / `src/App.svelte` | Root component | Yes |
| `.env.example` | Environment variable template | No |
| `.gitignore` | Version control exclusions | No |

### Critical Warnings

**NEVER** omit `isolatedModules: true` from `tsconfig.json` -- Vite uses transpile-only transforms that require this setting. Omitting it causes silent type-system mismatches.

**NEVER** set `envPrefix` to `''` in `vite.config.ts` -- this exposes ALL environment variables (including secrets like `DB_PASSWORD`) to client-side code.

**NEVER** include `type: "module"` in `package.json` when using `.ts` config files -- Vite handles module resolution internally. Adding it causes resolution conflicts.

**ALWAYS** use `/// <reference types="vite/client" />` in `src/vite-env.d.ts` -- this provides types for `import.meta.env`, asset imports, and CSS modules.

**ALWAYS** set `"moduleResolution": "bundler"` in `tsconfig.json` -- Vite resolves modules like a bundler, not like Node.js.

**ALWAYS** run type checking separately with `tsc --noEmit` -- Vite NEVER type-checks during dev or build.

---

## Framework Plugin Selection

### Plugin Comparison Table

| Framework | Plugin Package | Transform | When to Use |
|-----------|---------------|-----------|-------------|
| React | `@vitejs/plugin-react` | Babel | Need Babel plugins (relay, emotion, styled-components) |
| React | `@vitejs/plugin-react-swc` | SWC | Default choice -- 20x faster than Babel |
| Vue | `@vitejs/plugin-vue` | Vue compiler | ALWAYS for Vue SFC support |
| Vue + JSX | `@vitejs/plugin-vue-jsx` | Babel | Only when using JSX in Vue |
| Svelte | `@sveltejs/vite-plugin-svelte` | Svelte compiler | ALWAYS for Svelte |
| Vanilla | None | Built-in | No framework plugin needed |

### Plugin Configuration Patterns

**React (SWC -- default choice):**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

export default defineConfig({
  plugins: [react()],
})
```

**React (Babel -- only when Babel plugins needed):**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: ['babel-plugin-styled-components'],
      },
    }),
  ],
})
```

**Vue:**
```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
})
```

**Svelte:**
```typescript
import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  plugins: [svelte()],
})
```

---

## Scaffolding Procedure

### Step 1: Determine Project Parameters

Collect these before generating any files:

1. **Framework**: React / Vue / Svelte / Vanilla
2. **Vite version**: 6, 7, or 8 (affects config keys)
3. **CSS preprocessor**: None / Sass / Less / Stylus
4. **Path alias**: `@` -> `./src` (recommended)
5. **API proxy**: Backend URL if needed

### Step 2: Generate Files in Order

ALWAYS generate files in this order to avoid import resolution issues:

1. `package.json` (defines project identity and deps)
2. `tsconfig.json` + `tsconfig.node.json` (TypeScript must resolve before config)
3. `vite.config.ts` (depends on tsconfig for path resolution)
4. `index.html` (entry point)
5. `src/vite-env.d.ts` (type declarations)
6. `src/main.tsx` or `src/main.ts` (application entry)
7. `src/App.tsx` / `src/App.vue` / `src/App.svelte` (root component)
8. `.env.example` (environment template)
9. `.gitignore` (version control)

### Step 3: Install Dependencies

After generating files, run:
```bash
npm install
```

NEVER run `npm install` before all files are generated -- `package.json` must be complete first.

---

## TypeScript Configuration

### tsconfig.json Requirements

**ALWAYS include these settings** (non-negotiable for Vite):

| Setting | Value | Reason |
|---------|-------|--------|
| `isolatedModules` | `true` | Vite uses transpile-only transforms |
| `moduleResolution` | `"bundler"` | Matches Vite's module resolution |
| `target` | `"ES2020"` or higher | Vite targets modern browsers |
| `module` | `"ESNext"` | Vite uses native ESM |
| `types` | `["vite/client"]` | Provides `import.meta.env` types |
| `skipLibCheck` | `true` | Speeds up type checking |

**Framework-specific JSX settings:**

| Framework | `jsx` | `jsxImportSource` |
|-----------|-------|-------------------|
| React | `"react-jsx"` | `"react"` |
| Vue | Not needed | Not needed |
| Svelte | Not needed | Not needed |
| Vanilla | Not needed | Not needed |

### tsconfig.node.json (for vite.config.ts)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "noEmit": true
  },
  "include": ["vite.config.ts"]
}
```

---

## Environment Variables Setup

### .env.example Pattern

ALWAYS create `.env.example` with documented variables:

```bash
# Application
VITE_APP_TITLE=My Vite App
VITE_APP_VERSION=1.0.0

# API
VITE_API_BASE_URL=http://localhost:3000/api
```

### TypeScript Env Types

ALWAYS extend `ImportMetaEnv` in `src/vite-env.d.ts` to match `.env.example`:

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  readonly VITE_APP_VERSION: string
  readonly VITE_API_BASE_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

### .gitignore Env Rules

```
.env.local
.env.*.local
*.local
```

**NEVER** gitignore `.env` or `.env.example` -- these contain non-secret defaults and serve as documentation.

---

## CSS Preprocessor Setup

CSS preprocessors require ONLY a package install -- NEVER a Vite plugin:

| Preprocessor | Package to Install | File Extension |
|-------------|-------------------|----------------|
| Sass | `sass-embedded` (preferred) or `sass` | `.scss` / `.sass` |
| Less | `less` | `.less` |
| Stylus | `stylus` | `.styl` |

**NEVER** install `vite-plugin-sass` or similar -- Vite has built-in preprocessor support.

**ALWAYS** prefer `sass-embedded` over `sass` -- it runs Dart Sass in a separate process for better performance.

---

## Version-Specific Configuration

### Vite 8 (Oxc + Rolldown)

```typescript
export default defineConfig({
  oxc: {
    jsx: {
      runtime: 'automatic',
    },
  },
  build: {
    rolldownOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
})
```

### Vite 6/7 (esbuild + Rollup)

```typescript
export default defineConfig({
  esbuild: {
    jsx: 'automatic',
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
})
```

**NEVER** mix version-specific config keys -- using `esbuild` in Vite 8 triggers a deprecation warning and internal conversion.

---

## Reference Links

- [references/templates.md](references/templates.md) -- Complete file templates for React-TS, Vue-TS, Svelte-TS, and Vanilla-TS projects
- [references/examples.md](references/examples.md) -- Full scaffold output per framework showing every generated file
- [references/anti-patterns.md](references/anti-patterns.md) -- Common scaffolding mistakes and why they fail

### Official Sources

- https://vite.dev/guide/
- https://vite.dev/config/
- https://vite.dev/guide/env-and-mode
- https://vite.dev/guide/features#typescript
- https://vite.dev/guide/features#css-pre-processors
