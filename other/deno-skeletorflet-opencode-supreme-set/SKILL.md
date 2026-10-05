---
name: deno
description: Secure JavaScript/TypeScript runtime with URL imports, KV store, built-in tooling, npm compatibility, and permission-based security.
trigger: deno, deno runtime, deno serve, deno compile, deno run, deno kv, url imports, permissions, --allow-net
---

# Deno

## Permissions Model
Secure by default. Scripts need explicit `--allow-read`, `--allow-write`, `--allow-net`, `--allow-env`, or `--allow-run` flags. Permissions can be scoped to specific paths or domains.

## Standard Library
Curated std library at `jsr.io/@std/`. Includes HTTP, filesystem, streams, testing, encoding, and crypto. Zero external dependencies.

## URL Imports
Modules imported directly from URLs. No node_modules or package.json needed. Supports npm specifiers (`npm:express`) and JSR specifiers.

## Deno.serve
Built-in HTTP server with simple `Deno.serve(handler)`. Supports HTTP/1.1, HTTP/2, and TLS.

## KV Store
`Deno.openKv()` provides SQLite-backed key-value storage. Supports atomic operations, transactions, secondary indexes, and queue listeners.

## npm Compatibility
Use npm packages via `npm:` specifiers. Built-in Node.js compatibility layer works with most packages.

## Deno compile
Bundle scripts into standalone executables. Includes runtime and dependencies in a single binary.

## Testing
`Deno.test()` with code coverage, resource sanitization, and leak detection built in.
