---
name: node-idioms
description: "Modern Node 24+ idioms and dependency selection - pure ESM, node: builtins, top-level await, structuredClone, AbortController. Use when writing or refactoring any Node code, or when adding, auditing, or upgrading a dependency in package.json. Triggers on require, module.exports, __dirname, import.meta, node: prefixed imports, JSON.parse(JSON.stringify()), fetch timeouts, AbortSignal, and any package.json dependency change."
user-invocable: false
---

# Node Idioms

**The Node 24+ baseline every file is written to, and how a dependency earns a line in `package.json`.**

The version is pinned in `.node-version` and declared as `"engines": { "node": ">=24" }`. Development and tests run on real Node with no transpiler and no bundler, so a current standard-library helper is always available.

## Pure ESM

`package.json` sets `"type": "module"`. `import` and `export` are the only module syntax; `require`, `module.exports`, `__dirname`, and `__filename` do not appear.

```js
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';

export function makeRouter(routes) {
  return (req, res) => { /* ... */ };
}
```

A module's own directory comes from `import.meta`, which Node 24 exposes directly:

```js
const here = import.meta.dirname;
```

The longer `dirname(fileURLToPath(import.meta.url))` form is only needed when supporting a runtime older than this baseline, which nothing here does.

## Top-Level Await

ESM supports `await` at module scope, so boot-time async work needs no IIFE wrapper. The wrapper swallowed rejections unless every call site remembered a `.catch`, and a top-level rejection surfaces on its own.

```js
import { loadConfig } from './config.js';
import { startServer } from './server.js';

const config = await loadConfig(process.argv);
await startServer(config);
```

## node: Builtins

Builtins are always imported with the `node:` prefix. The prefix is unambiguous and cannot be shadowed by a dependency that happens to publish the same name.

| Need | Builtin |
|---|---|
| HTTP server and client | `node:http`, `node:https` |
| Hashing, random bytes, HMAC | `node:crypto` |
| Filesystem | `node:fs/promises`, `node:fs` |
| Paths | `node:path` |
| URLs and file URLs | `node:url` |
| Tests | `node:test`, `node:assert/strict` |
| Streams | `node:stream`, `node:stream/promises` |
| Events | `node:events` |
| Subprocesses | `node:child_process` |

```js
import { scrypt, randomBytes, timingSafeEqual } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
```

## structuredClone

`structuredClone` is a global. It replaces `JSON.parse(JSON.stringify(x))`, which silently drops `undefined`, functions, `Map`, `Set`, and `Date` types, turning a deep copy into a lossy one.

```js
const snapshot = structuredClone(config);
```

A recursive merge for config layering, where plain objects merge and everything else including arrays replaces:

```js
const isObj = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);

export function deepMerge(base, override) {
  const out = structuredClone(base);
  for (const [key, value] of Object.entries(override)) {
    out[key] = isObj(value) && isObj(out[key]) ? deepMerge(out[key], value) : value;
  }
  return out;
}
```

Arrays replace rather than concatenate, because a user overriding a list means "use these" rather than "add these to the defaults", and there is no way to remove a default under the other rule.

## AbortController

`AbortController` and `AbortSignal` are the standard cancellation primitive: they time out a fetch, unwind a server lifecycle, and cancel any API that accepts a signal.

```js
const ac = new AbortController();
const timer = setTimeout(() => ac.abort(new Error('timeout')), 5000);
try {
  const res = await fetch(url, { signal: ac.signal });
  return await res.json();
} finally {
  clearTimeout(timer);
}
```

`AbortSignal.timeout(ms)` covers the common case without the manual timer:

```js
const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
```

Process signals drive graceful shutdown the same way:

```js
process.on('SIGTERM', () => server.close());
```

## Dependency Selection

A `node:` builtin goes first whenever it can reasonably do the job. A well-scoped Web Only app has a very short dependency list, and every entry on it is a version to track and a supply chain to trust.

A dependency is added for a genuine gap a builtin cannot cover. A spec-complete WebSocket server is one, since `node:http` provides the upgrade event but not the protocol. A frontend package vendored into `public/` is another.

| Package | Version | Fills |
|---|---|---|
| `ws` | `8.21.3` | WebSocket server, which `node:http` does not implement |
| `@xterm/xterm` | `6.0.0` | terminal frontend, when the app has one |

Judge whether a dependency is justified rather than whether it appears on a list. A fixed allow-list either blocks legitimate work or grows until it means nothing.

Prefer the well-maintained standard choice over the niche alternative, because its breaking changes are documented and its issues are already answered.

Dependencies stay at their latest stable version. Prefer stable over pre-release, and read the release notes before a major bump rather than after the build breaks. Auditing means scanning `package.json` and any pinned asset versions in the Makefile, checking each against its current release, and bumping deliberately.

### Native addons

A C++ N-API addon is a real cost, not just another dependency. A pure-JS app can ship as one self-contained binary; the moment a compiled `.node` file is in the tree that path closes, and the release becomes a per-platform bundle built on an arch-native runner. Reach for one only when a builtin or a pure-JS package genuinely cannot do the job, such as a real PTY.
