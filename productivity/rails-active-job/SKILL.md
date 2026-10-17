---
name: rails-active-job
description: Use when creating, changing, reviewing, debugging, testing, or operating Rails Active Job and queue-backed background processing.
license: MIT
---

# Rails Active Job

## Purpose

Treat a background job as a distributed execution contract, not merely a method moved off the request thread.

A job has at least these boundaries:

```text
enqueue -> serialize -> persist -> schedule -> claim -> execute
       -> retry/discard/fail -> observe -> recover/replay
```

The current Rails guide documents Active Job as the common interface for background jobs and Solid Queue as the default backend in Rails 8+. Solid Queue provides delayed jobs, concurrency controls, priorities, recurring tasks, and database-backed execution. 

## Activate when

- creating or changing `ApplicationJob` or Active Job classes
- moving synchronous work to the background
- changing queues, priorities, scheduling, or bulk enqueue behavior
- designing retries, backoff, discard rules, or failure reporting
- changing job arguments or serialization
- changing enqueue behavior inside database transactions
- adding idempotency/deduplication
- adding concurrency limits
- using or reviewing Rails 8.1 Active Job Continuations (`ActiveJob::Continuable`)
- configuring Solid Queue workers/processes/dispatchers/schedulers
- adding recurring jobs
- changing job shutdown/recovery semantics
- testing asynchronous workflows
- debugging stuck, duplicated, lost, retried, or unexpectedly discarded jobs
- changing job observability or operational recovery

## Repository inspection

Inspect:

1. Ruby/Rails version and Active Job API available in that version
2. queue adapter and adapter-specific gem/version
3. `ApplicationJob` and inherited job bases
4. job classes and queue naming
5. job tests and test helpers
6. database transaction boundaries around `perform_later`
7. retry/discard/error-reporting configuration
8. worker/queue configuration
9. concurrency settings and downstream capacity
10. recurring-task configuration
11. deployment/restart/shutdown behavior
12. serialization/custom serializers/GlobalID usage
13. idempotency or uniqueness mechanisms
14. monitoring, structured logs, metrics, and failed-job tooling
15. existing job conventions before introducing new abstractions

## Job boundary

A useful job should make explicit:

```text
input contract
queue
priority
execution side effects
retry policy
discard policy
idempotency requirement
concurrency boundary
transaction boundary
observability
failure/recovery semantics
```

Do not hide business behavior in a giant `perform` method merely because it runs asynchronously. Keep domain/application behavior in the repository's appropriate service/domain layer and make the job a durable execution boundary.

## Decision rules

1. Resolve the Rails, Active Job, and queue-adapter versions; adapter semantics decide enqueue timing, retries, and concurrency.
2. Classify the change: arguments, idempotency, and enqueue timing; retry, discard, and error reporting; concurrency, queues, scheduling, and bulk enqueue; or callbacks, shutdown, observability, security, and testing.
3. Load the matching reference below before changing behavior; a new job needs at least the arguments-and-idempotency and retries references.

## Critical invariants

- Do not use an in-memory mutex as an idempotency mechanism across processes or hosts.
- Do not retry deterministic bugs, malformed input, authorization failures, or permanent domain-invalid states.
- Do not rescue `StandardError` and silently return success.
- Do not assume authorization at enqueue time remains valid later.
- Never log secrets or sensitive payloads merely for debugging.
- Never claim a job is reliable from a unit test that only exercises `perform`.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change alters job arguments or serializers, duplicate-execution safety, or enqueueing from a transaction | [references/arguments-idempotency-enqueue.md](references/arguments-idempotency-enqueue.md) | Arguments and serialization; Idempotency; Transactions and enqueue timing | `activejob-argument-serialization-contract`, `custom-activejob-serializer-contract`, `idempotent-job`, `transactional-job-enqueue` |
| a change alters retry_on/discard_on, backoff, failure classification, or error reporting | [references/retries-and-failures.md](references/retries-and-failures.md) | Retry policy; Discard policy; Retry storm prevention; Error reporting | `job-retry-policy` |
| a change adds concurrency limits, queues or priorities, recurring/scheduled jobs, or bulk enqueue | [references/concurrency-queues-scheduling.md](references/concurrency-queues-scheduling.md) | Concurrency controls; Queues and priorities; Scheduling and recurring tasks; Bulk enqueue | `concurrency-controlled-job`, `scheduled-maintenance-overlap-contract` |
| a change adds job callbacks, affects worker shutdown, job telemetry, or job security, or needs job tests | [references/operations-and-testing.md](references/operations-and-testing.md) | Callbacks; Shutdown and graceful termination; Observability; Security; Testing | `rspec-job-and-mail-enqueue` |
| the repository's queue adapter resolves to `:sidekiq` (Sidekiq-specific operational surface: `sidekiq_options`, Web UI security, Redis connection pooling, retry/dead-set, sidekiq-cron, sharding, Sidekiq 6→7 migration) | [references/sidekiq-adapter.md](references/sidekiq-adapter.md) | Sidekiq operational surface; adapter-specific configuration; Active Job `JobWrapper` interop | none |

## Debugging procedure

For a failing or duplicated job:

```text
1. capture job class, job_id, queue, arguments, attempt
2. identify adapter and version
3. determine whether enqueue succeeded
4. inspect serialized arguments/deserialization
5. inspect worker/queue selection
6. inspect transaction boundary
7. inspect retry/discard handlers
8. inspect idempotency guarantees
9. inspect concurrency controls
10. inspect downstream failure/rate limiting
11. inspect worker shutdown/restarts
12. replay safely when possible
```

Never diagnose a duplicate side effect as "Rails ran it twice" without tracing enqueue, claim, retry, and application-level idempotency.

## Agent review checklist

- [ ] Rails/Ruby/Active Job/adapter versions resolved
- [ ] arguments are stable and serializable
- [ ] idempotency behavior is explicit
- [ ] transaction/enqueue semantics are understood
- [ ] retry exceptions are genuinely transient
- [ ] retry count/backoff are justified
- [ ] discard behavior is intentional
- [ ] concurrency boundary is explicit
- [ ] queue/priority choice is justified
- [ ] downstream capacity is respected
- [ ] recurring/scheduled behavior is durable
- [ ] shutdown/restart behavior is safe
- [ ] payloads do not leak secrets
- [ ] tests cover failure and retry paths
- [ ] observability supports diagnosis/recovery
- [ ] final diff is narrow

## Anti-patterns

- using `rescue StandardError; nil; end` in `perform`
- infinite immediate retries
- retries for permanent validation/authentication failures
- using sleep loops inside jobs as a scheduler
- relying on process-local state for distributed idempotency
- assuming enqueue inside a transaction always waits for commit
- passing huge Active Record objects or entire request state as arguments
- putting core business logic into job callbacks
- creating a queue per job without operational reasoning
- using concurrency controls when simple worker capacity is the real requirement
- bulk enqueuing without measuring queue-store pressure
- logging credentials or full sensitive payloads
- treating successful enqueue as successful execution

## Verification

Never claim a job is reliable from a unit test that only exercises `perform`.

Verify the enqueue contract, execution behavior, failure policy, and relevant adapter/worker configuration.

For Rails/Solid Queue changes, inspect actual queue configuration and use version-supported commands/tests.

## Rails 8.1 current framework considerations

- Rails 8.1 exposes `ActiveJob::Continuable` for resumable multi-step jobs. Inspect the repository's supported Rails version and job adapter before using continuations.
- Design each continuation step around durable progress and restart semantics; a step boundary is not a substitute for idempotency or explicit retry behavior.

## Source foundation

Primary Rails guidance:
- Active Job Basics: https://guides.rubyonrails.org/active_job_basics.html
- Rails Testing: https://guides.rubyonrails.org/testing.html
- Solid Queue: https://github.com/rails/solid_queue

Use the target Rails/Active Job/adapter version as the compatibility authority when APIs or semantics differ.

## Active Job/background-job changes

For background-job changes:
- resolve the Rails/Active Job/queue-adapter versions first;
- inspect ApplicationJob and existing job conventions;
- make serialization and idempotency explicit;
- classify retryable versus permanent failures;
- inspect transaction/commit semantics when enqueueing from database transactions;
- analyze concurrency and downstream capacity;
- verify queue/worker configuration and shutdown behavior when operational behavior changes;
- test enqueue, perform, failure, retry/discard, and duplicate-execution behavior as applicable.
