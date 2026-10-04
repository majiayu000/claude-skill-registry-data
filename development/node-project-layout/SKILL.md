---
name: node-project-layout
description: The Node Web Only project shape - directory layout, package.json, the thin bin/ launcher, and console logging. Use when starting a Node project, deciding where a module belongs, writing package.json or .node-version, or emitting a log line. Triggers on "type":"module", engines node >=24, .node-version, bin/, src/, public/, test/, config.example.json, and console.log with level prefixes.
user-invocable: false
---

# Node Project Layout

**One Node project type: a process you launch that serves an HTTP and WebSocket backend plus a vendored single-page frontend.**

Node CLI Only, Node CLI + Web, and Node Library types do not exist here. Do not invent them; a Node project in this set is a Web Only server, and anything else is out of scope until a skill defines it.

Node Web Only parallels the Go Web Only discipline: no utils package, no logging framework, an embedded frontend, and a container or tarball artifact.

| Marker | Value |
|---|---|
| `package.json` | `"type": "module"` and `"engines": { "node": ">=24" }` |
| `.node-version` | the pinned Node version |
| Source | pure ESM under `src/` |
| Frontend | vendored under `public/` |
| Entry | a thin launcher under `bin/` |
| Stack | `node:http` plus `ws` |
| Logging | `console.*` with manual level prefixes |
| CLI framework | none |

## Layout

```
project-root/
├── package.json          # "type":"module", tiny dependency list, "engines": {"node": ">=24"}
├── .node-version         # pinned Node version
├── bin/                  # thin launcher, e.g. app.js
├── src/                  # backend: server, routing, auth, state
├── public/               # frontend: index.html, css/, js/, fonts/, vendor/
├── test/                 # node:test suites, plus an optional e2e script
├── config.example.json
├── Makefile              # vendor assets, build, assemble the artifact
└── .github/workflows/    # release
```

`bin/` holds the launcher and nothing else: it reads a `--config` path from argv and calls into `src/`. Keeping argv, process signals, and `process.exit` at the entry layer is what leaves the feature modules importable by a test.

Backend code lives in `src/` and the frontend is vendored into `public/`. Keeping them apart means the static handler serves one directory and never has to reason about which files are code.

`public/` is self-contained with nothing fetched from a CDN at run time, so the app works on an air-gapped network and leaks no visitor's address to a third party.

`test/` holds `node:test` unit suites. A live end-to-end script sits beside them and stays separate, because a unit run should not need a free port.

Config ships as `config.example.json` and a user's `config.json` is merged over built-in defaults at boot.

## package.json

```json
{
  "name": "example",
  "version": "0.1.0",
  "type": "module",
  "engines": { "node": ">=24" },
  "bin": { "example": "bin/app.js" },
  "scripts": {
    "start": "node bin/app.js",
    "dev": "node --watch bin/app.js",
    "test": "node --test",
    "test:watch": "node --test --watch"
  },
  "dependencies": {
    "ws": "^8.21.3"
  },
  "devDependencies": {
    "@tailwindcss/browser": "4.3.3",
    "lucide": "1.34.0"
  }
}
```

Every script runs real Node with no transpiler and no bundler, so what runs in development is what runs in production.

Tailwind and Lucide are development dependencies because nothing in `src/` imports them. `make vendor` copies their built files into `public/vendor/`, and the running process only ever serves those copies as static bytes.

`.node-version` pins the version for `fnm`, `nvm`, CI, and anything else that reads it:

```
24.20.0
```

Pinning an exact version rather than a major keeps a native addon compiled against the same ABI everywhere.

## The Launcher

```js
#!/usr/bin/env node
import { loadConfig } from '../src/config.js';
import { startServer } from '../src/server.js';

function configPath(argv) {
    const i = argv.indexOf('--config');
    return i !== -1 ? argv[i + 1] : undefined;
}

const config = await loadConfig(configPath(process.argv.slice(2)));
await startServer(config);
```

The argv read stays a hand-rolled few lines. A CLI framework here would add a dependency, a plugin surface, and a help system for a program that accepts exactly one flag.

Top-level `await` replaces an IIFE wrapper, since ESM modules support it directly.

## Logging

`console.*` with manual level prefixes, timestamped and sequential, with no color and no logging dependency. Go Web Only projects reach the same destination through zerolog, and the reason is shared: container logs are collected by something that neither interprets ANSI codes nor cares about a styled glyph.

```js
const ts = () => new Date().toISOString();

export const log = {
  info: (msg) => console.log(`${ts()} INFO ${msg}`),
  error: (msg) => console.error(`${ts()} ERROR ${msg}`),
  debug: (msg) => {
    if (process.env.DEBUG) console.debug(`${ts()} DEBUG ${msg}`);
  },
};
```

Errors go to stderr through `console.error` and normal output to stdout, so a caller can separate the two with a redirect.

Messages stay generic and carry no module-name prefix, because the line is already unique enough to grep for and the prefix has to be kept true as files move.
