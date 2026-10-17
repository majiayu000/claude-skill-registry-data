---
name: check-in-later
description: >-
  Park until a wall-clock time or a named condition, then resume the next
  named step. Use when asked to wait until a change window, check in later,
  or resume a parked wait.
---

# check-in-later

The wait between two steps hours apart: a change window opens tonight, the deploy runs then. This skill **parks**: it records the **wake**, ends the run, and **resumes** later by reading that record. The steps on either side own their own reads (the open and close CHG skills read ServiceNow); this skill only times the resume.

Two entries. A `when` given means park. None given means resume from the record.

## Inputs

- **when**: a local datetime, or a condition (`when the CHG is Scheduled`). A condition is the gate `next` checks for itself on resume; its time is the one the caller expects it to hold by (a CHG: its planned start).
- **next**: the caller's resolved skill path and a one-line brief. Keep that path as given (a product skill may live under the checkout, not `~/.agents/skills/`).
- **reread** (optional): loadable paths (a status file) and identifiers to pass through to `next` (a CHG number). Paths are read here; identifiers are handed on, not fetched.
- **record** (optional on resume): the status file or wait-record path Park named. Required when more than one wait exists.

## Park

1. Resolve `when` to `wake_at`. A condition without a time: ask for its expected time. Done when `wake_at` is one absolute datetime with offset.
2. Record the wake: `wake_at`, `condition` (the original `when` text, or empty for a bare datetime), `next`, `reread`. Into the status file when one was given, keeping its other fields; else `${XDG_STATE_HOME:-$HOME/.local/state}/check-in-later/<name>.json`, named for the thing waited on. Rewrite atomically. Done when the record reads back from disk, including `condition`.
3. Wait by length:
   - **An hour or more**: tell the user `wake_at`, the record path, the next step, and that a session at or after `wake_at` resumes this skill with that record path and no `when`. Then end this run. Done when the reply names all four and is the last thing this run does.
   - **Under an hour**: wait in this session with the harness's timer, a one-shot scheduled prompt for that minute or a background sleep that reports when it exits, then Resume. Done when `wake_at` has passed and Resume has run.

## Resume

Read the record named by `record`, or the one `reread` path that is a status file. With neither, the newest file in the default directory, newest by `wake_at`. Missing record: report that and end. Load every `reread` path; pass identifiers through.

- `wake_at` has passed, or the user says the recorded `condition` holds: read `next` from its path and follow it with its brief, the loaded paths, the identifiers, and the recorded `condition`. Done when that skill's first step has been started with those inputs.
- Otherwise: report the time left and end the run.
