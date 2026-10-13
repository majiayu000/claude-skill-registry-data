---
name: add-job
description: Add a background job, queue, scheduled task or domain-event consumer, in TypeScript or in the Python service. Use when work should run outside the request (sending, processing, syncing, cleanup) or when a service must react to an event another service emits.
---

# Add a job or event consumer

Every queue and payload is declared once, in `packages/jobs/src/queues.ts`. Producers can
only enqueue what type-checks there, and consumers re-validate with `parseJob`, because
producer and consumer can be different versions during a rollout.

## A job on a queue

1. In `queues.ts`, add the job (a zod payload) to an existing queue, or a new queue with
   its `options` (retries, `removeOnComplete`, `removeOnFail`). Payloads carry ids, not
   copies of rows. Work that must never be lost goes through the outbox (below), not a
   direct job.
2. Produce: `createProducer("<queue>", redis)`, then `add("<job>", payload, { jobId })`.
   `jobId` is required: a UUIDv7 or a natural key, so a retried request enqueues once.
3. Consume in the owning service: `BullModule.registerQueue({ name, prefix: queuePrefix(name) })`
   in its module, and a `@Processor(name, { concurrency, prefix: queuePrefix(name) })`
   class extending `JobProcessor` (`@repo/nest-common`, never `WorkerHost` directly: it
   logs failed jobs) whose `process(job: UncheckedJob)` starts with
   `parseJob("<queue>", "<job>", job.data)` (or `jobName` first, for a queue with several jobs)
   (see `apps/worker/src/files/`). The handler must be idempotent: jobs are delivered at
   least once.
4. Scale: add the queue to the consuming service's `keda.queues` in
   `deploy/charts/stack/values.yaml`. A queue KEDA scales must not use job priorities.
5. Scheduled work: a job on the `maintenance` queue and a cron line in `SCHEDULES` in
   `apps/worker/src/maintenance/maintenance.processor.ts` (upserted at boot, runs once
   whatever the replica count).

## A consumer of domain events

Add a queue with `jobs: { event: eventEnvelope }` and a filter in `eventSubscribers` in
`queues.ts`; the outbox relay (apps/worker) copies matching events into it with
`jobId` = event id. Consumers must be idempotent and not depend on order: the current
ones dedupe on a key of their own (the audit log on the event id, webhook deliveries on
endpoint and event, notifications on their delivery log key). A consumer without one
inserts `(event_id, consumer)` into its schema's `processed_event` in the same
transaction as its effect and skips when the row already exists. New events are declared in `packages/contracts/src/events.ts`.

## Python producer or consumer (apps/ai)

1. In `packages/jobs/scripts/export-schemas.ts`, add the payload to `schemas` and the
   queue to `shared`.
2. `bun run gen`: writes `packages/jobs/generated/` and the Pydantic models in
   `apps/ai/app/contracts/`, plus the queue's prefix and options.
3. Use the generated model and `queue_options` in `apps/ai/app/queues.py`; the worker
   loop is `apps/ai/app/worker.py` (run locally with `bun run --cwd apps/ai worker`).

## Check

`bun run test` (payload schemas in `packages/jobs/src/producer.test.ts`), then
`bun run test:integration`: the consuming service's suite in its `test/` folder drives
the queue against real Redis.

## Finish

The verify skill, then the `reviewer` agent (idempotency, `jobId`, `parseJob`, no
awaits inside a transaction). A Python producer or consumer: the `python-reviewer` agent
too.
