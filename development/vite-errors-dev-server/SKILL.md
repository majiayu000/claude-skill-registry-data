---
name: vite-errors-dev-server
description: >
  Use when encountering dev server startup failures, HMR issues, proxy errors,
  CORS blocks, or module not found errors during development.
  Prevents misconfiguring server.hmr behind reverse proxies and forgetting
  appType: 'custom' in middleware mode.
  Covers HMR full-reload debugging, proxy configuration, CORS setup, HTTPS
  certificates, server.fs.strict violations, port conflicts, WebSocket
  failures, file watcher issues, and middleware mode.
  Keywords: dev server, HMR, proxy, CORS, HTTPS, WebSocket, port conflict,
  server.fs.strict, middleware mode, file watcher.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-errors-dev-server

## Quick Diagnostic Table

| Symptom | Cause | Fix |
|---------|-------|-----|
| Full page reload instead of HMR | No HMR boundary — module lacks `import.meta.hot.accept()` | Add `import.meta.hot.accept()` in the changed module or a parent importer |
| HMR accept not detected | Whitespace before `(` in `import.meta.hot.accept(` | ALWAYS write `import.meta.hot.accept(` with NO line break between `accept` and `(` |
| WebSocket connection failed | Wrong HMR config behind reverse proxy | Set `server.hmr.clientPort`, `server.hmr.host`, `server.hmr.protocol` |
| `EADDRINUSE` on startup | Port already in use | Kill the process on that port, or set `server.strictPort: false` (default) for auto-fallback |
| Proxy returns 500/ECONNREFUSED | Wrong `target` format or backend not running | Verify target URL includes protocol (`http://`), add `changeOrigin: true` |
| CORS blocked request | Default `server.cors` allows only localhost origins | Set `server.cors: true` for any origin, or configure specific `origin` |
| "Outside of Vite serving allow list" | `server.fs.strict` blocks files outside workspace root | Add the directory to `server.fs.allow` |
| HTTPS certificate errors | Missing or invalid cert/key files | Pass valid `key` and `cert` to `server.https`, or use `@vitejs/plugin-basic-ssl` |
| Module not found / alias not working | Alias path uses wrong format | Use absolute paths with `path.resolve()` or `/src/...` root-relative format |
| File changes not detected | Chokidar fails in Docker/WSL2 | Set `server.watch.usePolling: true` |
| 403 Forbidden on all requests | `server.allowedHosts` blocks the hostname | Add the hostname to `server.allowedHosts` array, or set to `true` |
| Slow initial page load | Modules transformed on-demand on first request | Configure `server.warmup.clientFiles` with frequently used entry files |
| Middleware mode errors | Missing `appType: 'custom'` | ALWAYS set `appType: 'custom'` when using `server.middlewareMode: true` |
| Browser errors not in terminal | `server.forwardConsole` not enabled | Set `server.forwardConsole: true` (v8+ only, auto-enabled for AI agents) |

---

## HMR Debugging Flowchart

When a file change triggers a **full page reload** instead of an HMR update, follow this decision tree:

```
File changed
  |
  v
Does the module call import.meta.hot.accept()?
  |
  +-- NO --> Does any PARENT module accept it?
  |            |
  |            +-- NO --> FULL RELOAD (no HMR boundary exists)
  |            |          FIX: Add import.meta.hot.accept() to the module
  |            |               or to a parent that imports it
  |            |
  |            +-- YES --> HMR update at the parent boundary
  |
  +-- YES --> Is accept() detected by static analysis?
               |
               +-- NO --> Check: is there a line break between
               |          "accept" and "(" ?
               |          FIX: Write import.meta.hot.accept( on one token
               |
               +-- YES --> Does the accept callback succeed?
                            |
                            +-- NO --> Does it call hot.invalidate()?
                            |           |
                            |           +-- YES --> Propagates up; if no
                            |           |           parent boundary: FULL RELOAD
                            |           +-- NO --> Error in callback: FULL RELOAD
                            |
                            +-- YES --> HMR UPDATE (success)
```

### Critical HMR Rules

**ALWAYS** wrap HMR code in `if (import.meta.hot) { ... }` — this guard is required for production tree-shaking.

**ALWAYS** write `import.meta.hot.accept(` as a single token — Vite uses static analysis to detect HMR boundaries. A line break between `accept` and `(` causes the boundary to go undetected, resulting in full reloads.

```javascript
// CORRECT - detected as HMR boundary
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    // handle update
  })
}

// WRONG - NOT detected as HMR boundary
if (import.meta.hot) {
  import.meta.hot.accept
    ((newModule) => {
      // handle update
    })
}
```

**NEVER** reassign `import.meta.hot.data` — mutate its properties instead:

```javascript
// CORRECT
import.meta.hot.data.count = 42

// WRONG - reassignment is NOT supported
import.meta.hot.data = { count: 42 }
```

---

## WebSocket / HMR Connection Failures

When the HMR WebSocket fails to connect (common behind reverse proxies, Docker, or non-standard setups):

```javascript
// vite.config.ts
export default defineConfig({
  server: {
    hmr: {
      protocol: 'ws',      // 'ws' or 'wss' for HTTPS
      host: 'localhost',    // Client-visible hostname
      port: 5173,           // Server-side WebSocket port
      clientPort: 443,      // Port the CLIENT connects to (proxy port)
    },
  },
})
```

**ALWAYS** set `clientPort` when a reverse proxy terminates SSL or maps ports. The client needs to know the external port, not the internal one.

**NEVER** assume WebSocket auto-detection works behind proxies — explicitly configure `server.hmr` when using nginx, Caddy, or cloud-based dev environments.

---

## Proxy Configuration Errors

### Common Proxy Mistakes

```javascript
// WRONG: missing protocol in target
server: {
  proxy: {
    '/api': {
      target: 'localhost:3000',  // WRONG - needs http://
    },
  },
}

// CORRECT
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:3000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
  },
}
```

**ALWAYS** include the protocol (`http://` or `https://`) in proxy targets.

**ALWAYS** set `changeOrigin: true` when proxying to a different hostname — this sets the `Host` header to match the target.

### WebSocket Proxy

```javascript
server: {
  proxy: {
    '/socket.io': {
      target: 'ws://localhost:5174',
      ws: true,  // REQUIRED for WebSocket proxying
    },
  },
}
```

**ALWAYS** set `ws: true` explicitly when proxying WebSocket connections.

---

## CORS Issues

Default `server.cors` allows only localhost origins (pattern: `/^https?:\/\/(?:(?:[^:]+\.)?localhost|127\.0\.0\.1|\[::1\])(?::\d+)?$/`).

```javascript
// Allow all origins (development only)
server: {
  cors: true,
}

// Allow specific origin (backend integration)
server: {
  cors: {
    origin: 'http://my-backend.example.com',
  },
}
```

**NEVER** set `cors: true` in production preview servers without understanding the security implications.

---

## server.fs.strict Violations

Error: `"The request url is outside of Vite serving allow list"`

```javascript
// FIX: Add the directory to the allow list
server: {
  fs: {
    allow: [
      // Workspace root (auto-included)
      searchForWorkspaceRoot(process.cwd()),
      // Additional directories
      '/path/to/shared/packages',
      '../sibling-project/src',
    ],
  },
}
```

**ALWAYS** use `searchForWorkspaceRoot()` from `vite` to auto-detect the workspace root in monorepos.

**NEVER** set `server.fs.strict: false` to work around this error — it disables an important security boundary. Add specific paths to `server.fs.allow` instead.

---

## Port Conflicts

```javascript
server: {
  port: 5173,
  strictPort: false,  // DEFAULT: tries next port if 5173 is taken
}
```

- `strictPort: false` (default): Vite silently increments to the next available port
- `strictPort: true`: Vite exits with `EADDRINUSE` if the port is occupied

**ALWAYS** set `strictPort: true` in CI/CD environments where port predictability matters.

---

## File Watcher Issues (Docker / WSL2)

Chokidar's native file watching does NOT work reliably on network filesystems, Docker volumes, or WSL2 cross-filesystem mounts:

```javascript
server: {
  watch: {
    usePolling: true,    // REQUIRED for Docker/WSL2
    interval: 1000,      // Poll every 1s (reduce CPU; default 100ms)
  },
}
```

**ALWAYS** enable `usePolling` when running Vite inside Docker or when source files are on a different filesystem (WSL2 accessing Windows files or vice versa).

---

## Middleware Mode Errors

**ALWAYS** set `appType: 'custom'` together with `server.middlewareMode: true`:

```javascript
import express from 'express'
import { createServer as createViteServer } from 'vite'

const app = express()
const vite = await createViteServer({
  server: { middlewareMode: true },
  appType: 'custom',  // REQUIRED - disables built-in HTML handling
})
app.use(vite.middlewares)
```

**NEVER** omit `appType: 'custom'` when using middleware mode — Vite's default SPA fallback middleware will interfere with your custom server routing.

---

## Module Resolution Errors

### Alias Not Working

```javascript
import path from 'node:path'

export default defineConfig({
  resolve: {
    alias: {
      // CORRECT: absolute path
      '@': path.resolve(import.meta.dirname, './src'),

      // CORRECT: root-relative (Vite resolves from project root)
      '@components': '/src/components',

      // WRONG: relative path without resolve
      '@': './src',
    },
  },
})
```

**ALWAYS** use `path.resolve()` or root-relative paths (`/src/...`) for aliases. Relative paths like `./src` resolve from the config file location, which may not be what you expect.

### Extension Not Resolved

Vite resolves these extensions by default: `.mjs`, `.js`, `.mts`, `.ts`, `.jsx`, `.tsx`, `.json`.

**NEVER** add `.vue`, `.svelte`, or other framework extensions to `resolve.extensions` — framework plugins handle those. Adding them causes double-resolution issues.

---

## server.allowedHosts (DNS Rebinding Protection)

Since Vite 6.2+, the dev server validates the `Host` header to prevent DNS rebinding attacks:

```javascript
server: {
  allowedHosts: ['my-app.dev.local', '.example.com'],  // dot prefix = subdomains
}

// Or disable protection entirely (development only)
server: {
  allowedHosts: true,
}
```

**ALWAYS** add custom dev domains to `allowedHosts` when using tools like `ngrok`, `localtunnel`, or custom `/etc/hosts` entries.

---

## Slow Initial Load

Use `server.warmup` to pre-transform frequently needed modules:

```javascript
server: {
  warmup: {
    clientFiles: [
      './src/main.ts',
      './src/components/**/*.vue',
      './src/router/index.ts',
    ],
  },
}
```

This transforms and caches these files BEFORE the browser requests them, eliminating the cold-start waterfall on first page load.

---

## server.forwardConsole (v8+)

Forward browser runtime errors and console output to the terminal:

```javascript
server: {
  forwardConsole: true,  // Auto-detected for AI agents in v8+
}
```

**NEVER** rely on `server.forwardConsole` in Vite 6.x or 7.x — this feature was introduced in Vite 8.x.

---

## Reference Links

- [references/error-catalog.md](references/error-catalog.md) -- Complete error pattern catalog: symptom, cause, fix
- [references/examples.md](references/examples.md) -- Error scenarios with full config solutions
- [references/anti-patterns.md](references/anti-patterns.md) -- Dev server configuration mistakes to avoid

### Official Sources

- https://vite.dev/config/server-options
- https://vite.dev/guide/api-hmr
- https://vite.dev/guide/dep-pre-bundling
- https://vite.dev/guide/backend-integration
