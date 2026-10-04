---
name: vite-impl-ssr
description: >
  Use when implementing SSR, configuring SSR externals, building SSR applications,
  or debugging SSR errors.
  Prevents incorrect SSR externals configuration and missing ssrFixStacktrace() for error debugging.
  Covers SSR dev workflow with Express middleware, ssrLoadModule(), SSR externals (ssr.noExternal,
  ssr.external, ssr.target), SSR manifest, import.meta.env.SSR, and production build steps.
  Keywords: SSR, ssrLoadModule, ssrFixStacktrace, ssr.noExternal, ssr.external, SSR manifest, middleware mode.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-impl-ssr

## Quick Reference

### SSR Architecture Overview

| Component | Purpose | Location |
|-----------|---------|----------|
| Entry Client | Hydrates server-rendered HTML in browser | `src/entry-client.js` |
| Entry Server | Exports `render()` function for SSR | `src/entry-server.js` |
| Custom Server | Express/Koa server with Vite middleware | `server.js` (project root) |
| index.html | Template with `<!--ssr-outlet-->` placeholder | Project root |
| SSR Manifest | Maps module IDs to chunks/assets for preloading | `dist/client/.vite/ssr-manifest.json` |

### SSR Dev vs Production

| Aspect | Development | Production |
|--------|-------------|------------|
| Module loading | `vite.ssrLoadModule()` | `import('./dist/server/entry-server.js')` |
| HTML template | Read from project root `index.html` | Read from `dist/client/index.html` |
| HTML transforms | `vite.transformIndexHtml()` applies plugins | Pre-built, no transforms needed |
| Static files | Vite middleware serves files | Express static middleware from `dist/client` |
| Error handling | `vite.ssrFixStacktrace(e)` maps to source | Standard Node.js stack traces |

### Build Commands

```json
{
  "scripts": {
    "dev": "node server",
    "build:client": "vite build --outDir dist/client",
    "build:server": "vite build --outDir dist/server --ssr src/entry-server.js",
    "build": "npm run build:client && npm run build:server"
  }
}
```

**ALWAYS** change `"dev": "vite"` to `"dev": "node server"` in `package.json` when implementing SSR -- the custom server replaces the default Vite dev server.

### Critical Warnings

**NEVER** call `vite.ssrLoadModule()` in production -- it is a development-only API. ALWAYS use `import('./dist/server/entry-server.js')` for production.

**NEVER** forget to call `vite.ssrFixStacktrace(e)` in your catch block during development -- without it, error stack traces point to transformed code instead of original source files.

**NEVER** read `index.html` from the project root in production -- ALWAYS read from `dist/client/index.html` which contains the built asset references.

**NEVER** omit `appType: 'custom'` when creating the Vite server in middleware mode -- this prevents Vite from injecting its own HTML handling logic that conflicts with SSR.

**NEVER** set `ssr.noExternal: true` for Node.js targets unless you explicitly need a single-file bundle -- it forces bundling of all dependencies, which is unnecessary and slower for Node.js.

---

## SSR Dev Server Setup

### Middleware Mode with Express

ALWAYS use middleware mode (`server: { middlewareMode: true }`) for SSR development. This lets Express handle routing while Vite handles module transformation and HMR.

```javascript
import fs from 'node:fs'
import path from 'node:path'
import express from 'express'
import { createServer as createViteServer } from 'vite'

async function createServer() {
  const app = express()

  const vite = await createViteServer({
    server: { middlewareMode: true },
    appType: 'custom',
  })

  app.use(vite.middlewares)

  app.use('*all', async (req, res, next) => {
    const url = req.originalUrl
    try {
      let template = fs.readFileSync(
        path.resolve(import.meta.dirname, 'index.html'),
        'utf-8',
      )
      template = await vite.transformIndexHtml(url, template)
      const { render } = await vite.ssrLoadModule('/src/entry-server.js')
      const appHtml = await render(url)
      const html = template.replace(`<!--ssr-outlet-->`, () => appHtml)
      res.status(200).set({ 'Content-Type': 'text/html' }).end(html)
    } catch (e) {
      vite.ssrFixStacktrace(e)
      next(e)
    }
  })

  app.listen(5173)
}

createServer()
```

### index.html Template

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>SSR App</title>
  </head>
  <body>
    <div id="app"><!--ssr-outlet--></div>
    <script type="module" src="/src/entry-client.js"></script>
  </body>
</html>
```

ALWAYS place `<!--ssr-outlet-->` inside the mount element. The server replaces this comment with rendered HTML. The client entry script handles hydration.

---

## Decision Tree: SSR Configuration

### When to use ssr.noExternal

```
Does the dependency use browser-specific code that Vite must transform?
├─ YES → Add to ssr.noExternal: ['dependency-name']
├─ Is it a linked/monorepo package?
│  └─ YES → Linked packages are NOT externalized by default; add to ssr.noExternal if they need Vite transforms
└─ Do you need a single-file SSR bundle (e.g., for webworker)?
   └─ YES → Set ssr.noExternal: true (bundles everything)
```

### When to use ssr.external

```
Is a linked dependency causing issues when processed by Vite?
├─ YES → Add to ssr.external: ['dependency-name']
└─ NO → Leave default (node_modules are externalized automatically)
```

### SSR Target Selection

```
Where does the SSR code run?
├─ Node.js server → ssr.target: 'node' (default, NEVER set explicitly)
└─ Cloudflare Workers / Deno Deploy / edge runtime
   └─ ssr.target: 'webworker'
      └─ ALWAYS also set ssr.noExternal: true for webworker targets
```

---

## SSR Config Options

### Externals

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  ssr: {
    // Force these through Vite's transform pipeline
    noExternal: ['@my-org/ui-components', 'some-esm-only-lib'],

    // Externalize despite being linked
    external: ['legacy-linked-package'],

    // SSR runtime target
    target: 'node', // default; or 'webworker'
  },
})
```

### Resolve Conditions

```typescript
export default defineConfig({
  ssr: {
    resolve: {
      // Override resolve.conditions for SSR builds
      conditions: ['node', 'import'],
      // Additional conditions for externalized deps
      externalConditions: ['node', 'import'],
    },
  },
})
```

---

## SSR Conditional Logic

```javascript
if (import.meta.env.SSR) {
  // Server-only code -- tree-shaken from client bundle
}
```

This boolean is statically replaced during build, so dead code elimination removes the unused branch entirely. ALWAYS use this for code that must run only on the server or only on the client.

---

## Plugin SSR Detection

Plugins detect SSR context through the `options` parameter in hooks:

```javascript
export function mySSRPlugin() {
  return {
    name: 'my-ssr-plugin',
    transform(code, id, options) {
      if (options?.ssr) {
        // SSR-specific transform
      }
    },
  }
}
```

ALWAYS use `options?.ssr` (optional chaining) -- the options parameter may be undefined in some contexts.

---

## SSR Manifest for Preload Directives

Generate the manifest during client build:

```bash
vite build --outDir dist/client --ssrManifest
```

This produces `dist/client/.vite/ssr-manifest.json` mapping module IDs to their output chunks and assets. Use this in the server to inject `<link rel="modulepreload">` and `<link rel="stylesheet">` tags for optimal loading.

---

## Reference Links

- [references/api-reference.md](references/api-reference.md) -- ssrLoadModule, ssrFixStacktrace, SSR config options with full signatures
- [references/examples.md](references/examples.md) -- Complete Express SSR dev server, build commands, production server setup
- [references/anti-patterns.md](references/anti-patterns.md) -- Common SSR mistakes and how to avoid them

### Official Sources

- https://vite.dev/guide/ssr
- https://vite.dev/config/ssr-options
- https://vite.dev/guide/api-javascript
