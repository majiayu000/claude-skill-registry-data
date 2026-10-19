---
name: bug-debugger
description: Use when something is broken, a test fails, an error or stack trace appears, behavior is wrong or intermittent, a regression appeared after a change, or a fix attempt did not work — any language or framework.
---

# Bug Debugger

## Overview

Find the root cause before changing code. Reproduce, narrow down with evidence, fix the cause, and prove the fix with a test that failed before and passes after. Guess-and-patch loops waste more time than they save.

## Method

1. **Reproduce.** Get the exact command, input or steps that show the bug. Write it down. If it is intermittent, find the condition that makes it frequent (load, timing, data, order).
2. **Read the evidence fully.** The whole error message and stack trace, the first error in the logs (not the last), the failing assertion's expected vs actual.
3. **Check what changed.** `git log -p --since=<date> -- <path>`, recent dependency updates, config or environment differences. For a known good commit, `git bisect run <test command>`.
4. **Form one hypothesis** that explains all the evidence. State it in one sentence.
5. **Test the hypothesis cheaply:** a log line, a breakpoint, a minimal script, or a failing unit test. Confirm or discard it. Never change two things at once.
6. **Trace to the root.** Ask why the bad value or state exists, and keep asking until you reach the place where it was first wrong. Fix there, not where it crashed.
7. **Write a failing test** that reproduces the bug, then fix, then watch the test pass and run the full suite.
8. **Remove debugging code** (temporary logs, prints, breakpoints).

## Output contract

```
Bug: <one line>
Reproduce: <command or steps>
Root cause: <what was wrong, file:line, and why it happened>
Fix: <the change>
Proof: <test name> failed before, passes after; full suite: <result>
```

If the root cause is not found yet, report what was ruled out and the next experiment instead of guessing a fix.

## Quick reference

| Symptom | Look first at |
|---|---|
| Works locally, fails in CI or prod | Environment variables, versions, time zone, file paths, case sensitivity |
| Intermittent | Shared state, ordering, async without await, timeouts, caching |
| Wrong value | Where the value is first computed or transformed, not where it is displayed |
| Started after an update | Changelog of the updated dependency; lockfile diff |
| `undefined` / `null` errors | The caller that passed it, and the data source |
| Slow or hanging | Unbounded loops, missing timeouts, locks, N+1 queries |

## Common mistakes

- Changing code before reproducing the bug.
- Reading only the last line of a stack trace.
- Fixing the symptom (adding a null check) while the bad data still comes from upstream.
- Trying a third fix after two failed ones without new evidence. Step back and re-read the evidence.
- Declaring it fixed without a test that failed before the fix.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
