---
name: epics
description: Use when delivery work needs structuring into epics — defining a new epic, refining or superseding an existing one, or decomposing a PRD's requirements into durable delivery structures that feed issue decomposition. Writes docs/product/epics/NN-<slug>.md (durable, id-stable, superseded-never-deleted), each epic tracing to the JTBD ids it serves and the PRD requirement IDs it bundles. In the A-Team pipeline this is a definition-phase output ("the Epics"). Do not use for full roadmap/portfolio planning across quarters (deliberately not ported), for delivery tickets or acceptance criteria (ticket-writer), or to create or revise jobs (jobs-to-be-done).
metadata:
  version: 0.1.0
  owner: Alvaro Bezerra
  provenance: cherry-picked 2026-07-24 from product-craft roadmap-writer's epic-only mode (github.com/ABZerra/product-craft) and adapted to the A-Team contract. Roadmap planning was deliberately left behind — the A-Team is scoped to 0→1 work, not portfolio sequencing.
---

# epics

Define and maintain **epics** — the durable delivery structures between the
PRD and the ticket backlog. An epic bundles requirement IDs from feature PRDs
into an outcome-oriented workstream, traced to the jobs it serves, prioritized
explicitly, and owned. Epics are what `ticket-writer` decomposes and what the
product team steers delivery by.

This skill **consumes** jobs and PRD requirements; it never mints or rewrites
jobs (`jobs-to-be-done`) and never writes tickets or acceptance criteria
(`ticket-writer`). Full roadmap/portfolio planning is deliberately out of
scope — that part of the source skill was not ported.

## Where epics live

**`<target>/docs/product/epics/NN-<slug>.md`** — one file per epic, template
in `references/epic-template.md`. Durable-artifact rules, identical in spirit
to `jtbd/`:

- **Ids are forever.** Next free `NN`; never renumber or reuse.
- **Never delete or silently replace.** A reshaped epic is a **new file**
  whose `## Related` says `supersedes [[epic:NN-...]]` (bare `[[NN]]` always
  cites a job); the old one flips
  `status: superseded` with a pointer. `parked` marks a real-but-not-now epic;
  `done` marks a delivered one.
- **Never write without human review in the same session** — read-back before
  every write (standalone) or the definition gate (pipeline).
- **`milestone:` is not yours.** The harness's issues phase writes that single
  frontmatter key back into an epic after projecting it to GitHub (the one
  cross-owner write `CONTRACT.md` permits). You never author or edit it — but
  a REVISE that rewrites frontmatter "per the template" must **carry it
  through unchanged**. Dropping it strips the back-reference, and the next run
  creates a duplicate milestone in GitHub. A superseded epic keeps its
  `milestone:` too: the issues phase closes that milestone with a pointer to
  the replacement rather than deleting it.
- **One commit per run**, message naming what changed and why
  (`docs(epics): 02 split from 01 — triage and reporting are different
  outcomes`).

Repo-first-and-always; a Cowork folder is a valid target, never a blocker.

## Modes

- **DEFINE** — create epic(s): from a PRD's requirements (definition phase),
  or standalone from an objective + jobs.
- **REVISE** — refine, split, merge, park, complete, or supersede existing
  epics as delivery reality changes. Revisions follow the supersede rules —
  history is breadcrumb, not clutter.

## Inputs

- `docs/product/jtbd/` — active jobs (ids + verbatim headlines). An epic that
  serves no existing job is evidence a job is missing → `TBD`, route to
  `jobs-to-be-done`; keep the epic out of committed scope until resolved.
- `docs/features/<slug>/prd.md` — requirement IDs to bundle (when run in a
  feature's definition phase).
- `docs/product/ateam-plan.md` — the goals/deliverables the epics must ladder up to;
  `context.md` for glossary terms and the ledger.
- Existing `docs/product/epics/` — always read before writing; extend and
  supersede, never duplicate.
- Ownership, dependency, and prioritization context from the human — captured
  as `TBD` when missing, never guessed.

## Workflow

1. **Read the existing epic set** and the jobs. New work extends it; a fresh
   run never re-derives epics that already exist.
2. **Shape each epic around one primary job-outcome.** More than one distinct
   primary job inside a candidate epic → split it. Explicit JTBD framing: ids
   + verbatim headlines, language preserved.
3. **Initiatives, outcome-oriented.** Ordered by how directly they unlock the
   jobs served; dependency-constrained ordering made visible. Optional time
   windows only — no mandatory dates.
4. **Bundle requirements.** In a feature run, map each epic to the PRD
   requirement IDs it realizes (`assisted-triage-v0: R1–R3`) and record the
   feature slug in frontmatter. Requirements left unbundled are a flag for the
   gate, not a silent drop.
5. **Prioritize explicitly.** Default **MoSCoW** when shaping scope without
   effort/impact data; **2x2** when the trade-off data exists; Eisenhower and
   RICE as offered alternatives. State the chosen approach and rationale in
   the epic — an unexplained priority is an opinion, not a decision.
6. **Keep unknowns visible.** Missing owner, dependency, or success signal is
   `TBD`; genuinely open questions mirror into the context.md ledger.
7. **Read-back / gate, write, commit.** Present drafted or revised epics for
   correction; write per the durable rules; commit.
8. **Hand off.** `ticket-writer` decomposes the epics into the backlog;
   `discovery-plan` folds epic-level deliverables into ateam-plan.md's
   initiatives. Close with **Next likely skill(s)** · **What to pass forward**
   (epic ids, requirement bundles, priority calls) · **Suggested next
   prompts**.

## No human present

Durable writes require review. With nobody present: deliver the drafted
epic(s) in your report only, write nothing, and state that the run awaits
review. In pipeline mode the definition gate is that review.

## References

- `references/epic-template.md` — the durable epic file template + lifecycle
  rules.
