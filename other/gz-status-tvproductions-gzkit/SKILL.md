---
name: gz-status
description: Use for status inquiries, blockers and next actions; reports workflow fronts with ADR lifecycle and gates.
category: governance-infrastructure
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
metadata:
  skill-version: "1.7.1"
model: haiku
---

# gz status

## Overview

`gz status` is read-only: it writes no ledger event and no file
(`status` in `src/gzkit/commands/status.py`). After the `Lane:` line it prints:

- **Workflow fronts** — when `data/active_campaign.json` exists, the
  `## Workflow fronts` section of the campaign its `active` key names, with
  that source path (`_read_workflow_fronts`). It is declared context: the
  command does not refresh the GHI queue, inspect handoff lineage or run
  research. A malformed registry, a campaign outside the project, or a missing
  or empty section prints `Workflow fronts unavailable: <reason>` and the run
  still exits 0. Without the registry the section is omitted.
- **One entry per ADR in the ledger graph**, semver ADRs in semver order,
  then pool ADRs: lane, gate projection, OBPI summary and rows, closeout
  readiness and blockers, lifecycle, and a TASK summary when tasks exist.
  An ADR whose linked OBPIs are not all complete reports `Pending` whatever its
  attestation or receipt events say.

`--table` prints one summary row per ADR; `--show-gates` adds the per-gate
breakdown; `--full` keeps full IDs and renders every OBPI row; `--json` emits
`mode`, `adrs`, `pending_attestations` and, with a registry, `workflow_fronts`;
`--epic <slug>` keeps only pool ADRs of that epic (the ADRs are filtered, the
front map is not). `docs/user/manpages/status.md` defines each field.

Tracked-defect GHI refs in this summary are never resolved live and render
`(unresolved)`; resolve one with `gz adr status <ADR-ID>`,
`gz obpi status <OBPI-ID>`, or `gh issue view`. Exit 0 on success, 1 when the
project is not initialized.

## Operator ruling (verbatim canon)

Status covers handoff system, GHI triage, ADR/OBPI campaign, and new R&D. Read Workflow fronts in the campaign selected by data/active_campaign.json; use gz-status to report evidence, freshness or unknowns, and next actions. Focused inquiries include material dependencies. Handoffs preserve the map reference and session changes. The campaign owns the map; live sources establish progress. Campaign sequence, ascending feature-ADR order, and operator-only OBPI initiation govern execution.

> Carried verbatim from root `AGENTS.md` § Operator Doctrine on 2026-09-17 (GHI #921); the corpus `.gzkit/corpus/AGENTS.md.jsonl` keeps the ruling's history.

## Work order (operator ruling, verbatim canon)

- Work feature ADRs in ascending semver order: the lowest version with unlanded OBPIs is in flight. Do not work, author, or recommend a higher feature ADR ahead of it. The campaign selects work but cannot override that order. If campaign sequencing conflicts, semver governs; surface the conflict to the operator rather than silently resolving it. “One feature at a time” does not authorize swapping the order. An ADR in flight may be revised to take more OBPIs. The revision updates the document (an Intent amendment, a Decision item, a checklist item and the scorecard baseline) and the briefs table in the same change. A Validated ADR is not revised: scope missed from one enters the in-flight ADR as a repair assignment that cites the obligation it repairs. An item off the ADR's theme is labelled as such in the Intent amendment. The (m)ADR is a stopgap: a release-increment bucket, meant to be thematically cohesive. Its successor is a feature bundle between an enhancement proposal and a feature specification. Names are chosen later. This replaces the exception of 2026-09-29 (GHI #871), by which a correction to a Validated ADR took the next unallocated feature semver and could be worked ahead of the in-flight ADR; that route is retired (operator rulings 2026-10-04: 'the new loosening law here is we need to be able to revise an adr to allow for more obpis - the document and briefs table gets updated'; 'A, in-flight only'; the wording and the retirement, each 'A').

> Carried verbatim from root `AGENTS.md` § Operator Doctrine on 2026-09-17 (GHI #921), and into this skill on 2026-09-24 (GHI #1091, sweep finding S06): the ruling governs authoring and recommending, not only working. The corpus `.gzkit/corpus/AGENTS.md.jsonl` keeps the ruling's history.

## Workflow

1. Decide whether the inquiry is project-wide or focused on one ADR or OBPI.
   An ordinary "status?" is project-wide; the operator need not name every front.
2. Run `uv run gz status` (add `--table` for the ADR summary, `--json` to read
   fields). Read the workflow-fronts section it prints, or the
   `workflow_fronts` JSON field. That section is the campaign's declared map,
   not a live assessment of any front. If it reports the source unavailable,
   say so; do not infer that a front is healthy.
3. For project-wide status, consider every front the ruling above names:
   **handoff system**, **GHI triage**, **ADR/OBPI campaign**, and **new R&D**.
   The campaign section is the authority for what each front covers and which
   evidence to read. Typical sources: handoff lineage, rulings and observed
   resume behaviour (`gz-session-handoff`); current GitHub work orders
   (`ghi-triage` for a full ranked pass); campaign sequencing and the
   ledger-backed ADR/OBPI state from step 2; research records (`gz-rnd`).
   Date cached evidence and label anything not re-verified. Do not equate
   issue volume, an unresolved hypothesis, or declared context with ill
   health. Keep observed defects and actual blockers specific.
4. For a focused inquiry:
   - one ADR: `uv run gz adr status <ADR-ID>` (the `gz-adr-status` skill),
     which resolves tracked-defect GHIs live;
   - one OBPI: `uv run gz obpi status <OBPI-ID>` for its runtime, proof,
     attestation and anchor state and its issues. It does not report locks;
     `uv run gz obpi lock check <OBPI-ID>` does.
5. Give each front a concise state, evidence/date, and next action in a general
   answer. A focused answer covers its target and material cross-front
   dependencies. Campaign sequence and operator initiation govern execution; a
   status inquiry does not initiate OBPI work or promote an R&D question into
   a new ADR.

## Example

```bash
# Project fronts and ADR summary
uv run gz status --table

# Machine-readable fronts, ADRs and pending attestations
uv run gz status --json

# Focused single-ADR and single-OBPI views
uv run gz adr status ADR-0.0.67-tool-skill-invariant1-enforcement
uv run gz obpi status OBPI-0.0.67-02-wire-orphan-verbs-into-skills
```
