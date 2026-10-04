---
name: ts-deno-review
description: Review TypeScript code for correct Deno API usage. Use when reviewing code that runs on Deno to verify it uses native Deno APIs instead of Node.js equivalents, follows the permissions model correctly, and uses Deno-specific patterns.
---

# Deno API Review

Review code and flag issues in three categories: **Node.js APIs that have Deno-native replacements**, **incorrect Deno API usage**, and **permissions model violations**.

## Node.js to Deno Replacements

Flag these Node.js patterns and suggest the Deno native equivalent:

| Node.js Pattern | Deno Native | Why |
|-----------------|-------------|-----|
| `fs.readFile` / `fs.writeFile` | `Deno.readTextFile()` / `Deno.writeTextFile()` | Native, permission-aware |
| `node:http` / `express` | `Deno.serve()` | Built-in, simpler, faster |
| `node-fetch` / `undici` | Native `fetch` | Built into Deno runtime |
| `dotenv` | Native `.env` loading (`--env` flag or `Deno.env`) | Built-in since Deno 1.38 |
| `jest` / `vitest` | `Deno.test()` + `@std/testing` | Built-in test runner |
| `child_process` | `Deno.Command` | Native subprocess API |
| `path` module | `@std/path` | Deno standard library |
| `lodash` (common utils) | `@std/*` modules | Standard library covers most cases |
| `npm:chalk` | `@std/fmt/colors` | Standard library, no npm needed |
| `npm:dotenv` | `Deno.env.get()` + `--env` flag | Built-in |

## Deno API Correctness

Flag these common mistakes:

- **`Deno.serve()`**: Returns a `Deno.HttpServer` — must `await server.finished` in scripts or the process exits immediately
- **`Deno.readTextFile()`**: Is async — don't forget `await`; use `Deno.readTextFileSync()` only in scripts, not servers
- **`Deno.Command`**: Must call `.output()` or `.spawn()` after construction — the constructor doesn't execute
- **`Deno.test()`**: Use `@std/testing/bdd` (`describe`/`it`) for complex test suites; bare `Deno.test()` for simple cases
- **Import maps**: Use `deno.json` `imports` field, not a separate `import_map.json`
- **`@std` imports**: Must pin version (`@std/path@1.0.0`), not use bare `@std/path`
- **Fresh/Oak**: If using a framework, verify it's Deno 2.x compatible

## Permissions Model

Flag code that would fail without proper permissions:

| API | Required Permission |
|-----|-------------------|
| `Deno.readTextFile()`, `Deno.writeTextFile()` | `--allow-read`, `--allow-write` |
| `fetch()` to external URLs | `--allow-net` (specify domains) |
| `Deno.env.get()` | `--allow-env` (specify vars) |
| `Deno.Command` | `--allow-run` (specify binaries) |
| FFI (`Deno.dlopen`) | `--allow-ffi` |

- **Must** document required permissions in README or `deno.json` tasks
- **Should** use granular permissions (`--allow-read=./data`) over broad (`--allow-read`)
- **Should** define `deno.json` tasks with explicit permissions instead of using `--allow-all`
- **Never** recommend `--allow-all` for production

## Out of Scope

Don't flag:
- General TypeScript quality (typing, formatting) — that's for a TS standards skill
- Business logic or architecture decisions
- npm packages used via `npm:` specifier that don't have Deno equivalents (these are fine)
