---
name: iru-knowledge-complete
description: Mark one pending agreement/task as completed — given a task id matching a
  `knowledge/pending/pending-<task-id>.md` file, delete that pending file and check off the matching numbered
  item in its `knowledge/agreements/agreement-<timestamp>.md` file. Invoke as `/iru-knowledge-complete
  <task-id>`, or `/iru-knowledge-complete` with no argument to be asked for the task id. Use whenever a task or
  agreement produced by `iru-knowledge-process-inbox` has actually been completed and its tracking should
  reflect that, instead of hand-editing the agreement/pending files.
model: haiku
---

# Knowledge Complete

Mark a single pending task as completed: remove its `knowledge/pending/pending-<task-id>.md` file and check off
the corresponding numbered item in the meeting's agreement file.

## Step 1 — Get the task id

If provided as an argument, use it directly. Otherwise ask the user for it via `AskUserQuestion` (or a plain
question if that tool isn't available). The task id is everything between the `pending-` prefix and the `.md`
suffix of the file the user wants completed — e.g. for `pending-2026-08-01T10-00-00Z-3.md` the task id is
`2026-08-01T10-00-00Z-3`.

## Step 2 — Locate the pending file

Look for `knowledge/pending/pending-<task-id>.md`.

- **Not found**: list the task ids that do exist in `knowledge/pending` (derived from the actual filenames
  present) so the user can pick the right one, and stop — don't guess a close match.
- **Found**: read it. Per how `iru-knowledge-process-inbox` writes it (its Step 9), it should state which
  agreement file and item number it came from — use that directly. If the file's content doesn't clearly state
  this (e.g. it was hand-created or edited), fall back to deriving it from the task id itself: split off the
  trailing `-<n>` (the item number); the remainder is the meeting `<timestamp>`, giving
  `knowledge/agreements/agreement-<timestamp>.md` and item number `<n>`.

## Step 3 — Locate the matching agreement item

Open the agreement file identified in Step 2. Find the numbered item matching this task — it should currently
read `<n>. [ ] ...`.

- **Agreement file missing, the numbered item isn't found, or it's already checked (`[x]`)**: stop and tell the
  user what's inconsistent, without deleting the pending file — an unresolvable inconsistency here is worth a
  human look before anything is removed.

## Step 4 — Apply the completion

- In the agreement file, change that item's checkbox from `[ ]` to `[x]`, leaving its text and every other item
  untouched.
- Delete `knowledge/pending/pending-<task-id>.md`.

## Step 5 — Report

State which task id was completed, which agreement file and item number were checked off, and confirm the
pending file was removed.
