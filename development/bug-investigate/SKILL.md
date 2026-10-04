---
name: bug-investigate
description: Use when someone wants to know WHY something is broken and has not asked for it to be fixed — "why is this happening", "what's causing this error", "find out what's wrong", "diagnose this before we decide". Also use before committing to a fix, when the cause is unknown and the decision depends on it. Not for fixing — that is superb:bug-fix.
argument-hint: "[the bug report]"
---

# Bug Investigate

## Overview

Finds the root cause of a bug and reports it. **That is the whole job.**

No plan, no fix, no edits. Knowing what is wrong is often the thing that is
actually needed — because the fix is obvious once you know, because the decision
about *whether* to fix is someone else's, or because the answer changes what gets
built rather than what gets patched.

**This is the same investigation `superb:bug-fix` runs as its first step.** The
difference is where it stops. If you already know you want the bug fixed end to
end, use `superb:bug-fix` and let it carry the result into a plan.

## Step 0 — Assemble the report

The investigator needs five things, and the invocation argument usually supplies
one or two:

| Field | Example |
| ----- | ------- |
| Symptom | "uploads over ~5MB fail silently" |
| Reproduction | the steps, or `unknown` |
| Error text | stack trace, log line, or `none surfaced` |
| Affected surface | endpoint, screen, command, job |
| Last known good | a date, a release, a commit, or `never worked` |

Ask for whatever is missing in **one batched question**, not five. `unknown` is a
fine answer and belongs in the brief; a silently empty field is not, because the
investigator will fill it with a guess.

## Step 1 — Investigate

Take the first branch that applies:

| Condition | What to do |
| --------- | ---------- |
| A subagent mechanism, and `superb:bug-investigator` is in your available agent types | Dispatch **`superb:bug-investigator`** with the Step 0 report. |
| A subagent mechanism, but that agent is not listed | Dispatch a general subagent, briefed with the text **between the `SHARED BRIEF` markers** in `../bug-fix/references/investigator.md`. |
| No subagent mechanism | Follow that same bracketed brief **yourself**, inline, including its "modify no files" rule. |

Name the agent `superb:bug-investigator`, with the prefix. A bare
`bug-investigator` resolves to whatever personal agent happens to exist.

Do **not** substitute `superpowers:systematic-debugging`. Its four phases run
through hypothesis-testing and implementation, so it would fix the bug — which
is the one thing this skill is for not doing.

## Step 2 — Report, and stop

Give the investigator's report as it came back — symptom, root cause at
`file:line`, execution path, what introduced it, suggested fix. **The suggested
fix is a description, not an instruction to carry out.**

Then say what is now known and what it would take to act on it, and **stop
there.** Offer `superb:bug-fix` if fixing is the obvious next step; do not start
it.

**If the cause could not be pinned**, say so plainly, list what was ruled out,
and name what would narrow it — a reproduction, a log, a version that worked. A
confident guess is worse than an honest "not found", because the next person
builds on it.

## Red flags — STOP

- About to edit a file → wrong skill. This one does not fix.
- About to write a plan → also wrong skill. `superb:bug-fix` does that.
- About to say "I'll just fix it while I'm here, it's one line" → the user asked
  what was wrong. One line is still a change they did not ask for.
- About to report a cause with no `file:line` behind it → that is a hypothesis.
  Label it as one, or keep looking.
- About to run the app or start a dev server → the brief forbids it.
