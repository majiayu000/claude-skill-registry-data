---
name: vault-answer
description: 'Answers a question from vault notes with inline wikilink citations and an Unknowns list. Use when the user wants a note-grounded answer ("what does my vault say about X", "search my vault for Y"). Not for codebase or web questions (use ask).'
argument-hint: <question>
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Read, Grep, Glob, Write, AskUserQuestion
---

# Vault Answer

## Overview

Discipline skill for grounded Q&A over vault notes. Dispatches `vault-query-answerer` to produce an answer with inline `[[wikilink]]` citations plus an explicit `## Unknowns` list (claims the vault could not support). Read-only on the vault — writes nothing outside `.mz/task/<task_name>/`. Discipline type because the skill enforces strict citation-grounding rules; the agent must resist the shortcut of answering from general LLM knowledge.

## When to Use

Answering factual questions from the content of vault notes, with inline wikilink citations and no vault writes.

### When NOT to use

- Questions about a code repo or the web, not the user's notes — use `ask`.
- Editing notes — use `Edit` directly.
- Finding links between notes — use `vault-connect`.
- General LLM questions not tied to vault content — answer directly without this skill.
- Frontmatter/schema questions — use `vault-schema`.

## Arguments

`$ARGUMENTS` is the question. If empty, escalate via AskUserQuestion — never guess the question.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **MAX_NOTES_READ**: 20 — hard cap on notes the answerer may read.
- **MAX_PREVIEW_WORDS**: 300 — per-note preview slice for the answerer.
- **CITATION_DENSITY_MIN_RATIO**: 0.02 — at least 1 `[[wikilink]]` per 50 words of answer prose.

## Core Process

### Phase Overview

| Phase | Goal                | Details                           |
| ----- | ------------------- | --------------------------------- |
| 0     | Setup               | Inline below                      |
| 1     | Search + synthesize | `phases/search_and_synthesize.md` |

No approval gate — read-only skill, no vault writes.

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Capture `$ARGUMENTS` as the question. If empty, AskUserQuestion for the question — never guess.
1. Resolve vault path from `OBSIDIAN_VAULT_PATH` env, then `MZ_VAULT_PATH` env, then walk up from the working directory until a `.obsidian/` folder is found. If nothing resolves, escalate via AskUserQuestion.
1. Derive `task_name = <YYYY_MM_DD>_vault-answer_<question-slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<question-slug>` is a snake_case summary of the question (max 20 chars); on same-day collision append `_v2`, `_v3`.
1. Create `TASK_DIR<task_name>/` on disk.
1. Write `state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `Vault: <path>`, `Question: <verbatim>`, `phase_complete: false`, `what_remains: []`.

## Common Rationalizations

| Rationalization                                                                  | Rebuttal                                                                                                                                                                                                                 |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "Answer from general LLM knowledge when the vault is thin."                      | "This skill exists to surface what the vault knows; general knowledge belongs elsewhere. Thin vault = long `## Unknowns` section — surfacing the gap is the correct behavior, not compensating from general knowledge."  |
| "Skip the `## Unknowns` section if every claim looks grounded."                  | "The `## Unknowns` section is always present; an empty list is still informative — it signals the vault fully covered the question. Omitting the section removes a load-bearing signal from the answer."                 |
| "Invent a plausible-sounding `[[wikilink]]` to hit the citation density target." | "Every `[[wikilink]]` must resolve to a note that was actually read. Invented links corrupt the citation trail silently and make the answer unauditable. Prefer low density with honest citations over fabricated ones." |

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
