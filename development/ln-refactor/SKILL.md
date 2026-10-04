---
name: ln-refactor
description: "Plan a refactor as a sequence of tiny safe commits via interview and codebase exploration. Use when restructuring working code, or when the user says 'plan a refactor'."
argument-hint: "[area or module to refactor]"
---

# Ln Refactor

"Make the change easy, then make the easy change" (Beck). Plan a refactor as tiny commits that each leave the codebase working (Fowler). Preparatory refactoring first, behavioral changes last.

`memory/REFACTOR.md` is a temporary derivative execution aid. Do not create alternate refactor ledgers or archive completed refactor plans; delete the file when the refactor is finished or superseded.

Skip steps you consider unnecessary.

## Input

The area to refactor: $ARGUMENTS

## Plan

1. Capture the problem. Explore the codebase to verify assertions. Present alternatives the user may not have considered. Hammer out exact scope — what changes, what stays.
2. Check test coverage of the affected area. If coverage is insufficient for safe refactoring, the first step must be characterization tests (Feathers, *Working Effectively with Legacy Code*) — suggest `ln-build` for that before continuing.
3. Break the refactor into tiny commits. Order by safety: renames first (align to the lexicon in `memory/SPEC.md` if it exists), then extractions (deepen shallow modules — Ousterhout), then interface alignments, then behavioral changes last. Each commit is a complete, passing state.
4. Write the refactor plan to `memory/REFACTOR.md`. Delete the file when the refactor is complete or superseded.

## Output

Use this structure:

```md
## Problem Statement

What is wrong, from the developer's perspective.

## Solution

The target state, from the developer's perspective.

## Commits

Ordered list of tiny commits. Each described in plain English — no file paths or snippets. Each leaves the codebase working.

1. [Commit description]
2. [Commit description]
3. ...

## Decisions

- Modules built or modified
- Interface changes
- Architectural decisions
- Schema changes, API contracts

No file paths or code snippets — they go stale. Record in `memory/SPEC.md` §Decisions when finalized.

## Testing Decisions

- What makes a good test here (behavior, not implementation)
- Which modules get tested
- Prior art in the codebase

## Out of Scope

What this refactor deliberately excludes.
```

## Routing

After filing the refactor plan, present these options to the user (use `tool-ask-question`):

| #   | Label              | Target       | Why                                                          |
| --- | ------------------ | ------------ | ------------------------------------------------------------ |
| 1   | Build first commit | `ln-build`   | Refactor plan is clear; implement one commit-sized step from `memory/REFACTOR.md` |
| 2   | Scope a commit     | `ln-scope`   | A commit needs more precise behavior/acceptance definition   |
| 3   | Back to triage     | `ln-consult` | Plan needs reassessment                                      |

Recommended: **1** when the first commit step is concrete enough to execute; otherwise **2**

---
*Adapted from [mattpocock/skills/request-refactor-plan](https://github.com/mattpocock/skills/tree/main/request-refactor-plan).*
