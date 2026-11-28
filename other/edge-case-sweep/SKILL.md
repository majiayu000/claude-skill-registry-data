---
name: edge-case-sweep
description: Enumerate edge cases against a fixed checklist — empty, absent, boundaries, huge, weird text, duplicates, repeated/concurrent calls, stale state, time, failing dependencies — before declaring code complete. Use after the happy path of any new or changed function, handler, parser, validator, CLI, or data transformation works, and when reviewing one, before reporting done. Not for test structure or mocking decisions (see test-design).
---

# edge-case-sweep

Weak sweeping looks like: happy path passes, one `if (!input) return` added, done. Strong sweeping walks a fixed list against every new or changed code path, decides each applicable case, and proves the decision with a run.

## Procedure

1. List the changed entry points (functions, handlers, commands) and the inputs each receives.
2. Walk the checklist below against each. For every case that *can* reach the code, record one of: **handle** (a code path exists), **reject loudly** (specific error, non-zero exit, 4xx — and say what the caller sees), or **note** (deliberately unhandled, listed in the report). Silent wrong behavior is the one unacceptable outcome.
3. For every handle/reject decision, exercise it: run a test or a one-off call with that input and observe the outcome. "Handled" without an observed run is a claim, not a result.
4. Do not add guards for inputs the code cannot receive; state the invariant that excludes them instead. Defensive noise hides the real checks.

## Checklist

**Inputs**
- empty: `""`, `[]`, `{}`, zero rows, zero-byte file
- absent: null / undefined / missing key / missing flag — distinct from empty, and the distinction must survive the whole path, not just the entry check
- boundaries: 0, -1, exactly-at-limit, limit+1, first and last element, single element
- huge: 10^6 items, multi-GB file, pathologically long string — does it stream or load everything?
- weird text: unicode, emoji, RTL, newlines in fields, quotes, leading/trailing whitespace, case variants, path separators
- duplicates and unsorted order wherever uniqueness or order is assumed

**State & time**
- called twice (idempotency), called concurrently, retried after partial success — is any output left half-written?
- stale state: file changed since read, record deleted between fetch and update
- timezone, DST, end-of-month/year, leap day, clock skew

**Environment**
- dependency down / slow / returning errors or malformed data: what does the caller see, and does it time out?
- permissions denied, disk full, network cut mid-operation

**Outputs**
- the reject path returns the documented type (exception class, status code, exit code), never a success-shaped value with bad contents
- partial results are impossible or clearly marked as partial

## Report

List the cases you exercised and the cases you deliberately left unhandled. A stated limitation is fine; a hidden one is a bug report waiting.
