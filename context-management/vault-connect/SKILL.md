---
name: vault-connect
description: 'Proposes typed wikilinks between a note and related vault notes. Use when the user wants a note connected to the vault ("link notes", "suggest wikilinks", "improve link density"). Not for splitting a capture into new notes (use process-notes).'
argument-hint: <note name or path to find links for>
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Read, Write, Grep, Glob, AskUserQuestion
---

# Vault Connect

## Overview

Discipline skill that finds existing vault notes that should be linked to or from a given note. Dispatches `link-suggester` to search by keyword and title mentions, then uses typed relationship labels (`supports`, `contradicts`, `extends`, `example-of`, `prerequisite-for`, `see-also`) for each proposed link. All wikilinks require explicit user approval before being written. Writes wikilinks in-body where topically appropriate, or in a `## Related` section otherwise.

## When to Use

Finding existing vault notes that should link to or from a given note, with typed relationship labels and approval before any link is written.

### When NOT to use

- Splitting a capture or fleeting note into new atomic notes — use `process-notes`.
- Immediately after `process-notes` on the same note — link suggestions are already part of that pipeline.
- For semantic search or content retrieval — search and read the vault files directly, or use an MCP-based search tool.
- For note content editing unrelated to links — just use `Edit` directly.

## Constants

- **MAX_OUTBOUND_LINKS**: 5
- **MAX_INBOUND_LINKS**: 3
- **TARGET_PREVIEW_WORDS**: 500
- **MATCH_PREVIEW_WORDS**: 200
- **MAX_CANDIDATES_READ**: 15
- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`

## Core Process

### Phase Overview

| Phase | Goal            | Details                       |
| ----- | --------------- | ----------------------------- |
| 0     | Setup           | Inline below                  |
| 1     | Find candidates | `phases/find_candidates.md`   |
| 1.5   | User approval   | Inline below                  |
| 2     | Write links     | `phases/suggest_and_write.md` |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Resolve the target note from `$ARGUMENTS`. If it is a path, `Read` the file directly. If it is a note name, glob the vault for `<name>.md` — if zero or multiple matches, escalate via AskUserQuestion with the candidates.
1. If `$ARGUMENTS` is empty, ask the user via AskUserQuestion which note to connect — never guess.
1. Resolve the vault path from `OBSIDIAN_VAULT_PATH` env, then `MZ_VAULT_PATH` env, then the target note's parent directory tree (walk up until a `.obsidian/` folder is found).
1. `task_name` = `<YYYY_MM_DD>_vault-connect_<note-slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<note-slug>` is a snake_case summary of the note title (max 20 chars); on same-day collision append `_v2`, `_v3`.
1. Create `TASK_DIR<task_name>/`.
1. Write `state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `Vault: <path>`, `Target: <path>`, `phase_complete: false`, `what_remains: []`.

### Phase 1.5: User approval — Proposed Links

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/link_proposals.md` and capture the full contents into context. The proposals are grouped by direction (outbound / inbound), each labelled with a letter for skip-list responses.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: link gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the link proposals verbatim as a normal markdown chat message:

```
## Link proposals ready for review — vault-connect

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/link_proposals.md>

---
**Approve** → proceed to Phase 2, write all approved links  ·  **Reject** → abort task, no links written  ·  reply with feedback to revise (or a letter list like `a,c` to skip specific proposals)
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/link_proposals.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the proposals in the question body, they live in the plan message above:

- question: `The proposed links above are ready for review.`
- header: `Links`
- options:
  - **Approve** — proceed to Phase 2, write all approved links
  - **Reject** — abort task, no links written

Response handling:

- **Approve** → add `- links approved: .mz/task/<task_name>/link_proposals.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: links_approved`, and proceed to Phase 2 with all proposals.
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Letter list** (e.g. `a,c`) → mark those proposals as skipped, proceed to Phase 2 with the remaining set.
- **Any other reply (feedback)** → pass feedback to `link-suggester`, re-run Phase 1, return to this gate, re-read `<PROJECT_ROOT>/.mz/task/<task_name>/link_proposals.md`, and re-emit the entire plan message from scratch. This is a loop — repeat until the user explicitly approves. Never write links without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: link gate`, stop. A missing answer is never approval.

## Common Rationalizations

| Rationalization                                     | Rebuttal                                                                                                                                                                       |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "The note has plenty of links already, skip this."  | "Link quantity is not link quality — vault-connect finds typed relationships (`prerequisite-for`, `contradicts`) that generic backlinking tools and casual linking miss."      |
| "Just add all suggested links, no need to approve." | "Auto-wikilinks create false relationships when context is superficial; typed relationship proposals force articulation of WHY two notes connect, which is where value lives." |
| "I'll do this manually later."                      | "Link suggestions carry full context at write time; manual linking requires re-reading both notes; it will not happen later. The unlinked note is the Zettelkasten failure."   |

## Red Flags

- Writing wikilinks before presenting them to the user.
- Proposing links based on shared keywords alone without checking topical alignment.
- Adding wikilinks to the note's frontmatter `links:` property instead of in-body.
- Proceeding to Phase 2 without explicit "approve" from the user.

## Verification

Print this block before concluding — silent checks get skipped:

```
vault-connect verification:
  [ ] Proposals shown via AskUserQuestion before any write
  [ ] All written links use [[wikilink]] syntax, not [text](path) markdown
  [ ] Outbound and inbound links placed in-body or in a ## Related section
  [ ] state.md Status is `complete` with Completed timestamp
```

If any box is unchecked, the skill did not run correctly — report the failure explicitly rather than claiming success.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

## Error Handling

- **Target note not found or ambiguous** → escalate via AskUserQuestion with the candidate list; never guess.
- **Vault path unresolvable** → escalate via AskUserQuestion; never guess a substitute path.
- **`link-suggester` returns empty proposals** → report the empty result to the user via AskUserQuestion with the option to broaden search or abort — do not silently write nothing and claim success.
- **Vault has fewer than 10 readable notes** → accept `DONE_WITH_CONCERNS` from the agent, surface the small-vault concern in the approval gate.
