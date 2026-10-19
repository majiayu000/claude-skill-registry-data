---
name: nodejs-development
description: >
  Develop, test, and package server-side Node.js applications and CLI utilities
  using modern ES Modules and runtime APIs. Use when building Node.js backend
  services, implementing streaming I/O with stream.pipeline, managing ESM/CommonJS
  compatibility, handling unhandled rejections and signals, or configuring package.json.
compatibility: >
  Agent Skills-compatible coding agents operating on Node.js 18+ runtimes.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "nodejs, npm, esm, streams, event-loop, backend, cli"
  topics: "programming-languages, software-development"
---

# Modern Node.js Development

Node.js provides an asynchronous, event-driven JavaScript runtime for server-side services and CLI tools. Modern Node.js development (Node 18+, 20+, 22+) emphasizes standard **ES Modules (ESM)**, built-in APIs (Fetch, Test Runner, Streams), strict error boundaries, and non-blocking I/O.

## Core Rules

1. **Use `"type": "module"` in `package.json`**: Adopt native ES Modules across the project.
2. **Never block the Event Loop**: Do not run synchronous file methods (`fs.readFileSync`) or CPU-heavy encryption loops in request handlers.
3. **Always use `stream.pipeline` for stream piping**: Never use raw `.pipe()` in production, as it fails to properly forward errors and can cause memory leaks.
4. **Register shutdown signals (`SIGTERM`, `SIGINT`)**: Gracefully close open sockets, database connections, and background workers when containers shut down.
5. **Handle process-level error events**: Always monitor `unhandledRejection` and `uncaughtException` to log errors and exit gracefully.

---

## 1. Native ES Modules and `package.json`

```json
{
  "name": "my-service",
  "version": "1.0.0",
  "type": "module",
  "engines": {
    "node": ">=20.0.0"
  },
  "main": "./src/index.js",
  "bin": {
    "my-cli": "./src/cli.js"
  },
  "scripts": {
    "start": "node src/index.js",
    "test": "node --test tests/**/*.test.js"
  }
}
```

Importing built-in modules using the standard `node:` protocol prefix:
```javascript
import { readFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
```

---

## 2. High-Performance Streaming with `pipeline`

Safely stream large files without loading them entirely into heap memory:

```javascript
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';

export async function compressFile(sourcePath, destPath) {
  try {
    await pipeline(
      createReadStream(sourcePath),
      createGzip(),
      createWriteStream(destPath)
    );
    console.log(`Successfully compressed ${sourcePath} -> ${destPath}`);
  } catch (err) {
    console.error('Pipeline compression failed:', err);
    throw err; // Pipeline automatically cleans up all streams on error!
  }
}
```

---

## 3. Graceful Shutdown & Signal Handling

In containerized environments (Docker, Kubernetes), applications receive `SIGTERM` when scaling down:

```javascript
import { createServer } from 'node:http';

const server = createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ status: 'healthy' }));
});

server.listen(3000, () => {
  console.log('Server running on port 3000');
});

function gracefulShutdown(signal) {
  console.log(`Received ${signal}. Closing HTTP server...`);
  server.close((err) => {
    if (err) {
      console.error('Error during shutdown:', err);
      process.exit(1);
    }
    console.log('Server closed. Releasing resources...');
    // Close database pools, message brokers, etc.
    process.exit(0);
  });

  // Force exit if hanging beyond 10 seconds
  setTimeout(() => {
    console.error('Forced shutdown due to timeout.');
    process.exit(1);
  }, 10000).unref();
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
```

---

## 4. Built-in Test Runner (Node 18+)

No external framework needed for fast, zero-dependency unit tests:

```javascript
import { test, describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { parseConfig } from '../src/config.js';

describe('Config Parser', () => {
  it('parses valid port and host', () => {
    const config = parseConfig({ PORT: '8080', HOST: '0.0.0.0' });
    assert.equal(config.port, 8080);
    assert.equal(config.host, '0.0.0.0');
  });

  it('rejects non-numeric port with TypeError', () => {
    assert.throws(
      () => parseConfig({ PORT: 'invalid' }),
      { name: 'TypeError', message: /Invalid port/ }
    );
  });
});
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| `readable.pipe(writable)` | Memory leak and dangling file descriptors if an error occurs | Use `await pipeline(readable, writable)` |
| `fs.readFileSync()` in server routes | Stalls all other HTTP requests on the event loop | Use `await fs.promises.readFile()` |
| Silent `process.exit(0)` on error | Obscures crashes in monitoring tools | Exit with non-zero code: `process.exit(1)` |
| Omission of `"node:"` import prefix | Risk of importing malicious npm packages squatting core names | Always import as `node:fs`, `node:path`, etc. |

---

## 6. Verification Checklist

- [ ] `"type": "module"` set in `package.json`.
- [ ] Core imports use `node:` prefix.
- [ ] Stream pipelines use `node:stream/promises`.
- [ ] Graceful shutdown handlers attached to `SIGTERM`/`SIGINT`.
- [ ] Tests pass via `node --test`.
