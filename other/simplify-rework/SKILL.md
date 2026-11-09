---
name: simplify-rework
description: "Use when a whole codebase has grown by accretion and is to be audited or cut back, with no commit range to start from: superseded paths left behind by past shifts, unused exports and files, two implementations of one concern, or the person asks where the dead code is, to clean up the repo, or to stop it coming back. Produces a ranked audit of families, each approved family cut back through the simplify skill, and the guard. Not for the code one piece of work changed (simplify), branching complexity (complexity-rework) or an interface's shape (deepen-module)."
---

# Simplify rework

**Detection is deterministic, deletion is narrow.** An agent asked to explore for dead code spends the budget rebuilding context and finds a different set each time. Tools find, the person chooses, and each family is cut by the `simplify` skill, handed its files, never a mandate to look around.

## The phases

One artefact each, and a stop.

| Phase | Produces | Stops for | Read |
|---|---|---|---|
| 1 Audit | the report: families ranked by lines saved over risk, each with its evidence and its kind (dead, superseded, duplicate) | the person's choice of families and their order | `references/audit.md` |
| 2 Cut | one approved family, through the `simplify` skill, its files and evidence as the brief | that skill's stops; a duplicate's survivor, the person's yes | |
| 3 Guard | a check that fails on new dead code, and the done-rule for the work that creates it | the person's yes on each | `references/guard.md` |

## Where to start

| The ask | Phases |
|---|---|
| where is the dead code, audit, what can go | 1, then stop |
| clean up, an approved audit | 2 per family, in the approved order |
| stop this coming back | 3 |

## Rules

- **The audit is the context.** Without it, a cut rebuilds by exploration what the audit already found.
- **Add no dependency without the person's yes**: not an analyzer, not a CI step.
- **When the project plans its work in documents**, the audit is their input and each family is one piece of work.

## Red flags

| Thought | Reality |
|---|---|
| "Unused per the tool, so delete it" | Loads by string, public API, entry points found by convention and scripts read as unused. The audit marks each family's reach before it is proposed. |
| "I'll cut every family in one sweep" | One family per pass, or no reviewer can attribute the diff. |
