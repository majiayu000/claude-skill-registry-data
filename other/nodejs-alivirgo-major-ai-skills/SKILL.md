---
name: nodejs
description: "Build Node.js modules and services with async I/O, streams, package scripts, and deliberate process-lifecycle handling."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["nodejs", "javascript", "esm", "streams", "runtime", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Node.js Runtime AI Skill Guide

## Overview & Engine Architecture

Node.js is a single-threaded event-loop runtime with libuv for async I/O. Agents choose ESM vs CJS deliberately, keep CPU-heavy work off the event loop (or isolate it), handle uncaught errors, and pin engines in `package.json` so local and CI Node versions match production.

```
HTTP / CLI entry
      |
  event loop
   +--+---+---+
   | timers     |
   | I/O polls  |
   | microtasks |
   +------------+
      |
  worker_threads / child_process (when needed)
```

## When to use this skill

- Scaffolding or hardening Node services and CLIs
- Fixing ESM/CJS interop and `package.json` `type` issues
- Streaming large payloads without buffering entire bodies
- Diagnosing event-loop stalls and unhandled rejections

## Operational directives

1. Prefer native `fetch`, `node:fs/promises`, and `node:path` over legacy callback APIs.
2. Set `"type": "module"` or use `.mjs` / `.cjs` extensions explicitly - do not mix blindly.
3. Never swallow `unhandledRejection` / `uncaughtException` without logging and controlled exit.
4. Use streams or async iterators for files and HTTP bodies larger than memory comfort.
5. Pin `engines.node` and match CI to that range.

## Minimal HTTP server (ESM)

```js
import http from "node:http";

const port = Number(process.env.PORT ?? 3000);

const server = http.createServer(async (req, res) => {
  if (req.method === "GET" && req.url === "/health") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ ok: true }));
    return;
  }
  res.writeHead(404);
  res.end();
});

server.listen(port, () => {
  console.log(`listening on ${port}`);
});
```

## Commands

```bash
node --version
node --watch src/index.js
npm run start
NODE_OPTIONS=--enable-source-maps node dist/index.js
```

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Sync `fs` in request path | Blocks event loop | Use promises/streams |
| Missing `await` on promise | Silent failures | Enable lint rules; handle rejections |
| Relativizing without `node:` | Ambiguous imports | Prefer `node:` built-ins |
| No `engines` field | Version skew in prod | Pin and enforce in CI |

## Best practices

- Structure apps with clear entrypoints and env validation at boot.
- Prefer structured logs (JSON) with request IDs.
- Use AbortController for cancelable fetches and timeouts.
- Keep secrets in env or a secret manager - never in source.

## Limitations

- CPU-bound work needs workers or an external job runner.
- Native addons (`node-gyp`) complicate cross-platform builds.
- Bun/Deno compatibility is not assumed - verify APIs per runtime.

## Related skills

- `@express` - HTTP framework patterns on Node
- `@typescript` - typed Node services
- `@docker` - containerizing Node processes
