---
name: gz-plan
description: Use to create an ADR, a pool ADR included, recording architecture intent and lane scope.
category: adr-lifecycle
metadata:
  skill-version: "1.8.1"
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
model: opus
---

# gz plan

## Overview

> **Self-Escalation (opus-tier).** The dialogue with the operator stays in the main session: a subagent cannot ask the operator a question or hear the answer, and what the operator adds is this skill's primary input. When the session model is below opus-tier, you may spawn an `Agent` with `model="opus"` for a bounded drafting or QC track that needs no operator input — pass the operator's words verbatim and the relevant context (ADR IDs, OBPI IDs, prior decisions), and treat what it returns as a draft you verify, not as the operator-facing result.

Scaffold one ADR from its template and, for a non-pool kind, book it in the
ledger. `uv run gz plan create <name>` (`plan_cmd`, `src/gzkit/commands/plan.py`):

- **refuses before any write, exit 1,** when `--kind` is missing (argparse gives
  it no default; `_validate_kind_and_semver` requires it); when `--kind
  foundation` is asked in a project that has sunset the kind
  (`foundation_kind_is_closed`: `data/foundation_grandfather.json` exists, as it
  does in gzkit per ADR-0.34.0; an adopter without that file keeps the kind
  open); when `--kind feature` carries a `0.0.x` `--semver`; and, for a non-pool
  kind, when `name` is a bare semver or a bare `ADR-<semver>` id without a slug
  (`_reject_noncanonical_name`, GHI #494);
- **non-pool:** composes the id `ADR-<semver>-<name>` (a `name` already of that
  form is used as given), renders `src/gzkit/templates/adr.md` with status
  `Draft`, a Decomposition Scorecard and a `## Checklist` seeded with one
  placeholder `OBPI-<semver>-NN` item per targeted OBPI, and writes it to
  `<paths.adrs>/pre-release/<id>/<id>.md` (`foundation/<id>/` for an open
  foundation kind);
- then appends `adr_created` through `register_adr_in_ledger`, which skips an id
  that already has one (`Ledger.has_adr_created`). It exits 3 when the
  directory name is not a canonical id or the package is an ungrandfathered
  foundation, and 2 when the append fails or the id is missing from the graph
  afterwards, each time naming `uv run gz register-adrs --all` as the recovery.
  The ADR file is already on disk in all of those cases;
- **pool:** writes `<paths.adrs>/pool/ADR-pool.<name>.md` from
  `src/gzkit/templates/adr_pool.md` (no scorecard, no checklist, no `kind:` or
  `semver:`; `--semver` is ignored) and **books nothing**: the pool branch
  returns before `register_adr_in_ledger`. `uv run gz register-adrs` books pool
  entries.

`--dry-run` runs every refusal above, prints the path it would write and, for a
non-pool kind, the `adr_created` it would append, and writes nothing.

It creates no OBPI briefs: `gz specify` (skill `gz-obpi-specify`) authors each
brief against a checklist item. `gz-adr-create` is the full authoring flow that
books an ADR together with its briefs.

**Scorecard.** The five `--score-*` flags (0–2) default from
`default_dimension_scores` (`src/gzkit/core/scoring.py`), which reads the semver
and lane. `baseline_range_for_total` maps their total to a baseline range;
`--baseline-selected` picks a count inside it (default: the lower bound; a value
outside the range fails, exit 1); each `--split-*` flag adds one OBPI. The sum
is the number of checklist items seeded. The doctrine the numbers implement is
`docs/governance/GovZero/obpi-decomposition-matrix.md` § Deterministic
Decomposition Gate.

## Work order (operator ruling, verbatim canon)

- Work feature ADRs in ascending semver order: the lowest version with unlanded OBPIs is in flight. Do not work, author, or recommend a higher feature ADR ahead of it. The campaign selects work but cannot override that order. If campaign sequencing conflicts, semver governs; surface the conflict to the operator rather than silently resolving it. “One feature at a time” does not authorize swapping the order. An ADR in flight may be revised to take more OBPIs. The revision updates the document (an Intent amendment, a Decision item, a checklist item and the scorecard baseline) and the briefs table in the same change. A Validated ADR is not revised: scope missed from one enters the in-flight ADR as a repair assignment that cites the obligation it repairs. An item off the ADR's theme is labelled as such in the Intent amendment. The (m)ADR is a stopgap: a release-increment bucket, meant to be thematically cohesive. Its successor is a feature bundle between an enhancement proposal and a feature specification. Names are chosen later. This replaces the exception of 2026-09-29 (GHI #871), by which a correction to a Validated ADR took the next unallocated feature semver and could be worked ahead of the in-flight ADR; that route is retired (operator rulings 2026-10-04: 'the new loosening law here is we need to be able to revise an adr to allow for more obpis - the document and briefs table gets updated'; 'A, in-flight only'; the wording and the retirement, each 'A').

> Carried verbatim from root `AGENTS.md` § Operator Doctrine on 2026-09-17 (GHI #921), and into this skill on 2026-09-24 (GHI #1091, sweep finding S06): the ruling governs authoring and recommending, not only working. The corpus `.gzkit/corpus/AGENTS.md.jsonl` keeps the ruling's history.

## Workflow

1. **Route first.** A GHI authorizes direct defect repair, and a small in-flight
   defect without one is fixed directly when it meets `AGENTS.md` § Defect-fix
   routing. Neither gets an ADR.
2. **Read the target.** Read the code and docs the change touches before sizing
   it. Hand a subagent only an independent research track, with its Why
   (`AGENTS.md` § Behavior Rules).
3. **Size the decomposition** with the matrix doc: the Rule of Three baseline
   (which the doc sets for heavy-lane ADRs), then the Matrix of Four overlay,
   whose four principles are the four `--split-*` flags. Choose the dimension
   scores, then present them, the resulting OBPI count and the rationale for
   the operator's approval: the Granularity Assessment the doc's § Enforcement
   asks of this skill.
4. **Ask before creating.** Put up to 20 non-obvious questions to the operator
   on edge cases, dependencies and possible regressions. Do not create the ADR
   until they are answered.
5. **Ask the operator for `--kind`; never propose a default.** In gzkit the
   choices are `feature` (ships a named capability, semver `0.y.z` and up) and
   `pool` (noted, not committed). `foundation` is closed here by ADR-0.34.0
   and the command refuses it. In an adopter project without
   `data/foundation_grandfather.json` it stays open: offer it with the
   invariance test,
   *"Foundation = without it, we wouldn't be doing the project"*
   (the hexagonal-ports lens: ports point to invariance; adapters are features),
   and see `docs/user/concepts/foundation-feature-invariance-test.md` and
   `docs/user/concepts/adr-taxonomy.md`. Bare `uv run gz plan` exits 2, since
   the subcommand is required.
6. **Preview, then create.** Pick a descriptive kebab-case `name` and, for a
   feature, the semver the work order allows. Run with `--dry-run`, then without
   it, passing the operator's `--kind` through unchanged.
7. **Verify the booking.** Non-pool: `uv run gz adr status <ADR-ID>` shows the
   ADR. Do not re-run a registrar on success; `register-adrs --all` is only the
   recovery the exit-2/3 messages name. Pool: `uv run gz register-adrs
   --pool-only --dry-run` lists the entry as unregistered, and `uv run gz
   register-adrs ADR-pool.<name>` books it.
8. **Hand off.** The template's `_[Author: …]_` prompts are the ADR sections
   left to write. Briefs follow 1:1 with the checklist through
   `gz-obpi-specify`. A pool ADR needs a non-empty `## Target Scope` section
   before `gz adr promote` accepts it, and the pool template carries none
   (`gz-adr-promote`).
9. **Report** the ADR id, its path, the `adr_created` event or, for pool, that
   none was booked, and the next step.

## Example

```bash
uv run gz plan create login-impl --kind feature --semver 0.2.0 --lane heavy --dry-run
uv run gz plan create login-impl --kind feature --semver 0.2.0 --lane heavy \
  --score-interface 2 --split-surface-boundary
uv run gz adr status ADR-0.2.0-login-impl

uv run gz plan create exotic-idea --kind pool
uv run gz register-adrs ADR-pool.exotic-idea
```

## Related

- `gz-adr-create`: authoring an ADR with its briefs end to end
- `gz-obpi-specify`: one brief per checklist item
- `gz-adr-promote`: moving a pool ADR into a versioned package
- `gz-plan-audit`: `gz plan audit`, the plan-to-brief alignment check
