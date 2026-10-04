---
name: worker-job-testing
category: qa
description: Use when the task has a background job, queue consumer, scheduler or webhook - firing the real trigger, polling for the side effect, and the retry, idempotency and poison-message cases
---
# Worker & Async Job Testing

## Overview

A worker has no HTTP response to assert on. You verify it the way the product uses it: fire the real trigger, then observe the side effects. Reading the worker's source to convince yourself it works is not testing.

## The Pattern

1. **Identify the worker processes** the repo defines (a `cmd/worker`, a queue consumer, a scheduler) and start them alongside the API with logs captured to a file.
2. **Trigger through the product path.** Prefer the API call or user action that enqueues the job over inserting queue rows by hand — the enqueue side is part of what you are testing. Hand-crafted messages are a fallback for hard-to-reach cases and must match the real schema.
3. **Assert on observable outcomes**: the DB state the job must produce, the outbound request it must make (assert against the stub's received requests — test-data-and-stubs), the file/notification/event it must emit, and the log line that marks completion.
4. **Poll, don't guess.** Async means eventually: loop with a timeout (`for i in $(seq 30); do check && break; sleep 1; done`) instead of one arbitrary sleep. A job that needs longer than the product's own expectation is a finding.

## The scenarios a worker always owes you

| Scenario | How | PASS looks like |
|----------|-----|-----------------|
| Happy path | real trigger → poll | expected side effect appears, completion logged |
| Idempotency / duplicate delivery | fire the same trigger twice | effect applied once, no double-charge/double-send |
| Dependency failure | WireMock returns 5xx/timeout | retries with backoff per config, then DLQ/parked state — not an infinite hot loop |
| Poison message | malformed payload | job fails contained: logged, quarantined, worker keeps processing others |
| Restart mid-work | kill the worker during a job, restart | job resumes or reruns safely; nothing half-applied |

Skip a row only if the task's scope genuinely excludes it — say so in the scenario plan rather than silently.

## Evidence

Per scenario: the trigger command, the poll/check command, and the observed side effect (query output, WireMock request log, log lines). "The worker probably picked it up" is not evidence.

## Red Flags

- Only the happy path was exercised → the failure paths are where workers rot.
- You asserted on a log line alone when the job's purpose is a DB/external effect.
- The test enqueued directly into the queue table when a product API for it exists.
