---
name: dream
description: >-
  Consolidate the project's durable knowledge (auto memory, CLAUDE.md lessons, notes files) against what
  actually happened in the session records written since the last run. Finds entries a later decision has
  contradicted, duplicates, and lessons that recurred in several sessions but were never written down, then
  writes one cited report and applies only what the user approves. Use when the user asks to "dream",
  "consolidate memory against the sessions", "what patterns are we repeating", "what keeps going stale",
  "clean up what Claude remembers". User-invoked only: never scheduled, never run by a hook. Does NOT fire
  at session close (that is session-summary) or to save a single fact (write that directly).
license: Apache-2.0
metadata:
  author: Marc Taccolini
  version: 1.1.0
---

# Dream

Sessions write durable knowledge one fact at a time. Over a few hundred sessions that store collects
duplicates, entries a later decision contradicts, and lessons that recurred in five sessions and were
written down in none. A dream reads the store, reads what happened since the last dream, and corrects the
store.

A plain memory cleanup only looks at the memory files. A dream checks them against the record of what
actually happened, and the record wins.

## What it reads

| Role | Source |
|---|---|
| Store | Claude Code's auto memory for this project, plus any lessons or notes sections in `CLAUDE.md` and the project's notes files |
| Corpus | Session records written since the last dream (for example the ones `session-summary` writes), newest first, at most 100 per run |
| Ground truth, outranks the store | The decision log, the tracker, the changelog, and git history |
| Watermark | A small state file, for example `.claude/dream-state.json`: when the last dream ran and the newest record it consumed |

**Read the watermark's timestamp, not the watermark file's modification time.** Any edit moves the file's
time and silently skips records. Enumerate session records by their own modification time against that
timestamp.

## Procedure

1. **Orient.** Read the watermark and list the records newer than it. Fewer than about ten new records and
   the user did not insist: say so and stop, there is not enough to find patterns in. Count the store
   before touching it.
2. **Mine.** Read every new record in full, not by search hit. Look for four things:
   - the same class of mistake corrected in two or more sessions
   - a preference the user stated more than once
   - a workflow that converged across several sessions
   - a store entry a later record or decision contradicts
   For a large backlog, split the records by date across parallel read-only agents and treat an item two
   agents surface independently as the stronger signal.
3. **Apply the two-record floor.** One occurrence is an event, not a pattern. A NEW entry needs two
   independent records, or one record plus a decision log entry. A CORRECTION to an existing entry needs
   one decision or one record that clearly overtakes it.
4. **Verify each candidate.** Re-open its sources and confirm them before it goes in the report. A
   candidate that came from a search hit or a title is not verified. A claim about live state (a service
   running, a setting on) is re-checked live, never taken from the record.
5. **Report.** One file, every entry citing the records or decisions behind it. An entry with no citation
   is an invention and does not go in.

```markdown
# Dream, YYYY-MM-DD HH:MM
Records read: <N>, <first> to <last>; <N> still pending
Store read: <N> entries

## Proposed corrections   (entry, old -> new, source)
## Proposed new entries    (text, the two sources)
## Proposed merges or drops (files, and every reference that would need repointing)
## Refuted on verification (candidates that failed step 4, one line each)
```

6. **Apply what the user approves**, then update the watermark.

Keep the "refuted" section. It is the dream's own error rate, and it is how you learn whether to trust the
next run.

## Rules

- **The record wins.** A memory entry contradicting a recorded decision is stale. Correct the memory and
  cite the decision, never the reverse.
- **Never rewrite a record or a decision log entry.** Those are read, not edited.
- **Merges and drops are proposals.** Other files may reference a memory entry by name; removing it needs
  those references repointed.
- **Point, do not copy.** If a fact has a canonical home in the repository, the memory entry points there
  instead of restating it.
- **No secrets** in the report or the store.

## Anti-patterns

Finding patterns in three records. Applying a candidate nobody re-checked. Rewriting history because memory
disagrees with it. Turning every one-off event into a permanent rule.
