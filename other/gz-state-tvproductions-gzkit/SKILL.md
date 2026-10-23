---
name: gz-state
description: Use to report artifact lineage, relationships or readiness.
category: governance-infrastructure
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
metadata:
  skill-version: "0.3.2"
model: haiku
---

# gz state

## Overview

Read the artifact graph the ledger derives: every PRD, ADR and OBPI with its
type, parent and attestation. `gz state` is a Layer 3 view of the ledger, so
cite it for an artifact's relationships, and read completion from the ledger
through `gz obpi status` or `gz adr status`.

- With no flag it prints the `Artifact State` table (ID, Type, Parent,
  Attested). `--full` folds long IDs instead of truncating them.
- `--json` prints the whole graph, including ADR lifecycle fields
  (`lifecycle_status`, `closeout_phase`, `attestation_term`) and, for an OBPI
  with TASKs, a `task_summary` with counts by status.
- `--blocked` keeps only unattested artifacts. That is every pool ADR and
  pending OBPI, not only work that is blocked.
- `--ready` keeps only unattested ADRs whose lane-required gates are satisfied,
  that is, ADRs ready for attestation.
- Withdrawn OBPIs are hidden, and removed from their parent's children;
  `--include-withdrawn` shows them.

`--repair` is the one mode that writes. It ignores the query flags, has no dry
run, and makes two repairs from the ledger:

- It sets each OBPI brief's frontmatter `status`: `Completed` when the ledger
  records completion, `Abandoned` when it records withdrawal, unchanged
  otherwise. A terminal brief is never overwritten.
- It repairs the pipeline marker files of the run in flight that was launched
  last, and is the only command that does. With one of the run's two files on
  disk it restores the missing one as a copy; with neither it rebuilds both
  from the run's `pipeline_launched` and `pipeline_stage_transition` events.
  It overwrites no marker file. With neither file on disk it declines a run
  whose last recorded boundary is past the stale bound; with one file on disk
  the stale bound does not apply and the copy is restored. It declines an
  older run while a later one is in flight. The manpage `docs/user/manpages/state.md` states the whole contract.

## Workflow

1. Query: `uv run gz state`, or `--json`, `--blocked`, `--ready`,
   `--include-withdrawn` as the question needs. Add `--full` when IDs are
   quoted as evidence.
2. Before `--repair`, tell the operator that it edits brief files and may write
   pipeline marker files under `.claude/plans/`. Run it, then report its
   `State Repair Results` table, or `All frontmatter is aligned with ledger
   state. No changes.`, and each `Restored pipeline marker file`, `Rebuilt
   pipeline marker` and `Pipeline marker not rebuilt` line it prints, the last
   with its reason. With `--json` these are the `markers` object: `rebuilt`,
   `restored` and `declined`. Include the changed brief files in the commit.

## Example

```bash
uv run gz state --ready
uv run gz state --json
uv run gz state --repair
```
