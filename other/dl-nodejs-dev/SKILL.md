---
name: dl-nodejs-dev
description: Implement, debug, test, or optimize Node.js CLIs, libraries, background workers, and HTTP services. Use for server-side JavaScript/TypeScript, async I/O, package tooling, Express/Fastify, and Node performance work. Preserve the project's language, module system, runtime target, and framework.
---

# Node.js development

## Start from the running contract

Read `package.json`, the lockfile, runtime pins, entry points, test scripts, and nearby project instructions. Determine whether the changed module is a CLI, library, server, or worker. Run the smallest relevant existing check before changing behavior when practical.

For bugs, reproduce the input/state that fails. For features, identify success, expected failure, and the caller's observable contract. For performance, record a representative baseline before optimizing. Do not migrate JavaScript to TypeScript, CommonJS to ESM, or frameworks as an incidental improvement.

## Boundaries that matter

- Keep parsing/transport separate from reusable logic when this makes testing or reuse easier. A small script need not acquire controllers, repositories, or a dependency-injection container.
- A library must not bind ports, install process-wide handlers, read mandatory environment variables, or call `process.exit` merely because it is imported. Put those operations in the executable entry point.
- Select APIs supported by the minimum Node version in `engines` and CI. Native TypeScript execution and `.env` loading are separate features; do not assume that support for one implies the other.
- Validate external data at its boundary, including fetched JSON, paths, subprocess output, and configuration. TypeScript types do not validate runtime input.

## Async work and resources

Every started task needs an owner that awaits, cancels, or observes completion. Use bounded concurrency for collections; keep dependent writes sequential. `Promise.all` rejects early without cancelling siblings. Await all in-flight writes before deleting their temporary directory or reporting completion.

Apply a deadline to connection and body consumption, not only receipt of HTTP headers. Propagate abort signals to work that supports them, release timers/listeners in `finally`, and distinguish timeouts from invalid responses. Retry only transient, idempotent operations with a bounded policy.

Use streams and backpressure for large data. Bound captured subprocess output and in-memory queues. Put CPU-heavy work off the event loop when profiling proves it is needed. See [async and errors](references/async-and-errors.md).

## CLI and filesystem behavior

- Keep machine-readable data on stdout and diagnostics on stderr. Return a nonzero status on failure; let buffered output finish using `process.exitCode` where practical.
- Validate arguments before side effects. Invoke child processes with an argument array and no shell by default; account for Windows command shims explicitly.
- Resolve paths against the intended root. For containment checks use relative-path segments, not a string prefix; account for symlinks when the boundary is security-sensitive.
- Use exclusive creation when overwrites are forbidden. For replacing configuration or downloaded content, stage and validate first, then publish using the filesystem's supported rename behavior. Define what happens if installation fails midway.
- Test the packed artifact in a temporary installation, including `bin`, exports, relative assets, file modes, and execution outside the repository. Passing source tests does not prove packaging works.

## HTTP and persistent state

Read [API and validation](references/api-and-validation.md) for framework-specific handling. Trace authentication, object-level authorization, tenant scope, validation, persistence, and serialization as separate decisions. Do not return raw internal exception messages.

Treat retries, transactions, and concurrency as behavior: enforce uniqueness in the database, make retried external effects idempotent, bound pagination and uploads, and close clients on shutdown. Match the project's public error envelope and status codes.

## Verification and delivery

Use [testing](references/testing.md) for regression scenarios and isolated fixtures. A test should fail on the original defect, not merely assert a helper was called. Validate the documented minimum runtime as well as the development runtime when syntax or platform APIs changed.

For optimizations, compare equivalent outputs with fixed inputs, warmup, and repeated measurements; report the workload and median/tail or memory metric. Do not generalize a local microbenchmark to network or production performance.

Report the changed behavior, checks run, and untested platforms or external dependencies.

## References

- [Project structure](references/project-structure.md): choose boundaries for a new module or service; the HTTP layout is illustrative, not mandatory.
- [Async and errors](references/async-and-errors.md): cancellation, error propagation, shutdown, and bounded concurrency.
- [API and validation](references/api-and-validation.md): HTTP validation and response contracts.
- [Testing](references/testing.md): filesystem, subprocess, async, and integration regressions.
- [Tooling](references/tooling.md): module/runtime compatibility, TypeScript, scripts, and packaging.
