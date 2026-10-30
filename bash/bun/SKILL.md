---
name: bun
description: Develop, test, build, and troubleshoot JavaScript or TypeScript applications using the Bun runtime and package manager. Use for bun.lock, bun:test, Bun.serve, Bun.build, or Node-to-Bun compatibility work.
---

# Bun

Check `bun --version`, the repository's `packageManager` field, lockfiles, scripts,
and `bunfig.toml` before choosing commands. Keep the project's package manager and
runtime choices; using Bun to run a file does not require migrating its dependencies.

## Dependencies and scripts

- Current Bun lockfiles are text `bun.lock`; older projects may use binary
  `bun.lockb`. Commit the lockfile. Do not create another manager's lockfile
  merely to run an existing project.
- Use `bun install --frozen-lockfile` in CI. Change dependencies deliberately with
  `bun add` / `bun add -d` or the project's selected package manager.
- `bun run <script>` runs a package script; `bun <file.ts>` runs a file.
  `bunx <package>` can fetch and execute a package, so prefer an already installed
  project binary when its version matters. Read `--help` for unfamiliar flags.
- A native dependency can fail because its lifecycle script was blocked.
  Inspect the package and Bun's lifecycle output before changing
  `trustedDependencies`. An explicit list replaces Bun's default trust list;
  include only the packages this project needs to execute.

Do not assume Node compatibility is complete. Check the actual package's native
addons, Node APIs, and subprocess behavior under the project's Bun version.

## TypeScript and tests

Bun runs TypeScript directly, but ordinary `bun run`, `bun test`, and
`bun build` do not establish type correctness. Run the repository's typecheck
script. Current Bun supports `bun check` and `--check`; older versions may need
`tsc --noEmit`. Preserve the project's compiler baseline rather than changing
its TypeScript version or tsconfig just to use a newer checker.

For Bun APIs, install the project-compatible `@types/bun` and include `"bun"`
in the tsconfig `types` list. Use `noEmit` when Bun supplies runtime transpilation.

```ts
import { expect, test } from "bun:test";

test("rejects a missing identifier", async () => {
  const response = await handler(new Request("http://localhost/items/"));
  expect(response.status).toBe(400);
});
```

Use the existing test runner unless the task calls for a change. Bun's Jest-like
API does not imply every Jest plugin, mock, or configuration works unchanged.
Await async assertions and release servers, subprocesses, and temporary files in
teardown or `finally`; retries must not conceal a deterministic failure.

## HTTP and build targets

Use Web `Request`/`Response` with `Bun.serve`. For a local smoke test, bind to
`127.0.0.1` with `port: 0`, read `server.url`, and call
`await server.stop(true)` in cleanup. Resolve paths with
`new URL("/health", server.url)`; `server.url` already ends with a slash.
Production graceful shutdown can use `await server.stop()` to let requests finish.

Choose `bun build --target=bun`, `--target=node`, or `--target=browser`
according to the runtime that will execute the result. A successful Bun-target
build does not prove Node or browser compatibility. Run the built artifact in its
intended runtime. `--compile` creates an executable and has separate target and
asset requirements; inspect the current CLI help before using it.

## Verify the requested behavior

Use the project's install, typecheck, test, and build commands. Check at least one
failure path at the changed boundary. For a dependency-free example of an actual
HTTP request, server cleanup, and running a built module, run:

```bash
bun test /absolute/path/to/this/skill/scripts/smoke.test.ts
```

The fixture uses loopback networking and temporary files; it needs no registry or
external service. It checks Bun itself and is a starting example, not a substitute
for the application's own tests.

## Primary references

Read the relevant current documentation and the installed CLI's help when a
version-specific detail matters:

- [Lockfile](https://bun.com/docs/pm/lockfile)
- [Lifecycle scripts](https://bun.com/docs/pm/lifecycle)
- [Type checking](https://bun.com/docs/runtime/check)
- [HTTP server and lifecycle](https://bun.com/docs/runtime/http/server)
- [Test runner](https://bun.com/docs/test)
- [Build targets](https://bun.com/docs/bundler)

Source reviewed: `oven-sh/bun@179664ea89f402c02af3fcd13b9bafeff1b7bcfd`,
`docs/pm/{lockfile,lifecycle}.mdx`, `docs/runtime/{typescript,check}.mdx`,
`docs/runtime/http/server.mdx`, and `docs/test/writing-tests.mdx`.
