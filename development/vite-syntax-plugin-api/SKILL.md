---
name: vite-syntax-plugin-api
description: >
  Use when writing Vite plugins, understanding hook lifecycle, creating virtual
  modules, or customizing the build pipeline.
  Prevents incorrect hook ordering (enforce pre/post), missing the virtual module
  resolved-id prefix convention, and using build-only hooks during dev.
  Covers plugin structure, naming conventions, Vite-specific hooks (config,
  configResolved, configureServer, transformIndexHtml, handleHotUpdate),
  Rollup-compatible hooks (resolveId, load, transform), plugin ordering,
  conditional application (apply), virtual modules, hook filters (v6.3+),
  and client-server WebSocket communication.
  Keywords: vite, plugin, hooks, virtual modules, resolveId, transform, enforce, configureServer.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-syntax-plugin-api

## Quick Reference

### Plugin Structure

A Vite plugin is a **factory function** returning an object with a required `name` property:

```js
export default function myPlugin(options = {}) {
  return {
    name: 'vite-plugin-my-feature',
    // hooks...
  }
}
```

### Naming Conventions

| Type | Prefix | npm Keywords |
|------|--------|-------------|
| Vite-only plugin | `vite-plugin-` | `vite-plugin` |
| Rolldown plugin | `rolldown-plugin-` | `rolldown-plugin`, `vite-plugin` |
| Framework-specific | `vite-plugin-vue-`, `vite-plugin-react-`, `vite-plugin-svelte-` | framework + `vite-plugin` |

### Plugin Execution Order

Plugins execute in this EXACT order:

1. **Alias** (internal)
2. User plugins with `enforce: 'pre'`
3. **Vite core plugins** (internal)
4. User plugins with **no** `enforce` value
5. **Vite build plugins** (internal)
6. User plugins with `enforce: 'post'`
7. **Vite post-build plugins** (internal)

### Conditional Application (`apply`)

```js
// String form: 'build' or 'serve'
apply: 'build',

// Function form: precise control
apply(config, { command }) {
  return command === 'build' && !config.build.ssr
}
```

### Plugin Arrays and Falsy Values

Falsy plugins are ignored. Arrays are flattened. This enables conditional plugins:

```js
plugins: [
  myPlugin(),
  condition ? optionalPlugin() : null,
  [pluginA(), pluginB()],
]
```

---

## Critical Warnings

**NEVER** inject plugins inside the `config` hook -- user plugins resolve BEFORE the `config` hook runs, so injected plugins have no effect.

**NEVER** rely on the `moduleParsed` hook during dev -- Vite does NOT call it for performance reasons. It only runs during production builds.

**ALWAYS** prefix virtual module IDs with `\0` internally -- this prevents other plugins from processing them. The `virtual:` prefix is for user-facing imports only.

**ALWAYS** use `normalizePath()` on file paths in plugins -- Vite uses forward slashes internally, even on Windows.

**ALWAYS** return `null` from `resolveId` and `load` hooks when a module is NOT handled by your plugin -- returning `undefined` silently breaks the plugin chain.

---

## Vite-Specific Hooks

| Hook | Kind | When Called |
|------|------|------------|
| `config` | async, sequential | Before config resolution |
| `configResolved` | async, parallel | After config resolution |
| `configureServer` | async, sequential | Dev server setup (NOT production) |
| `configurePreviewServer` | async, sequential | Preview server setup |
| `transformIndexHtml` | async, sequential | HTML entry transformation |
| `handleHotUpdate` | async, sequential | Custom HMR handling (dev only) |

## Rollup-Compatible Hooks

| Hook | When Called |
|------|------------|
| `options` | On dev server start |
| `buildStart` | On dev server start |
| `resolveId` | Per module request |
| `load` | Per module request |
| `transform` | Per module request |
| `buildEnd` | On server close |
| `closeBundle` | On server close |

---

## Decision Trees

### When to Use `enforce`

```
Need to run before core transforms (e.g., resolve aliases)?
├─ YES → enforce: 'pre'
└─ NO
   Need to run after all other plugins (e.g., minification, final transforms)?
   ├─ YES → enforce: 'post'
   └─ NO → omit enforce (default ordering)
```

### When to Use `apply`

```
Plugin only meaningful during dev (e.g., middleware, HMR)?
├─ YES → apply: 'serve'
└─ NO
   Plugin only meaningful during build (e.g., minification)?
   ├─ YES → apply: 'build'
   └─ NO
      Need conditional logic (e.g., skip for SSR builds)?
      ├─ YES → apply: function
      └─ NO → omit apply (runs always)
```

### Virtual Modules vs Transform

```
Need to generate code from scratch (no source file)?
├─ YES → Virtual modules (resolveId + load)
└─ NO
   Need to modify existing source code?
   ├─ YES → transform hook
   └─ NO
      Need to inject HTML tags?
      ├─ YES → transformIndexHtml
      └─ NO → Different hook needed
```

---

## Virtual Modules Pattern

ALWAYS use the `virtual:` prefix for user-facing imports and `\0` prefix for internal IDs:

```js
export default function myPlugin() {
  const virtualModuleId = 'virtual:my-module'
  const resolvedId = '\0' + virtualModuleId

  return {
    name: 'vite-plugin-virtual',
    resolveId(id) {
      if (id === virtualModuleId) return resolvedId
    },
    load(id) {
      if (id === resolvedId) {
        return `export const data = ${JSON.stringify({ key: 'value' })}`
      }
    },
  }
}
```

Consumer usage:

```js
import { data } from 'virtual:my-module'
```

---

## Hook Filters (v6.3+)

Modern hook syntax with performance optimization via `filter` property:

```js
import { exactRegex } from '@rolldown/pluginutils'

export default function myPlugin() {
  return {
    name: 'vite-plugin-filtered',
    transform: {
      filter: { id: /\.custom$/ },
      handler(code, id) {
        return { code: transformCode(code), map: null }
      },
    },
    resolveId: {
      filter: { id: exactRegex('virtual:my-module') },
      handler(id) {
        return '\0virtual:my-module'
      },
    },
  }
}
```

Utility functions from `@rolldown/pluginutils`: `exactRegex()`, `prefixRegex()`.

---

## Plugin Context Meta

Access version metadata inside hooks via `this.meta`:

```js
buildStart() {
  console.log('Vite version:', this.meta.viteVersion)
  if (this.meta.rolldownVersion) {
    // Rolldown-powered Vite (v8+)
  }
}
```

---

## Client-Server Communication

ALWAYS use namespaced event names (e.g., `my-plugin:event-name`) to avoid collisions.

**Server to client:**

```js
configureServer(server) {
  server.ws.send('my-plugin:update', { data: 'hello' })
}
```

**Client to server:**

```js
if (import.meta.hot) {
  import.meta.hot.send('my-plugin:request', { msg: 'Hi' })
}
```

**Server listening for client events:**

```js
configureServer(server) {
  server.ws.on('my-plugin:request', (data, client) => {
    client.send('my-plugin:response', { result: 'ok' })
  })
}
```

TypeScript custom event typing -- see [references/examples.md](references/examples.md).

---

## Output Bundle Metadata

During builds, Vite augments output chunks/assets with `viteMetadata`:

```ts
interface ViteMetadata {
  importedCss: Set<string>
  importedAssets: Set<string>
}
```

Access in `generateBundle` hook -- see [references/examples.md](references/examples.md).

---

## Utilities

| Function | Purpose |
|----------|---------|
| `normalizePath(path)` | Convert backslashes to forward slashes |
| `createFilter(include, exclude)` | Create inclusion/exclusion filter function |

```js
import { normalizePath, createFilter } from 'vite'

const filter = createFilter(['src/**/*.vue'], ['node_modules/**'])
```

---

## Rollup Plugin Compatibility

Rollup plugins work in Vite if they:
- Do NOT use `moduleParsed` hook
- Do NOT rely on Rolldown-specific options
- Do NOT tightly couple bundle-phase and output-phase hooks

Scope Rollup-only plugins to build phase:

```js
plugins: [
  { ...rollupPlugin(), enforce: 'post', apply: 'build' },
]
```

---

## Reference Links

- [references/hooks.md](references/hooks.md) -- ALL hook signatures with complete TypeScript types
- [references/examples.md](references/examples.md) -- Complete plugin template, virtual modules, tag injection, client-server communication, hook filters
- [references/anti-patterns.md](references/anti-patterns.md) -- Plugin development mistakes and how to avoid them

### Official Sources

- https://vite.dev/guide/api-plugin
- https://vite.dev/guide/api-hmr
