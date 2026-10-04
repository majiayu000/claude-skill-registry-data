---
name: vite-syntax-build
description: >
  Use when configuring production builds, optimizing output, setting build targets,
  or configuring chunk splitting.
  Prevents using wrong bundler config key for the target Vite version (rollupOptions
  vs rolldownOptions) and misconfiguring minifier or sourcemap settings.
  Covers build.target, build.outDir, build.assetsDir, build.assetsInlineLimit,
  build.cssCodeSplit, build.cssTarget, build.cssMinify, build.sourcemap,
  build.rolldownOptions (v8)/build.rollupOptions (v6-v7), build.lib, build.manifest,
  build.ssr, build.minify (oxc/terser/esbuild), build.emptyOutDir, and build.watch.
  Keywords: vite, build, rollup, rolldown, minify, sourcemap, chunk splitting, build target.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-syntax-build

## Quick Reference

### Build Tool Chain Per Version

| Version | Production Bundler | Minifier (client) | Minifier (SSR) | CSS Minifier | Config Key |
|---------|-------------------|--------------------|----------------|--------------|------------|
| Vite 6  | Rollup            | esbuild            | false          | esbuild      | `build.rollupOptions` |
| Vite 7  | Rollup            | esbuild            | false          | esbuild/lightningcss | `build.rollupOptions` |
| Vite 8+ | **Rolldown**      | **oxc**            | false          | **Lightning CSS** | `build.rolldownOptions` |

### Essential Build Options

| Option | Type | Default | Version Notes |
|--------|------|---------|---------------|
| `build.target` | `string \| string[]` | `'baseline-widely-available'` | v7+ default; v6 used `'modules'` |
| `build.outDir` | `string` | `'dist'` | All versions |
| `build.assetsDir` | `string` | `'assets'` | Not used in Library Mode |
| `build.assetsInlineLimit` | `number \| function` | `4096` (4 KiB) | Function form available in all versions |
| `build.cssCodeSplit` | `boolean` | `true` | All versions |
| `build.cssTarget` | `string \| string[]` | Same as `build.target` | All versions |
| `build.cssMinify` | `boolean \| 'lightningcss' \| 'esbuild'` | Same as `build.minify` | v8 defaults to Lightning CSS |
| `build.sourcemap` | `boolean \| 'inline' \| 'hidden'` | `false` | All versions |
| `build.minify` | `boolean \| 'oxc' \| 'terser' \| 'esbuild'` | `'oxc'` (v8+), `'esbuild'` (v6-v7) | See minifier table |
| `build.write` | `boolean` | `true` | All versions |
| `build.emptyOutDir` | `boolean` | `true` if outDir inside root | All versions |
| `build.copyPublicDir` | `boolean` | `true` | All versions |
| `build.reportCompressedSize` | `boolean` | `true` | Disable for large projects |
| `build.chunkSizeWarningLimit` | `number` | `500` (KiB, uncompressed) | All versions |
| `build.watch` | `WatcherOptions \| null` | `null` | Set `{}` to enable |
| `build.manifest` | `boolean \| string` | `false` | Generates `.vite/manifest.json` |
| `build.ssrManifest` | `boolean \| string` | `false` | Generates `.vite/ssr-manifest.json` |
| `build.ssr` | `boolean \| string` | `false` | All versions |
| `build.license` | `boolean \| { fileName? }` | `false` | **v8+ only** |

### Bundler Options Per Version

| Version | Option | Type | Notes |
|---------|--------|------|-------|
| v6-v7 | `build.rollupOptions` | `RollupOptions` | Standard Rollup config |
| v8+ | `build.rolldownOptions` | `RolldownOptions` | **Replaces** rollupOptions |
| v8+ | `build.rollupOptions` | `RolldownOptions` | **Deprecated** alias for rolldownOptions |

### Library Mode Options

| Option | Type | Description |
|--------|------|-------------|
| `build.lib.entry` | `string \| string[] \| Record<string, string>` | Entry point(s) — REQUIRED |
| `build.lib.name` | `string` | Global variable name for UMD/IIFE |
| `build.lib.formats` | `string[]` | `['es', 'umd']` single entry; `['es', 'cjs']` multi-entry |
| `build.lib.fileName` | `string \| ((format, entryName) => string)` | Output filename (auto-adds extension) |
| `build.lib.cssFileName` | `string` | Custom CSS output filename |

### Module Preload

| Option | Type | Default |
|--------|------|---------|
| `build.modulePreload` | `boolean \| object` | `{ polyfill: true }` |
| `build.modulePreload.polyfill` | `boolean` | `true` |
| `build.modulePreload.resolveDependencies` | `Function` | — |

### Critical Warnings

**NEVER** use `build.rollupOptions` in Vite 8+ projects — it is deprecated. ALWAYS use `build.rolldownOptions` instead. Using the old key may work as an alias but will be removed in future versions.

**NEVER** set `build.minify: 'esbuild'` in Vite 8+ — esbuild is no longer a direct dependency. If you need esbuild minification, install it manually first. ALWAYS use `'oxc'` (default) or `'terser'` in v8+.

**NEVER** set `build.emptyOutDir: true` when `outDir` is outside your project root without understanding the risk — Vite warns and skips this by default to prevent accidental deletion of important files.

**NEVER** rely on `build.assetsDir` in Library Mode — it is ignored. Library output filenames are controlled by `build.lib.fileName` and `build.lib.cssFileName`.

**NEVER** forget to externalize peer dependencies in Library Mode — bundling frameworks like React or Vue into your library creates duplicate instances and breaks consumer applications. ALWAYS set them in `rolldownOptions.external` (v8+) or `rollupOptions.external` (v6-v7).

**ALWAYS** set `build.sourcemap: true` or `'hidden'` for production debugging — without sourcemaps, production error traces are unreadable. Use `'hidden'` to generate maps without exposing them to browsers.

**ALWAYS** handle `vite:preloadError` events in production SPAs — after deployments, cached pages may reference stale chunks that no longer exist.

---

## Decision Tree: Choosing Minifier

```
Is your project on Vite 8+?
├─ YES → Use default 'oxc' (30-90x faster than terser)
│        Need maximum compression? → Use 'terser' (install terser package)
│        Need esbuild? → Install esbuild manually, then set 'esbuild'
└─ NO (v6-v7) → Use default 'esbuild'
                 Need maximum compression? → Use 'terser' (install terser package)
```

## Decision Tree: Bundler Options Key

```
Which Vite version?
├─ v8+ → ALWAYS use build.rolldownOptions
├─ v7  → ALWAYS use build.rollupOptions
└─ v6  → ALWAYS use build.rollupOptions
```

## Decision Tree: build.target

```
Which Vite version?
├─ v8+ → Default: 'baseline-widely-available' (Chrome 111+, Edge 111+, Firefox 114+, Safari 16.4+)
├─ v7  → Default: 'baseline-widely-available' (Chrome 107+, Edge 107+, Firefox 104+, Safari 16.0+)
└─ v6  → Default: 'modules' (native ESM support)

Need older browsers?
├─ YES → Use @vitejs/plugin-legacy (adds polyfills + syntax transforms)
└─ NO  → Use 'esnext' for minimal transpiling, or keep default
```

## Decision Tree: Sourcemap Strategy

```
What environment?
├─ Development → Sourcemaps automatic (no config needed)
├─ Production (internal tools) → build.sourcemap: true
├─ Production (public-facing) → build.sourcemap: 'hidden'
│  (maps generated for error tracking services, not exposed to browsers)
└─ Production (no debugging) → build.sourcemap: false (default)
```

---

## Patterns

### Standard Production Build

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    target: 'baseline-widely-available',
    outDir: 'dist',
    sourcemap: 'hidden',
    minify: 'oxc',          // v8+ default; use 'esbuild' for v6-v7
    cssCodeSplit: true,
    chunkSizeWarningLimit: 500,
  },
})
```

### Multi-Page Application

```typescript
// vite.config.ts
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rolldownOptions: {       // v8+; use rollupOptions for v6-v7
      input: {
        main: resolve(import.meta.dirname, 'index.html'),
        about: resolve(import.meta.dirname, 'about/index.html'),
        dashboard: resolve(import.meta.dirname, 'dashboard/index.html'),
      },
    },
  },
})
```

### Library Mode

```typescript
// vite.config.ts
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    lib: {
      entry: resolve(import.meta.dirname, 'lib/main.ts'),
      name: 'MyLib',
      fileName: 'my-lib',
    },
    rolldownOptions: {       // v8+; use rollupOptions for v6-v7
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
  },
})
```

### Watch Mode

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    watch: {},               // Enable rebuild on file changes
  },
})
```

Or via CLI: `vite build --watch`

### Handling Preload Errors

```typescript
// main.ts — ALWAYS add this for production SPAs
window.addEventListener('vite:preloadError', (event) => {
  event.preventDefault()
  window.location.reload()   // Reload to fetch fresh assets
})
```

### Backend Integration with Manifest

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    manifest: true,
    rolldownOptions: {       // v8+; use rollupOptions for v6-v7
      input: '/path/to/main.ts',
    },
  },
})
```

---

## Build Optimizations

### CSS Code Splitting

Vite ALWAYS extracts CSS from async chunks into separate files by default. The CSS file loads automatically via `<link>` before the chunk executes, preventing FOUC (Flash of Unstyled Content).

Disable with `build.cssCodeSplit: false` to bundle ALL CSS into a single file.

### Preload Directives

Vite ALWAYS generates `<link rel="modulepreload">` directives for entry chunks and their direct imports in built HTML output. This instructs browsers to prefetch required modules.

### Async Chunk Loading

When async chunk A imports common chunk C, Vite rewrites the import to fetch A and C in parallel. This eliminates sequential round-trips regardless of import depth.

---

## Reference Links

- [references/config-options.md](references/config-options.md) — ALL build.* options with types, defaults, and version annotations
- [references/examples.md](references/examples.md) — Production build, multi-page, library mode, watch mode examples
- [references/anti-patterns.md](references/anti-patterns.md) — Build configuration mistakes and corrections

### Official Sources

- https://vite.dev/config/build-options
- https://vite.dev/guide/build
- https://vite.dev/guide/static-deploy
- https://v6.vite.dev/config/build-options (Vite 6 reference)
