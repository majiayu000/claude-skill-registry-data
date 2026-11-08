---
name: audit
description: 'Audits code for bugs, security and quality issues, writing a report-only findings file. Use when the user wants code checked for problems and reported without changes ("audit", "find bugs", "security review"). Not for one known bug (use debug).'
argument-hint: '[depth:standard|deep] [scope:branch|global|working] [optional focus]'
allowed-tools: Agent, Bash(git rev-parse *), Bash(git symbolic-ref *), Bash(git merge-base *), Bash(git diff *), Bash(git ls-files *), Bash(git log *), Bash(git check-ignore *), Bash(mkdir *), Bash(date *), Bash(sort *), Bash(uniq *), Bash(mv *), Bash(printf *), Bash(${CLAUDE_PLUGIN_ROOT}/shared/journal-artifact.sh *), Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskGet, TaskList, TaskStop, AskUserQuestion, WebFetch, WebSearch
---

# Autonomous Problem-Locator Pipeline (report-only)

## Overview

Orchestrates a multi-lens codebase audit and produces a ranked findings report. Two depth modes:

- **`depth:standard`** (default) — single-wave parallel researchers across correctness, security, performance, maintainability, and reliability lenses. Quick scan suitable for in-progress work or focused bug hunts. Cap mode: `quick` per `<PLUGIN_ROOT>/shared/severity-lattice.md`.
- **`depth:deep`** — pre-PR multi-wave audit with blast-radius tier gating, evidence-tiered severity caps, trust-boundary STRIDE delta, three blinded adversarial lenses, rollback rehearsal (BLOCKING for missing down-migrations), cognitive-load budget, and persistent ledger append. Cap mode: `pre-PR`.

No code is modified in either mode. Hand the summary to `build`, `debug`, or `polish` to act on it.

## When to Use

A report-only hunt for problems across multiple files and concern categories, as a quick scan or a deeper pre-PR pass.

### When NOT to use

- A single known bug — use `debug`.
- Building new functionality — use `build`.
- Behavior-preserving cleanup with no bug hunt — use `polish` with a cleanup criterion.
- Only running the existing tests, lint and type checks — run them directly; no pipeline is needed.
- You want the findings fixed automatically — this skill does not edit code; pass the summary to `build`, `debug`, or `polish` afterwards.

## Input

- `$ARGUMENTS` — Optional `depth:` modifier (default `standard`), scope hint (`scope:branch`), lens hint (`"security review"`), or combination. If ambiguous, ask. Never guess.

## Scope Parameter

See `<PLUGIN_ROOT>/shared/scope-parameter.md` for the canonical scope modes (`branch`, `global`, `working`) and their git commands.

- `scope:` controls files, remaining argument text controls lenses (orthogonal).
- **Default**: `depth:standard` → path-like tokens → scope, no path tokens → roam. `depth:deep` → default scope `branch`.
- `global` mode additionally excludes test files in this skill.
- Bounded scopes (`branch`, `working`, path-list) auto-invoke `<PLUGIN_ROOT>/shared/blast-radius.md` to expand the inspection set with downstream-impacted files. `global` skips the auto-invocation.

## Core Principles

1. **Research only.** This skill is read-only — it finds and reports, it does not fix.
1. **Parallel lenses, consolidated output.** Diverse lenses find different bug classes; one merged report is the final artifact.
1. **Severity lattice is shared.** Both depth modes produce findings on the same 6-level lattice (`<PLUGIN_ROOT>/shared/severity-lattice.md`) so reports compare cleanly.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **MAX_RESEARCHERS**: 5 (standard) | **MAX_RESEARCHERS_WAVE_A**: 6 (deep) | **MAX_RESEARCHERS_WAVE_B**: 3 (deep)
- **Severity caps**: cap modes `quick` (standard) and `pre-PR` (deep) from `<PLUGIN_ROOT>/shared/severity-lattice.md`. Findings over a cap are written to `findings_capped.md`, never dropped.
- **CRITICAL_CAP**: unlimited, BLOCKING included — a ship-stopper cut from the report body would defeat the audit.
- **HIGH_CAP**: 10 (standard) | unlimited (deep) — standard lists what is worth fixing today; deep makes every HIGH visible before a PR.
- **MEDIUM_CAP**: 5 (standard) | 10 (deep) — keeps the report body scannable.
- **LOW_CAP**: 0, INFO included (both modes) — style-level findings are counted in the report and listed in `findings_capped.md`.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/` | **LEDGER_PATH**: `<PROJECT_ROOT>/.mz/reports/audit_ledger.md` (deep mode only)
- **HOTSPOT_LOOKBACK_DAYS**: 90 (deep mode only — git log lookback for hotspot table; falls back to all-history on shallow clones)
- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`. Phase files write `<SKILL_DIR>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

#### `depth:standard` (default)

| #   | Phase                  | Reference                | Loop? |
| --- | ---------------------- | ------------------------ | ----- |
| 0   | Setup                  | inline below             | —     |
| 1   | Scope & Lens Selection | `phases/research.md`     | —     |
| 2   | Multi-Lens Research    | `phases/research.md`     | —     |
| 3   | Consolidate & Rank     | `phases/consolidate.md`  | —     |
| 4   | Final Report           | `phases/final_report.md` | —     |

#### `depth:deep`

| #   | Phase                                               | Reference                       | Loop? |
| --- | --------------------------------------------------- | ------------------------------- | ----- |
| 0   | Setup (+ tooling detect + git hotspots)             | inline below                    | —     |
| 1   | Scope Intelligence Gate (T0–T3 tiering)             | `phases/scope_and_tier_deep.md` | —     |
| 2   | Multi-Lens Research (Wave A + Wave B)               | `phases/research_deep.md`       | —     |
| 3   | Consolidate, Evidence-Cap, Rollback, Cognitive-Load | `phases/consolidate_deep.md`    | —     |
| 4   | Final Report + Ledger Update                        | `phases/final_report_deep.md`   | —     |

### Phase 0: Setup

Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.

Derive `<YYYY_MM_DD>_audit_<slug>` (or `<YYYY_MM_DD>_deep_audit_<slug>` when `depth:deep`). **Resume check** (before creating the task directory): follow `<PLUGIN_ROOT>/shared/resume-protocol.md`, "On entry". A `complete`, `completed` or `aborted_by_user` file starts a `_vN`. A `pending`, `running`, `blocked` or `failed` file gets the resume gate. When the run is unattended or nobody can answer, report the path, `Status` and `what_remains`, and stop. For a fresh task, run `mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>"` and write `state.md` per `<PLUGIN_ROOT>/shared/state-schema.md` — first line `schema_version: 2`, followed by `Status`, `Phase`, `Started`, `Iteration` (review iterations), `FilesWritten`, and the progress-ledger keys `phase_complete: false` and `what_remains: []`, plus skill-specific keys (`depth: standard|deep`). TaskCreate per phase.

When `depth:deep`: additionally dispatch `pipeline-tooling-detector` to detect test/lint commands for informational purposes (no tests are run); pass `project_root: <PROJECT_ROOT>` and `output_path: <PROJECT_ROOT>/.mz/task/<task_name>/tooling.md`. Phase 1 also computes git hotspot scores (commit counts over the last `HOTSPOT_LOOKBACK_DAYS` days, bot commits filtered) and records them in `scope.md`.

### Phases 1–4

Route by `depth:` to the phase files in the table above. Both depth modes stop at the report — neither modifies code. The blinded invariant in `depth:deep` Phase 2 (Wave B dispatched as typed `pipeline-researcher` agents, in its own wave after Wave A completes) has no exceptions.

## Common Rationalizations

| Rationalization                       | Rebuttal                                                               |
| ------------------------------------- | ---------------------------------------------------------------------- |
| "severity is subjective, label later" | "unlabeled audits get ignored"                                         |
| "one-pass scan is enough"             | "multi-lens is the point of an audit; single-lens is a grep"           |
| "let me just fix this one thing"      | "audit is report-only; fixing mid-run destroys the report's integrity" |

## Red Flags

- You modified code. This skill does not edit files; if fixes are needed, hand off to `build`, `debug`, or `polish`.
- Findings were not severity-labeled before writing `summary.md`.
- A single-lens scan was declared "audit complete".

## Verification

Output the final `summary.md` block: finding counts by severity, files touched (scanned, not modified), lenses run, path to `findings.md` for the full detail.

## References

- `${CLAUDE_SKILL_DIR}/references/owasp-top-10-checklist.md`: OWASP Top 10 (2021) checks by category, with detection patterns. Grep it for the category a finding touches.
- `${CLAUDE_SKILL_DIR}/references/blast-radius-tier-rules.md`: T0-T3 blast-radius tier definitions and the overall-tier computation. Read it in full at Phase 1 of `depth:deep`.
- `${CLAUDE_SKILL_DIR}/references/trust-boundary-patterns.md`: code patterns that mark a trust boundary, by language and layer. Read it at Phase 1 of `depth:deep` when `overall_tier` is T2 or higher.
- `${CLAUDE_SKILL_DIR}/references/evidence-tier-rules.md`: evidence tiers and severity caps. Read it in full at Phase 3 of `depth:deep`.

## Error Handling

- **Ambiguous argument**: ask before Phase 1. **Empty scope / zero findings**: report and exit.
- **Researcher fails**: continue with remaining lenses, flag in the report.
- **Write conflict on findings.md**: retry once, then escalate.

## State Management

Update `state.md` after each phase with current phase, files scanned, escalation notes. Allows resumption if interrupted.

Maintain the progress ledger on every phase transition: set `phase_complete: false` on entering a phase and `true` only once its artifacts are written and its gates pass; refresh `what_remains` (outstanding work as plain strings) — it must be `[]` when `Status: complete`. Stamp `last_verified` whenever a verification gate passes clean. Reading a `schema_version: 1` or unversioned `state.md` upgrades it in place: add the ledger keys, set `schema_version: 2`, and log the upgrade. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`.
