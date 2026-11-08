---
name: gov-init
description: 'Installs, updates or removes the governance policy in CLAUDE.md. Use when the user wants governance set up ("gov init", "install governance policy", "set up governance"). Not for running a decision (use govern) or auditing records (use gov-review).'
argument-hint: '[project|global] [--force] [--uninstall]'
allowed-tools: Read, Write, Edit, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Glob, Grep, AskUserQuestion
---

# Gov Init

## Overview

Install the `mz-gov` governance policy into `CLAUDE.md` so Claude proactively reaches for the `govern` pipeline on substantial, ambiguous decisions. The policy is injected as a single sentinel-wrapped block — idempotent on re-run, cleanly removable on `--uninstall`. This is the only delivery mode: the block goes into `CLAUDE.md`, nothing else.

## When to Use

Installing, updating or removing the governance policy block in `CLAUDE.md`, for one project or globally.

### When NOT to use

- The user wants to run a governance decision on a change — use `govern`.
- The user wants to audit existing artifacts — use `gov-review`.
- The user wants to edit the policy text itself — open the injected block in `CLAUDE.md` directly, or re-run with `--force` after editing the source.
- `CLAUDE.md` is managed by another tool and must not be touched.

## Arguments

- `project` (default) → inject into `./CLAUDE.md`
- `global` → inject into `~/.claude/CLAUDE.md`
- `--force` → replace the existing policy block in place (only between the sentinels)
- `--uninstall` → remove the policy block previously installed by this skill

Parse from `$ARGUMENTS`. Unknown or conflicting tokens → AskUserQuestion; never guess.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`. Phase files write `<SKILL_DIR>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Expand `<PLUGIN_ROOT>/...` in phase files the same way.

## Core Process

### Phase Overview

| Phase | Goal                         | Details         |
| ----- | ---------------------------- | --------------- |
| 0     | Setup                        | Inline below    |
| 1     | Install / update / uninstall | `phases/run.md` |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS`: scope (`project`/`global`, default `project`), `--force`, `--uninstall`. Unknown or conflicting token → AskUserQuestion.
1. `task_name` = `<YYYY_MM_DD>_gov-init_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<slug>` is a snake_case summary of the args (e.g. `project`, `global_uninstall`, max 20 chars). On same-day collision append `_v2`, `_v3`.
1. Create `<PROJECT_ROOT>/.mz/task/<task_name>/`.
1. Write `state.md` with `schema_version: 2` as its first line, then `Status: running`, `Phase: 0`, `Started: <ISO>`, `phase_complete: false`, `what_remains: []`, `Scope: <project|global>`, `Force: <bool>`, `Uninstall: <bool>`, `Action: <pending>`, `Target: <resolved path>`.
1. Emit setup block: task_name, scope, resolved target path, mode flags.

The approval gate in `phases/run.md` must run before any write to `CLAUDE.md`. A single run-level confirmation covers the write.

Read `phases/run.md` and proceed to Phase 1.

## Verification

After install, grep `CLAUDE.md` for exactly one `mz-gov:governance-policy` start sentinel (zero after uninstall). See `phases/run.md`.

## Error Handling

- **Empty / ambiguous / conflicting argument** → AskUserQuestion; never guess.
- **Missing tooling** — if `${CLAUDE_SKILL_DIR}/policy/governance-policy.md` is not readable, AskUserQuestion with the failing path.
- **`CLAUDE.md` unreadable or unwritable** → AskUserQuestion with the exact path and error; never fall back silently.
- **Duplicate `mz-gov:governance-policy` sentinels found** (manual edit or prior bug) → stop, report the conflicting lines, ask the user to resolve before re-running.
- **Plugin version unreadable** → use the literal `unknown` for the version tag and note it in the report.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

Record `Action:` (`installed` | `replaced` | `skipped` | `removed`) and the resolved `Target:` after Phase 1. Never rely on conversation memory for cross-phase state — context compaction destroys specific paths and decisions.
