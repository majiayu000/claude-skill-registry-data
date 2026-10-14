---
name: bun-pro
description: Bun runtime guidance — fast installs, built-in bundler and test runner, Bun.serve APIs, and migration from Node.
category: development
---

## Overview

Bun is an all-in-one JavaScript and TypeScript runtime built on JavaScriptCore that replaces Node plus npm plus your bundler plus your test runner with a single fast binary. Its headline features are near-instant installs, a native bundler, a Jest-compatible test runner, and a high-performance HTTP server API (`Bun.serve`). Bun also aims for broad Node.js compatibility, so most existing projects run with little or no change. This skill covers using Bun effectively, migrating from Node, and knowing where the edges still are.

## When to use

- Starting a new JS/TS project where install speed and a single toolchain matter.
- Migrating a Node project to reduce toolchain complexity (one binary for runtime, bundler, tests).
- Building high-throughput HTTP services or WebSocket servers on `Bun.serve`.
- Speeding up CI with faster installs and test runs.
- Evaluating runtime tradeoffs between Bun, Node, and Deno.
- Bundling frontend assets without a separate webpack/vite setup.
- Writing CLIs where a single compiled binary simplifies distribution.

## Core concepts

- **One binary, four tools.** `bun run` (runtime), `bun install` (package manager), `bun build` (bundler), `bun test` (test runner). Learn all four before reaching for webpack/vite/jest equivalents — you often do not need them.
- **Node compatibility layer.** Bun implements `node:` builtins and npm package semantics. Most pure-JS packages work; native addons and exotic `node_modules` layouts are where breaks happen — test before switching production.
- **Bun.serve and WebSockets.** The native server API handles HTTP and WebSocket upgrades with far less overhead than framework stacks:
  ```ts
  Bun.serve({
    port: 3000,
    fetch(req) { return new Response("hi"); },
    websocket: { message(ws, msg) { ws.send("echo: " + msg); } },
  });
  ```
- **Built-in SQLite and FFI.** `bun:sqlite` gives a zero-dependency embedded database; `bun:ffi` calls native libraries directly. Both remove whole dependency classes for small services.
- **Transpiler on by default.** Bun runs TypeScript, JSX/TSX, and modern syntax natively — no tsconfig wrangling for runtime behavior (though you still want `tsc` or an editor for type errors).
- **Workspaces and lockfile.** Bun supports npm-style workspaces with its own lockfile (`bun.lockb`, binary by default — text lockfile mode gives readable diffs). Commit it for reproducible installs.
- **npm registry compatibility.** `bun install` reads the npm registry and respects `package.json` semantics, so migration is usually `bun install` plus `bun run` away.
- **Hot reloading.** `--hot` watches and reloads on file changes — fast iteration in dev, never in production.
- **Macros.** Compile-time code execution (`macro()`) for codegen-like patterns without a build plugin — powerful, but keep macros simple and deterministic.
- **Environment and dotenv.** Bun loads `.env` files automatically — convenient, but ensure secrets still come from the environment in production, not committed files.

## Practical workflow

1. **Install and verify.** Use the official install script from the Bun website, then confirm the version your team pins with `bun --version`.
   - Record the version in README/CI; Bun moves fast and behavior changes between minors.
2. **Migrate or scaffold.** In an existing Node project, run `bun install` (npm scripts keep working) or start fresh with `bun init`. Prefer the text lockfile for clean git diffs.
3. **Replace the toolchain.** Swap scripts to `bun run`, tests to `bun test` (Jest-style `describe`/`it`/`expect` mostly works), and builds to `bun build ./src/index.ts --outdir=dist --target=bun`.
   - Run the full test suite under both runtimes during migration; snapshot-test differences are the usual finding.
4. **Build the server.** Use `Bun.serve` for hot paths; keep framework code (Elysia, Hono) for routing structure. Put SQLite behind `bun:sqlite` for local-first persistence.
5. **Handle WebSockets properly.** Define `open`/`message`/`close` handlers, track connections in a Set with metadata, and implement application-level heartbeats — the same reliability rules as any socket server.
   ```ts
   const clients = new Set<ServerWebSocket<unknown>>();
   Bun.serve({
     fetch(req, server) {
       if (server.upgrade(req)) return;
       return new Response("websocket only", { status: 400 });
     },
     websocket: {
       open(ws) { clients.add(ws); },
       close(ws) { clients.delete(ws); },
       message(ws, msg) { /* handle */ },
     },
   });
   ```
6. **Compile for distribution.** `bun build --compile` produces a standalone executable — handy for CLIs and single-binary deploys without a runtime install.
7. **Containerize.** Use the official Bun image, copy `package.json` plus lockfile, run `bun install --frozen-lockfile`, then copy source — same layer-caching discipline as Node images.
8. **Monitor in production.** Track event-loop lag, memory, and request latency like any Node service; Bun's speed doesn't exempt it from observability.

## Common pitfalls

- **Assuming 100% Node parity** — check Bun's compatibility tracker for the APIs you use (streams edge cases, cluster, some `child_process` behaviors) before cutting over.
- **Binary lockfile diffs** — `bun.lockb` is unreadable in PRs; use text lockfile mode if reviewability matters to your team.
- **Native dependencies** built for Node's V8 ABI — some need rebuilds or do not work under JavaScriptCore; test on the target platform.
- **Skipping type checking** — Bun runs TS without checking it; run `tsc --noEmit` in CI or type errors accumulate silently.
- **Overusing watch mode in production** — `--hot` is for development; production needs a process manager and graceful shutdown.
- **Ignoring `--frozen-lockfile` in CI** — without it, CI can install different versions than your machine.
- **Treating Bun APIs as portable** — `Bun.serve`, `bun:sqlite`, and `bun:ffi` do not exist in Node/Deno; isolate them behind adapters if you may switch runtimes.
- **No graceful shutdown** — `Bun.serve` needs explicit signal handling to drain connections on deploy; don't rely on defaults.
- **SQLite concurrency assumptions** — `bun:sqlite` is single-writer; high-write workloads need WAL mode or a client-server DB.
- **Version churn** — pinning matters more with a fast-moving runtime; unpinned CI picks up breaking changes.
- **No `.env` discipline** — auto-loaded `.env` files committed with secrets; keep them gitignored and document required vars.
- **Forgetting `bun outdated`** — dependencies drifting because installs are so fast nobody audits; review updates regularly.
