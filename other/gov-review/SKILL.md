---
name: gov-review
description: 'Audits ADRs, RFDs and design docs into a read-only findings report. Use when the user wants existing decision records checked ("review our ADRs", "audit decision records", "check governance docs"). Not for reviewing code changes (use review-branch).'
argument-hint: '[path-or-glob] [docs/decisions|docs/rfcs|docs/design]'
allowed-tools: Agent(gov-audit-reviewer), Read, Write, Grep, Glob, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), AskUserQuestion
---

# Governance Artifact Review (read-only)

## Overview

Audits already-written governance artifacts — ADRs, RFDs, and design docs — against a six-axis quality rubric and reports where they fall short. Globs the artifact directories (or a user-supplied path/glob), fans `gov-audit-reviewer` out one-per-artifact, collects each `VERDICT:`, and writes a single ranked review report with a per-artifact table plus an aggregate roll-up. This skill reads and reports only — it never edits an artifact. Hand the report to `govern` (to re-decide a failing record) or fix the artifact by hand.

## When to Use

Checking the quality of existing decision records (ADRs, RFDs and design docs), whether one artifact or a whole directory.

### When NOT to use

- Making or recording a **new** decision — use `govern`.
- Reviewing **code** for bugs or a branch diff — use `audit` or `review-branch`.
- Writing or fixing an artifact — this skill is read-only; it produces findings, not edits.

## Input

- `$ARGUMENTS` — Optional. A path or glob to the artifacts to review (`docs/decisions/0003-*.md`, `docs/rfcs/`, a single file), and/or one of the dir hints `docs/decisions` | `docs/rfcs` | `docs/design`. If empty, the audit phase globs all three default artifact directories. Ambiguous or unrecognizable input → ask via AskUserQuestion, never guess.

## Approval gate

None. This skill is read-only — it scores artifacts and writes a report under `REPORT_DIR`, modifying no governance artifact — so no user approval gate is required. The reviewer agents are likewise read-only (`Read, Grep, Glob`).

## Constants

- **MAX_REVIEWERS**: 6 (parallel `gov-audit-reviewer` agents per wave; overflow runs in sequential waves)
- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **REPORT_DIR**: `<PROJECT_ROOT>/.mz/reviews/`
- **ARTIFACT_DIRS**: `docs/decisions/*.md`, `docs/rfcs/*.md`, `docs/design/*.md` (the default glob set when no path/glob is supplied)
- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`. Phase files write `<SKILL_DIR>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Expand `<PLUGIN_ROOT>/...` in phase files the same way.

## Core Process

### Phase Overview

| #   | Phase | Reference         | Loop? |
| --- | ----- | ----------------- | ----- |
| 0   | Setup | inline below      | —     |
| 1   | Audit | `phases/audit.md` | —     |

### Phase 0: Setup

1. **Resolve `PROJECT_ROOT`** with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. **Parse the argument.** Split `$ARGUMENTS` into tokens. A token that is a path, a glob (contains `*`/`?`), or an existing directory becomes the artifact source. A bare dir hint (`docs/decisions` | `docs/rfcs` | `docs/design`) selects that one directory. No path/glob token → the audit phase falls back to **ARTIFACT_DIRS**. If a token is unrecognizable (neither a path, a glob, nor a dir hint), ask via AskUserQuestion which artifacts to review — never guess a source.
1. **Derive the task name** `<YYYY_MM_DD>_gov-review_<slug>` where `<YYYY_MM_DD>` is today's date with underscores and `<slug>` is a snake_case summary (max 20 chars) of the argument (e.g. `decisions`, `all_docs`); on same-day collision append `_v2`, `_v3`.
1. **Create** `TASK_DIR<task_name>/` and **write `state.md`** per the inline v2 contract below — `Status: running`, `Phase: 0`, the parsed artifact source, and the resolved **REPORT_DIR** report path.
1. **Emit a visible setup block**: `task_name`, the artifact source (parsed glob/path or "default ARTIFACT_DIRS"), **MAX_REVIEWERS**, and the report path. Then read `phases/audit.md` and run Phase 1.

### Phase 1: Audit

List the files in the artifact source, dispatch `gov-audit-reviewer` per artifact (parallel up to **MAX_REVIEWERS**, sequential overflow waves, each wave with a pre-dispatch manifest and a post-wave rollup), collect every `VERDICT:`, and write the review report to **REPORT_DIR**. See `phases/audit.md`. If zero artifacts are found, report that clearly and stop — do not fabricate findings.

## Red Flags

- You dumped the full report inline instead of reporting its path, or claimed a verdict for an artifact whose reviewer returned no `VERDICT:` line.

## Verification

Output a final block: the report path under **REPORT_DIR**, the aggregate roll-up (N artifacts reviewed, M failing), and the per-artifact verdict list. Confirm the report file exists. If any reviewer returned no `VERDICT:`, name that artifact as unscored rather than counting it as a pass.

## References

- `${CLAUDE_SKILL_DIR}/references/review-rubric.md`: the six scoring axes, severity labels, output format and the false-positive list. `gov-audit-reviewer` reads it in full before scoring each artifact; `phases/audit.md` passes its path in every dispatch.

## Error Handling

- **Zero artifacts found** at the resolved source → report it (the directories may be empty or the glob too narrow) and stop. Do not invent artifacts.
- **Unrecognizable argument** → escalate via AskUserQuestion before Phase 1; never guess the source.
- **A reviewer returns `BLOCKED` / `NEEDS_CONTEXT` / no `VERDICT:`** → record it in the report as unscored (not a pass) and continue with the rest; retry a single empty dispatch once before marking it unscored.
- Never guess on ambiguity — escalate via AskUserQuestion.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
