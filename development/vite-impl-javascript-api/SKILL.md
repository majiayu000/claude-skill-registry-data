---
name: vite-impl-javascript-api
description: >
  Use when using Vite programmatically, building custom dev servers, running
  builds from scripts, or accessing Vite utilities.
  Prevents misuse of createServer(), build(), preview() signatures and
  incorrect ViteDevServer interface usage.
  Covers createServer(), build(), preview(), resolveConfig(), mergeConfig(),
  loadConfigFromFile(), loadEnv(), searchForWorkspaceRoot(), transformWithOxc(),
  normalizePath(), createFilter(), and version constants.
  Keywords: JavaScript API, createServer, build, preview, InlineConfig,
  ViteDevServer, moduleGraph, resolveConfig, mergeConfig, loadEnv.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-impl-javascript-api

## Quick Reference

### Core API Functions

| Function | Return Type | Purpose |
|----------|------------|---------|
| `createServer(inlineConfig?)` | `Promise<ViteDevServer>` | Start a programmatic dev server |
| `build(inlineConfig?)` | `Promise<RollupOutput \| RollupOutput[]>` | Run a production build |
| `preview(inlineConfig?)` | `Promise<PreviewServer>` | Start a preview server for built output |
| `resolveConfig(inlineConfig, command, ...)` | `Promise<ResolvedConfig>` | Resolve and merge all config sources |
| `mergeConfig(defaults, overrides, isRoot?)` | `Record<string, any>` | Deep-merge two Vite configs |
| `loadConfigFromFile(configEnv, ...)` | `Promise<{path, config, dependencies} \| null>` | Load config from a file path |
| `loadEnv(mode, envDir, prefixes?)` | `Record<string, string>` | Load `.env` files for a given mode |

### Utility Functions

| Function | Purpose |
|----------|---------|
| `searchForWorkspaceRoot(current, root?)` | Find monorepo workspace root directory |
| `normalizePath(id)` | Convert Windows backslashes to forward slashes |
| `createFilter(include, exclude)` | Create a picomatch-based file filter |
| `transformWithOxc(code, filename, options?, inMap?)` | Transform code with OXC (Vite 8+) |
| `transformWithEsbuild(code, filename, options?, inMap?)` | Transform code with esbuild (DEPRECATED) |
| `preprocessCSS(code, filename, config)` | Preprocess CSS (experimental) |

### Version Constants

| Constant | Description |
|----------|-------------|
| `version` | Current Vite version string |
| `rolldownVersion` | Rolldown version used (Vite 8+) |
| `esbuildVersion` | Backward compatibility only |
| `rollupVersion` | Backward compatibility only |

### Critical Warnings

**NEVER** use `createServer()` and `build()` in the same Node.js process without setting `process.env.NODE_ENV` or the `mode` config option consistently. Inconsistent modes cause unpredictable behavior.

**NEVER** call `mergeConfig()` with `isRoot=true` (the default) when merging nested config subsections like `build` or `server`. ALWAYS pass `isRoot=false` for nested option merging.

**NEVER** use `transformWithEsbuild()` in new projects targeting Vite 8+. ALWAYS use `transformWithOxc()` instead -- `transformWithEsbuild` is deprecated.

**ALWAYS** call `server.close()` in cleanup/shutdown handlers when using `createServer()` programmatically. Failing to close leaks file watchers, HTTP connections, and WebSocket handles.

**ALWAYS** call `server.listen()` after `createServer()` -- the server is NOT listening by default. `createServer()` only creates the server instance.

---

## Decision Tree: Which API Function?

```
Need to run Vite programmatically?
├── Development server → createServer()
│   ├── Custom middleware → server.middlewares.use()
│   ├── SSR rendering → server.ssrLoadModule()
│   ├── Transform a file → server.transformRequest()
│   └── Transform HTML → server.transformIndexHtml()
├── Production build → build()
├── Preview built output → preview()
├── Read resolved config → resolveConfig()
├── Combine configs → mergeConfig()
├── Load config file → loadConfigFromFile()
├── Load env variables → loadEnv()
├── Transform code standalone → transformWithOxc() (v8+) / transformWithEsbuild() (v5-v7)
└── Find workspace root → searchForWorkspaceRoot()
```

---

## ViteDevServer Interface

The `ViteDevServer` object returned by `createServer()` provides full programmatic control:

### Properties

| Property | Type | Purpose |
|----------|------|---------|
| `config` | `ResolvedConfig` | Fully resolved Vite configuration |
| `middlewares` | `Connect.Server` | Connect-compatible middleware stack |
| `httpServer` | `http.Server \| null` | Underlying Node HTTP server (null in middleware mode) |
| `watcher` | `FSWatcher` | Chokidar file system watcher |
| `ws` | `WebSocketServer` | WebSocket server for HMR communication |
| `pluginContainer` | `PluginContainer` | Runs plugin hooks programmatically |
| `moduleGraph` | `ModuleGraph` | Tracks import relationships and HMR state |
| `resolvedUrls` | `ResolvedServerUrls \| null` | Resolved local and network URLs (available after `listen()`) |

### Methods

| Method | Signature | Purpose |
|--------|-----------|---------|
| `transformRequest` | `(url, options?) → Promise<TransformResult \| null>` | Transform a module by URL |
| `transformIndexHtml` | `(url, html, originalUrl?) → Promise<string>` | Apply HTML transforms |
| `ssrLoadModule` | `(url, options?) → Promise<Record<string, any>>` | Load a module for SSR |
| `ssrFixStacktrace` | `(e: Error) → void` | Fix SSR error stack traces |
| `reloadModule` | `(module: ModuleNode) → Promise<void>` | Trigger HMR reload for a module |
| `listen` | `(port?, isRestart?) → Promise<ViteDevServer>` | Start listening on a port |
| `restart` | `(forceOptimize?) → Promise<void>` | Restart the dev server |
| `close` | `() → Promise<void>` | Shut down the server and clean up |
| `bindCLIShortcuts` | `(options?) → void` | Enable keyboard shortcuts (r, u, c, q) |
| `waitForRequestsIdle` | `(ignoredId?) → Promise<void>` | Wait until all pending requests complete |

---

## PreviewServer Interface

The `PreviewServer` object returned by `preview()`:

| Member | Type | Purpose |
|--------|------|---------|
| `config` | `ResolvedConfig` | Resolved configuration |
| `middlewares` | `Connect.Server` | Connect middleware stack |
| `httpServer` | `http.Server` | HTTP server (ALWAYS present, unlike dev server) |
| `resolvedUrls` | `ResolvedServerUrls \| null` | Resolved URLs |
| `printUrls()` | method | Print server URLs to console |
| `bindCLIShortcuts(options?)` | method | Enable keyboard shortcuts |

---

## Key Types

### InlineConfig

Extends `UserConfig` with:
- `configFile`: Set to a path to specify config file, or `false` to disable auto-resolving. ALWAYS set `configFile: false` when you want zero config file influence.

### ResolvedConfig

All `UserConfig` properties resolved (no undefined values), plus:
- `config.assetsInclude(id)`: Function to check if an ID is an asset
- `config.logger`: Internal logger object

### resolveConfig Signature

```typescript
async function resolveConfig(
  inlineConfig: InlineConfig,
  command: 'build' | 'serve',  // 'serve' for dev AND preview
  defaultMode?: string,        // default: 'development'
  defaultNodeEnv?: string,     // default: 'development'
  isPreview?: boolean,         // default: false
): Promise<ResolvedConfig>
```

**ALWAYS** pass `command: 'serve'` for both dev and preview scenarios. The `command` parameter is `'build'` ONLY for production builds.

---

## Version Differences

| Feature | Vite 5.x / 6.x | Vite 8.x+ |
|---------|----------------|-----------|
| Transform API | `transformWithEsbuild()` | `transformWithOxc()` |
| Bundler engine | Rollup-based | Rolldown-based |
| Version constants | `version` only | `version`, `rolldownVersion`, `esbuildVersion` (compat), `rollupVersion` (compat) |
| Filter utility | `@rollup/pluginutils` | `createFilter()` re-exported from Vite directly |

---

## Reference Links

- [references/api-reference.md](references/api-reference.md) -- Complete API signatures for all programmatic functions
- [references/examples.md](references/examples.md) -- Working code examples for dev server, build, preview, and utilities
- [references/anti-patterns.md](references/anti-patterns.md) -- Common programmatic API mistakes and how to avoid them

### Official Sources

- https://vite.dev/guide/api-javascript
- https://vite.dev/guide/api-environment
- https://vite.dev/guide/ssr
