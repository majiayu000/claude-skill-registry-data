---
name: debug-systematically
description: Use when a test fails, a build breaks or the code does something unexpected, before proposing a fix. Read the error fully, reproduce it, find the root cause by evidence, test one hypothesis at a time, and fix the cause with a failing test first.
license: MIT
metadata:
  bundled-by: Shodh
  sources: obra/superpowers (systematic-debugging, root-cause-tracing)
---

# Debug systematically

Guessing at fixes is slower than finding the cause. A fix that removes the
symptom and leaves the cause comes back, usually somewhere worse.

Third of Shodh's six building skills (plan-before-building → test-first →
**debug-systematically** → design-polish for UI work → verify-before-done →
fresh-eyes-review). Use it
whenever something fails, including the tests test-first just ran.

**No fix before the root cause is found.**

## 1. Read and reproduce

- Read the whole error: every line of the message and the stack trace, the
  file paths, line numbers and error codes. The first error is usually the
  real one; later ones often follow from it. Warnings count too.
- Reproduce it with one command you can run again. If it does not happen every
  time, find out what differs between the runs before going further: order,
  timing, data, environment.
- Check what changed: `git diff`, `git log -5 --stat`, a new dependency, a
  changed setting.

## 2. Find the cause by evidence

- **Trace backwards.** Start at the line that fails and ask where the bad
  value came from, then where that came from, until you reach the place it
  was first wrong. Fix it there, not where it surfaced. When this session has
  Shodh's code map tools, `code_references` lists the callers of a function
  with `path:line`, and `code_definition` jumps to where a value's type or
  helper is defined.
- **Compare with what works.** Find similar code in the project that works and
  list every difference, however small.
- **Find the failing layer.** When data passes through several parts (a
  request, a parser, a store), check what goes in and comes out of each part
  once, to see which one breaks it. Add a temporary print or log line where
  needed, and remove it afterwards.
- Read the documentation or source of a library before assuming how it
  behaves.

## 3. One hypothesis at a time

- Write the hypothesis down: "X fails because Y".
- Make the **smallest** change or check that would prove or disprove it.
  Change one thing at a time.
- Wrong? Undo that change before trying the next idea. Never stack guesses.

## 4. Fix the cause

- First a test that reproduces the bug and fails (see test-first).
- Then one fix, at the root cause.
- Run the test and then the whole suite.

## 5. When fixes keep failing

After **three** fixes that did not work, stop. Repeated failure usually means
the design is wrong, not the last line. Tell the user what you tried, what each
attempt showed, and what you now suspect about the design, and ask how to
proceed. Do not try a fourth patch on your own. If the work has a checklist
(`update_plan`), mark the step blocked, with what stops it as the reason.

## Signs you are guessing

- "Let me just try..." without a hypothesis.
- Several changes at once.
- A fix you cannot explain.
- Widening a timeout, adding a retry or skipping a test to make a failure go
  away. These hide the cause; never do them unless the user asks after seeing
  the cause.
- Saying it is fixed without running the failing case again.

## When you are stuck

Say so plainly, with what you know and what you do not. Name the next thing
you would check. An honest "I have not found it yet" helps the user more than a
confident wrong answer.

## Sources and credit

Rewritten for Shodh from **obra/superpowers**, skill `systematic-debugging`
and its `root-cause-tracing.md` (https://github.com/obra/superpowers, commit
22f0b463e7a5e579904dd6211a520321035526f7), MIT License, Copyright (c) 2025
Jesse Vincent. See `LICENSE-superpowers.txt`.

Left out for Shodh: the shell scripts that ship with the sources (nothing a
skill ships is ever run), and the multi-agent and keychain examples.
