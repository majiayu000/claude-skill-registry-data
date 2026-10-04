---
name: ts-bun-review
description: Review TypeScript code for correct Bun API usage. Use when reviewing code that runs on Bun to verify it uses native Bun APIs instead of Node.js equivalents and follows Bun-specific patterns correctly.
---

# Bun API Review

Review code and flag issues in two categories: **Node.js APIs that have Bun-native replacements**, and **incorrect usage of Bun APIs**.

## Node.js to Bun Replacements

Flag these Node.js patterns and suggest the Bun native equivalent:

| Node.js Pattern | Bun Native | Why |
|-----------------|------------|-----|
| `fs.readFile` / `fs.writeFile` | `Bun.file().text()` / `Bun.write()` | 10x faster, no callback overhead |
| `node:http` / `node:https` server | `Bun.serve()` | Built-in, faster, simpler API |
| `express` / `koa` / `fastify` | `Bun.serve()` + `Hono` or `Elysia` | Bun-optimized frameworks |
| `node-fetch` / `undici` | Native `fetch` | Built into Bun runtime |
| `dotenv` | Native `.env` loading | Bun loads `.env` automatically |
| `bcrypt` / `bcryptjs` | `Bun.password.hash()` / `.verify()` | Native, no C bindings needed |
| `jest` / `vitest` | `bun:test` | Built-in test runner |
| `child_process.spawn` | `Bun.spawn()` / `Bun.$` shell | Simpler API, better perf |
| `ws` (WebSocket lib) | `Bun.serve()` websocket option | Built-in WebSocket server |
| `crypto.randomUUID()` | `Bun.randomUUIDv7()` | Sortable, better for DB keys |
| `node:path.resolve` | `Bun.resolveSync()` | Module resolution |
| `sqlite3` / `better-sqlite3` | `bun:sqlite` | Built-in, zero-copy |
| `glob` / `fast-glob` | `Bun.Glob` | Native, faster |
| `chalk` / `picocolors` | `Bun.color()` | Built-in ANSI color support |

## Bun API Correctness

Flag these common mistakes:

- **`Bun.file()`**: Must call `.text()`, `.json()`, `.arrayBuffer()`, or `.stream()` to actually read — the `BunFile` object is lazy
- **`Bun.serve()`**: Must store the return value if you need to call `.stop()` or `.reload()` later
- **`Bun.write()`**: Second arg can be string, Blob, BunFile, or Response — don't unnecessarily convert to string first
- **`Bun.spawn()`**: Use `Bun.$` (shell) for simple commands; use `Bun.spawn()` for streaming or fine-grained control
- **`bun:sqlite`**: Use `.prepare()` for repeated queries — don't call `.query()` in loops
- **`bun:test`**: Use `expect().toEqual()` for deep equality, not `toBe()` on objects
- **Hot reload**: Use `Bun.serve({ development: true })` in dev, not nodemon/ts-node-dev

## Out of Scope

Don't flag:
- General TypeScript quality (typing, formatting) — that's for a TS standards skill
- Business logic or architecture decisions
- Node.js APIs that Bun doesn't have native replacements for (these are fine via Node.js compat)
