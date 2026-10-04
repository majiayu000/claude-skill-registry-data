---
name: vite-errors-dependency
description: >
  Use when encountering pre-bundling errors, dependency resolution failures,
  stale cache issues, or slow development server startup.
  Prevents excluding CJS dependencies from pre-bundling (which breaks runtime
  module resolution) and misconfiguring optimizeDeps.
  Covers CJS/ESM conversion failures, missing dependency auto-discovery,
  optimizeDeps configuration, monorepo linked dependencies, cache invalidation,
  browser cache staleness, and large dependency tree performance.
  Keywords: pre-bundling, optimizeDeps, CJS, ESM, cache, dependency resolution,
  monorepo, node_modules/.vite.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-errors-dependency

## Quick Reference

### Pre-Bundling Overview

Vite pre-bundles dependencies in dev mode ONLY. It converts CJS/UMD packages to ESM and collapses large dependency trees into single modules. The cache lives at `node_modules/.vite`.

| Version | Pre-Bundling Engine | Config Key for Engine Options |
|---------|--------------------|-----------------------------|
| Vite 5  | esbuild            | `optimizeDeps.esbuildOptions` |
| Vite 6–7 | esbuild          | `optimizeDeps.esbuildOptions` |
| Vite 8  | Rolldown           | `optimizeDeps.rolldownOptions` |

**NEVER** assume pre-bundling affects production builds. Production uses Rollup (v5–v7) or Rolldown (v8) natively with `@rollup/plugin-commonjs` or built-in CJS support.

### Critical Warnings

**NEVER** exclude a CJS dependency from pre-bundling via `optimizeDeps.exclude`. The browser cannot load CommonJS modules natively. Excluding a CJS package breaks module resolution at runtime.

**NEVER** edit files inside `node_modules/` without also clearing the Vite cache (`node_modules/.vite`) and using `--force`. The browser aggressively caches pre-bundled deps with `max-age=31536000,immutable`.

**ALWAYS** add linked monorepo dependencies that do NOT export ESM to `optimizeDeps.include`. Vite skips pre-bundling for linked deps by default, assuming they are ESM source code.

**ALWAYS** restart the dev server with `--force` after modifying linked dependency source code in a monorepo.

---

## Debugging Flowchart

```
Dev server error or unexpected behavior with a dependency?
│
├─ Error: "Failed to resolve import" or "does not provide an export named"
│  ├─ Is the package CJS-only?
│  │  ├─ YES → Is it in optimizeDeps.exclude?
│  │  │  ├─ YES → REMOVE it from exclude. CJS MUST be pre-bundled.
│  │  │  └─ NO  → Add to optimizeDeps.include explicitly.
│  │  └─ NO (ESM) → Check package.json "exports" field for correct conditions.
│  │
│  └─ Is it a monorepo linked dep?
│     ├─ Does it export ESM? → No action needed (Vite treats as source).
│     └─ Does it export CJS? → Add to optimizeDeps.include.
│
├─ Error: "Outdated pre-bundle" or stale module content
│  ├─ Did you manually edit node_modules/?
│  │  ├─ YES → Run: vite --force AND clear browser cache.
│  │  └─ NO  → Delete node_modules/.vite, restart dev server.
│  └─ Check: Did lockfile, vite.config, NODE_ENV, or patches change?
│     └─ YES → Vite should auto-invalidate. If not, run: vite --force.
│
├─ Slow dev server startup (many HTTP requests)
│  ├─ Check Network tab: hundreds of requests to one dependency?
│  │  └─ YES → Add that dependency to optimizeDeps.include.
│  │     Example: lodash-es triggers 600+ module requests without pre-bundling.
│  └─ Check: Are there undiscovered deps from plugin transforms?
│     └─ YES → Add to optimizeDeps.include (auto-discovery misses these).
│
└─ Import works in dev but fails in production (or vice versa)
   └─ Pre-bundling is dev-only. Production uses a different CJS handling path.
      Check build output for CJS interop issues separately.
```

---

## Diagnostic Table: Symptom → Cause → Fix

| Symptom | Cause | Fix |
|---------|-------|-----|
| `does not provide an export named 'X'` from CJS package | CJS module uses `module.exports` — named ESM imports fail | Add package to `optimizeDeps.include`; use `import pkg from 'pkg'` then destructure |
| `Failed to resolve import "X"` for plugin-generated import | Auto-discovery crawls source only — plugin transforms are invisible | Add the dependency to `optimizeDeps.include` explicitly |
| `optimizeDeps.exclude` breaks a CJS package | Excluded CJS is served raw — browser cannot parse `require()` | REMOVE the package from `exclude`. NEVER exclude CJS deps |
| Linked monorepo dep throws ESM errors | Vite treats linked deps as source but the dep exports CJS | Add linked dep to `optimizeDeps.include` |
| Stale module content after editing `node_modules/` | Browser cache holds immutable pre-bundled version | Run `vite --force`, disable browser cache in DevTools, reload |
| Dev server re-bundles on every start | Config, lockfile, or NODE_ENV changes between starts | Stabilize config; check for CI/env variable differences |
| 600+ HTTP requests on page load for one import | ESM dependency has many internal modules (e.g., `lodash-es`) | Add to `optimizeDeps.include` to collapse into single module |
| `Uncaught TypeError: X is not a function` | ESM interop incorrectly wraps default export | Add package to `optimizeDeps.needsInterop` (experimental) |
| Pre-bundling runs but changes not picked up | `node_modules/.vite` cache is stale | Delete `node_modules/.vite` directory OR run `vite --force` |
| Import works in dev, fails in production | Dev uses pre-bundling (esbuild/Rolldown); prod uses Rollup/Rolldown natively | Check `build.commonjsOptions` or CJS interop settings for production |

---

## Cache Invalidation Triggers

| Trigger | Automatic? | Description |
|---------|-----------|-------------|
| Package manager lockfile change | YES | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb` |
| `vite.config.js` relevant fields change | YES | Changes to `optimizeDeps`, `resolve`, `plugins` |
| `NODE_ENV` value change | YES | Switching between development/production/staging |
| Patches folder modification time | YES | Changes in `patches/` directory (patch-package, pnpm patches) |
| Manual `node_modules/` edits | NO | MUST run `vite --force` and clear browser cache manually |
| New dependency discovered at runtime | YES | Vite re-bundles and reloads the page automatically |
| Linked dep source code changes | NO | MUST restart dev server with `--force` |

---

## Core Configuration Patterns

### Force Pre-Bundling Specific Dependencies

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  optimizeDeps: {
    include: [
      'lodash-es',           // Collapse 600+ internal modules
      'linked-dep',          // Monorepo CJS linked dep
      'my-plugin > dep',     // Dep imported via plugin transform
    ],
  },
})
```

### Force Cache Reset

```bash
# CLI flag (recommended)
vite --force

# Manual deletion
rm -rf node_modules/.vite
```

### Force ESM Interop

```typescript
export default defineConfig({
  optimizeDeps: {
    needsInterop: ['legacy-cjs-package'],  // Experimental
  },
})
```

### Customize Pre-Bundling Engine (Version-Aware)

```typescript
// Vite 5–7: esbuild options
export default defineConfig({
  optimizeDeps: {
    esbuildOptions: {
      target: 'es2020',
      plugins: [/* esbuild plugins */],
    },
  },
})

// Vite 8: Rolldown options
export default defineConfig({
  optimizeDeps: {
    rolldownOptions: {
      plugins: [/* Rolldown plugins */],
    },
  },
})
```

### Disable Auto-Discovery

```typescript
export default defineConfig({
  optimizeDeps: {
    noDiscovery: true,         // Disable crawling
    include: ['react', 'react-dom'],  // Only optimize these
  },
})
```

---

## Browser Cache Debugging

When pre-bundled deps appear stale in the browser:

1. Open DevTools → Network tab
2. Check "Disable cache" checkbox
3. Restart dev server with `vite --force`
4. Hard reload the page (Ctrl+Shift+R / Cmd+Shift+R)

Pre-bundled deps use HTTP header `max-age=31536000,immutable` with a version query string (`?v=abc123`). The version query changes when Vite re-bundles, but the browser may hold the old version if you bypass normal cache invalidation (e.g., manual `node_modules` edits).

---

## Reference Links

- [references/error-catalog.md](references/error-catalog.md) — Complete error pattern catalog with detailed symptoms, causes, and fixes
- [references/examples.md](references/examples.md) — Real-world error scenarios with step-by-step solutions
- [references/anti-patterns.md](references/anti-patterns.md) — Dependency optimization mistakes to avoid

### Official Sources

- https://vite.dev/guide/dep-pre-bundling
- https://vite.dev/config/dep-optimization-options
- https://v6.vite.dev/guide/dep-pre-bundling
- https://v6.vite.dev/config/dep-optimization-options
