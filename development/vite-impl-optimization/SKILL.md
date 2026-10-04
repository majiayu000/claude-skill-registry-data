---
name: vite-impl-optimization
description: >
  Use when configuring dependency pre-bundling, troubleshooting slow dev server starts,
  handling monorepo dependencies, or forcing cache invalidation.
  Prevents stale cache issues and missing optimizeDeps.include for dynamically imported dependencies.
  Covers pre-bundling (CJS-to-ESM conversion), optimizeDeps.include/exclude/force, automatic
  discovery, monorepo linked deps, caching (node_modules/.vite), and Rolldown vs esbuild.
  Keywords: optimizeDeps, pre-bundling, node_modules/.vite, cache invalidation, monorepo, esbuild, Rolldown.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-impl-optimization

## Quick Reference

### Why Pre-Bundling Exists

Vite pre-bundles dependencies on first dev server start for two reasons:

| Reason | Problem | Solution |
|--------|---------|----------|
| CJS/UMD to ESM conversion | Dev server serves native ESM only; most npm packages ship CJS/UMD | Pre-bundler converts to ESM with smart import analysis |
| HTTP request reduction | ESM deps with many internal modules cause hundreds of requests (e.g., lodash-es = 600+ modules) | Pre-bundler collapses into a single module |

**CRITICAL**: Pre-bundling applies ONLY in development mode. Production builds use Rolldown (v8) or Rollup (v5-v7) natively.

### Pre-Bundling Tool by Version

| Vite Version | Pre-Bundling Tool | Bundler Options Key |
|-------------|-------------------|---------------------|
| v5, v6, v7 | esbuild | `optimizeDeps.esbuildOptions` |
| v8+ | Rolldown | `optimizeDeps.rolldownOptions` |

### Critical Warnings

**NEVER** exclude CJS dependencies from pre-bundling -- they MUST be converted to ESM. Excluding a CJS dep causes runtime errors in the browser.

**NEVER** set `optimizeDeps.noDiscovery: true` without explicitly listing ALL dependencies in `include` -- the dev server will fail to resolve unlisted bare imports.

**ALWAYS** add linked monorepo packages to `optimizeDeps.include` if they do NOT export ESM -- Vite skips pre-bundling for linked deps by default.

**ALWAYS** use `--force` flag after modifying files inside `node_modules` -- the cache will serve stale pre-bundled code otherwise.

---

## How Automatic Discovery Works

1. Vite crawls source code starting from HTML entry points (or `optimizeDeps.entries`)
2. Every bare import (e.g., `import X from 'package-name'`) is identified
3. Discovered dependencies are pre-bundled into `node_modules/.vite`
4. If a NEW dependency import appears after initial crawl, Vite re-runs pre-bundling and reloads the page

### When Discovery Fails

Automatic discovery misses dependencies when:
- Imports come from plugin-transformed code (not in original source)
- Dependencies are dynamically imported with variable paths
- Imports exist only in files not reachable from entry points

**FIX**: Add missed dependencies to `optimizeDeps.include` explicitly.

---

## Decision Tree: optimizeDeps.include vs exclude

```
Is the dependency from node_modules?
├── YES: Is it CommonJS or UMD?
│   ├── YES → NEVER exclude. Let pre-bundling convert it.
│   │         Add to include if auto-discovery misses it.
│   └── NO (pure ESM): Does it have many internal modules?
│       ├── YES (e.g., lodash-es) → Add to include for performance
│       └── NO (few modules) → Can exclude safely
└── NO (linked/monorepo package):
    ├── Exports ESM? → Vite treats as source code (no pre-bundling needed)
    └── Does NOT export ESM? → MUST add to optimizeDeps.include
```

---

## Decision Tree: Monorepo Linked Dependencies

```
Is the package linked (symlinked from workspace)?
├── YES: Vite auto-detects linked packages
│   ├── Does the package export valid ESM?
│   │   ├── YES → No action needed. Vite analyzes its dependency list instead.
│   │   └── NO → Add to optimizeDeps.include
│   ├── Did you change the linked dep's code?
│   │   └── Restart dev server with --force flag
│   └── Does the linked dep have deep imports?
│       └── Use glob pattern: include: ['my-lib/components/**/*.vue']
└── NO → Standard node_modules dependency (auto-handled)
```

---

## Cache Invalidation Triggers

Vite automatically re-bundles dependencies when ANY of these change:

| Trigger | What Vite Checks |
|---------|-----------------|
| Package manager lockfile | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb` |
| Patches folder | Modification time of `patches/` directory |
| `vite.config.js` | Relevant config fields (optimizeDeps, resolve, plugins) |
| `NODE_ENV` value | Environment variable change between runs |

### Browser Cache Behavior

Pre-bundled dependencies are served with aggressive cache headers:

```
Cache-Control: max-age=31536000,immutable
```

Vite appends a version query string (e.g., `?v=abc123`) to invalidate browser cache when dependencies change. The browser NEVER re-requests cached deps unless the version query changes.

### Force Cache Reset

| Method | Command |
|--------|---------|
| CLI flag | `vite --force` or `vite dev --force` |
| Config option | `optimizeDeps.force: true` |
| Manual delete | Remove `node_modules/.vite` directory |

---

## Debugging Dependency Issues

### Symptom: Dev Server Slow to Start

1. Check if many dependencies lack pre-bundling → add large ESM deps to `include`
2. Check if `optimizeDeps.holdUntilCrawlEnd` is `false` → set to `true` (default) to batch discovery
3. Check if repeated re-bundling occurs → look for dynamic imports triggering new discoveries

### Symptom: Module Not Found or CJS Errors in Browser

1. Verify the dependency is NOT in `optimizeDeps.exclude`
2. If CJS dep → MUST be pre-bundled, remove from exclude
3. If linked dep → add to `optimizeDeps.include`
4. Run `vite --force` to clear stale cache

### Symptom: Stale Code After Editing node_modules

1. Stop dev server
2. Delete `node_modules/.vite`
3. Disable browser cache in DevTools Network tab
4. Restart with `vite --force`
5. Hard-reload the page

### Symptom: Interop Issues with CJS Default Exports

Use `optimizeDeps.needsInterop` (experimental) to force ESM interop for specific packages:

```javascript
export default defineConfig({
  optimizeDeps: {
    needsInterop: ['cjs-package-with-broken-default'],
  },
})
```

---

## Common Patterns

### Standard SPA with Heavy Dependencies

```javascript
export default defineConfig({
  optimizeDeps: {
    include: [
      'lodash-es',           // 600+ internal modules → collapse to one
      'rxjs',                // Many sub-modules
      'chart.js',            // CJS package
    ],
  },
})
```

### Monorepo with Linked Packages

```javascript
export default defineConfig({
  optimizeDeps: {
    include: [
      'shared-utils',                        // Linked CJS package
      'ui-lib/components/**/*.vue',          // Deep imports from linked package
    ],
  },
})
```

### Disable Auto-Discovery (Full Manual Control)

```javascript
export default defineConfig({
  optimizeDeps: {
    noDiscovery: true,
    include: [
      'react',
      'react-dom',
      'my-specific-dep',
    ],
  },
})
```

**WARNING**: With `noDiscovery: true`, you MUST list every dependency. Missing deps cause runtime failures.

### Custom Entry Points for Discovery

```javascript
export default defineConfig({
  optimizeDeps: {
    entries: [
      'src/main.ts',
      'src/workers/*.ts',    // tinyglobby patterns supported
    ],
  },
})
```

---

## Reference Links

- [references/config-options.md](references/config-options.md) -- Complete optimizeDeps.* option reference
- [references/examples.md](references/examples.md) -- Working configuration examples for common scenarios
- [references/anti-patterns.md](references/anti-patterns.md) -- Dependency optimization mistakes and fixes

### Official Sources

- https://vite.dev/guide/dep-pre-bundling
- https://vite.dev/config/dep-optimization-options
- https://v6.vite.dev/guide/dep-pre-bundling
- https://v6.vite.dev/config/dep-optimization-options
