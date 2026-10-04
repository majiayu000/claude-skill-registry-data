---
name: vite-impl-migration
description: >
  Use when upgrading Vite versions, encountering deprecated APIs, or resolving
  version-specific breaking changes.
  Prevents using removed APIs after migration (e.g., rollupOptions in v8,
  legacy Sass API in v7, esbuild transforms in v8).
  Covers v5-to-v6 breaking changes (Environment API, json.stringify, PostCSS),
  v6-to-v7 (Node.js 20+, build.target), and v7-to-v8 (Rolldown, Oxc,
  Lightning CSS, rolldownOptions, moduleType).
  Keywords: migration, upgrade, breaking changes, Rolldown, Oxc, Lightning CSS,
  deprecated API, version compatibility.
license: MIT
compatibility: "Designed for Claude Code. Covers migration paths from Vite 5 through Vite 8."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-impl-migration

## Quick Reference

### Version Requirements

| Version | Node.js Requirement | Production Bundler | Dev Transform | CSS Minifier |
|---------|--------------------|--------------------|---------------|--------------|
| Vite 5  | 18+                | Rollup             | esbuild       | esbuild      |
| Vite 6  | 18+                | Rollup             | esbuild       | esbuild / Lightning CSS |
| Vite 7  | 20.19+ / 22.12+    | Rollup             | esbuild       | esbuild / Lightning CSS |
| Vite 8  | 20.19+ / 22.12+    | **Rolldown**       | **Oxc**       | **Lightning CSS** |

### build.target Defaults Per Version

| Version | Default build.target |
|---------|---------------------|
| Vite 5  | `'modules'` (es2020) |
| Vite 6  | `'modules'` (es2020) |
| Vite 7  | `'baseline-widely-available'` (`chrome107, edge107, firefox104, safari16.0`) |
| Vite 8  | `'baseline-widely-available'` (`chrome111, edge111, firefox114, safari16.4`) |

### Critical Warnings

**NEVER** upgrade Vite major versions without checking Node.js compatibility first. Vite 7+ drops Node.js 18 support entirely.

**NEVER** use `build.rollupOptions` in Vite 8 -- it is deprecated and mapped internally. ALWAYS use `build.rolldownOptions` instead.

**NEVER** use `esbuild` config in Vite 8 for new projects -- it is deprecated and converted to `oxc` internally. ALWAYS use the `oxc` config option.

**NEVER** use `api: 'legacy'` for Sass in Vite 7+ -- the legacy Sass API is completely removed. ALWAYS use the modern Sass API.

**NEVER** use the object form of `output.manualChunks` in Vite 8 -- it has been removed. ALWAYS use the function form.

**ALWAYS** add `moduleType: 'js'` in plugin `load`/`transform` hooks when returning non-JS content in Vite 8. Omitting this causes silent failures.

**ALWAYS** handle `BundleError` when using the `build()` API in Vite 8. Raw errors are no longer thrown.

---

## Decision Tree: Which Migration Path?

```
Upgrading Vite?
├── From v5 → v6?
│   ├── Using Sass? → Switch to modern API (api: 'modern-compiler')
│   ├── Using PostCSS TS config with ts-node? → Switch to tsx or jiti
│   ├── Using json.stringify: true/false? → Review: default is now 'auto'
│   └── Using resolve.conditions? → Review new defaults
│
├── From v6 → v7?
│   ├── On Node.js 18? → MUST upgrade to Node.js 20.19+ or 22.12+
│   ├── Using splitVendorChunkPlugin? → Remove it, use manual chunking
│   ├── Using Sass legacy API? → MUST migrate to modern API
│   └── Using hook-level enforce on transformIndexHtml? → Move to plugin-level
│
├── From v7 → v8?
│   ├── Using build.rollupOptions? → Rename to build.rolldownOptions
│   ├── Using esbuild config? → Rename to oxc config
│   ├── Writing plugins with load/transform? → Add moduleType: 'js'
│   ├── Using object manualChunks? → Convert to function form
│   ├── Using import.meta.url in UMD/IIFE? → Find alternative
│   └── Catching build() errors? → Handle BundleError type
│
└── Multi-version jump (v5 → v8)?
    → Apply changes sequentially: v5→v6, v6→v7, v7→v8
```

---

## Migration Path: Vite 5 to 6

### 1. Environment API (Internal Refactoring)

The Environment API restructures Vite internals. Most user-facing code is unaffected, but plugin authors MUST review their hooks.

### 2. Vite Runtime API Replaced by Module Runner

```javascript
// BEFORE (v5): Vite Runtime API
import { createViteRuntime } from 'vite'

// AFTER (v6): Module Runner API
import { createServerModuleRunner } from 'vite'
```

### 3. resolve.conditions Defaults Changed

Vite 6 explicitly defines `resolve.conditions` defaults. If you relied on implicit conditions, verify your package resolution still works.

### 4. json.stringify Default Changed to 'auto'

```javascript
// BEFORE (v5): json.stringify default was false
// AFTER (v6): json.stringify default is 'auto' (stringifies files >10kB)

// To restore v5 behavior:
export default defineConfig({
  json: { stringify: false },
})
```

### 5. PostCSS Config Loader Updated

PostCSS config loading now uses `postcss-load-config` v6. TypeScript PostCSS configs MUST use `tsx` or `jiti` instead of `ts-node`.

### 6. Sass Modern API Default

```javascript
// BEFORE (v5): Legacy API was default
// AFTER (v6): Modern API is default

// To temporarily use legacy (ONLY in v6, removed in v7):
export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: { api: 'legacy' },
    },
  },
})
```

### 7. Library CSS Filename Change

Library mode CSS filename now uses the `name` field from `package.json` instead of generic `style.css`.

### 8. build.cssMinify Enabled for SSR

CSS minification is now enabled by default for SSR builds.

### 9. CommonJS strictRequires Default Changed

`strictRequires` now defaults to `true` (was `'auto'`). This may affect CJS dependency resolution.

See [references/breaking-changes.md](references/breaking-changes.md) for complete details.

---

## Migration Path: Vite 6 to 7

### 1. Node.js 20.19+ or 22.12+ Required

**ALWAYS** verify your Node.js version before upgrading. Node.js 18 is no longer supported.

```bash
node --version  # MUST be >= 20.19.0 or >= 22.12.0
```

### 2. build.target Updated

Default target changed to `'baseline-widely-available'` (Chrome 107, Edge 107, Firefox 104, Safari 16.0).

### 3. Sass Legacy API Removed

The `api: 'legacy'` option for Sass no longer works. ALWAYS use the modern Sass API.

### 4. splitVendorChunkPlugin Removed

```javascript
// BEFORE (v6): Built-in plugin
import { splitVendorChunkPlugin } from 'vite'
export default defineConfig({
  plugins: [splitVendorChunkPlugin()],
})

// AFTER (v7): Use manual chunking
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) return 'vendor'
        },
      },
    },
  },
})
```

### 5. transformIndexHtml Hook Changes

Hook-level `enforce` and `transform` properties for `transformIndexHtml` are removed. Use plugin-level `enforce` instead.

### 6. optimizeDeps.entries Receives Globs

`optimizeDeps.entries` ALWAYS receives glob patterns, not literal file paths.

See [references/breaking-changes.md](references/breaking-changes.md) for complete details.

---

## Migration Path: Vite 7 to 8

### 1. Rolldown Replaces Rollup

```javascript
// BEFORE (v7):
export default defineConfig({
  build: {
    rollupOptions: { /* ... */ },
  },
})

// AFTER (v8):
export default defineConfig({
  build: {
    rolldownOptions: { /* ... */ },
  },
})
```

### 2. Oxc Replaces esbuild

```javascript
// BEFORE (v7):
export default defineConfig({
  esbuild: {
    jsxFactory: 'h',
    jsxFragment: 'Fragment',
  },
})

// AFTER (v8):
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

### 3. Lightning CSS Default Minifier

Lightning CSS is now the default CSS minifier. No configuration needed.

### 4. Oxc Minifier Default (30-90x Faster Than Terser)

`build.minify` defaults to `'oxc'` for client builds. Terser is still available if explicitly configured.

### 5. Plugin Authors: moduleType Required

```javascript
// BEFORE (v7): Return string directly
transform(code, id) {
  return { code: transformedCode }
}

// AFTER (v8): MUST specify moduleType for non-JS content
transform(code, id) {
  return { code: transformedCode, moduleType: 'js' }
}
```

### 6. build() API Throws BundleError

```javascript
// BEFORE (v7):
try {
  await build()
} catch (e) {
  console.error(e.message)
}

// AFTER (v8):
try {
  await build()
} catch (e) {
  if (e.errors) {
    for (const error of e.errors) {
      console.log(error.code)
    }
  }
}
```

### 7. Object manualChunks Removed

```javascript
// BEFORE (v7): Object form allowed
manualChunks: { vendor: ['react', 'react-dom'] }

// AFTER (v8): MUST use function form
manualChunks(id) {
  if (id.includes('react')) return 'vendor'
}
```

### 8. import.meta.url Not Polyfilled in UMD/IIFE

If your library build uses UMD/IIFE format and references `import.meta.url`, you MUST find an alternative approach.

### 9. esbuild Is Now Optional

esbuild is no longer a direct dependency. If your plugins require esbuild, ALWAYS install it explicitly:

```bash
npm install -D esbuild
```

See [references/breaking-changes.md](references/breaking-changes.md) for complete details.

---

## Migration Checklist

### Pre-Upgrade

- [ ] Check current Node.js version against target Vite version requirements
- [ ] Review `vite.config.ts` for deprecated options
- [ ] Check all plugins for version compatibility
- [ ] Run `npm outdated` to identify plugin updates needed
- [ ] Read the official migration guide for your target version

### Post-Upgrade

- [ ] Run `vite build` and verify no deprecation warnings
- [ ] Test dev server (`vite`) for HMR and proxy behavior
- [ ] Verify CSS output matches expectations
- [ ] Test SSR build if applicable
- [ ] Run full test suite
- [ ] Check bundle size for unexpected changes

---

## Reference Links

- [references/breaking-changes.md](references/breaking-changes.md) -- Complete breaking changes lists per version
- [references/examples.md](references/examples.md) -- Config migration before/after examples
- [references/anti-patterns.md](references/anti-patterns.md) -- Common migration mistakes

### Official Sources

- https://vite.dev/guide/migration
- https://v6.vite.dev/guide/migration
- https://v7.vite.dev/guide/migration
- https://vite.dev/changes/
