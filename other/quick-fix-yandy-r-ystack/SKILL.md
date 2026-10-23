---
name: quick-fix
description: 'Applies inline Quick Review findings without review artifacts. Use when choosing Apply fixes after quick-review, fixing pasted Quick Review findings, or making artifact-free review fixes.'
argument-hint: '[--parallel] [--severity <level>] <quick-review findings block>'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Agent
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(git:*)
  - Bash(npm:*)
  - Bash(pnpm:*)
  - Bash(yarn:*)
  - Bash(bun:*)
  - Bash(npx:*)
  - Bash(cargo:*)
  - Bash(go:*)
  - Bash(pytest:*)
  - Bash(python:*)
  - Bash(python3:*)
  - Bash(make:*)
---

# Quick Fix

Apply fixes from an inline Quick Review findings block without writing or
updating a review artifact.

**Core rule**: This skill is artifact-free. It MUST NOT create files under
`docs/prps/reviews/` — that would lose the audit contract — and it MUST NOT
update any review markdown file. If the
user wants an auditable artifact, route them to `/ycc:review-fix` with a saved
review file instead.

**Input**: `$ARGUMENTS`

---

## Phase 0 — Parse flags

Extract flags from `$ARGUMENTS`:

| Flag                 | Effect                                                                                |
| -------------------- | ------------------------------------------------------------------------------------- |
| `--parallel`         | Dispatch independent same-file groups to `ycc:review-fixer` in parallel.              |
| `--severity <level>` | Minimum severity to fix. Valid: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`. Default: `HIGH`. |

Strip these flags and set `PARALLEL_MODE` and `MIN_SEVERITY` (default `HIGH`).
The remaining text is the inline review payload.

**Validation**:

- `--severity` value not one of `CRITICAL|HIGH|MEDIUM|LOW` -> abort with:
  `Invalid --severity value. Use CRITICAL, HIGH, MEDIUM, or LOW.`
- Remaining payload is empty -> abort with:
  `Error: /ycc:quick-fix requires an inline Quick Review findings block.`

---

## Phase 1 — Parse findings

Parse the inline payload — the quick-review findings subset of the shared
Review Artifact Format:

`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/review-artifact-format.md`

Build an in-memory list of `Finding` objects:

- `id`
- `severity`
- `file`
- `line`
- `description`
- `status`
- `category`
- `suggested_fix`

If no parseable findings exist, stop with:

```
Error: No parseable quick-review findings found.
```

If every parsed finding is already `Fixed` or `Failed`, stop with:

```
All findings in this quick review have already been processed.
Nothing to do.
```

---

## Phase 2 — Filter

Apply filters in this order:

1. Keep only findings with `Status: Open`.
2. Keep only findings at or above `MIN_SEVERITY`, using
   `CRITICAL > HIGH > MEDIUM > LOW`.
3. Drop findings without a non-empty `Suggested fix`.
4. Drop findings whose target file no longer exists (`test -f "$FILE"`).

Print a compact filter summary:

```
Quick Fix Filter Results:
  Total findings:              N
  Already processed:           A
  Below severity threshold:    B  (threshold: HIGH)
  No suggested fix:            C
  Missing files:               D
  Eligible for fixing:         M
```

If `M == 0`, stop with `No eligible findings to fix.`

---

## Phase 3 — Detect validation command

Detect one project-level type-check command to pass to `ycc:review-fixer`.
Use the first matching rule:

| File Exists         | Command            |
| ------------------- | ------------------ |
| `bun.lockb`         | `bun test`         |
| `pnpm-lock.yaml`    | `pnpm typecheck`   |
| `yarn.lock`         | `yarn typecheck`   |
| `package-lock.json` | `npx tsc --noEmit` |
| `Cargo.toml`        | `cargo check`      |
| `go.mod`            | `go vet ./...`     |
| `pyproject.toml`    | `pytest`           |

If no command is detected, set:

```
PROJECT TYPE-CHECK COMMAND: SKIP (no supported project validation command detected)
```

`ycc:review-fixer` is allowed to skip verification only for this explicit
`SKIP (...)` value.

---

## Phase 4 — Plan batches

Group eligible findings by file. Same-file findings MUST be processed by the
same `ycc:review-fixer` agent and sorted by line number descending.

Sort groups by highest severity in the group (`CRITICAL`, `HIGH`, `MEDIUM`,
`LOW`), then by file path.

Print:

```
Quick Fix Plan:
  Eligible findings:  M
  Same-file groups:   G
  Mode:               sequential | parallel

Group 1: src/file.ts (2 findings)
  - F003 HIGH line 80
  - F001 HIGH line 42
```

---

## Phase 5 — Execute

Every `ycc:review-fixer` prompt must include:

```
SOURCE REVIEW FILE: (quick-fix ephemeral handoff)
PROJECT TYPE-CHECK COMMAND: <detected command or SKIP (...)>
```

This tells the fixer not to expect or edit a review artifact.

### Sequential mode

Process groups one at a time.

For a one-finding group, dispatch a single `ycc:review-fixer` agent with Shape A:

```text
FINDING:
  ID: F001
  Severity: HIGH
  File: src/file.ts
  Line: 42
  Category: Correctness
  Description: Description
  Suggested fix: Concrete fix

SOURCE REVIEW FILE: (quick-fix ephemeral handoff)
PROJECT TYPE-CHECK COMMAND: pnpm typecheck
```

For a same-file group, dispatch one `ycc:review-fixer` agent with Shape B:

```text
FINDINGS (same file, sorted by line descending):
  1. F003 — HIGH — src/file.ts:80 — Description — Suggested fix: Concrete fix
  2. F001 — HIGH — src/file.ts:42 — Description — Suggested fix: Concrete fix

SOURCE REVIEW FILE: (quick-fix ephemeral handoff)
PROJECT TYPE-CHECK COMMAND: pnpm typecheck
```

Collect each agent's `STATUS: Fixed` or `STATUS: Failed` result. Do NOT edit any
artifact status lines.

### Parallel mode

Process one batch containing all same-file groups. Dispatch all groups in a
single message with multiple `Agent` calls, one call per file group:

- `subagent_type`: `ycc:review-fixer`
- `description`: `Quick-fix <ids> in <file>`
- `prompt`: Shape A or Shape B as above

Wait for all agents to return, then collect statuses.

---

## Phase 6 — Report

Print an inline result summary:

```markdown
# Quick Fix Results

Fixed: N
Failed: M
Skipped: K

## Fixed

- F001 `src/file.ts:42` — <brief agent-reported change>

## Failed

- F004 `src/other.ts:10` — <blocker and recommendation>

## Notes

No review artifact was written. Re-run `/ycc:quick-review` if you need a fresh
post-fix review.
```

If any finding failed, include the fixer agent's `BLOCKER` and `RECOMMENDATION`
so the user can decide whether to save a formal review artifact or fix manually.

---

## Relationship to review-fix

- `/ycc:quick-fix` is for ephemeral, inline quick-review findings.
- `/ycc:review-fix` is for artifacts under `docs/prps/reviews/`.
- Do not teach `/ycc:review-fix` to parse inline quick-review payloads; keeping
  the workflows separate preserves the audit trail contract for artifact-backed
  reviews.
