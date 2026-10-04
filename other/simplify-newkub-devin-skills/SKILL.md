---
name: simplify
description: Simplify files — shorter and clearer with identical behavior — condense verbosity, remove redundancy
argument-hint: "[@files... | dir]"
related:
  - refactor
  - refactor-skills
  - check-long-files
  - improve
  - deep-validate
  - report
  - suggest-next-action

---

## Goal

Reduce file size and complexity while preserving exact behavior and semantics — condense verbose blocks, remove redundancy, flatten unnecessary nesting.

## Scope

Code files, docs, and SKILL.md files. Boundary: restructuring/splitting files or changing boundaries → `/refactor`; skill-package conventions → `/refactor-skills`.

## Execute

### 1. Identify Targets

> Goal: know which files to simplify

1. `@files...` or dir → those targets; no arg → run `/check-long-files` and pick the worst offenders, or `/ask-me`

### 2. Detect Opportunities

> Goal: every simplification has evidence

| No. | Pattern | Fix |
|-----|---------|-----|
| 1 | Duplicated blocks/branches | Extract once or collapse to shared path |
| 2 | Verbose conditionals / unneeded nesting | Guard clauses, ternaries, early returns |
| 3 | Dead code, unused vars/imports | Delete |
| 4 | Single-use variables / over-abstraction | Inline |
| 5 | Redundant comments / repeated prose | Remove what the code already says |
| 6 | Verbose docs sections (docs/SKILL.md) | Condense to tables/lists; merge near-duplicate items |

### 3. Simplify

> Goal: minimal diff, identical behavior

1. Apply smallest change per pattern — public API, semantics, and behavior unchanged
2. Keep readability — never compress into cryptic one-liners
3. Checkpoint per file before moving to the next

### 4. Validate

> Goal: behavior proven identical

Code → `/run-check` (lint/typecheck); docs → re-read for preserved meaning.

### 5. Report

> Goal: measurable result

`/report` table: No. | File | Before | After | Change — then `/suggest-next-action`.

## Rules

| No. | Group | Rule |
|-----|-------|------|
| 1 | Preserve behavior | No semantic changes — Two Hats; simplification is a refactor, not a rewrite |
| 2 | Minimal diff | Touch only what the detected pattern requires — no drive-by edits |
| 3 | Readability first | Shorter only when clearer — never trade clarity for line count |
| 4 | Boundary | Splitting files or moving code across boundaries → `/refactor`, not this skill |
| 5 | Evidence | Report real before/after counts — never claim a reduction without measuring |

## Expected Outcome

- Target files measurably shorter and clearer — same behavior, same public API
- Lint/typecheck pass; docs keep identical meaning
- Before/after report with per-file line counts
