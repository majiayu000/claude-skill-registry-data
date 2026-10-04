---
name: vite-impl-project-setup
description: >
  Use when creating a new Vite project, adding Vite to an existing project,
  or configuring TypeScript and framework plugins.
  Prevents missing vite-env.d.ts for TypeScript or using wrong tsconfig settings.
  Covers create-vite scaffolding, CLI commands, TypeScript config, project structure,
  package.json scripts, and framework plugin integration.
  Keywords: create-vite, vite dev, vite build, vite preview, tsconfig, vite-env.d.ts, project setup.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-impl-project-setup

## Quick Reference

### Project Creation (create-vite)

| Package Manager | Command |
|----------------|---------|
| npm | `npm create vite@latest my-app -- --template react-ts` |
| pnpm | `pnpm create vite my-app --template react-ts` |
| yarn | `yarn create vite my-app --template react-ts` |

Omit `--template` for interactive template selection.

### Available Templates

| Template | TypeScript Variant | Framework Plugin |
|----------|-------------------|-----------------|
| `vanilla` | `vanilla-ts` | None |
| `react` | `react-ts` | `@vitejs/plugin-react` (Babel) |
| `react-swc` | `react-swc-ts` | `@vitejs/plugin-react-swc` (SWC) |
| `vue` | `vue-ts` | `@vitejs/plugin-vue` |
| `preact` | `preact-ts` | `@preact/preset-vite` |
| `lit` | `lit-ts` | None |
| `svelte` | `svelte-ts` | `@sveltejs/vite-plugin-svelte` |
| `solid` | `solid-ts` | `vite-plugin-solid` |
| `qwik` | `qwik-ts` | None (Qwik CLI) |

### CLI Commands

| Command | Alias | Default Port | Purpose |
|---------|-------|-------------|---------|
| `vite` | `vite dev` / `vite serve` | 5173 | Start dev server with HMR |
| `vite build` | — | — | Production build to `dist/` |
| `vite preview` | — | 4173 | Preview production build locally |

### Common CLI Flags

| Flag | Example | Purpose |
|------|---------|---------|
| `--port <number>` | `vite --port 3000` | Set dev server port |
| `--open` | `vite --open` | Open browser on start |
| `--mode <mode>` | `vite build --mode staging` | Set mode (loads `.env.staging`) |
| `--force` | `vite --force` | Re-bundle dependencies, ignore cache |
| `--host` | `vite --host` | Expose on LAN (0.0.0.0) |

### Critical Warnings

**ALWAYS** set `isolatedModules: true` in `tsconfig.json` — Vite transpiles TypeScript without type information. Without this flag, code that relies on cross-file type analysis (like `const enum` re-exports) will silently produce incorrect output.

**NEVER** rely on Vite for type checking — Vite performs transpile-only. ALWAYS run `tsc --noEmit` separately for type safety, either in CI or as a parallel dev process.

**NEVER** set `envPrefix` to `''` in `vite.config.ts` — this exposes ALL environment variables (including secrets like `DB_PASSWORD`) to client-side code.

**NEVER** omit `/// <reference types="vite/client" />` from `vite-env.d.ts` — without it, TypeScript cannot resolve `import.meta.env`, asset imports (`.svg`, `.png`), or HMR types.

---

## Decision Tree: New Project Setup

```
Need a new Vite project?
├── Greenfield project → Use create-vite with --template
│   ├── React project?
│   │   ├── Need fastest dev builds → react-swc-ts (SWC compiler)
│   │   └── Need Babel plugins → react-ts (Babel compiler)
│   ├── Vue project? → vue-ts
│   ├── Svelte project? → svelte-ts
│   ├── No framework? → vanilla-ts
│   └── Other framework? → Check create-vite templates list
│
├── Adding Vite to existing project → Manual setup
│   ├── Install vite as devDependency
│   ├── Create vite.config.ts with framework plugin
│   ├── Move/create index.html at project root
│   ├── Add <script type="module" src="/src/main.ts"> to index.html
│   └── Add dev/build/preview scripts to package.json
│
└── TypeScript project?
    ├── ALWAYS set isolatedModules: true in tsconfig.json
    ├── ALWAYS create src/vite-env.d.ts with /// reference types
    ├── ALWAYS run tsc --noEmit separately for type checking
    └── ALWAYS use type-only imports: import type { T } from '...'
```

---

## Project Structure

```
my-app/
├── index.html                 # Entry point (MUST be at project root)
├── public/                    # Static assets (copied as-is, no processing)
│   └── favicon.ico
├── src/
│   ├── main.ts                # Application entry (referenced from index.html)
│   ├── App.tsx                # Root component (framework-dependent)
│   ├── vite-env.d.ts          # Vite client type declarations
│   └── assets/                # Processed assets (hashed in build)
│       └── logo.svg
├── vite.config.ts             # Vite configuration
├── tsconfig.json              # TypeScript configuration
├── package.json               # Dependencies and scripts
└── .gitignore                 # Source control exclusions
```

**ALWAYS** place `index.html` at the project root — Vite uses it as the entry point, NOT inside `public/` or `src/`. The dev server maps `<root>/index.html` to `http://localhost:5173/`.

---

## TypeScript Configuration

### Required tsconfig.json Settings

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "isolatedModules": true,
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "types": ["vite/client"]
  },
  "include": ["src"]
}
```

### Critical Settings Explained

| Setting | Value | Why |
|---------|-------|-----|
| `isolatedModules` | `true` | **REQUIRED** — Vite transpiles each file independently without type info |
| `useDefineForClassFields` | `true` | Matches ES2022+ class field semantics used by Vite |
| `noEmit` | `true` | Vite handles emit; tsc is for type checking only |
| `moduleResolution` | `"bundler"` | Matches Vite's module resolution strategy |
| `types` | `["vite/client"]` | Provides types for `import.meta.env`, asset imports, HMR API |

### vite-env.d.ts (REQUIRED)

```typescript
/// <reference types="vite/client" />
```

This file MUST exist in `src/` to provide TypeScript with Vite-specific type definitions. It enables types for:
- `import.meta.env.VITE_*` variables
- Asset imports (`import logo from './logo.svg'`)
- `import.meta.hot` HMR API

### Type Checking Workflow

Vite does NOT type-check — it only transpiles. ALWAYS run type checking separately:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview",
    "typecheck": "tsc --noEmit",
    "typecheck:watch": "tsc --noEmit --watch"
  }
}
```

---

## Framework Plugin Setup

### Framework Plugin Table

| Framework | Plugin Package | Import | Config |
|-----------|---------------|--------|--------|
| React (Babel) | `@vitejs/plugin-react` | `import react from '@vitejs/plugin-react'` | `plugins: [react()]` |
| React (SWC) | `@vitejs/plugin-react-swc` | `import react from '@vitejs/plugin-react-swc'` | `plugins: [react()]` |
| Vue | `@vitejs/plugin-vue` | `import vue from '@vitejs/plugin-vue'` | `plugins: [vue()]` |
| Vue JSX | `@vitejs/plugin-vue-jsx` | `import vueJsx from '@vitejs/plugin-vue-jsx'` | `plugins: [vue(), vueJsx()]` |
| Svelte | `@sveltejs/vite-plugin-svelte` | `import { svelte } from '@sveltejs/vite-plugin-svelte'` | `plugins: [svelte()]` |

### Minimal vite.config.ts (React + TypeScript)

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

export default defineConfig({
  plugins: [react()],
})
```

### JSX Configuration (Non-Framework)

For Vite 8+ (Oxc transformer):
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

For Vite 6/7 (esbuild transformer):
```typescript
export default defineConfig({
  esbuild: {
    jsxFactory: 'h',
    jsxFragment: 'Fragment',
    jsxInject: `import { h, Fragment } from 'preact'`,
  },
})
```

---

## CSS Preprocessor Setup

Install the preprocessor package only — NO Vite plugins needed:

| Preprocessor | Install Command | File Extensions |
|-------------|----------------|-----------------|
| Sass | `npm add -D sass-embedded` | `.scss`, `.sass` |
| Less | `npm add -D less` | `.less` |
| Stylus | `npm add -D stylus` | `.styl`, `.stylus` |

**ALWAYS** prefer `sass-embedded` over `sass` — it is significantly faster for large projects.

---

## Source Control (.gitignore)

```gitignore
node_modules
dist
*.local
.env.local
.env.*.local
```

**ALWAYS** ignore `node_modules` and `dist`. **ALWAYS** ignore `.env.local` and `.env.*.local` — these contain environment-specific secrets. **NEVER** ignore `vite.config.ts`, `tsconfig.json`, or `package-lock.json` / `pnpm-lock.yaml` — these are required for reproducible builds.

---

## Reference Links

- [references/templates.md](references/templates.md) — All create-vite templates with framework plugin setup details
- [references/examples.md](references/examples.md) — Step-by-step project creation workflows and configuration examples
- [references/anti-patterns.md](references/anti-patterns.md) — Common project setup mistakes and how to avoid them

### Official Sources

- https://vite.dev/guide/
- https://vite.dev/config/
- https://vite.dev/guide/features.html#typescript
- https://vite.dev/guide/cli.html
