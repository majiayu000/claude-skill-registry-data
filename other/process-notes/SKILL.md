---
name: process-notes
description: 'Turns fleeting notes, long notes and raw captures into permanent atomic notes. Use when the user wants notes processed or atomized ("process fleeting notes", "atomize this note"). Not for a fast keep/merge/discard pass (use vault-triage).'
argument-hint: '<note name, daily note date YYYY-MM-DD, #fleeting tag, or paste raw text>'
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Read, Write, AskUserQuestion
---

# Process Notes

## Overview

Discipline skill that runs the fleeting-to-permanent pipeline with explicit approval gates. Takes raw input (a fleeting note, a daily note, or pasted text), proposes atomic splits with claim-style titles, drafts each note, writes approved drafts to the vault, and suggests `[[wikilinks]]` to existing notes — all with explicit user approval before any write and before any link is added. Enforces claim-style titles (sentence asserting one idea), `status: draft` frontmatter on every new note, and vault CLAUDE.md conventions for folder placement, frontmatter schema, and tag taxonomy.

## When to Use

Writing inbox or `#fleeting` notes, daily notes, highlights and pasted raw captures up as permanent atomic notes, splitting long multi-idea notes into separately linkable ones.

### When NOT to use

- A fast keep/merge/discard/defer pass over an inbox without writing notes up — use `vault-triage`.
- Quick single-note editing — just use `Edit` directly.
- Vault maintenance (orphan detection, broken links, frontmatter sweeps) — use `vault-health`.
- Link suggestions for notes that already exist in the vault — use `vault-connect`.

## Constants

- **MAX_ATOMIC_NOTES_PER_RUN**: 10 (if input would produce more, ask the user to split input first)
- **MIN_INPUT_WORDS**: 100 (below this, input is likely already atomic — confirm before atomizing)
- **MAX_INPUT_WORDS_PER_PASS**: 2000 (quality degrades above this cap)
- **MAX_LINKS_PER_NOTE**: 5 (cap on link suggestions per new note)
- **MAX_TITLE_CHARS**: 70
- **MAX_FILENAME_CHARS**: 60
- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`

## Core Process

### Phase Overview

| Phase | Goal                   | Details                       |
| ----- | ---------------------- | ----------------------------- |
| 0     | Setup                  | Inline below                  |
| 1     | Atomize & Draft        | `phases/atomize_and_draft.md` |
| 1.5   | User approval — drafts | Inline below                  |
| 2     | Link & Write           | `phases/link_and_write.md`    |
| 2.5   | User approval — links  | Inline below                  |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Read vault CLAUDE.md if present at the vault root — extract folder structure, frontmatter schema, naming conventions, and tag taxonomy.
1. Resolve input: if the argument is a note name, Read the note. If it matches `YYYY-MM-DD`, try `<vault>/daily/YYYY-MM-DD.md`. If it is raw text, use directly.
1. If the resolved input is empty, ask the user what to process via AskUserQuestion — never guess.
1. Derive `task_name = <YYYY_MM_DD>_process-notes_<slug>` where `<YYYY_MM_DD>` is today's date (underscores); on same-day collision append `_v2`, `_v3`. Create `TASK_DIR<task_name>/` on disk.
1. Write `state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `VaultClaude: <path or none>`, `phase_complete: false`, `what_remains: []`.

### Phase 1.5: User Approval — Proposed Atomic Notes

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/proposals.md` and capture the full contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: proposals gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the proposals verbatim as a normal markdown chat message:

```
## Proposals ready for review — process-notes

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/proposals.md>

---
**Approve** → proceed to Phase 2, write all approved notes with links  ·  **Reject** → abort, discard proposals, do not write  ·  reply with feedback to revise (or a number list like `1,3` to skip specific notes)
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/proposals.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the proposals in the question body, they live in the plan message above:

- question: `The proposed atomic notes above are ready for review.`
- header: `Proposals`
- options:
  - **Approve** — proceed to Phase 2, write all notes with links
  - **Reject** — abort, discard proposals, do not write

Response handling:

- **Approve** → add `- drafts approved: .mz/task/<task_name>/proposals.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: drafts_approved`, and proceed to Phase 2 with all notes.
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Number list** (e.g. `1,3`) → mark those note numbers as skipped, proceed to Phase 2 with the remaining set.
- **Any other reply (feedback)** → pass feedback to the atomization-proposer, re-run Phase 1, overwrite `<PROJECT_ROOT>/.mz/task/<task_name>/proposals.md`, return to this gate, re-read the updated proposals, and re-emit the entire plan message from scratch. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: proposals gate`, stop. A missing answer is never approval.

### Phase 2.5: User Approval — Proposed Links

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/link_proposals.md` and capture the full contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: links gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the link proposals verbatim as a normal markdown chat message:

```
## Link proposals ready for review — process-notes

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/link_proposals.md>

---
**Approve** → write all proposed links and complete the task  ·  **Reject** → abort link writing, notes remain unlinked  ·  reply with feedback to revise (or a number list like `1,3` to skip specific links)
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/link_proposals.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the link proposals in the question body, they live in the plan message above:

- question: `The proposed links above are ready for review.`
- header: `Links`
- options:
  - **Approve** — write all proposed links and complete the task
  - **Reject** — abort link writing, notes remain unlinked

Response handling:

- **Approve** → add `- links approved: .mz/task/<task_name>/link_proposals.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: links_approved`, write all links, and proceed to completion.
- **Reject** → update state to `aborted_by_user` for links (notes already written in Phase 2 remain on disk without links).
- **Number list** (e.g. `1,3`) → mark those link numbers as skipped, proceed with the remaining set.
- **Any other reply (feedback)** → skip specified links or apply feedback, re-present the updated set. Return to Surface 1, re-read `<PROJECT_ROOT>/.mz/task/<task_name>/link_proposals.md`, and re-emit the entire plan message from scratch. This is a loop — repeat until the user explicitly approves. Never write links without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: links gate`, stop. A missing answer is never approval.

## Common Rationalizations

| Rationalization                                                | Rebuttal                                                                                                                                                                                                                |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Just write the notes without proposing first, it'll be fine." | "Atomization is heuristic — wrong splits create orphaned fragments that never get linked, and missed splits bury compound ideas that AI cannot surface later. The gate costs seconds, the miss costs the note forever." |
| "Use topic-style titles like 'Habits' — they're cleaner."      | "Topic titles are folders, not ideas. 'Variable reward schedules drive habit persistence' is searchable, linkable, and tells you what the note argues without opening it."                                              |
| "Skip the link step — I'll add links later."                   | "Links added at write time carry context; links added later require re-reading every note. The Zettelkasten failure mode is unlinked notes — the linking step is where connections actually happen."                    |

## Red Flags

- Writing notes to the vault without presenting proposals first.
- Using topic-style titles (`"Habits"`, `"Leadership"`) instead of claim-style assertions (`"Variable rewards drive habit formation"`).
- Writing notes without `status: draft` frontmatter.
- Processing more than `MAX_INPUT_WORDS_PER_PASS` words in a single atomization pass — quality degrades, split the input first.
- Proceeding to Phase 2 without explicit "approve" from the user.

## Verification

Print this block before concluding — silent checks get skipped:

```
process-notes verification:
  [ ] Proposals shown via AskUserQuestion before any write
  [ ] All written notes carry `status: draft` frontmatter
  [ ] All titles are claim-style assertions (no bare topics)
  [ ] Link proposals shown via AskUserQuestion before any link was written
  [ ] state.md Status is `complete` with Completed timestamp
```

If any box is unchecked, the skill did not run correctly — report the failure explicitly rather than claiming success.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
