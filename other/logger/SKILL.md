---
name: logger
description: Apply the shared logging contract and lifecycle pairing. Use when adding, changing, or reviewing log statements in any driver.
---

# Logging

The normative reference is the shared
[`SPEC.md`](../../../static/ergopti_plus/_shared/modules/logger/SPEC.md): it owns
the eight variants, the importance/lifecycle grid, punctuation, and driver
conformance contract. `AGENTS.md` owns the universal English and fail-fast
rules. This skill covers how to apply and verify that contract in practice.

## Log extensively

Under-logging is the default failure. Every meaningful state change, lifecycle
event, decision and failure path gets a line. Future debugging depends on it —
including yours, tomorrow, from a user's log file with no repro.

Selection heuristic: _"would I need this line to diagnose a bug in production?"_
Yes → `info` or above. Only useful during active development → `debug`/`trace`/`done`.
High-frequency events (per keystroke, per frame) → `debug` only.

## The pairing rule is enforced

`start` ↔ `success` and `trace` ↔ `done` must always come in pairs. This is not
cosmetic: **a `START` with no matching `SUCCESS` in a log is the primary signal
of a silent failure**, and the whole convention exists to make that visible.

`tests/meta/test_logger_pairing.ahk` checks this. An unpaired lifecycle call
fails the suite.

Practical consequence: if a function can return early between `start` and
`success`, every early-return path needs its own terminal log — usually an
`error` or `warn`, not a `success`.

## Common mistakes

- **Swallowing an error and logging nothing.** Violates the fail-fast contract
  in `AGENTS.md`. A bare `try … catch {}` is never acceptable; at minimum log
  at `error`.
- **`success` on a path that did not succeed.** A function that could not fulfil
  its contract must say so via return value _and_ log.
- **Setters that do not log.** Every public setter logs its new value at `debug`,
  as specified by the shared logger contract; this makes a boot log reconstruct
  the exact applied config.
- **French log text.** Logs are developer-facing and always English; only UI
  strings are French (see the `i18n` skill).
- **A `start` whose `success` sits after a `return`.** Reads fine, never fires.

## Throttling

High-frequency error paths need a throttle (the hook dispatcher uses a 60 s
per-label cache) or a single failing keystroke floods the log and buries the
context you need. Throttle the _repeat_, never the first occurrence.
