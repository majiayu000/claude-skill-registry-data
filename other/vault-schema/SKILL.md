---
name: vault-schema
description: 'Validates vault frontmatter against a note-type schema and migrates notes to match. Use when the user wants frontmatter checked ("vault schema", "frontmatter validation", "schema migration"). Not for links, orphans, stubs or tags (use vault-health).'
argument-hint: '<validate|migrate> [vault path]'
allowed-tools: Agent, Read, Write, Grep, Glob, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(sha256sum *), Bash(awk *), Bash(cut *), AskUserQuestion
---

# Vault Schema

## Overview

Discipline skill that manages a flat YAML schema DSL at `.mz/vault-schema.yml` and governs vault frontmatter compliance. The `validate` mode dispatches `schema-validator` to produce severity-labeled findings against declared note_types. The `migrate` mode turns `Critical:` findings into an approval-gated migration plan, writes a rollback manifest before any write, and patches non-conforming frontmatter only after explicit user approval.

## When to Use

Declaring a vault schema, checking notes against it, or back-filling missing frontmatter after a schema change.

### When NOT to use

- Editing note body content — use `Edit` directly.
- Orphan detection, broken-link sweeps, or stub audits — use `vault-health`.
- Renaming or moving notes across the vault — use `vault-refactor`.
- Adding links to existing notes — use `vault-connect`.

## Arguments

`$ARGUMENTS` is `<mode> [vault path]` where `<mode>` is `validate` (default) or `migrate`. If the mode is omitted, default to `validate`. If the vault path is omitted, resolve from `OBSIDIAN_VAULT_PATH` env, then `MZ_VAULT_PATH` env, then walk up from the working directory looking for `.obsidian/`. If no path resolves, escalate via AskUserQuestion — never guess.

## Constants

- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`. Phase files write `<SKILL_DIR>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.
- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **SCHEMA_PATH**: `.mz/vault-schema.yml` — relative to vault root.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **MAX_MIGRATION_BATCH**: 50 — hard cap on notes patched per migrate run.
- **REPORT_PREVIEW_WORDS**: 200 — truncation cap if an approval gate needs a preview.

## Core Process

### Phase Overview

| Phase | Goal                      | Details              |
| ----- | ------------------------- | -------------------- |
| 0     | Setup                     | Inline below         |
| 1     | Validate                  | `phases/validate.md` |
| 1.5   | User approval — findings  | Inline below         |
| 2     | Plan migration + rollback | `phases/migrate.md`  |
| 2.5   | User approval — plan      | Inline below         |
| 3     | Apply frontmatter patches | `phases/migrate.md`  |

Phases 2, 2.5, and 3 run only when `<mode>` is `migrate`. In `validate` mode the skill stops after Phase 1.5 approval and reports the findings as-is.

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS` for `<mode>` (default `validate`) and `[vault path]`.
1. Resolve vault path via the ladder in the Arguments section. Escalate via AskUserQuestion if nothing resolves.
1. Compute `SCHEMA_PATH` as `<vault>/.mz/vault-schema.yml`.
1. If `SCHEMA_PATH` does not exist, present the bootstrap template from `${CLAUDE_SKILL_DIR}/references/schema-dsl-syntax.md` via AskUserQuestion with options **Accept** — write the template to `SCHEMA_PATH` and continue · **Edit** — provide your own schema text · **Abort** — stop. On **Accept**, write the template. On **Edit**, accept the user's pasted YAML. On **Abort**, halt cleanly. Never fabricate a schema.
1. Derive `task_name = <YYYY_MM_DD>_vault-schema_<mode>` where `<YYYY_MM_DD>` is today's date (underscores); on same-day collision append `_v2`, `_v3`. Create `TASK_DIR<task_name>/` on disk.
1. Write `state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `phase_complete: false`, `what_remains: []`, `Mode: <validate|migrate>`, `Vault: <path>`, `SchemaPath: <path>`.
1. Print a visible setup block showing `task_name`, resolved vault path, mode, and schema path.

### Phase 1 — Validate

See `phases/validate.md`.

### Phase 1.5: User approval — findings

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/validation_report.md` and capture its full contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: findings gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the artifact verbatim as a normal markdown chat message:

```
## Validation findings ready for review — vault-schema

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/validation_report.md>

---
**Approve** → findings approved; proceed to Phase 2 (migration planning) if mode is migrate, otherwise mark complete  ·  **Reject** → abort, no further action  ·  reply with feedback to revise
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/validation_report.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the artifact in the question body:

- question: `The validation findings above are ready for review.`
- header: `Findings`
- options: **Approve** — proceed to Phase 2 (migration planning) or complete if mode is validate · **Reject** — abort, no further action

**Response handling**:

- **Approve** → add `- findings approved: .mz/task/<task_name>/validation_report.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, and set `Phase: findings_approved`. If `Mode: validate`, set `Status: complete`, `phase_complete: true`, `what_remains: []` and stop — nothing is written to the vault in validate mode. If `Mode: migrate`, proceed to Phase 2.
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → incorporate (e.g., "re-scan with a corrected schema", "treat note_type X as pass-through"), re-run Phase 1 if needed, overwrite `validation_report.md`, return to Surface 1, re-read the updated artifact, and re-emit the entire plan message from scratch. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: findings gate`, stop. A missing answer is never approval.

### Phase 2 — Plan migration + rollback

See `phases/migrate.md` (Step 1 + Step 2).

### Phase 2.5: User approval — migration plan

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/migration_plan.md` and capture its full contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: migration gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the artifact verbatim as a normal markdown chat message:

```
## Migration plan ready for review — vault-schema

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/migration_plan.md>

---
**Approve** → proceed to Phase 3 (apply patches)  ·  **Reject** → abort, no vault writes occurred, rollback manifest preserved  ·  reply with feedback to revise
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/migration_plan.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the artifact in the question body:

- question: `The migration plan above is ready for review.`
- header: `Migration`
- options: **Approve** — proceed to Phase 3 (apply patches) · **Reject** — abort, no vault writes occurred, rollback manifest preserved

**Response handling**:

- **Approve** → add `- plan approved: .mz/task/<task_name>/migration_plan.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: plan_approved`, and proceed to Phase 3. The user must have filled in every `"<NEEDS_VALUE>"` and `"<PICK: ...>"` placeholder — Phase 3 re-checks this and loops back here if any remain.
- **Reject** → update state to `aborted_by_user` and stop. The rollback manifest stays on disk for reference; no vault writes occurred.
- **Any other reply (feedback)** → incorporate edits to the plan (value picks, skip specific notes, adjust proposed frontmatter), re-run Phase 2 to refresh both `migration_plan.md` and `rollback.md`, overwrite the artifact, return to Surface 1, re-read the updated artifact, and re-emit the entire plan message from scratch. This is a loop — repeat until the user explicitly approves. Never apply frontmatter patches without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: migration gate`, stop. A missing answer is never approval.

### Phase 3 — Apply frontmatter patches

See `phases/migrate.md` (Step 4).

## Common Rationalizations

| Rationalization                                                                            | Rebuttal                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "The schema is missing — just validate against sensible defaults."                         | "Pass-through is the declared behavior when a schema is absent. Fabricated defaults invent a contract the user never approved and produce false-positive findings that erode trust across runs. Bootstrap via AskUserQuestion, never guess." |
| "Skip the rollback manifest — patches are trivial, we can undo by hand."                   | "Rollback is non-negotiable. Ctrl-C mid-batch leaves the vault half-patched with no recovery record. The manifest is a disk-persisted artifact that survives context compaction; memory of what changed does not."                           |
| "Auto-pick values for `allowed_values` violations — the user will accept the obvious one." | "Enum picks are irreversible without rollback and 'obvious' is a guess. The skill surfaces `<PICK: ...>` placeholders precisely so the user owns the value, not the orchestrator. Silent auto-pick is how 'helpful' becomes data loss."      |
| "The batch exceeds MAX_MIGRATION_BATCH — just raise the cap inline."                       | "The cap exists so approval-gate review stays human-sized. Raising it inline silently moves the review from 'readable' to 'rubber-stamped'. Split the batch and run again — the gate is load-bearing, not decoration."                       |

## References

- `${CLAUDE_SKILL_DIR}/references/schema-dsl-syntax.md`: DSL v1 syntax, semantics, migrator interaction, common patterns and v2 candidates. Grep it for the construct you need; read its v1 template in Phase 0 when `SCHEMA_PATH` is missing.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
