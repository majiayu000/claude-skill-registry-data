---
name: vault-triage
description: 'Triages inbox fleeting notes with promote, merge, discard or defer decisions. Use when the user wants the inbox cleared fast ("triage inbox", "fleeting review", "clear inbox", "batch decide"). Not for resurfacing permanent notes (use vault-review).'
argument-hint: '[vault path]'
allowed-tools: Agent, Read, Write, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(rm *), Bash(sha256sum *), Bash(shasum *), Glob, AskUserQuestion
---

# Vault Triage

## Overview

Discipline skill that runs a 30-second triage pump over a small batch of fleeting inbox notes. The `triage-scorer` agent scores each note with a deterministic heuristic ladder and proposes a default decision from a closed vocabulary (`promote | merge | discard | defer`). The user accepts the defaults wholesale or overrides individual decisions. Merge targets are never chosen by the agent — the user names them explicitly.

## When to Use

Clearing a backlog of fleeting inbox notes in small fast batches, such as after a bursty capture session.

### When NOT to use

- Resurfacing permanent notes already in the vault for review — use `vault-review`.
- Editing a single known note — use `Edit` directly.
- Atomizing a long fleeting note into multiple permanent notes — use `process-notes`.
- Proposing `[[wikilinks]]` between existing notes — use `vault-connect`.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **BATCH_SIZE**: 7
- **INBOX_FOLDER**: `inbox/`
- **FLEETING_AGE_DAYS_DEFER_THRESHOLD**: 14
- **STUB_WORD_THRESHOLD**: 20

## Core Process

### Phase Overview

| Phase | Goal                      | Details                       |
| ----- | ------------------------- | ----------------------------- |
| 0     | Setup                     | Inline below                  |
| 1     | Score batch               | `phases/score_batch.md`       |
| 1.5   | User approval — decisions | Inline below                  |
| 2     | Execute decisions         | `phases/execute_decisions.md` |

### Phase 0: Setup

1. **Resolve the project root.** Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.

1. **Resolve the vault path.** Resolve the vault path with precedence: `$ARGUMENTS` → `OBSIDIAN_VAULT_PATH` env → `MZ_VAULT_PATH` env → walk up from cwd to the nearest `.obsidian/` directory.

1. **Resolve the permanent-notes folder.** Read `<vault>/CLAUDE.md`. Extract the permanent-notes folder name from it (e.g., `04 - Permanent/`). If `CLAUDE.md` is absent or does not declare the permanent-notes folder, ask the user via AskUserQuestion: `What is your vault's permanent-notes folder path (relative to vault root)?` Store the answer in `state.md` under the key `PERMANENT_FOLDER`. Never hardcode a fallback path.

1. **Resolve the batch.** List `<vault>/<INBOX_FOLDER>/*.md` sorted by mtime ascending; take the first `BATCH_SIZE` notes. If zero notes are found, create the task directory and `state.md` as in the next step, but with `Status: complete`, `Phase: empty_inbox`, `phase_complete: true` and `what_remains: []`; tell the user the inbox is empty, then stop.

1. **Create the task directory.** Derive `task_name = <YYYY_MM_DD>_vault-triage_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<slug>` is a short mode tag (e.g., `weekly`); on same-day collision append `_v2`, `_v3`. Create `TASK_DIR<task_name>/` on disk. Write `state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `phase_complete: false`, `what_remains: []`, `Vault: <absolute path>`, `PERMANENT_FOLDER: <resolved path>`, `BatchPaths: <list of absolute paths>`.

### Phase 1.5: User approval — Triage Decisions

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/triage_batch.md` in full and capture its contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: triage gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the artifact verbatim as a normal markdown chat message — each note's title, preview, proposed decision, and rationale:

```
## Triage batch ready for review — vault-triage

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/triage_batch.md>

---
**Approve** → proceed to Phase 2 and execute all proposed decisions  ·  **Reject** → abort the triage session, no vault changes  ·  reply with an override list (e.g. 1=discard, 3=merge::Target Note Name) to revise
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/triage_batch.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the artifact in the question body:

- question: `The triage batch above is ready for review.`
- header: `Triage`
- options: **Approve** — proceed to Phase 2 and execute all proposed decisions · **Reject** — abort the triage session, no vault changes

The user may also reply with an override list such as `1=discard, 3=merge::Target Note Name`. Each override binds to the note's index in the batch.

**Response handling**:

- **Approve** → add `- decisions approved: .mz/task/<task_name>/triage_batch.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: decisions_approved`, and proceed to Phase 2 with the default decision map from `triage_batch.md`.
- **Reject** → update state to `aborted_by_user` and stop.
- **Any other reply (feedback or override list)** → apply overrides to the decision map and return to Surface 1, re-read `triage_batch.md`, and re-emit the entire plan message from scratch; OR proceed with the user-supplied override map if the user's reply is an explicit and unambiguous override list. For any `merge` decision in the override list, require `merge::<target note name>` syntax; if the user writes just `merge` without a target, re-ask for the missing target via AskUserQuestion. This is a loop — repeat until explicit approval. Never proceed to Phase 2 without the user's explicit approval or an unambiguous override map.
- **No answer** → set `Status: blocked`, keep `awaiting approval: triage gate`, stop. A missing answer is never approval.

## Decision Vocabulary

- **promote** — move the note from the inbox folder to the permanent-notes folder and patch frontmatter.
- **merge** — append the note's body to a user-named target note, then delete the inbox source.
- **discard** — delete the inbox file.
- **defer** — stamp a `review_after` frontmatter field and keep the note in the inbox.

## Common Rationalizations

| Rationalization                                                   | Rebuttal                                                                                                                               |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| "Auto-discard all stubs without showing them to the user."        | "Even stubs might represent intentional micro-notes; every discard must be approved."                                                  |
| "Pick the merge target automatically from the most-similar note." | "Merge target requires user intent; the agent proposes, the user names the target."                                                    |
| "Process the whole inbox in one pass, don't cap at 7."            | "`BATCH_SIZE = 7` keeps each session under 30 seconds; larger batches cause decision fatigue and erode the quality of every decision." |

## Red Flags

- Applying any decision before Phase 1.5 approval — all vault writes are gated.
- Auto-selecting a merge target instead of leaving `proposed_merge_target: null` and requiring the user to name it.
- Processing more than `BATCH_SIZE` (7) notes in a session — batching prevents decision fatigue.
- Deleting an inbox source file before verifying the destination write on promote or merge.
- Proceeding to Phase 2 without explicit "approve" from the user at Phase 1.5.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
