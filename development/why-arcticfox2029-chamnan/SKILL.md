---
description: Work out whether a failure is your machine or your code before debugging either, using the environment this repository has declared and the dependency map. Use when a test, build or command fails and the cause is not obvious from the error.
---

# Your machine, or your code — decide that first

The expensive mistake is not picking the wrong fix. It is spending two hours in the code when the
problem was a version, or two hours on the environment when the problem was a line somebody changed.
One decision comes before any debugging, and this repository holds evidence for both sides of it.

## 1 · The machine

```
chamnan-env
```

What this repository has declared about the environments it runs in — the constraints nobody writes
down and everybody re-learns. A shell alias that hangs without a terminal, a binary that is not on
this platform, a Python whose certificate bundle is broken. **If the failure matches one of these,
stop: there is nothing wrong with the code.**

An error that mentions a command not found, a version mismatch, a certificate, a path separator or a
permission is a machine failure until something rules that out.

## 2 · The code

```
chamnan-impact <the file the failure points at>
```

Who imports it, **which tests cover it**, and what this repository has recorded about it. If the
failing test is in that list, the change and the failure are connected. If it is not, the error's
file and the failure's cause are probably different files.

## 3 · What this cannot tell you, and do not pretend otherwise

**chamnan does not know when the test last passed.** A Bash tool response carries no exit code —
only stdout, stderr and whether it was interrupted — and the `stderr` field was measured to be a
constant rather than a signal, so there is no record of outcomes to consult. `git log` on the files
`chamnan-impact` names is the substitute, and it is a weaker one: it shows what changed, not what
broke.

Say that plainly rather than inventing a history.

## When the agent already knows

If you just edited the file the failure names, this adds nothing — you have the diff and the error,
which is more than either command above can give you. **Use it when the failure is one you did not
cause:** a test that was already red when the session opened, a failure in code you did not touch,
or one that appeared after pulling somebody else's work.

## What not to say

**Do not report both halves.** The output of this skill is a decision — machine or code — and then
the evidence for that one. Listing everything from both commands is the raw material, not the answer.

**Do not treat a quiet `chamnan-env` as proof the machine is fine.** It lists what somebody declared,
and an undeclared constraint is the most likely kind to be biting you. A silent environment file
means *nobody has written this down yet*, which is worth saying — and worth fixing with
`chamnan-env set` once you find it.
