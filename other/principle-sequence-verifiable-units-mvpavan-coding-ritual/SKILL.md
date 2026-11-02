---
name: principle-sequence-verifiable-units
description: Apply when doing multi-step work (a sweep, a migration, a run of similar edits) or stacking commits.
disable-model-invocation: true
---

# Sequence verifiable units

Every step ends somewhere a check can confirm.

- Before the first change, run the work's checks on the starting base and
  record the results, so a later failure can be classed as pre-existing or as
  a regression.
- Split the work into small units that each end in a checked state, and start
  the next only when the current one passes. In a declared migration group
  the group is the unit (`principle-migrate-without-shims`).
- Where commits are authorized, keep each small and about one thing.
- Where commits are authorized, order them so the history proves the work:
  the failing test before the fix, removal before reshaping, baseline before
  treatment, scaffold before feature, each commit standing on its own.
