---
name: bun
description: Bun runtime and toolkit — server, bundler, package manager, test runner, SQLite, and Node.js compatibility.
trigger: bun, bun.sh, bun runtime, bun.serve, bun file, bun install, bun build, bun test, bunx, node.js compatibility
---

# Bun

## Overview
Bun is an all-in-one JavaScript runtime and toolkit designed for speed. It replaces Node.js, npm, npx, Jest, Webpack, and ts-node with a single binary.

## Core APIs

### bun.serve
HTTP server with built-in request/response handling. Supports TLS, streaming, and WebSockets natively.

### bun.file
Lazy file reader with BLOB support. Works with `Response`, `ArrayBuffer`, and streaming interfaces.

### bun:sqlite
Built-in SQLite3 binding. Synchronous API, no C dependencies. Supports prepared statements, transactions, and WAL mode.

## Package Management
- `bun install` — fast lockfile-free installs with global cache
- `bun add` / `bun remove` — dependency management
- `bunx` — npx-compatible package runner

## Build System
Bun.build bundles JavaScript/TypeScript for browser and server. Supports entry points, external modules, minification, source maps, and targeting.

## Plugin System
Bun plugins intercept module resolution and transformation. Useful for loaders (CSS, YAML, .env) and custom transpilation.

## Test Runner
`bun test` provides Jest-compatible API (`describe`, `it`, `expect`) with TypeScript and JSX support, snapshots, and lifecycle hooks.

## Node.js Compatibility
Bun aims for full Node.js API compatibility. Most npm packages work without modification. Built-in support for `node:*` modules, CommonJS, and ESM.
