---
name: resource-lifecycle
description: Every acquired resource — connection, file, lock, transaction, subprocess, timer, listener, stream, temp file, cursor — has an owner and a release on every exit path, including errors and cancellation. Use when writing or reviewing code that opens, connects, spawns, subscribes, schedules, locks, begins a transaction, or creates anything with a close/dispose/unsubscribe counterpart, and for bugs described as "slow after a while", "too many open files", "pool exhausted", or "process won't exit".
---

# resource-lifecycle

Weak resource handling opens, uses, and closes on the happy path; the first exception leaks the handle, and the leak surfaces a week later as "pool exhausted" or a process that never exits. Strong handling decides who owns each resource at the moment it is acquired and writes the release before the use.

## 1. Inventory the acquisitions

Before finishing a diff, grep it for every acquire: `open(`, `connect`, `spawn` / `exec` / `Popen`, `begin` / `transaction`, `lock` / `acquire`, `setInterval` / `setTimeout` / `schedule`, `addEventListener` / `.on(` / `subscribe`, `createReadStream` / `pipe`, `mkstemp` / `tmp`, `cursor`, `Session(`, `new Client(`. One line per hit: `resource → owner → release site`. A hit with no release site is a leak until proven otherwise.

## 2. Use the scoped construct the language gives you

- Python `with`, JS/TS `try/finally` (or `using` / `await using` where supported), Go `defer` on the line after the acquire, Java try-with-resources, Rust drop. The release lives in the construct, not at the bottom of the function.
- Check the release runs on every exit: early `return`, `continue`, thrown error, and in async code, cancellation and abort (see concurrency-reasoning). An `AbortSignal`, `CancelledError`, or context cancellation must still reach the release.
- Release in reverse acquisition order. A release that can itself throw is wrapped so the remaining releases still run.

## 3. Ownership across boundaries

- A function that returns an open resource (stream, connection, cursor) hands ownership to the caller. Say so in its name or docstring (`open_…`, `acquire_…`) and check every caller closes it. Prefer returning the result and closing inside.
- A resource held in a field or module global needs a shutdown hook. Find where the project shuts down (signal handler, `app.on('close')`, `atexit`, lifespan) and register the release there.
- Callbacks registered in a lifecycle (React effect, component mount, plugin activate) are unregistered in the matching teardown. Every `on` has an `off`; every `setInterval` has a `clearInterval`.

## 4. Pools, transactions, subprocesses, temp files

- Pools: acquire with a timeout; return in `finally`; never hold a connection across an `await` on something unrelated (an external HTTP call). Pool size comes from config, not a literal.
- Transactions: commit on success, roll back on any exception, and never hold one open across a user or network wait. A "transaction" opened inside another is a savepoint or a bug; check which the library does.
- Subprocesses: read or redirect both stdout and stderr (an unread pipe fills and deadlocks the child); set a timeout; on timeout kill and then `wait` so no zombie remains; close the pipes.
- Temp files and directories: create through the platform API, remove in `finally`, and never present one as the result.

## 5. Bound what accumulates

Caches, listener lists, in-memory queues, and pending-promise maps grow forever unless something removes entries. Name the eviction: TTL, max size, or removal on completion. An unbounded `Map` keyed by request ID is a leak with extra steps (see perf-sanity).

## 6. Prove it

Exercise the error path once: force an exception after the acquire (bad input, a mocked failure) and observe that the release ran — pool count back to baseline, open-handle count flat, the process exits without `process.exit()`, the temp dir empty. Then run the operation 100 times in a loop and watch the count. A leak invisible once is obvious at 100.

## Reporting

Paste the step-1 inventory with each release site, and the step-6 observation. "Closes the connection" without an observed run is a claim, not a result.
