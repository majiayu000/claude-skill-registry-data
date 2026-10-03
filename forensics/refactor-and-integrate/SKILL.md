---
name: refactor-and-integrate
description: Codebase integration discipline. Use when refactoring for local conventions, reviewing post-sync quality, auditing project docs, pruning diffs, or using Sync Impact evidence.
---

# Refactor and Integrate

A human has to read, trust, and maintain this work after you leave — code, prose, notes, or slides. Every technique here serves two ends:

1. **Consistency** — the result reads as if one author produced the whole project. New work follows the host's conventions (names, utilities, patterns in code; terminology, notation, structure in prose), so a reader cannot tell it from what was already there.
2. **Minimum reviewable diff** — the surviving change is the smallest that achieves the task, with no incidental noise for the reviewer to wade through.

For a change no rule below anticipates: keep what reads as one author's work and serves the task, prune what does not, raise what you cannot judge.

Load whichever domain skill(s) the work touches; each routes its own integration reference at the `integration` stage.

---

## Establish the baseline first

Before triaging anything, fix the governing diff — the changes made on *this branch* since it diverged from the base: `git diff BASE...HEAD` (three-dot), equivalently `git diff $(git merge-base BASE HEAD)..HEAD`. A dispatch supplying an explicit range overrides.

The **minimum net diff** is the smallest set of surviving hunks that supports the protected record when one exists, or achieves the task objective in standalone use. Everything below works toward it.

## Apply the reviewed refactoring task

A dispatch supplying a researcher-reviewed temporary refactoring task: execute its objective against the linked permanent documentation, result files, and mature task results. Those artifacts define the protected record; their documented reproduction, validation, interpretation, and presentation paths justify supporting carriers.

The reviewed task is the action boundary — apply its pruning and other refactoring mechanically. New evidence requiring a materially different protected outcome or refactoring action: return to the owning workflow gate so the record and task can be revised before that work runs.

## Fit the host project

Before keeping a change, read its neighbors — surrounding functions and sibling files in code, adjacent sections and paragraphs in a document. Find how the host already names the concept, which utilities or shared definitions exist, which patterns it follows. Then match them, so a reader cannot tell your work from what was already there:

- name things the way the surrounding work already names the same concept;
- reuse an existing utility or definition instead of rolling your own;
- follow the local pattern for the same kind of work.

An intentional deviation is fine when the local convention does not fit, but it carries a one-line reason at the deviation site so the next reader knows it was a choice, not an oversight.

## Triage every hunk

Walk the governing diff hunk by hunk.

**With a protected record:** only a result shown in the permanent documentation, result files, or mature task results—or a reproduction, validation, interpretation, or presentation path explicitly documented there—excludes an in-scope hunk from the automatic pruning list. Before researcher approval, put every unmatched hunk in the temporary task as a pruning action. Task objectives, checklist items, task-file coherence, matching documentation, logged decisions, and Sync Impact may explain the hunk or shape its proposed action; they do not exempt it.

**Standalone:** revert confident junk; keep a hunk justified by the objective, checklist, task-file coherence, matching documentation, a logged decision, or Sync Impact; keep and raise a scope-ambiguous but plausibly load-bearing hunk.

The same mode-specific boundary gates base-current deletions and relocations.

## Consolidate for maintainability

Minimum net diff is not only deletion. Look across the surviving changes for a simpler, more host-consistent shape reaching the same objective. Cues:

- a procedure or passage repeated across the work → state it once (extract a helper, consolidate the duplicated text);
- a near-duplicate of an existing module, dataset, or section → extend it minimally rather than fork a parallel copy;
- nested conditionals that can flatten → flatten them;
- comments or prose that restate what is already plain → cut them.

Keep abstractions that aid clarity; clarity over brevity. Two guardrails:

- **Target the net-minimum diff, not the files you happened to touch.** The smallest change leaving the codebase consistent often reaches into existing shared code to extend a utility minimally rather than duplicating its logic alongside. "Only refine code you already touched" is not the boundary.
- **The selected protection is the behavior guardrail.** A refactor must preserve the permanent record and pass every automated mechanism selected at Protect. Investigate any movement rather than silently revising documentation or test expectations.

Domain-specific consolidation rules (redundant intermediary datasets, variable-construction consistency, and the like) live in the domain `integration.md` references — load the domain skill for those.

## Project Doc Audit

Both Integrate-step refactoring and integration review cover project-level docs reachable from the diff.

For every file in the governing diff, walk up from its directory to the repo root and collect every `CLAUDE.md` / `AGENTS.md` / `README.md` encountered. Always also check the repo-root `README.md` and root `CLAUDE.md`.

For each doc in the set:

- update stale claims contradicted by the diff;
- add new patterns at the nearest appropriate level;
- link rather than duplicate parent-level content;
- create a missing `CLAUDE.md` + relative `AGENTS.md -> CLAUDE.md` pair for new module directories.

Leave docs above the affected area alone unless they are stale.

## Sync Impact Context

In standalone use, a task-local `## Sync Impact` section can justify an existing hunk; it does not create new refactor targets or excuse unrelated codebase changes.

## Final Diff Self-Check

Implementers run this immediately before every commit, including no-change cases:

1. **Recompute the governing diff** using the range from §Establish the baseline first.
2. **Leave a compact trail in the commit body** — `Final diff self-check: <command/range>; <protected record or standalone objective>; <removed and surviving change classes>; <suspicious hunk justifications or none>`. Per-commit process evidence: it belongs in history, not the task's `## Results`. A pass changing no files carries the trail on an empty commit.
3. **Summarize ordinary hunks by class** — "utility reuse in task scripts", "module README currency", "test contract wording". No line-by-line justification when the task objective or checklist already covers the class.
4. **Justify suspicious hunks by file and line/hunk.** Suspicious: `skills/*` or `agents/*` instruction edits, prior overprescription or scope-creep findings, base-side restorations or relocations, touched tasks already marked `status: approved`, broad formatting or rewrite hunks, changes justified only by Sync impact. Apply any local instruction-prose gate only to files local guidance covers.
5. **Triage** per §Triage every hunk; standalone work records its kept, reverted, and raised classes.
6. **Respect the dispatch scope.** Refactor implementer and integration reviewer act on the reopened or changed tasks in the dispatch, plus any `approved` task the branch-wide surviving-diff sweep reopens when it surfaces an unjustified hunk touching that task.

The integration reviewer recomputes the same governing diff and compares it with the self-check trail in the integrate commits under that range. A missing or stale trail is `[BLOCKING]`, including when no code changed.

## Checklist

`[BLOCKING]` items must be satisfied for APPROVE; `[ADVISORY]` items are recorded and do not block. These are the pass/fail points; the method is in the sections above.

**Code integration:**

- `[BLOCKING]` **Final Diff Self-Check present and fresh** per §Final Diff Self-Check.
- `[BLOCKING]` **Reviewed refactoring task honored when supplied:** every proposed action was executed or returned to the researcher gate before the proposal changed.
- `[BLOCKING]` **Protected record preserved:** permanent documentation, mature task results, and their required support paths remain coherent and reproducible.
- `[BLOCKING]` **Triage performed hunk by hunk** per §Triage every hunk, and no hunk was silently deleted.
- `[BLOCKING]` **Base-current deletions / relocations honor the active boundary** per §Triage every hunk.
- `[BLOCKING]` **Host-project fit** per §Fit the host project: names, utility reuse, and patterns match the host; deviations carry a reason.
- `[ADVISORY]` **Consolidation** per §Consolidate for maintainability, where the task or codebase-coherence review demanded the touch.
- `[ADVISORY]` **PR-friendly diffs:** no reformatting that obscures substantive changes.

**Handling inconsistencies:**

- `[BLOCKING]` **Methodological questions escalated, not resolved.** Diverging control variable sets, variable definitions, sample filters, equilibrium concepts, or normalization choices are research decisions.

**Docs match the code:**

- `[BLOCKING]` Module `CLAUDE.md` / `AGENTS.md` / `README.md` files do not reference files, functions, outputs, or methodology that no longer exist or have been superseded.
- `[BLOCKING]` Every output file mentioned in documentation is produced by the current code.
- `[BLOCKING]` Dates and version claims reflect the current commit.

**Project Doc Audit:**

- `[BLOCKING]` The §Project Doc Audit walk-up was executed for every file in the governing diff, applying all four rules listed there.
