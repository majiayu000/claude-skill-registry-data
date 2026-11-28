---
name: concurrency-reasoning
description: Async/concurrent/streaming discipline — five questions (overlapping runs, check-then-act, mutation across await, response ordering, cancellation), guard scope, fan-out failure, idempotent retries, shared-state audit, race amplification. Use for async fan-out (Promise.all, gather), streams/SSE/websockets, queue workers, cron jobs, webhooks, caches, locks, retries, and bugs described as "sometimes", "duplicate", "double-charged", or "only under load".
---

# Concurrency Reasoning

Concurrency bugs don't announce themselves in review — the code reads fine sequentially. Weak reasoning reads top to bottom and calls it correct. Strong reasoning asks a fixed set of questions about every async surface, because the compiler won't.

## Step 0 — Inventory the surfaces

Before writing or reviewing, list every await/callback/handler/worker in the diff and every piece of state it touches that outlives one invocation (module globals, singletons, caches, class fields, DB rows, files). The questions below are asked per item on that list, not once per file.

## The core question set

1. **What if this runs twice, overlapping?** Two clicks, two requests, a retry racing the original, cron overlapping its previous run, a webhook delivered twice. If the answer is corrupted state or a double effect, add a guard: idempotency key, unique constraint, mutex, request de-dupe, disable-on-click.
2. **What happens between the check and the act?** Every `if (exists) then update` on shared state is a TOCTOU window. Close it with an atomic operation (upsert, compare-and-swap, unique constraint, transaction) — not a smaller window.
3. **Who else mutates this while I await?** Every `await` is a yield point: module variables, caches, closure-captured objects can change under you. Re-read after the await if it matters; don't carry pre-await reads across the gap.
4. **What order do these land in?** Two in-flight requests resolve in either order. If responses update the same state (search-as-you-type, autosave), guard with sequence numbers, latest-wins checks, or cancel the superseded one.
5. **What happens on cancellation/unmount/disconnect mid-flight?** Handlers firing after teardown need abort signals, mounted flags, or subscription cleanup. Partial effects from an aborted multi-step operation need cleanup or resumability.

## Guard scope must match concurrency scope

An in-process mutex or in-memory de-dupe set guards one process only. If the service runs as multiple instances, workers, or serverless invocations, the guard must live where the contention is: database unique constraint, row lock, atomic compare-and-swap in the shared store, or a distributed lock with a lease. Name which one in the report.

## Fan-out

For `Promise.all`/`gather`-style fan-out, decide what happens when one of N fails (abort the rest, collect all outcomes, report partial success as partial) and bound the concurrency — unbounded fan-out over a list of unknown size is a self-DoS.

## Retries and exactly-once

- Retry only idempotent operations, or make them idempotent first (idempotency keys, natural unique constraints). A retried "create" without one is a duplicate.
- Backoff + jitter + a cap. Immediate retry in a loop is a DoS on your own dependency.
- Distinguish "the request failed" from "the response failed" — the operation may have succeeded server-side. Design reads-back or upserts accordingly.

## Shared-state audit

For each state item in the Step 0 inventory: who writes it, from how many concurrent contexts, and what serializes those writes? "Nothing serializes them, but it's probably fine" is a bug report from the future. Put the answer in the report.

## Debugging suspected races

- Flaky test → don't rerun until green. Amplify: run 20–100× in a loop, add load, add `sleep` at suspected interleaving points to widen the window until it fails deterministically.
- Bisect by interleaving, not by code: log timestamps + IDs at each async boundary and reconstruct the actual order of the failing run.
- The fix must name the interleaving it prevents, and a test must force that interleaving (two calls with a barrier or injected delay) and fail before the fix. "Added a lock and it stopped failing" without knowing the race is a hidden deadlock waiting.

## Deadlock/starvation reflexes

Consistent lock ordering; never hold a lock across an await/IO; timeouts on anything that waits on another party; bounded queues (an unbounded queue turns backpressure into an OOM).
