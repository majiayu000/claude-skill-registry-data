---
name: vite-errors-build
description: >
  Use when encountering Vite build failures, chunk size warnings, or
  version-specific build errors.
  Prevents the common mistake of using deprecated rollupOptions in v8 or
  misconfiguring build targets and minifiers.
  Covers Rolldown/Rollup bundling failures, CSS minification errors, sourcemap
  problems, library mode build failures, BundleError handling, and asset
  processing errors.
  Keywords: build error, Rolldown, chunk size, sourcemap, library mode, minify,
  BundleError, rollupOptions, build.target.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-errors-build

## Quick Reference: Build Error Diagnostic Table

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Could not resolve './module'` | Unresolved import path | Check file exists, verify `resolve.alias` config, ensure extensions match `resolve.extensions` |
| `Circular dependency detected` | Modules import each other | Refactor shared logic into a third module; use dynamic `import()` to break the cycle |
| `[vite]: Rollup failed to resolve import` | Bare import not in node_modules | Run `npm install`, verify package name spelling, check `optimizeDeps.include` |
| `Warning: Some chunks are larger than 500 KiB` | Chunk exceeds `build.chunkSizeWarningLimit` | Code-split with dynamic imports, increase limit, or use `build.rolldownOptions.output.manualChunks` |
| `build.target: Unexpected token` | Syntax too modern for target browsers | Lower `build.target` (e.g., `'es2020'`) or add `@vitejs/plugin-legacy` |
| `CSS minification error` (v8) | Lightning CSS cannot parse CSS | Set `build.cssMinify: 'esbuild'` as fallback; fix invalid CSS syntax |
| `Sourcemap is likely to be incorrect` | Plugin transforms without sourcemap | Set `build.sourcemap: false` or fix plugin to emit sourcemaps |
| `Missing "name" option for UMD export` | Library mode UMD without `name` | Add `build.lib.name: 'MyLib'` for UMD/IIFE formats |
| `build.rollupOptions is deprecated` (v8) | Using Rollup config key in v8 | Rename to `build.rolldownOptions` |
| `BundleError` thrown (v8) | Build API throws structured error | Catch with `e.errors` array iteration (see v8 Error Handling) |
| `terser not found` | Terser not installed | Run `npm install -D terser`; or switch to `build.minify: 'oxc'` (v8 default) |
| `esbuild not found` (v8) | esbuild no longer bundled in v8 | Run `npm install -D esbuild`; or migrate to `oxc` config |
| `Could not load content for ...` (sourcemap) | Sourcemap references missing source | Set `build.sourcemap: 'hidden'` or ensure sources exist |
| `vite:preloadError` in browser | Dynamic import chunk missing after deploy | Listen for `vite:preloadError` event, trigger page reload |
| `emptyOutDir: outDir is not inside root` | Safety check prevents deletion | Pass `build.emptyOutDir: true` explicitly to override |
| `assetsDir is ignored in lib mode` | Library mode ignores `build.assetsDir` | ALWAYS use flat output or `build.rolldownOptions.output.assetFileNames` in lib mode |
| `moduleType not set` (v8 plugin) | Plugin transforms non-JS without declaring type | Add `moduleType: 'js'` in plugin load/transform hook return |

---

## Critical Warnings

**NEVER** ignore chunk size warnings in production -- they indicate bundles that degrade page load performance. ALWAYS code-split large vendor dependencies with dynamic imports.

**NEVER** set `build.sourcemap: true` in production without understanding the security implications -- sourcemaps expose original source code. Use `'hidden'` to generate maps without embedding references.

**NEVER** use `build.rollupOptions` in Vite 8 -- it is deprecated and will be removed. ALWAYS use `build.rolldownOptions` instead.

**ALWAYS** install terser separately when using `build.minify: 'terser'` -- Vite does NOT bundle terser. In v8, esbuild is also not bundled.

**ALWAYS** handle `vite:preloadError` in SPAs to gracefully recover from stale chunk references after deployment.

---

## Decision Tree: Build Failure Diagnosis

```
Build fails?
  |
  +-- Error message contains "resolve"?
  |     +-- Bare import? --> Check node_modules, run npm install
  |     +-- Relative import? --> Verify file path, check resolve.alias
  |     +-- TypeScript path? --> Enable resolve.tsconfigPaths or add alias
  |
  +-- Error message contains "chunk" or "size"?
  |     +-- Warning only? --> Split code or raise build.chunkSizeWarningLimit
  |     +-- Build fails? --> Check build.rolldownOptions.output config
  |
  +-- Error message contains "CSS"?
  |     +-- Lightning CSS error (v8)? --> Fallback to build.cssMinify: 'esbuild'
  |     +-- Preprocessor error? --> Check sass/less/stylus installed
  |     +-- PostCSS error? --> Verify postcss config, check plugin versions
  |
  +-- Error message contains "minify"?
  |     +-- terser not found? --> npm install -D terser
  |     +-- esbuild not found (v8)? --> npm install -D esbuild or use oxc
  |     +-- oxc error? --> Check oxc config syntax, report upstream if bug
  |
  +-- Error message contains "target"?
  |     +-- Syntax error in output? --> Lower build.target
  |     +-- CSS feature unsupported? --> Set build.cssTarget separately
  |
  +-- Library mode error?
  |     +-- Missing name? --> Add build.lib.name for UMD/IIFE
  |     +-- Missing externals? --> Add to build.rolldownOptions.external
  |     +-- CSS filename? --> Use build.lib.cssFileName
  |
  +-- v8 migration error?
        +-- rollupOptions? --> Rename to rolldownOptions
        +-- esbuild config? --> Rename to oxc config
        +-- moduleType error? --> Add moduleType: 'js' in plugin
        +-- BundleError? --> Catch e.errors array
```

---

## v8 BundleError Handling

Vite 8 throws a `BundleError` from the `build()` API instead of raw errors. ALWAYS use structured error handling:

```typescript
import { build } from 'vite'

try {
  await build()
} catch (e) {
  if (e.errors) {
    // BundleError: iterate structured error array
    for (const error of e.errors) {
      console.error(`[${error.code}] ${error.message}`)
      if (error.frame) console.error(error.frame)
      if (error.loc) {
        console.error(`  at ${error.loc.file}:${error.loc.line}:${error.loc.column}`)
      }
    }
  } else {
    // Fallback for non-BundleError
    throw e
  }
}
```

---

## Chunk Size Optimization

Default warning limit: **500 KiB** (uncompressed). To fix large chunks:

```typescript
// Option 1: Dynamic imports for route-level code splitting
const AdminPanel = () => import('./views/AdminPanel.vue')

// Option 2: Manual chunk splitting (v8 with Rolldown)
export default defineConfig({
  build: {
    rolldownOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('lodash')) return 'vendor-lodash'
            if (id.includes('chart.js')) return 'vendor-charts'
            return 'vendor'
          }
        },
      },
    },
  },
})

// Option 3: Raise the limit (last resort)
export default defineConfig({
  build: {
    chunkSizeWarningLimit: 1000, // KiB
  },
})
```

**NEVER** raise `chunkSizeWarningLimit` without first attempting code splitting -- the warning exists to protect user experience.

---

## vite:preloadError Recovery

After deployment, users with cached pages may request chunks that no longer exist. ALWAYS add this handler to SPA entry points:

```typescript
// main.ts -- add BEFORE app initialization
window.addEventListener('vite:preloadError', (event) => {
  event.preventDefault()
  // Reload to fetch updated HTML with new chunk references
  window.location.reload()
})
```

---

## emptyOutDir Safety

Vite refuses to empty `outDir` if it is outside the project root:

```typescript
// outDir outside root triggers safety warning
export default defineConfig({
  build: {
    outDir: '../dist',           // Outside root -- Vite warns and skips
    emptyOutDir: true,           // Explicit override required
  },
})
```

**ALWAYS** set `build.emptyOutDir: true` explicitly when `outDir` is outside root. Vite adds this safety check to prevent accidental deletion of unrelated directories.

---

## Version-Specific Error Patterns

| Error Pattern | Vite 6 | Vite 7 | Vite 8 |
|--------------|--------|--------|--------|
| Bundler config key | `build.rollupOptions` | `build.rollupOptions` | `build.rolldownOptions` |
| Transform config | `esbuild` | `esbuild` | `oxc` |
| Default minifier | `esbuild` | `esbuild` | `oxc` |
| CSS minifier default | `esbuild` | `esbuild` | Lightning CSS |
| `build.target` default | `'modules'` | `'baseline-widely-available'` | `'baseline-widely-available'` |
| Build error type | Raw error | Raw error | `BundleError` |
| Plugin moduleType | Not required | Not required | Required for non-JS |
| Node.js minimum | 18+ | 20.19+ / 22.12+ | 20.19+ / 22.12+ |

---

## Reference Links

- [references/error-catalog.md](references/error-catalog.md) -- Complete build error catalog with symptom, cause, fix for every known pattern
- [references/examples.md](references/examples.md) -- Reproducible error scenarios with step-by-step solutions
- [references/anti-patterns.md](references/anti-patterns.md) -- Build configuration mistakes to avoid

### Official Sources

- https://vite.dev/guide/build
- https://vite.dev/config/build-options
- https://vite.dev/guide/migration
- https://vite.dev/guide/dep-pre-bundling
