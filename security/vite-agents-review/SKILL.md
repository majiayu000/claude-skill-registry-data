---
name: vite-agents-review
description: >
  Use when reviewing Vite configuration, validating a Vite project, checking
  for common mistakes, or auditing Vite code before deployment.
  Prevents shipping insecure envPrefix settings, wrong bundler options for the
  target version, and known anti-patterns.
  Covers config correctness, plugin hook signatures, HMR patterns,
  version-specific API usage, build optimization, environment variable
  security, SSR configuration, and anti-pattern detection.
  Keywords: review, validation, checklist, audit, anti-pattern, envPrefix,
  plugin hooks, security, SSR, build optimization.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-agents-review

## How to Use This Skill

Run every check in order. Mark each item PASS or FAIL. A single FAIL in a critical area (Security, Configuration) blocks deployment. Fix all FAILs before approving code.

---

## 1. Configuration Checks

| # | Check | Expected State | Common Failure |
|---|-------|---------------|----------------|
| C-01 | `defineConfig()` wraps config export | ALWAYS use `defineConfig()` for type safety and IDE support | Raw object export loses autocomplete and type checking |
| C-02 | Bundler options match target version | v8: `build.rolldownOptions` / v6-v7: `build.rollupOptions` | Using `rollupOptions` on v8 triggers deprecation; using `rolldownOptions` on v6 is invalid |
| C-03 | Transform config matches target version | v8: `oxc` option / v6-v7: `esbuild` option | Using `esbuild` on v8 is deprecated; using `oxc` on v6 is invalid |
| C-04 | `envPrefix` is NOT empty string | MUST be `'VITE_'` or a non-empty custom prefix | Setting `envPrefix: ''` exposes ALL environment variables to client code |
| C-05 | `appType` matches usage pattern | `'spa'` for single-page, `'mpa'` for multi-page, `'custom'` for SSR/middleware | Wrong `appType` causes missing HTML middleware or unwanted SPA fallback |
| C-06 | `build.target` is appropriate | Use `'baseline-widely-available'` (v7+/v8) or explicit browser list | Setting `'esnext'` for production breaks older browsers |
| C-07 | `loadEnv()` used in config, NOT `import.meta.env` | ALWAYS use `loadEnv(mode, root, prefix)` inside config files | `import.meta.env` is undefined during config resolution |
| C-08 | Conditional config uses function form | `defineConfig(({ command, mode }) => ({...}))` | Forgetting `command`/`mode` parameters leads to static config for all modes |

---

## 2. Plugin Checks

| # | Check | Expected State | Common Failure |
|---|-------|---------------|----------------|
| P-01 | Plugin is a factory function returning object | ALWAYS export a function, NEVER a plain object | Plain objects prevent configuration via options parameter |
| P-02 | Plugin object has `name` property | ALWAYS include `name` string on plugin object | Missing `name` makes errors/warnings untraceable |
| P-03 | `config` hook returns partial config or mutates | Return object is deep-merged; mutations are applied directly | Returning a full config object overwrites user settings |
| P-04 | `configResolved` stores config for later hooks | Store resolved config in closure variable | Accessing `config` parameter outside the hook lifecycle |
| P-05 | `configureServer` adds middleware correctly | Use `server.middlewares.use()` for pre-middleware; return function for post-middleware | Adding post-middleware directly instead of returning a function |
| P-06 | `transformIndexHtml` uses correct order property | `order: 'pre'` for before HTML processing, `order: 'post'` (default) for after | Using deprecated `enforce` property (removed in v7) |
| P-07 | `handleHotUpdate` returns correct type | Return `ModuleNode[]` to narrow updates, `[]` to skip, or `void` for default | Returning wrong type causes HMR failures |
| P-08 | `enforce` property used correctly | `'pre'` runs before core plugins, `'post'` runs after build plugins | Omitting `enforce` when ordering matters causes transform conflicts |
| P-09 | Virtual modules use correct prefix convention | User-facing: `virtual:` prefix; internal: `\0` prefix on resolved ID | Missing `\0` prefix lets other plugins process the virtual module |
| P-10 | `moduleParsed` hook NOT relied upon in dev | NEVER depend on `moduleParsed` during development | This hook is skipped in dev for performance — code silently fails |
| P-11 | v8: `moduleType: 'js'` set in load/transform for non-JS | ALWAYS set `moduleType: 'js'` when returning non-JS content | Rolldown cannot process content without explicit module type |

---

## 3. HMR Checks

| # | Check | Expected State | Common Failure |
|---|-------|---------------|----------------|
| H-01 | `import.meta.hot` guard wraps ALL HMR code | ALWAYS wrap in `if (import.meta.hot) { ... }` | HMR code ships to production, increasing bundle size |
| H-02 | `accept(` has no space before parenthesis | Write `import.meta.hot.accept(` exactly | Vite static analysis fails with `accept (` — HMR silently breaks |
| H-03 | `hot.data` mutated via properties, NEVER reassigned | `import.meta.hot.data.key = value` | `import.meta.hot.data = { key: value }` silently fails |
| H-04 | `accept()` called BEFORE `invalidate()` | ALWAYS call `accept()` first to establish HMR boundary | Calling `invalidate()` without `accept()` has no effect |
| H-05 | `dispose()` used for cleanup of side effects | Register cleanup in `import.meta.hot.dispose(cb)` | Timers, event listeners, WebSocket connections leak across updates |
| H-06 | `prune()` used for module removal cleanup | Register in `import.meta.hot.prune(cb)` when module may be removed | Resources persist after module is no longer imported |

---

## 4. Environment Variable Checks

| # | Check | Expected State | Common Failure |
|---|-------|---------------|----------------|
| E-01 | Only `VITE_*` vars accessed in client code | ALWAYS prefix client-exposed vars with `VITE_` | Non-prefixed vars are `undefined` in `import.meta.env` |
| E-02 | No secrets in `VITE_*` variables | NEVER put API keys, tokens, or passwords in `VITE_*` vars | Client code exposes all `VITE_*` values in browser source |
| E-03 | TypeScript: `ImportMetaEnv` interface defined | Declare in `src/vite-env.d.ts` with `/// <reference types="vite/client" />` | Missing types cause `import.meta.env.VITE_*` to be `any` |
| E-04 | `loadEnv()` used in config, NOT `import.meta.env` | `const env = loadEnv(mode, process.cwd(), '')` | `import.meta.env` is not available during config resolution |
| E-05 | `.env.local` files added to `.gitignore` | ALWAYS gitignore `.env*.local` files | Local secrets committed to version control |

---

## 5. Build Checks

| # | Check | Expected State | Common Failure |
|---|-------|---------------|----------------|
| B-01 | `build.target` matches deployment environment | Set explicit target or use `'baseline-widely-available'` | Default `'esnext'` (if set) breaks older browsers |
| B-02 | Sourcemaps not accidentally exposed in production | Use `'hidden'` or `false` for production deployments | `build.sourcemap: true` exposes source code via `.map` files |
| B-03 | CSS code splitting enabled | Keep `build.cssCodeSplit: true` (default) | Disabling creates single CSS file, hurting load performance |
| B-04 | Library mode: `name` set for UMD/IIFE builds | ALWAYS provide `build.lib.name` when formats include UMD or IIFE | Missing `name` causes build error for global variable |
| B-05 | Library mode: peer deps externalized | Add framework deps to `rolldownOptions.external` (v8) or `rollupOptions.external` (v6-v7) | Bundling React/Vue into library doubles framework in consumer app |
| B-06 | Library mode: `package.json` exports configured | Set `main`, `module`, and `exports` fields | Consumers cannot resolve the library entry point |
| B-07 | `build.minify` appropriate for target | v8 default: `'oxc'` for client; v6-v7: `'esbuild'`; SSR: `false` | Using Terser without installing it, or minifying SSR output |
| B-08 | Chunk size warnings addressed | Investigate chunks exceeding `build.chunkSizeWarningLimit` (500 KiB) | Ignoring warnings leads to slow page loads |

---

## 6. SSR Checks

| # | Check | Expected State | Common Failure |
|---|-------|---------------|----------------|
| S-01 | Middleware mode sets `appType: 'custom'` | ALWAYS pair `server: { middlewareMode: true }` with `appType: 'custom'` | Default SPA fallback interferes with custom server routing |
| S-02 | `ssr.noExternal` configured for deps needing transforms | Add deps with non-ESM code or Vite-processed imports to `ssr.noExternal` | Untransformed CSS imports or JSX crash Node.js at runtime |
| S-03 | `ssrFixStacktrace` in error handlers | ALWAYS call `vite.ssrFixStacktrace(e)` in SSR catch blocks | Stack traces point to transformed code instead of source files |
| S-04 | `import.meta.env.SSR` used for conditional logic | Use `import.meta.env.SSR` to branch server/client code | Using `typeof window` checks that fail in edge runtimes |
| S-05 | SSR build uses `--ssr` flag | Build with `vite build --ssr src/entry-server.js` | Building SSR entry without `--ssr` flag bundles as client code |
| S-06 | SSR manifest generated for preload hints | Add `--ssrManifest` to client build command | Missing preload directives degrade perceived load performance |

---

## 7. Security Checks

| # | Check | Expected State | Common Failure |
|---|-------|---------------|----------------|
| X-01 | `envPrefix` not set to empty string | NEVER use `envPrefix: ''` | Exposes ALL env vars (including `DB_PASSWORD`, `SECRET_KEY`) to client |
| X-02 | `server.fs.strict` not disabled without reason | Keep `server.fs.strict: true` (default) | Disabling allows dev server to serve any file on the machine |
| X-03 | `server.allowedHosts` configured for non-localhost | Set explicit host list when exposing dev server to network | DNS rebinding attacks can access dev server resources |
| X-04 | No secrets in client-exposed code | NEVER put credentials in `VITE_*` env vars, `define`, or client source | All client code is readable in browser DevTools |
| X-05 | Production sourcemaps restricted | Use `build.sourcemap: 'hidden'` or `false` | Public `.map` files expose full source code |
| X-06 | `server.fs.deny` includes sensitive patterns | Keep defaults: `['.env', '.env.*', '*.{crt,pem}', '**/.git/**']` | Removing deny rules exposes secrets and certificates |

---

## Validation Summary Template

```
## Review Results — [Project Name] — [Date]

### Version: Vite [6.x / 7.x / 8.x]

| Area            | Checks | Pass | Fail | Blocked |
|-----------------|--------|------|------|---------|
| Configuration   | 8      |      |      |         |
| Plugins         | 11     |      |      |         |
| HMR             | 6      |      |      |         |
| Env Variables   | 5      |      |      |         |
| Build           | 8      |      |      |         |
| SSR             | 6      |      |      |         |
| Security        | 6      |      |      |         |
| **TOTAL**       | **50** |      |      |         |

### Critical Failures (blocks deployment):
- [list any Security or Configuration FAILs]

### Non-Critical Failures (fix before merge):
- [list other FAILs]

### Notes:
- [version-specific observations]
```

---

## Reference Links

- [references/checklist.md](references/checklist.md) -- Complete validation checklist with detailed pass/fail criteria
- [references/examples.md](references/examples.md) -- Good code vs bad code examples for every check area
- [references/anti-patterns.md](references/anti-patterns.md) -- Consolidated anti-patterns from all Vite areas

### Official Sources

- https://vite.dev/config/
- https://vite.dev/guide/api-plugin
- https://vite.dev/guide/api-hmr
- https://vite.dev/guide/env-and-mode
- https://vite.dev/guide/ssr
- https://vite.dev/guide/build
