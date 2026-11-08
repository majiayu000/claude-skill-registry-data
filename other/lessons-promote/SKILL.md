---
name: lessons-promote
description: 'Turns lessons seen again and again into project rules in CLAUDE.md or .claude/rules/, one approval per lesson. Use when the session hint names promotion candidates or the user asks to "promote lessons". Not for saving a lesson (use memory-note).'
argument-hint: '[lesson ids such as L-0042 L-0017; default: lessons seen 3+ times]'
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/lessons-promote.sh *), Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Lessons Promote

## Overview

Moves lessons from `.mz/memory/lessons.md` into the project's own instructions, which every session loads in full. Lessons are only injected a few at a time. Each lesson gets its own Approve/Reject gate with a target proposed for it: `.claude/rules/<topic>.md` with `paths:` when the lesson concerns some files, or the project's CLAUDE.md when it holds everywhere. An approved lesson is written there and archived as promoted. A rejected one is not offered again until it recurs.

## When to Use

The SessionStart hint lists promotion candidates (lessons seen 3+ times) and the user agrees to review them, or the user asks to promote specific lessons by id.

### When NOT to use

- Saving a new lesson — use `/memory-note --lesson`.
- Editing or deleting a lesson — edit `.mz/memory/lessons.md` by hand.
- Installing curated rule packs — use `init-rules` (mz-rules).

## Arguments

`$ARGUMENTS` — optional lesson ids, curated (`L-0042`) or from the Inbox (`I-0107`). Empty → the curated lessons seen at least 3 times, minus those declined since they last recurred. Any other token → ask via `AskUserQuestion`. Never guess.

## Constants

- **LESSONS_FILE**: `.mz/memory/lessons.md`
- **PROMOTE_SCRIPT**: `${CLAUDE_PLUGIN_ROOT}/scripts/lessons-promote.sh`
- **MAX_PER_RUN**: 5 (the rest wait for the next run; the hint keeps naming them)
- **TASK_DIR**: `.mz/task/`

## Core Process

### Phase Overview

| Phase | Goal                              | Details      |
| ----- | --------------------------------- | ------------ |
| 0     | Setup and list the lessons        | Inline below |
| 1     | Draft one lesson's rule and place | Inline below |
| 2     | Approval gate for that lesson     | Inline below |
| 3     | Write the rule, archive, next     | Inline below |
| 4     | Summary                           | Inline below |

Phases 1 to 3 run once per lesson, in the order the script printed them.

### Phase 0: Setup

1. Resolve the project root once: `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`. Every path below is relative to it.
1. `task_name` = `<YYYY_MM_DD>_lessons-promote_<slug>`, where the slug is `candidates` or the given ids in snake_case, 20 characters at most. On a same-day collision append `_v2`, `_v3`. Create `.mz/task/<task_name>/` and write `state.md` (`Status: running`, `Phase: 0`).
1. Run `Bash PROMOTE_SCRIPT list [<id>...]`. It prints one lesson line per id: `- [L-0042] n=4 last=… trig=… src=… tags=… :: <text>`.
   - Exit 2 → surface stderr (an unknown or malformed id) and stop with `Status: failed`.
   - No output → say "No lessons to promote: none has been seen 3+ times since it was last declined." and stop with `Status: complete`.
1. Keep the first MAX_PER_RUN lines. Record their ids under `Candidates:` in `state.md`.

### Phase 1: Draft

1. Rewrite the lesson as one imperative bullet: what to do and when, then the reason after a colon. Keep its paths, commands and flags. Example: the lesson `WHEN a hook emits JSON → build it with jq -n — WHY printf broke on quotes` becomes `- Build hook JSON output with \`jq -n\`, never printf: quotes in values break hand-built JSON.\`
1. Choose the target:
   - **`.claude/rules/<topic>.md`** when the lesson is about particular files or directories. Its `paths:` globs come from the paths the lesson names. The topic is a short kebab-case word, usually a tag (`hooks`, `git`, `tests`). Prefer an existing rules file on that topic, widening its `paths:` if the lesson needs it.
   - **CLAUDE.md** when the lesson holds across the project. Use the root `CLAUDE.md`, or `.claude/CLAUDE.md` when that is the one the project has. Put the bullet under the heading it belongs to; when no heading fits, add a `## Conventions` section at the end.
1. Read the target first. Never edit inside `<!-- mz-rule:… -->` blocks or rule files that init-rules manages, because a re-run of init-rules overwrites them. If the target already says the same thing or the opposite, propose changing that line instead of adding one.

### Phase 2: Approval Gate

**This orchestrator** (not a subagent) presents this gate, once per lesson. This step is interactive and must not be delegated.

Write `state.md` first, with `Phase: 2` and `Current: <id>`.

**Surface 1 — emit the plan message.** Output the full proposal as a normal markdown chat message. Do not substitute a path, summary, or placeholder. Structure:

```
## Lesson promotion ready for review — lessons-promote (<k> of <total>)

Lesson: <the lesson line, verbatim>
Target: <path> (<new file | existing file, under "<heading>" | replaces line N>)

<the exact text to write; for a new rules file, the whole file with its frontmatter>

---
**Approve** → write the rule and archive the lesson  ·  **Reject** → keep the lesson; it is offered again only once it recurs  ·  reply with feedback to change the wording or target
```

**Surface 2 — call AskUserQuestion.** The question must not re-embed the proposal — it lives in the plan message above.

- question: `The lesson promotion above is ready for review.`
- header: `Promote`
- options:
  - **Approve** — write the rule and archive the lesson
  - **Reject** — keep the lesson, offer it again once it recurs

**Response handling**:

- **Approve** → Phase 3.
- **Reject** → run `Bash PROMOTE_SCRIPT decline <id>`, record the id under `Declined:` in `state.md`, and move on to the next lesson.
- **Any other reply (feedback)** → change the wording or target as asked, re-emit the whole plan message from scratch, and ask again. This is a loop — repeat until the user approves or rejects. When the feedback corrects a mistake, such as a wrong target, add a `(correction)` line under `## Lessons` in `state.md`.
- **No answer** → set `Status: blocked` with the unreviewed ids in `what_remains`, and stop. The user's silence never approves a promotion.

### Phase 3: Write and Archive

1. Write the rule exactly as approved: Edit an existing file, or `mkdir -p .claude/rules` and Write a new one.
1. Re-read the target and confirm the text is there.
1. Run `Bash PROMOTE_SCRIPT archive <id> <target>` with the target path relative to the project root. Exit 2 with "not in lessons.md" means the curator merged or archived the lesson in the meantime; keep the rule and note it in the summary.
1. Record `<id> → <target>` under `Promoted:` in `state.md`, then return to Phase 1 for the next lesson.

### Phase 4: Summary

Set `Status: complete` and `what_remains: []`, then output the block under Verification.

## Common Rationalizations

| Rationalization                               | Rebuttal                                                                              |
| --------------------------------------------- | ------------------------------------------------------------------------------------- |
| "one gate for all the lessons is quicker"     | each lesson needs its own target and wording; one bad rule then hides in a batch      |
| "CLAUDE.md is simpler than a rules file"      | a lesson about one area costs context in every session; `paths:` loads it only there  |
| "paste the lesson as is"                      | `WHEN → — WHY` is a note to self; a rule says what to do in the project's own voice   |
| "the target already says it, archive quietly" | show the existing line at the gate; the user decides whether the lesson adds anything |

## Red Flags

- You wrote a rule before its gate was approved.
- You edited a file or block that init-rules manages.
- You archived a lesson whose rule is not in the target file.
- You declined a lesson the user did not reject.
- You promoted to the user-level `~/.claude/` files instead of the project's own.

## Verification

Print this block before concluding:

```
lessons-promote summary:
  Promoted: <id> → <target>, ... (or none)
  Declined: <ids> (or none)
  Not reviewed: <ids left past MAX_PER_RUN or after a stop> (or none)
  State: .mz/task/<task_name>/state.md (Status: <status>)
```

## Error Handling

- `lessons-promote.sh` exits 2 on `list` → surface stderr and stop.
- `archive` exits 2 because the lesson is gone → keep the rule, report it, continue with the next lesson.
- `decline` exits 2 → surface stderr and continue; the lesson is simply offered again next session.
- A target file cannot be written → surface the error, leave the lesson in place, and set `Status: failed` with the reason in `what_remains`.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer. This skill adds `Candidates`, `Current`, `Promoted` and `Declined`.
