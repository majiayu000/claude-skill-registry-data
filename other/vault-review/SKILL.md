---
name: vault-review
description: 'Builds a ranked queue of permanent notes and runs a daily, weekly or monthly review session. Use when the user wants notes surfaced for review ("review session", "notes due for review", "weekly review"). Not for clearing the inbox (use vault-triage).'
argument-hint: '[optional: review mode — daily|weekly|monthly, or leave empty for smart queue]'
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(mv *), Read, Write, Glob, Grep, AskUserQuestion
---

# Vault Review

## Overview

Discipline skill that builds a composite review queue ranking notes by: days since last review (`last_reviewed` frontmatter), backlink density (notes with zero outlinks score highest), maturity stage (`maturity` frontmatter: seedling > sapling > tree > ancient-tree), and linked-note recency (notes connected to recently modified notes surface first). Surfaces 5-10 notes per session. Updates `last_reviewed` frontmatter on completion. Dispatches `moc-gap-detector` to surface structural gaps alongside the review.

## When to Use

Resurfacing permanent notes that need attention, ranked in a queue, for a daily, weekly or monthly review session.

### When NOT to use

- For clearing new fleeting notes out of the inbox — use `vault-triage`.
- For vault maintenance (orphans, broken links, stale sweeps) — use `vault-health`.
- For processing new notes into atomic form — use `process-notes`.
- For quick single-note review without the queue system — just `Read` and `Edit` directly.

## Constants

- **QUEUE_SIZE_DAILY**: 5
- **QUEUE_SIZE_WEEKLY**: 10
- **QUEUE_SIZE_MONTHLY**: 15
- **QUEUE_SIZE_SMART**: 10
- **SCORE_CAP**: 20
- **ORPHAN_PENALTY**: 10
- **NEVER_REVIEWED_DAYS**: 365
- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`

## Core Process

### Phase Overview

| Phase | Goal                  | Details                    |
| ----- | --------------------- | -------------------------- |
| 0     | Setup                 | Inline below               |
| 1     | Score & Queue         | `phases/score.md`          |
| 1.5   | User approval — queue | Inline below               |
| 2     | Review session        | `phases/review_session.md` |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Resolve vault path from `$ARGUMENTS`, then `OBSIDIAN_VAULT_PATH` env, then `MZ_VAULT_PATH` env. If none resolve, ask the user via AskUserQuestion — never guess.
1. Detect review mode: if `$ARGUMENTS` contains `daily`, `weekly`, or `monthly`, use that mode. Otherwise use `smart`.
1. `task_name` = `<YYYY_MM_DD>_vault-review_<mode>` where `<YYYY_MM_DD>` is today's date (underscores) and `<mode>` is the resolved review mode; on same-day collision append `_v2`, `_v3`.
1. Create `TASK_DIR<task_name>/`.
1. Write `state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `phase_complete: false`, `what_remains: []`, `Vault: <path>`, `Mode: <mode>`.

### Phase 1.5: User approval — Review Queue

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/review_queue.md` in full and capture its contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: queue gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the artifact verbatim as a normal markdown chat message:

```
## Review queue ready for review — vault-review

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/review_queue.md>

MOC gaps detected: <N gaps from moc-gap-detector> — details in .mz/task/<task_name>/moc_gaps.md

---
**Approve** → proceed to Phase 2 (review session)  ·  **Reject** → mark task aborted, no notes updated  ·  reply with feedback to revise
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/review_queue.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the artifact in the question body:

- question: `The review queue above is ready for review.`
- header: `Queue`
- options: **Approve** — proceed to Phase 2 (review session) · **Reject** — mark task aborted, no notes updated

**Response handling**:

- **Approve** → add `- queue approved: .mz/task/<task_name>/review_queue.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: queue_approved`, and proceed to Phase 2.
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → adjust queue parameters (exclude a folder, change weights, filter by maturity, resize), re-run Phase 1 if needed, overwrite `review_queue.md`, return to Surface 1, re-read the updated artifact, and re-emit the entire plan message from scratch. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: queue gate`, stop. A missing answer is never approval.

## Common Rationalizations

| Rationalization                                   | Rebuttal                                                                                                                                                                  |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "I know which notes need review, skip the queue." | "Interest-driven review creates survivorship bias — the notes you remember are already linked; the queue surfaces the orphaned ideas that have never found a connection." |
| "Update `last_reviewed` manually later."          | "Manual timestamp updates are skipped 80% of the time; without accurate `last_reviewed` data the queue degrades into random selection."                                   |
| "Skip the MOC gap detection, just do the review." | "MOC gaps and review needs are correlated — a cluster of seedling notes all lacking a MOC is exactly the pattern vault-review is designed to surface."                    |

## Red Flags

- Starting a review without showing the queue first — a hidden queue means the user cannot redirect.
- Marking notes as reviewed without the user confirming they were actually read.
- Reviewing notes in a fixed order (alphabetical, recency) instead of composite scoring.
- Proceeding to Phase 2 without explicit "approve" from the user.

## Verification

Print this block before concluding — silent checks get skipped:

```
vault-review verification:
  [ ] Ranked queue emitted verbatim as a chat message (Surface 1) and AskUserQuestion selector presented before session started
  [ ] `last_reviewed` updated only for notes the user confirmed reviewing
  [ ] MOC gaps surfaced alongside the queue (from moc-gap-detector)
  [ ] state.md Status is `complete` with Completed timestamp
```

If any box is unchecked, the skill did not run correctly — report the failure explicitly rather than claiming success.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

## Error Handling

- **Vault path missing or invalid** → escalate via AskUserQuestion; never guess a default.
- **Zero permanent notes found** (empty glob) → escalate via AskUserQuestion with the scanned folder path; the vault layout may differ from the default convention.
- **`moc-gap-detector` returns empty or malformed** → retry the dispatch once; if still empty, note the gap in `state.md` and continue the review session without MOC gap data.
- **All notes have identical scores** (degenerate queue) → fall back to recency sort and note the degenerate condition in `state.md`.
