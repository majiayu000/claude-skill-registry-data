---
name: debug
description: Systematic bug fixing — reproduce, localise with logs/tests/diagnostics, form and test a hypothesis, fix the root cause, add a regression test. USE WHEN the user reports an error, stack trace, crash, "doesn't work", "broken", "fails", "why does", unexpected output, or flaky behaviour.
---

# Debug

Goal: fix the cause, not the symptom, and prove it with a test or a reproducible check.

## 1. Capture the facts
- Get the exact error text, stack trace, command, input and expected vs actual behaviour. If the user pasted a trace, read every frame that points into the workspace.
- Check `get_diagnostics` (whole workspace) and `@problems`-style errors first — compile/type errors often *are* the bug.
- Look at recent changes: `run_command` `git status`, `git diff`, `git log --oneline -10`. Bugs usually live in what changed last.

## 2. Reproduce
- Find or write the smallest reproduction: a failing test (preferred), a script, a curl, or a browser step. Run it and confirm it fails the same way. If you cannot reproduce, say so and gather more data (logs, versions, environment) instead of guessing.
- For UI/web bugs use `browser_inspect` on the page: it returns console errors, failed requests and a screenshot; add `actions` to reproduce the flow.

## 3. Localise
- Follow the stack trace into the code with `read_file`; `find_references` on the failing function to see all callers; `grep_search` for the error message to find where it originates.
- Bisect the path: add a temporary log/assert at the midpoint, re-run, narrow. Remove temporary instrumentation before finishing.
- Common culprits checklist: off-by-one / boundary · null/undefined/empty · async ordering, missing await, unhandled rejection · stale cache or state · wrong path/cwd/env var · encoding/line endings · timezone · mutation of shared data · version mismatch after dependency change · error swallowed by a broad catch.

## 4. Hypothesis → fix
- State the hypothesis explicitly ("`parseRange` returns NaN when the header is missing, so the slice is empty"). Make the smallest change that fixes the cause. Don't paper over with a try/catch, a default that hides the problem, or a retry.
- Consider the same bug elsewhere: `grep_search` for the pattern and fix siblings.
- If the fix changes behaviour callers depend on, check them with `find_references`.

## 5. Prove it
- Turn the reproduction into a permanent regression test (see the `test` skill) and run it: fails before, passes after.
- Run the related test suite and `get_diagnostics` on touched files; for web, re-run `browser_inspect` until clean.

## 6. Report
- Root cause in one or two sentences, what changed (files), how it was verified, and anything related that still looks fragile. If you learned a durable gotcha about this project, `memory_save` it.
