---
name: glide-mq
description: Design glide-mq queue jobs, ordering lanes, worker concurrency, and cross-job caps when writing or reviewing queue producers, workers, and dispatchers.
---

# glide-mq queues

Read applicable `AGENTS.md` and the repository's local queue adapter when present.
Local policy overrides these portable conventions.

Names below are the glide-mq API: the job option `ordering: { key, concurrency }`, the worker
option `concurrency`, `lockDuration`, and `job.moveToDelayed(timestamp)`. Read
[lease patterns](references/lease-patterns.md) for the lease shape.

1. **Every shared-queue job sets `ordering`.** An ungrouped job in a shared queue competes for
   every worker slot, so a flood of it starves other families. Give each job an
   `ordering.key` prefixed with its domain name and an explicit `ordering.concurrency`.
2. **`ordering.concurrency` is a global cap; the worker `concurrency` is per process.** The key's
   cap holds across all workers and processes. The worker option only bounds one process's
   active jobs. Never size lane caps to sum to the worker option. Take caps from runtime
   configuration, and give batched families a low cap.
3. **Group FIFO ignores `priority`.** Jobs sharing an ordering key run in enqueue order whatever
   their priority. Work that must not wait behind a flood, and dispatchers that rely on
   priority, get their own lane. Put work that outsiders can flood in a lane of its own.
   Ordering keys are the orchestration layer; add none on top.
4. **`globalConcurrency` caps the whole queue.** The worker option `globalConcurrency` limits
   every job on the queue together, so on a shared queue it throttles all families at once. Use
   ordering lanes for per-family caps, and use `globalConcurrency` only when one resource bounds
   the whole queue.
5. **A job moved to delayed keeps its ordering slot until it completes.** A deferred job still
   counts against `ordering.concurrency`, so deferred jobs can fill a key and block ready work
   on it. A cap that must survive deferral belongs in a token-owned lease, released before
   `moveToDelayed`, not in the ordering key. Never fix starvation by raising the key's
   concurrency: overlap grows and the same number of deferred jobs still fill the slots.
6. **Lease mechanics.** Acquire a token-owned lease with `SET key token NX PX ttl` before the
   guarded work. Set the TTL at or above the job's `lockDuration`, renew it while the job runs,
   and release it with compare-and-delete in `finally`. On contention, `moveToDelayed` only this
   job by a short, bounded, jittered delay so it keeps its id, cursor, and dedup. Release the
   lease before any `moveToDelayed` for quota deferral. Reuse the repository's lease helper
   rather than adding a second. See [lease patterns](references/lease-patterns.md).
7. **Job count is not a KPI.** Many small jobs with a dispatcher and a sweep are fine. Do not
   merge or remove jobs to cut the count. Judge a design by model calls or spend per item and by
   how simply the jobs share a lifecycle.

Dispatchers, paged fan-out, and job-id deduplication follow
[bounded iteration](../bounded-iteration/SKILL.md). A lease for work that spans an external call
replaces holding a PostgreSQL transaction or advisory lock open across it; see
[performance patterns](../postgres-node-performance-tuning/references/performance-patterns.md).

Consumer policy owns queue names, lane keys, caps and their configuration source, the lease helper,
and enforcement configuration.
