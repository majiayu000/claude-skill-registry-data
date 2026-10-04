---
name: mutation-testing-stryker-gotchas
description: >-
  Use when a Stryker survivor cannot be explained by a missing assertion — a mutant reported
  `Survived` with an empty `killedBy` or `testsCompleted` of zero, a `Stryker disable next-line`
  comment that never turns a mutant `Ignored`, an `ArrayDeclaration` mutant on a React hook
  dependency array, a merged sharded score lower than every shard's own report, or survivors that
  appear and vanish when an unrelated file is edited.
---

# Stryker gotchas in sharded pipelines

## Profile keys consumed

- `make.test_mutation`
- `make.merge_mutation_reports`
- `quality.mutation_msi`
- `capabilities.mutation_testing`

Run the suite through the target mapped by `make.test_mutation` and merge shard reports through
`make.merge_mutation_reports`; skip this skill with a recorded note when
`capabilities.mutation_testing` is `false` or either key maps to `null`.

## Overview

Three Stryker behaviours fail silently and look like a broken gate: an equivalent mutant no test can
kill, a disable directive that attaches to the wrong node, and a sharded merge that keeps a result
from a shard which no longer owns the file. Each has a deterministic fix.

## When to use

- A survivor has no assertion that could plausibly kill it, or reports zero completed tests.
- A `Stryker disable next-line` comment has no effect on the report.
- Per-shard reports disagree, or the merged score is lower than every individual shard implies.
- Editing an unrelated file changes which mutants survive.
- Not for: ordinary survivors that a real assertion would kill — write the assertion.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — `stryker.config.mjs` runs `checkers: ['typescript']` with `ignoreStatic: true` and
  a flat `{ high, low, break }` of 100; CI shards incrementally and the target mapped by
  `make.merge_mutation_reports` merges by ownership.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — the
  equivalent-mutant and directive traps apply, but there is no `checkers` or `ignoreStatic` setting
  and the mutate scope is four curated files; shards run cold and the target mapped by
  `make.merge_mutation_reports` unions them, with `break` read from
  `config/mutation-policy.json`, so the stale-owner trap does not arise.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial — the
  same two traps apply; shards run cold and merge by union, thresholds are
  `{ high: 90, break: 80 }`.

Whatever the shape, `quality.mutation_msi` is the floor the merged report must clear, and it is
raise-only.

## Equivalent mutants

An equivalent mutant is proof that a piece of source does not matter. Prefer **adopting the simpler
program**: delete the half that cannot change behaviour and the mutant disappears along with dead
code. Prove equivalence first — a `?? ''` after a type guard is only dead if no reachable value can
be `undefined`; if one can, the fix is a real guard, not a deletion.

Annotate only when no honest refactor exists, and put the proof in the reason. React hook dependency
arrays are the standard case: `ArrayDeclaration` rewrites `[]` to a one-element constant, React
compares deps with `Object.is`, so the effect fires identically. Hoisting the literal to a named
constant would remove the mutant, but `react-hooks/exhaustive-deps` rejects a non-literal deps
argument.

## Directive placement

Stryker reads the directive from a node's leading comments and keys `next-line` off **that node's**
line. A comment dangling above `}, []);` leads no node and is silently ignored — no error, no log,
the mutant just survives. Expand the call so the array literal starts on its own line:

```ts
useEffect(
  () => {
    subscribe();
  },
  // Stryker disable next-line ArrayDeclaration: equivalent, deps stay Object.is-equal
  []
);
```

An inline deps array works when the comment leads the whole statement — a
`const toggle = useCallback(fn, []);` on one line is annotated fine.

## Sharded merge ownership

Shard membership is packed by file size, so editing a file can move it to a different shard. With
per-shard incremental caches, the previous owner still holds the old result. Merging on first
occurrence then lets a status decided against different source outrank the shard that actually
re-ran the file — reporting survivors that the owning shard already scored as killed.

The merge must rebuild the packing with the same algorithm the shards used, keep each file only from
its current owner, and report how many stale results it dropped. Never resolve a disagreement
between shards by re-running until the ordering favours the answer you want.

## Common mistakes

- Reaching for a disable directive before checking whether the simpler program is available.
- Writing a reason that says a test was hard to write instead of why the two programs cannot be told
  apart.
- Assuming a directive worked because the file looks annotated — confirm the mutant moved to
  `Ignored` in the report.
- Merging shard reports by union while incremental caches are in play.
- Lowering the break threshold, narrowing the mutated scope, or deleting an assertion to get past a
  survivor.
