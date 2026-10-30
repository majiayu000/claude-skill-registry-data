---
name: session-summary
description: >-
  Close a working session by writing a six-section record and, when something durable changed, one
  changelog row, so the next session starts from recorded state instead of archaeology. Use when the user
  closes the session or a substantial block of work reaches a natural close. Trigger phrases include "wrap
  up", "close the session", "we're done for today", "write the session summary", "log what we did", "that's
  it for now", "summarize this session". Also fire before a planned restart, since no skill runs on its
  own when a session simply ends.
license: Apache-2.0
metadata:
  author: Marc Taccolini
  version: 1.1.0
---

# Session Summary

A session ends with a **record** of what it did and, when the repository changed in a way that lasts,
**one changelog row**. The next session, yours tomorrow or someone else's, starts by reading state rather
than reconstructing it from diffs.

This is not a transcript. It is what a person needs to pick the work up cold.

## Where things go

| What | Default | Change it to |
|---|---|---|
| Session records | `docs/sessions/` (add it to `.gitignore` if you do not want them in history) | wherever your repository keeps notes |
| Changelog | the repository's existing `CHANGELOG.md`, if there is one | your own changelog, or none |

If the repository has no changelog, skip the row. Do not invent a location.

## When to fire

- The user closes the session: "wrap up", "done for today", "close it out".
- A substantial block of work reaches a natural close and the next block is unrelated.
- Before a planned restart or a context cap.

Do not fire after a trivial exchange. A session that answered one question and changed nothing needs no
record. **But a skipped record still reconciles what is open:** if the session opened or closed an item in
the tracker, say so in one line even when you write no file. A skip that also skips that check silently
freezes the open-items list, and nobody notices for weeks.

## Open items go to the tracker first

The record assembles facts that already live somewhere durable. It is not where open work is kept. Before
writing it, put each open item where the repository tracks work (issue, task list, TODO file), then point
at it from the record. An open item that exists only inside a session record is lost the day nobody reads
that record.

## The record: six sections

File: `<sessions-dir>/Session-YYYY-MM-DD-HHMM-<slug>.md`. The slug names the work, not the date.

Header line: **`Session id: <id>`**. Take the id from the transcript file name or a hook payload's
`session_id`. Never take the newest file in the transcripts directory: with parallel sessions that is
often someone else's. The id is what lets a later session or a hook tell whether this session was already
recorded.

1. **What this session was.** Two or three sentences: the goal as it stood at the end, which is often not
   the goal it started with. If the direction changed, say why. That line is often the most valuable one
   in the file.
2. **What changed.** Every file or record touched, each with the **marker that proves it**: a symbol, a
   heading, a config key, a test name. "`parseHeader()` in `src/parse.ts` now tolerates a missing charset;
   test `parse.header.missing-charset`", not "updated the parser". Separate **applied** from **drafted but
   not applied**.
3. **Decisions made.** Each decision, the alternative rejected, and why. One line each. A decision without
   its rejected alternative gets re-argued later.
4. **Still open.** First line by default: `None, session closed clean.` Otherwise each item with a pointer
   to where it is tracked. Include questions put to the user that never got an answer.
5. **Findings.** What this session learned the hard way: a tool that reported success but did not write,
   a flag that behaves differently than documented, an assumption that proved false. A finding that
   generalizes also goes into `CLAUDE.md` or the project notes, not only here.
6. **Next action.** One line: the single most valuable next step, written to be read cold.

## The changelog row

One row in the shape the file already uses. A durable statement of what changed and when, not a summary of
the record. If nothing durable changed, write no row: an honest gap beats "investigated X".

## Committing

Several sessions often share one working tree, and `git commit` takes the whole index, including what
another session staged and never committed. Commit only this session's own paths:

```bash
git add <new files this session created>
git commit -o <every path this session changed> -m "..."
```

`-o` limits the commit to the named paths. It still commits the whole of each named file, so a file two
sessions both edit goes in with both sets of changes. Say so in the message when that happens.

## Rules

- **Verify before recording.** Never write "done" for something you did not read back. Record an
  unverified change as unverified.
- **A closed record is not edited.** Once the session has ended, its record is history. Correct it with a
  new record that references it, never by rewriting it.
- **No secrets.** Session records are often the least-guarded files in a repository.
- **Memory stays on one machine.** Claude Code's auto memory lives on the machine that wrote it. Anything
  the next session needs on another machine belongs in the repository.
- **Length tracks substance.** A short session gets a short record.

## Anti-patterns

- Re-narrating the conversation turn by turn. The record is state, not history.
- "Updated the config" with no key named.
- An open question that quietly drops out of section 4 because it got awkward.
- `git add -A` at the close, which commits other sessions' work under your message.
