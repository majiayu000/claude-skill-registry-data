---
name: memory-note
description: 'Saves a note or decision to project memory; --lesson saves what a correction taught. Use when the user wants something remembered ("remember that", "note this", "pin this decision") or corrects you. Not for lookups (open MEMORY.md).'
argument-hint: '<the note, verbatim as the user wrote it>  [--log to append to Activity Log instead of Pinned]  [--lesson to save a lesson to the lessons Inbox]'
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/memory-note.sh *), Bash(date *), Read, AskUserQuestion
---

# Memory Note

## Overview

Appends a single dated entry to `.mz/memory/MEMORY.md`. By default the entry goes to the **Pinned** section (persistent, never auto-pruned). Pass `--log` to append to the **Activity Log** instead (FIFO, capped at 400 lines). Pass `--lesson` to add a lesson to the **Inbox** of `.mz/memory/lessons.md`, where the background curator later merges, keeps or drops it.

## When to Use

Records one note, decision, convention or invariant the user wants to outlive the current session, as a dated entry in `.mz/memory/MEMORY.md`.

With `--lesson`, records what a user's correction taught, so a later session does not repeat the mistake. After a correction, the prompt hook reminds you to run this mode.

### When NOT to use

- User wants to capture a completed task — that flows automatically through the SessionEnd hook
- A skill run learned something — it goes under `## Lessons` in that run's `state.md`, which the SessionEnd hook collects
- User wants to read or search memory — they should open `.mz/memory/MEMORY.md` directly
- User wants to remove an entry — edit the file by hand

## Input

`$ARGUMENTS` — the note body. Inline modifiers, at most one:

- `--log` — append to Activity Log instead of Pinned (use for transient activity-style notes)
- `--lesson` — save a lesson to the lessons Inbox instead of a note

If `$ARGUMENTS` is empty, ask via `AskUserQuestion`. Never guess. The one exception is an empty `--lesson`, which Phase 2 covers.

## Constants

- **MEMORY_FILE**: `.mz/memory/MEMORY.md`
- **LESSONS_FILE**: `.mz/memory/lessons.md`
- **NOTE_SCRIPT**: `${CLAUDE_PLUGIN_ROOT}/scripts/memory-note.sh`
- **MAX_BODY_CHARS**: 500 (longer notes go back to the user to shorten or split; never shorten them yourself)
- **LESSON_MAX_CHARS**: 400 (the script refuses a longer lesson rather than let the store cut it)

Pass the text to NOTE_SCRIPT in single quotes, writing each `'` inside it as `'\''`. Inside double quotes, the shell would run backticks and expand `$` before the script saw the text.

## Core Process

### Phase Overview

| Phase | Goal                           | Details      |
| ----- | ------------------------------ | ------------ |
| 0     | Parse                          | Inline below |
| 1     | Confirmation gate (notes only) | Inline below |
| 2     | Save a lesson (no gate)        | Inline below |
| 3     | Verification                   | Inline below |

### Phase 0: Parse

1. Strip `--log` or `--lesson` if present; remember it as `target=log` or `target=lesson`, otherwise `target=pinned`. If both are present, ask the user which one they meant.
1. Trim whitespace from the remaining body, and strip one pair of quotes around it.
1. If body is empty → `AskUserQuestion` for the note text. Never guess. With `target=lesson`, go to Phase 2 instead.
1. Count the characters of the note as the user wrote it in their message, not the Skill arguments, which may already be condensed. If it is longer than MAX_BODY_CHARS, ask the user to shorten or split it. Never shorten it yourself.
1. A lesson the user wrote follows the same rule with LESSON_MAX_CHARS. With `target=lesson`, go to Phase 2; otherwise continue to Phase 1.

### Phase 1: Confirmation Gate

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Compute the exact entry that will be written (`- [YYYY-MM-DD] <body>`) and capture it into context.

**Surface 1 — emit the plan message.** Output the entry verbatim as a normal markdown chat message. Emit the full verbatim contents — do not substitute a path, summary, or placeholder. Structure:

```
## Memory note ready for review — memory-note

- [YYYY-MM-DD] <body>

Target section: <pinned|log>
File: .mz/memory/MEMORY.md

---
**Approve** → write the entry to MEMORY.md  ·  **Reject** → discard, no file changes  ·  reply with feedback to revise
```

**Surface 2 — call AskUserQuestion.** After the plan message, call AskUserQuestion. The question must not re-embed the entry — it lives in the plan message above.

- question: `The memory note above is ready for review.`
- header: `Memory note`
- options:
  - **Approve** — write the entry to MEMORY.md
  - **Reject** — discard, no file changes

**Response handling**:

- **Approve** → run `Bash NOTE_SCRIPT [--log] '<body>'`, then proceed to verification.
- **Reject** → stop. Do not write. Surface "Note discarded."
- **Any other reply (feedback)** → revise the body using the user's input, return to Surface 1, re-emit the full updated plan message from scratch with the new entry, re-present the selector. This is a loop — repeat until the user explicitly approves.
- **No answer** → stop. A missing answer is never approval.

### Phase 2: Save a Lesson

A lesson goes to the Inbox without a gate. The curator reviews the Inbox later, and every session is told that lessons never override the user.

1. If the user wrote the lesson, save their words as they are. Otherwise, write it yourself from the correction in this conversation, as one line: `WHEN <situation> → <what to do> — WHY <cause>`. Keep it to about 40 words, under LESSON_MAX_CHARS, with concrete paths, commands and flags, and no secrets. If there is neither a lesson nor a correction to draw one from, ask via `AskUserQuestion`.
1. A slip no rule would have prevented, such as a typo the user fixed in passing, needs only the fix. Skip the lesson and say so.
1. Start the lesson with `(review)`, `(failure)` or `(change)` when it came from one of those. Untagged lessons are filed as corrections.
1. Run `Bash NOTE_SCRIPT --lesson '<lesson>'`, then proceed to verification.

### Phase 3: Verification

After the script runs, output a visible final block:

```
Memory note written.
File:    .mz/memory/MEMORY.md
Section: <pinned|log|lessons inbox>
Entry:   <verbatim entry line>
```

For a lesson, File is LESSONS_FILE and Entry is the line the script printed after `Wrote to lessons inbox:`. If the script exited non-zero, follow Error Handling.

## Common Rationalizations

| Rationalization                      | Rebuttal                                                                         |
| ------------------------------------ | -------------------------------------------------------------------------------- |
| "skip the gate, just write it"       | a wrong note pollutes pinned memory across every future session                  |
| "shorten the note to fit"            | the user will not notice the loss until the lost detail matters                  |
| "default to Activity Log"            | log entries roll off; user-driven notes belong in Pinned                         |
| "gate the lesson too, to be safe"    | lessons go straight to the Inbox by design; the curator is the review            |
| "the fix is enough, skip the lesson" | without the lesson, the next session makes the same mistake                      |
| "pin the lesson so it sticks"        | Pinned is for the user's notes; lessons are counted, merged and promoted instead |

## Red Flags

- You wrote to `MEMORY.md` or `lessons.md` directly with Edit/Write instead of the helper script.
- You skipped the approval gate for a note.
- You passed the text to the script in double quotes.
- You truncated or condensed a too-long note instead of handing it back to the user.
- You guessed the note body when `$ARGUMENTS` was empty.

## Error Handling

- Empty body → `AskUserQuestion` for the text. Never guess.
- The user's note > MAX_BODY_CHARS → ask the user to shorten or split it; do not truncate or condense it yourself.
- `memory-note.sh` exits 2 on a lesson over LESSON_MAX_CHARS → shorten it and run again if you wrote it; ask the user to if they did.
- `memory-note.sh` exits 2 for any other reason, or 1 → surface stderr and stop.
- `memory-note.sh` reports duplicate → surface the message; do not retry.

## State Management

This skill is single-shot — no `.mz/task/` state file is created. The only durable artifact is the line added to `MEMORY.md`, or to the Inbox of `lessons.md`.
