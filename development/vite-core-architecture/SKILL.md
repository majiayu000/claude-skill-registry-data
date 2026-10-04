---
name: vite-core-architecture
description: >
  Use when creating a new Vite project, understanding Vite internals, or reasoning
  about dev vs production behavior.
  Prevents confusing Vite's native ESM dev server with traditional bundler-based
  dev servers and misunderstanding the two-mode architecture.
  Covers dev server vs build pipeline, native ESM serving, dependency pre-bundling,
  module graph, internal tools evolution (esbuild to Oxc, Rollup to Rolldown),
  index.html as entry point, browser support targets, and Node.js requirements.
  Keywords: vite, architecture, dev server, build, ESM, Rolldown, Oxc, pre-bundling, module graph.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-core-architecture

## Quick Reference

### Two-Mode Architecture

Vite operates as **two completely different systems** depending on context:

| Aspect | Dev Server (`vite`) | Production Build (`vite build`) |
|--------|--------------------|---------------------------------|
| Strategy | Native ESM, no bundling | Full bundle via Rolldown/Rollup |
| Module delivery | Individual files over HTTP | Optimized chunks |
| Transform tool (v8) | Oxc | Oxc |
| Transform tool (v5-7) | esbuild | esbuild |
| Bundler (v8) | None (native ESM) | Rolldown |
| Bundler (v5-7) | None (native ESM) | Rollup |
| Speed priority | Instant startup + HMR | Optimized output size |
| Browser target | esnext | baseline-widely-available |

### Internal Tools Evolution

| Version | Dev Transform | Dev Pre-bundling | Production Bundler | CSS Minification | JS Minifier |
|---------|--------------|------------------|--------------------|------------------|-------------|
| Vite 5 | esbuild | esbuild | Rollup | esbuild | esbuild |
| Vite 6 | esbuild | esbuild | Rollup | esbuild/lightningcss | esbuild |
| Vite 7 | esbuild | esbuild | Rollup | esbuild/lightningcss | esbuild |
| Vite 8 | **Oxc** | **Rolldown** | **Rolldown** | **Lightning CSS** | **Oxc** (30-90x faster than Terser) |

### Node.js Requirements

| Vite Version | Minimum Node.js |
|-------------|----------------|
| v5, v6 | 18+ |
| v7+ | 20.19+ or 22.12+ |

### Browser Support Targets

| Context | Target | Meaning |
|---------|--------|---------|
| Dev server | esnext | Latest JavaScript/CSS features, no transpilation |
| Production (v8 default) | baseline-widely-available | Chrome 111, Edge 111, Firefox 114, Safari 16.4 |
| Production (v7 default) | baseline-widely-available | Chrome 107, Edge 107, Firefox 104, Safari 16.0 |
| Legacy browsers | `@vitejs/plugin-legacy` | Generates polyfilled fallback bundles |

### Critical Warnings

**NEVER** set `envPrefix` to `''` -- this exposes ALL environment variables (including secrets like `DB_PASSWORD`) to client-side code.

**NEVER** exclude CommonJS dependencies from pre-bundling via `optimizeDeps.exclude` -- they MUST be pre-bundled to be converted to ESM for the dev server.

**NEVER** edit files in `node_modules/.vite/` -- this is the pre-bundling cache directory. Use `optimizeDeps.force: true` or `--force` CLI flag to rebuild it.

**NEVER** use a JavaScript file as the application entry point -- Vite uses `index.html` as the entry point. The HTML file references your scripts via `<script type="module" src="...">`.

**ALWAYS** use `defineConfig()` wrapper for `vite.config.ts` -- this provides TypeScript IntelliSense and type checking for all configuration options.

**ALWAYS** run `tsc --noEmit` separately for type checking -- Vite performs transpile-only (no type checking) for speed. NEVER rely on Vite for TypeScript type safety.

---

## How Vite Works

### Dev Server: Native ESM Serving

The dev server serves source files as native ES modules over HTTP:

1. Browser requests `index.html` from `http://localhost:5173/`
2. HTML contains `<script type="module" src="/src/main.ts">`
3. Browser requests `/src/main.ts`, Vite transforms it on-the-fly (TypeScript, JSX, etc.)
4. Browser parses `import` statements and requests each dependency
5. Vite intercepts `node_modules` imports and serves pre-bundled versions

No bundling step occurs. Each source file is an individual HTTP request. HMR updates propagate through the module graph -- only changed modules are replaced.

### Dependency Pre-Bundling

Pre-bundling runs automatically on first `vite` startup for two reasons:

1. **CommonJS/UMD to ESM conversion** -- the dev server serves ONLY native ESM
2. **Performance** -- packages like `lodash-es` (600+ modules) are consolidated into a single request

Pre-bundling results are cached in `node_modules/.vite`. Cache invalidates when: lockfile changes, `vite.config` changes, `NODE_ENV` changes, or patches folder changes.

### Production Build Pipeline

`vite build` bundles the entire application:

1. Resolves the module graph starting from `index.html` entry points
2. Applies all plugin transforms (JSX, TypeScript, CSS modules, etc.)
3. Bundles via Rolldown (v8) or Rollup (v5-7) with code splitting
4. Minifies JS via Oxc (v8) or esbuild (v5-7)
5. Minifies CSS via Lightning CSS (v8) or esbuild/lightningcss (v5-7)
6. Outputs optimized static assets to `dist/`

### index.html as Entry Point

Unlike Webpack or other bundlers, Vite treats `index.html` as the entry point:

```
<root>/index.html       → http://localhost:5173/
<root>/about.html       → http://localhost:5173/about.html
<root>/nested/page.html → http://localhost:5173/nested/page.html
```

Vite resolves `<script type="module" src="...">` tags and inline `<script type="module">` blocks, processing all referenced modules and CSS.

---

## Decision Trees

### Choosing a Framework Template

```
Creating new project with create-vite?
├── React app?
│   ├── Want Babel plugins?     → react-ts (uses @vitejs/plugin-react with Babel)
│   └── Want fastest transforms? → react-swc-ts (uses @vitejs/plugin-react-swc)
├── Vue app?                    → vue-ts (uses @vitejs/plugin-vue)
├── Svelte app?                 → svelte-ts
├── Solid app?                  → solid-ts
├── Preact app?                 → preact-ts
├── Lit web components?         → lit-ts
├── Qwik app?                   → qwik-ts
└── No framework?               → vanilla-ts
```

**ALWAYS** use the `-ts` variant -- TypeScript variants include proper type definitions and `vite-env.d.ts`.

### Choosing Build Target

```
What browsers must you support?
├── Modern only (Chrome 111+, Safari 16.4+) → Default (baseline-widely-available)
├── Slightly older (ES2020, etc.)           → Set build.target: 'es2020'
├── IE11 / very old browsers                → Add @vitejs/plugin-legacy
└── Server-side / Node.js                   → Set build.target: 'node20'
```

---

## Official Plugins

| Plugin | Purpose | When to Use |
|--------|---------|-------------|
| `@vitejs/plugin-react` | React with Babel | ALWAYS for React unless SWC preferred |
| `@vitejs/plugin-react-swc` | React with SWC | Faster builds, fewer Babel plugin needs |
| `@vitejs/plugin-vue` | Vue 3 SFC support | ALWAYS for Vue projects |
| `@vitejs/plugin-vue-jsx` | Vue JSX/TSX | When using JSX syntax in Vue |
| `@vitejs/plugin-rsc` | React Server Components | RSC architecture |
| `@vitejs/plugin-legacy` | Legacy browser support | When targeting pre-ES2015 browsers |

---

## CLI Commands

| Command | Purpose | Default Port |
|---------|---------|-------------|
| `vite` | Start dev server with HMR | 5173 |
| `vite build` | Bundle for production | N/A |
| `vite preview` | Preview production build locally | 4173 |

Key flags: `--port <number>`, `--open`, `--mode <mode>`, `--force` (re-bundle deps), `--host` (expose to LAN).

### Standard package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

---

## Project Structure

```
my-vite-app/
├── index.html              # Application entry point (NOT in src/)
├── public/                 # Static assets (copied as-is, no processing)
│   └── favicon.ico
├── src/
│   ├── main.ts             # Module entry (referenced from index.html)
│   ├── App.tsx              # Root component (framework-dependent)
│   ├── vite-env.d.ts        # Vite client type declarations
│   └── assets/              # Processed assets (images, fonts, etc.)
├── vite.config.ts           # Vite configuration
├── tsconfig.json            # TypeScript configuration
├── package.json             # Dependencies and scripts
└── node_modules/
    └── .vite/               # Pre-bundling cache (auto-generated)
```

**ALWAYS** place `index.html` at the project root (not inside `src/`) -- Vite expects it at the `root` directory.

---

## Reference Links

- [references/internals.md](references/internals.md) -- Version evolution details, module graph internals, build pipeline specifics
- [references/examples.md](references/examples.md) -- Minimal project setup, CLI commands, package.json scripts
- [references/anti-patterns.md](references/anti-patterns.md) -- Common architecture mistakes with explanations

### Official Sources

- https://vite.dev/guide/
- https://vite.dev/config/
- https://vite.dev/guide/dep-pre-bundling
- https://vite.dev/guide/cli
- https://vite.dev/plugins/
