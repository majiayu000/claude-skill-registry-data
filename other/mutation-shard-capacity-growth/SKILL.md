---
name: mutation-shard-capacity-growth
description: Use when a Stryker mutation shard approaches or exceeds an already-calibrated CI timeout-minutes because the mutate scope grew, when shard wall clocks are badly uneven under byte-weighted packing, or when a change proposes raising that cap instead of raising MUTATION_SHARD_TOTAL and the matrix index list.
---

# Mutation shard capacity growth

## Profile keys consumed

- `make.test_mutation`
- `make.merge_mutation_reports`
- `make.test_unit_client`
- `capabilities.mutation_testing`
- `ci.workflows`

Every command resolves through the profile's `make` target map, and the matrix
job being resized is the mutation workflow declared in `ci.workflows`. Skip
this skill with a recorded note when `capabilities.mutation_testing` is `false`
or when `make.test_mutation` / `make.merge_mutation_reports` map to `null`.

## Overview

A sharded mutation matrix has two knobs: how many shards run in parallel and how long a shard may
take. Growth in the mutant set belongs to the first knob. The timeout is a structural tripwire that
catches a real regression — most importantly a return to reloading the whole suite per mutant — so
raising it trades away the only alarm that would fire.

## When to use

- One shard finishes near its `timeout-minutes` while another finishes in a fraction of the time.
- The mutate scope just grew (new components, a widened file list) and the slowest shard crossed the
  cap.
- A change is proposed that raises `timeout-minutes` rather than adding parallelism.
- Not for: a shard that is slow because one file drags an oversized related-test set behind a barrel
  import — fix the import graph first (see the
  [mutation-gate-barrel-leaf-extraction skill](../mutation-gate-barrel-leaf-extraction/SKILL.md)),
  then revisit the shard count.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — an eight-way matrix with `MUTATION_SHARD_TOTAL=8`, a 15-minute shard cap, and
  longest-processing-time packing keyed on file size in the mutation-scope script.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — a curated two-way
  matrix at a 40-minute cap plus a scheduled full-scope matrix at 120 minutes, both slicing
  round-robin in the Stryker shard config.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial — the
  same four-way matrix, lock-step, and fail-closed merge shape, but the shard job declares no
  `timeout-minutes`, so growth shows up as a slow run rather than a red tripwire.

## Why the cap is not a tuning knob

Uneven shard times are usually a packing problem, not a runtime regression: shards weighted by bytes
alone can cluster several expensive suites into one index while another index holds a single file of
the same weight. Raising the cap hides that and, repeated as the scope grows, eventually hides the
failure mode the cap exists for. Parallelism absorbs growth; the cap stays put.

## Procedure

1. Read the per-shard timings from the matrix run and confirm the slow shard is slow because it
   carries more expensive suites, not because every shard regressed. A uniform slowdown across all
   shards is a different bug — check that the runner still restricts each mutant to its related
   tests.
2. Raise the shard count, keeping every declaration in lock-step: the workflow matrix `index` list
   must be exactly `[0 .. TOTAL-1]`, and `MUTATION_SHARD_TOTAL` must match in both the shard job and
   the merge job. A mismatch fails closed at the merge gate rather than silently dropping mutants.
3. Update the shard-total constant in the partition-invariant test so the invariant is proven for
   the count CI actually runs — the React SPA shape pins it in a mutation-config tooling test run by
   the target mapped by `make.test_unit_client`, which asserts that the union of every shard equals
   the whole mutate scope exactly once, that a rerun of one shard mutates the same files, and that
   packing beats round-robin.
4. Run the new slice locally before pushing, through the repository's per-shard mutation target and
   the merge target mapped by `make.merge_mutation_reports`:

   ```bash # profile-example
   make test-mutation-shard MUTATION_SHARD_INDEX=0 MUTATION_SHARD_TOTAL=8
   make merge-mutation-reports MUTATION_SHARD_TOTAL=8
   ```

5. Confirm on CI that every shard finishes inside the unchanged cap and the merged score is the same
   as before the resplit — sharding is score-preserving, so a moved score means the partition
   changed, not the suite.

## Common mistakes

- Editing `timeout-minutes` in the same change that grows the mutate scope — raise the shard count
  and leave the cap alone.
- Bumping the matrix list without bumping `MUTATION_SHARD_TOTAL` in the merge job — change both in
  the same commit, since the merge gate is what fails closed on the mismatch.
- Leaving the partition-invariant test pinned to the old total — update its shard-total constant so
  the count CI runs is the count the invariant proves.
- Raising per-shard `concurrency` to buy speed — on a two-core runner that turns survivors into
  timeouts the gate counts as detected; add shards instead.
