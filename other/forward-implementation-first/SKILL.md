---
name: forward-implementation-first
description: >
  Keeps an agent building and validating real output instead of servicing its
  own bookkeeping. Use for multi-stage pipelines, capability roadmaps,
  long-running implementation loops, migrations, staged data or build runs, and
  any run where administrative hashes, locks, receipts, dashboards,
  certification markers, or progress metadata can block correct work. Use when
  an agent refuses to advance, rewinds finished stages, or reruns unchanged
  work because a marker is missing or stale.
---

# Forward implementation first

Build working capability and correct output before administrative bookkeeping.
Apply this contract both while building a system and while running it.

## Scope

This skill applies to:

- infrastructure and roadmap implementation;
- input intake and intermediate artifact production;
- transformation, derivation, and analysis stages;
- test construction, runtime verification, and measurement;
- publication of final output and closeout;
- manual invocation of any authorized pipeline stage.

It applies whether the action runs through a full orchestrator, a focused
command, or a manual stage invocation.

## Decision rule

Before each action, classify it as one of:

1. **Semantic implementation**: builds or connects a producer, consumer,
   adapter, runtime path, schema, fixture, or final output.
2. **Focused validation**: tests the changed dependency cone through behavior,
   schema, counts, samples, conservation, consistency, nontruncation, or
   measured resources.
3. **Administrative bookkeeping**: generates or repairs hashes, locks,
   receipts, dashboards, certification markers, progress metadata, or
   presence-only records.

Choose categories 1 and 2. Skip category 3 unless the user asks for it or the
artifact is itself part of the product. When administrative work blocks a path
without protecting correctness, remove that dependency from the path.

## Hard constraints

- Build the producer and consumer before polishing status or certification
  surfaces.
- Do not generate, repair, compare, or propagate administrative hashes.
- Do not create or wait on filesystem locks.
- Do not rerun an unchanged stage to regenerate a receipt or marker.
- Never invalidate valid output because an administrative receipt, hash,
  certification marker, dashboard row, or progress record is missing, stale, or
  incompatible.
- Never move the forward cursor backward for an administrative metadata change.
- Never invalidate a wide stage range when only one producer or consumer
  changed. Replay only that producer's dependency cone.
- Do not treat certification, receipts, dashboards, progress metadata, or
  artifact presence as the product.
- Remove hash-only, lock-only, receipt-only, and presence-only credit or gates
  from execution paths.
- Do not claim a capability works because its file exists. Run the smallest
  changed dependency cone and inspect the output.
- Publish valid output after focused validation. Do not add an extra review
  cycle when no defect remains.

## Forward cursor and manual execution

A stage may move backward or be replayed only when at least one real condition
holds:

- its input meaning changed;
- its target or pinned revision changed;
- its output is malformed, truncated, nonconserving, internally inconsistent,
  or incompatible with the consumer;
- an observed run disproves the earlier static result;
- the changed producer's declared dependency cone requires replay.

Missing or stale administrative metadata is not one of those conditions.

When the orchestrator refuses to run a stage only because of a receipt,
certification marker, progress record, administrative hash, or lock:

1. Run the exact stage manually.
2. Validate its output with the focused checks below.
3. Publish the valid output atomically.
4. Continue from the forward cursor.
5. Remove or downgrade the administrative-only gate in the execution path.

Do not refuse an authorized manual run because the full pipeline cannot issue a
receipt. Do not push the user toward another agent or tool to get around your
own bookkeeping.

## Required validation

Use the checks that match the change:

- runtime behavior and exit status;
- schema and type validity;
- exact input, output, accepted, rejected, and unknown counts;
- deterministic first, middle, and last samples;
- identity and partition conservation;
- join consistency and flag polarity;
- nontruncation and bounded diagnostic output;
- wall-clock time and peak memory for material stages.

Hashes may identify inputs or revisions, but they never grant correctness,
execution, or roadmap credit.

## Exceptions that stay substantive

Bookkeeping is cheap to skip. Evidence is not. Keep these:

- Integrity that belongs to the product itself. A checksum your users verify, a
  signature your format requires, a hash that is part of the output contract.
  Those are features, not paperwork.
- Input and revision identity when it decides which version of the thing you
  are operating on. Getting that wrong means correct work on the wrong target.
- Real measurement: tests that assert results, benchmarks, reproductions,
  end-to-end runs, and whatever your domain treats as proof.
- The difference between coverage and consequence. A run that exercises a path
  is not a check that the path produced the right answer.
- An execution record is substantive when it carries the command, the input,
  the result, and the expectation it was checked against. Its absence blocks
  that specific claim. It does not invalidate unrelated earlier stages.

## Parallel work invariants

These are behavior contracts, not a scheduler. Your runtime owns scheduling,
concurrency, resource contention, and worker topology, and this skill carries
no policy about them. Keep these invariants under any scheduler:

- Exactly one writer owns publication, cursor movement, acceptance, and
  conclusions. Parallel workers prepare, implement, inspect, and test
  nonoverlapping support work. They never become competing truth.
- Verify a worker's output locally before consuming it. A worker's report
  states intent, not result.
- Forward progress does not wait for every worker to finish. Consume completed
  output when the dependency that needs it is reached.
- Do not manufacture busywork to occupy idle workers. An idle slot is cheaper
  than fake work.
- If a run exposes a defect in a stage, fix that stage before rerunning its
  dependency cone.
- If the next proposed action is bookkeeping-only, select the next unresolved
  producer, consumer, adapter, or output instead.

If no system owns scheduling in your setup, write a small profile for it
yourself; [examples/execution-profile.md](examples/execution-profile.md) is a
starting point. The skill never loads it on its own.

## Status reporting

Report implemented behavior and measured output first. List blockers literally.
Keep infrastructure progress separate from evidence about the output. Do not
turn administrative completion into a substitute for working capability.
