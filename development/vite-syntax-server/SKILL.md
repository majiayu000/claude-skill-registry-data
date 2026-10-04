---
name: vite-syntax-server
description: >
  Use when configuring the Vite dev server, setting up proxy rules, enabling HTTPS,
  restricting file system access, or using middleware mode.
  Prevents exposing the dev server on the network without proper host/CORS settings
  and misconfiguring proxy rewrite rules.
  Covers server.host, server.port, server.proxy, server.cors, server.https,
  server.hmr, server.fs (strict/allow/deny), server.warmup, server.middlewareMode,
  server.open, server.headers, server.watch, server.forwardConsole, and server.allowedHosts.
  Keywords: vite, dev server, proxy, HTTPS, CORS, HMR, middleware mode, file system access.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-syntax-server

## Quick Reference

### Server Options Overview

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `server.host` | `string \| boolean` | `'localhost'` | Network interface to bind |
| `server.port` | `number` | `5173` | Dev server port |
| `server.strictPort` | `boolean` | `false` | Exit if port is in use |
| `server.https` | `https.ServerOptions` | -- | Enable TLS + HTTP/2 |
| `server.open` | `boolean \| string` | -- | Auto-open browser on start |
| `server.proxy` | `Record<string, string \| ProxyOptions>` | -- | API proxy rules |
| `server.cors` | `boolean \| CorsOptions` | localhost regex | CORS configuration |
| `server.headers` | `OutgoingHttpHeaders` | -- | Custom response headers |
| `server.hmr` | `boolean \| HmrOptions` | -- | HMR connection config |
| `server.warmup` | `{ clientFiles?, ssrFiles? }` | -- | Pre-transform files |
| `server.watch` | `object \| null` | -- | Chokidar watcher options |
| `server.middlewareMode` | `boolean` | `false` | Use Vite as middleware |
| `server.fs.strict` | `boolean` | `true` | Restrict file serving |
| `server.fs.allow` | `string[]` | -- | Allowed serve directories |
| `server.fs.deny` | `string[]` | sensitive defaults | Blocked file patterns |
| `server.origin` | `string` | -- | Asset URL origin |
| `server.sourcemapIgnoreList` | `false \| Function` | ignores node_modules | Sourcemap filtering |
| `server.allowedHosts` | `string[] \| true` | `[]` | Permitted hostnames |
| `server.forwardConsole` | `boolean \| object` | auto-detected | Forward browser console (v8+) |

### Critical Warnings

**NEVER** set `server.host` to `true` or `0.0.0.0` without also configuring `server.allowedHosts` -- this exposes the dev server to all network interfaces and risks DNS rebinding attacks.

**NEVER** set `server.fs.strict` to `false` in shared or team environments -- it allows serving ANY file on the machine, including sensitive system files.

**NEVER** set `server.cors` to `true` in production-like environments -- it allows any origin to make requests. ALWAYS use specific origin patterns.

**NEVER** disable `server.fs.deny` defaults -- the default list blocks `.env`, `.env.*`, `*.{crt,pem}`, and `**/.git/**` for security.

**ALWAYS** set `appType: 'custom'` when using `server.middlewareMode: true` -- without it, Vite injects SPA fallback middleware that conflicts with your custom server routing.

---

## Decision Trees

### When to Use Middleware Mode

```
Need custom HTTP server (Express, Koa, Fastify)?
  YES → server.middlewareMode: true + appType: 'custom'
  NO → Use standard Vite dev server

Building SSR application with custom rendering?
  YES → server.middlewareMode: true + appType: 'custom'
  NO → Standard config sufficient
```

### Proxy vs CORS

```
API on different origin during development?
  ├── Same domain, different port → Use server.proxy (RECOMMENDED)
  ├── Different domain entirely → Use server.proxy with changeOrigin: true
  └── Cannot proxy (third-party API with origin checks) → Use server.cors
```

### Host Binding

```
Local development only?
  YES → Keep default 'localhost'
  NO → Need LAN access (mobile testing, etc.)?
    YES → server.host: true + server.allowedHosts: ['your-hostname.local']
    NO → Keep default 'localhost'
```

---

## Patterns

### Basic Dev Server Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    host: 'localhost',
    port: 3000,
    strictPort: true,
    open: true,
  },
})
```

### Proxy Configuration (String Shorthand + Options)

```typescript
export default defineConfig({
  server: {
    proxy: {
      // String shorthand: /foo/bar → http://localhost:4567/foo/bar
      '/foo': 'http://localhost:4567',

      // With options: /api/users → http://jsonplaceholder.typicode.com/users
      '/api': {
        target: 'http://jsonplaceholder.typicode.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },

      // WebSocket proxy
      '/socket.io': {
        target: 'ws://localhost:5174',
        ws: true,
      },
    },
  },
})
```

### HTTPS with TLS Certificates

```typescript
import fs from 'node:fs'
import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    https: {
      key: fs.readFileSync('certs/localhost-key.pem'),
      cert: fs.readFileSync('certs/localhost-cert.pem'),
    },
  },
})
```

### Middleware Mode with Express

```typescript
import express from 'express'
import { createServer as createViteServer } from 'vite'

async function createServer() {
  const app = express()

  const vite = await createViteServer({
    server: { middlewareMode: true },
    appType: 'custom',
  })

  // Use Vite's connect-compatible middleware stack
  app.use(vite.middlewares)

  // Custom routes AFTER Vite middleware
  app.use('*', async (req, res) => {
    // SSR rendering or custom logic here
  })

  app.listen(5173)
}
createServer()
```

### File System Security

```typescript
export default defineConfig({
  server: {
    fs: {
      // ALWAYS keep strict: true (default)
      strict: true,
      // Allow serving from parent directories (monorepo)
      allow: ['..'],
      // Add custom deny patterns on top of defaults
      deny: ['.env', '.env.*', '*.{crt,pem}', '**/.git/**'],
    },
  },
})
```

### Server Warmup for Faster Initial Load

```typescript
export default defineConfig({
  server: {
    warmup: {
      clientFiles: [
        './src/components/*.vue',
        './src/pages/Home.tsx',
      ],
      ssrFiles: [
        './src/server/entry-server.ts',
      ],
    },
  },
})
```

### HMR Configuration (Custom WebSocket)

```typescript
export default defineConfig({
  server: {
    hmr: {
      protocol: 'ws',
      host: 'localhost',
      port: 5174,
      clientPort: 443,     // When behind a reverse proxy
      overlay: true,        // Show error overlay in browser
      timeout: 30000,       // Connection timeout (ms)
    },
  },
})
```

### LAN Access with Security

```typescript
export default defineConfig({
  server: {
    host: true,  // Listen on all interfaces
    allowedHosts: ['my-dev-machine.local', '.example.com'],
  },
})
```

### Forward Console (v8+ Only)

```typescript
export default defineConfig({
  server: {
    forwardConsole: {
      unhandledErrors: true,
      logLevels: ['error', 'warn'],
    },
  },
})
```

---

## Version Differences

| Feature | Vite 6.x | Vite 7.x | Vite 8.x |
|---------|----------|----------|----------|
| Default port | 5173 | 5173 | 5173 |
| `server.proxy` backend | `http-proxy` | `http-proxy` | `http-proxy-3` |
| `server.forwardConsole` | N/A | N/A | Available (auto-detected) |
| `server.cors` default | `true` (any origin) | localhost regex | localhost regex |
| `server.allowedHosts` | N/A | Available | Available |
| File system strict | Default `true` | Default `true` | Default `true` |

**ALWAYS** check your Vite version before using `server.forwardConsole` -- it is only available in Vite 8.x and later.

**ALWAYS** note that `server.cors` default changed between Vite 6 and 7 -- Vite 6 allowed any origin by default, while Vite 7+ restricts to localhost origins.

---

## Reference Links

- [references/config-options.md](references/config-options.md) -- Complete server.* options with types, defaults, and descriptions
- [references/examples.md](references/examples.md) -- Working code examples for proxy, HTTPS, middleware mode, warmup, and fs restrictions
- [references/anti-patterns.md](references/anti-patterns.md) -- Server configuration mistakes and how to avoid them

### Official Sources

- https://vite.dev/config/server-options
- https://vite.dev/guide/api-javascript#createserver
- https://vite.dev/guide/ssr
- https://vite.dev/guide/backend-integration
