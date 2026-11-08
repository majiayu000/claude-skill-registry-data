---
name: vault-health
description: 'Audits a whole Obsidian vault for orphan notes, broken wikilinks, stubs, stale notes and tag inconsistencies. Use when the user wants a vault audit ("vault health check", "find orphan notes"). Not for frontmatter schema rules (use vault-schema).'
argument-hint: '[vault path or leave empty to use OBSIDIAN_VAULT_PATH env]'
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Read, Glob, Grep, Write, AskUserQuestion
---

## Overview

Discipline skill that audits an Obsidian vault and produces a structured `_vault_audit_YYYY-MM-DD.md` health note at the vault root. Checks: orphan notes (zero backlinks), broken wikilinks, stub notes (\<100 words, zero outlinks), stale notes (mtime >90 days + zero outlinks), and tag inconsistencies. Uses the official `obsidian` CLI when available, falls back to file scanning.

## When to Use

Auditing the structure of a whole vault (orphans, broken links, stubs, stale notes, tags), for weekly maintenance, before a knowledge review session, or after large imports.

### When NOT to use

- Frontmatter schema validation or migration — use `vault-schema`.
- Fixing the issues found — use `process-notes` or `vault-connect` after the audit.
- Semantic search or note retrieval — this skill only inventories health, it does not answer content queries.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **AUDIT_NOTE_PREFIX**: `_vault_audit_`
- **STUB_WORD_THRESHOLD**: 100
- **STALE_DAYS**: 90

## Arguments

`$ARGUMENTS` is an optional vault path. If empty, resolve from `OBSIDIAN_VAULT_PATH` env, then `MZ_VAULT_PATH` env. If none are set, ask via AskUserQuestion.

## Core Process

### Phase Overview

| Phase | Goal          | Details             |
| ----- | ------------- | ------------------- |
| 0     | Setup         | Inline below        |
| 1     | Collect       | `phases/collect.md` |
| 1.5   | User approval | Inline below        |
| 2     | Write audit   | `phases/report.md`  |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Resolve vault path from `$ARGUMENTS`, then `OBSIDIAN_VAULT_PATH`, then `MZ_VAULT_PATH`.
1. If no vault path resolved, escalate via AskUserQuestion — never guess.
1. `task_name` = `<YYYY_MM_DD>_vault-health_<vault-slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<vault-slug>` is a snake_case summary of the vault directory name (max 20 chars); on same-day collision append `_v2`, `_v3`.
1. Create `<PROJECT_ROOT>/.mz/task/<task_name>/`.
1. Write `state.md` with `schema_version: 2`, `phase_complete: false`, `what_remains: []`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `Vault: <resolved path>`.
1. Emit a visible setup block showing `task_name`, resolved vault path, and working dir.

### Phase 1 — Collect

See `phases/collect.md`.

### Phase 1.5: User approval gate

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/audit_data.md` and capture the full contents into context. The file contains the verbatim audit findings (orphans, broken wikilinks, stubs, stale notes, tag statistics with note names).

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: audit gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the audit findings verbatim as a normal markdown chat message:

```
## Vault health findings ready for review — vault-health

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/audit_data.md>

---
**Approve** → proceed to Phase 2, write the audit report to the vault  ·  **Reject** → abort without writing, task marked `aborted_by_user`  ·  reply with feedback to revise
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/audit_data.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the audit data in the question body, it lives in the plan message above:

- question: `The vault health findings above are ready for review.`
- header: `Audit`
- options:
  - **Approve** — proceed to Phase 2, write the audit report to the vault
  - **Reject** — abort without writing, task marked `aborted_by_user`

**Response handling**:

- **Approve** → add `- audit approved: .mz/task/<task_name>/audit_data.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: audit_approved`, and proceed to Phase 2 (write report).
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → adjust what to include (narrow a check, drop a category, re-run a collector), re-run Phase 1 if needed, then return to this gate, re-read `<PROJECT_ROOT>/.mz/task/<task_name>/audit_data.md`, and re-emit the entire plan message from scratch. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: audit gate`, stop. A missing answer is never approval.

### Phase 2 — Write audit

See `phases/report.md`.

## Common Rationalizations

| Rationalization                                        | Rebuttal                                                                                                                                     |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| "I can see the issues in my head, skip the audit note" | "The audit note is the log. Without it, patterns across weeks are invisible and you redo the same checks next week."                         |
| "Only run the fast checks, skip stale detection"       | "Stale notes are the silent knowledge rot. Skipping them is how 47% of captures never get processed."                                        |
| "Auto-fix the orphans without asking"                  | "An orphan may be intentionally isolated (inbox item, template). Auto-delete creates irreversible data loss — always surface before acting." |

## Red Flags

- Reporting results without writing an audit note (no log means no pattern detection over time).
- Auto-fixing broken links without showing what they were (breaks provenance).
- Skipping the approval gate and writing directly.

## Verification

Confirm `_vault_audit_YYYY-MM-DD.md` was written to the vault root. Print the orphan count and broken link count from the written audit.

## Error Handling

- **Vault path missing or invalid** → escalate via AskUserQuestion; never guess a default.
- **Obsidian CLI unavailable** → fall back to file scanning by listing and searching vault files; record the fallback in `state.md`.
- **Empty collector result** (agent returns nothing) → retry once with a clarified prompt; if still empty, note the gap in `state.md` and escalate via AskUserQuestion before writing.
- Never guess — on any ambiguity (ambiguous vault path, missing tooling, conflicting results) escalate via AskUserQuestion rather than fabricate.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
