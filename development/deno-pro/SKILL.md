---
name: deno-pro
description: Deno runtime guidance — TypeScript-first development, permissions, standard library, and deploying Deno apps.
category: development
---

## Overview

Deno is a secure-by-default JavaScript/TypeScript runtime built by the creator of Node.js, designed to fix Node's historical pain points: it ships TypeScript support, a built-in toolchain (formatter, linter, test runner), and URL-based imports instead of a package manager by default. Its permission model — no file, network, or environment access unless explicitly granted — makes it a strong choice for running untrusted or third-party code. This skill covers practical Deno development, dependency management, and deployment.

## When to use

- Starting a new TypeScript backend, API, or edge function where you want zero toolchain config.
- Running third-party or generated code and needing sandbox-style permissions.
- Choosing between Deno, Node, and Bun for a project.
- Publishing a library for the Deno ecosystem (JSR) or cross-runtime code.
- Deploying to Deno Deploy or containerizing a Deno service.
- Building CLIs or scripts where a single binary with no install step is valuable.
- Evaluating supply-chain security for JavaScript dependencies.

## Core concepts

- **Secure by default.** Scripts run with no permissions. Grant explicitly with flags (`--allow-net`, `--allow-read`, `--allow-env=KEY`) or prompt the user. Prefer the narrowest scope: `--allow-net=api.example.com` beats blanket `--allow-net`.
- **TypeScript first-class.** No build step: Deno type-checks and runs `.ts` directly. Note that type checking is skipped with `--no-check` for speed — use it in dev, keep checks in CI.
- **URL and JSR imports.** Dependencies come from URLs or the JSR registry (`jsr:@std/http/file-server`). Pin versions in an import map (`deno.json` `imports`) so builds are reproducible and reviewable.
- **Built-in toolchain.** `deno fmt`, `deno lint`, and `deno test` replace Prettier/ESLint/Jest for most projects. Use them; the zero-config defaults are deliberately opinionated.
- **Standard library (`@std`).** JSR's `@std/*` packages (http, cli, testing, uuid, datetime) are the blessed equivalents of npm staples — prefer them over random URL imports.
- **Node compatibility.** Deno supports `node:` specifiers and a growing share of npm packages via `npm:` imports and `package.json` interop. It is good but not perfect — test npm deps, especially native ones, before committing.
- **Fresh and islands architecture.** For server-rendered web apps, the Fresh framework ships zero JS to the client by default, hydrating only interactive "islands" — a good fit for content-heavy sites.
- **Deno KV.** Built-in key-value store (backed by SQLite locally) for sessions, caches, and queues without provisioning a database — ideal for small services and edge deployments.
- **Permissions as documentation.** The flags a program needs are a readable manifest of what it touches — review them in code review like you would dependency changes.
- **Single-binary compile.** `deno compile` bundles your app into a standalone executable with no runtime install — excellent for CLIs and simple distributions.

## Practical workflow

1. **Install and pin the version.** Use the official installer and record the version in CI:
   ```bash
   deno --version
   ```
   - Pin the exact version in CI config so builds don't drift with new releases.
2. **Initialize the project.** Create `deno.json` with tasks and an import map:
   ```json
   {
     "tasks": { "dev": "deno run --watch --allow-net main.ts", "test": "deno test --allow-all" },
     "imports": { "@std/http": "jsr:@std/http@1" }
   }
   ```
   - Keep tasks as the canonical way to run things; document any required env vars alongside.
3. **Write with explicit imports.** Use `jsr:`/`npm:`/`node:` specifiers; avoid bare URLs scattered through code — centralize them in the import map.
4. **Develop with permissions in mind.** Run with the minimum flags your app needs; when a new permission prompt appears in dev, decide deliberately before adding the flag to the task definition.
   - Start restrictive and widen only with justification; record why each permission exists.
5. **Test and lint.** `deno test` with `@std/testing` assertions and `deno lint && deno fmt --check` in CI catch most issues.
   - Use `deno test --coverage` and enforce a coverage floor on critical modules.
6. **Benchmark hot paths.** `deno bench` for micro-benchmarks of parsing, serialization, or crypto code before optimizing blindly.
7. **Compile for distribution.** `deno compile --allow-net --output myapp main.ts` produces a single binary for CLIs or simple deploys.
8. **Deploy.** For containers, use the official minimal image and a multi-stage build; for Deno Deploy, push from git. Cache dependencies at build time (`deno cache main.ts`) so cold starts stay fast.
   - Bake the permission flags into the container CMD so production can't accidentally run with wider access.

   - When a permission error appears, run with `--allow-all` temporarily to identify what's needed, then narrow it back down — never ship the broad flags.

   ```bash
   # find which permissions a script actually needs
   deno run --allow-all main.ts   # works? now bisect:
   deno run --allow-net --allow-read main.ts
   ```

## Common pitfalls

- **Granting `--allow-all`** in production because a permission prompt was annoying — defeats the security model; scope flags per environment.
- **Unpinned URL imports** (`https://deno.land/x/.../mod.ts`) that silently upgrade and break builds — always pin with an import map and lockfile (`deno.lock`).
- **Assuming npm parity** — native modules and deep `node_modules` hacks often fail; verify each npm dependency under Deno before relying on it.
- **Skipping type checks** with `--no-check` everywhere — fast in dev, but CI must run `deno check` or type errors ship.
- **Using unstable APIs** without the `--unstable` flag pinned and documented — they can change between releases.
- **Forgetting the lockfile** in CI — `deno.lock` is your reproducibility guarantee; commit it.
- **Treating `deno.json` tasks as a full build system** — for complex pipelines (codegen, multi-service), pair with a real task runner.
- **Permissions drift** — flags accreting over time until the app effectively has `--allow-all`; audit the task definitions periodically.
- **No graceful shutdown** — Deno handles SIGTERM, but long-lived connections still need explicit draining in server code.
- **Developing against latest, deploying pinned old** — version skew between dev and prod causing "works on my machine"; pin everywhere.
- **Vendoring ignored** — remote-only dependencies breaking air-gapped or flaky-network deploys; `deno vendor` for critical services.
- **Fresh as a SPA** — skipping islands architecture and shipping a JS bundle for static content; Fresh's zero-JS default is the point.
