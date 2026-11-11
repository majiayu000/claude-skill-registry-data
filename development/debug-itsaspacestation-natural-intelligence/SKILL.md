---
name: debug
description: "Use when a test fails, a build breaks, a bug is reported, behaviour is unexpected, performance drops, or an integration misbehaves, before proposing or applying any fix. Also use when a previous fix did not work, when the cause is unknown, or when the user says stop guessing."
---
# Debug

## When to use
- A test, build, pipeline, or deployment fails
- A bug report, crash, wrong output, or unexpected behaviour
- A performance regression or intermittent failure
- A fix was applied and the problem is still there
- User says "stop guessing", "is that not happening?", "we're stuck?"

## Overview

No fix before the root cause is known. A fix for a symptom is a failure, even when the
test goes green. Systematic debugging is faster than guess and check, under pressure most
of all.

**REQUIRED BACKGROUND:** the [`evidence-based-analysis`](../evidence-based-analysis/SKILL.md)
skill sets the standard of proof. Every claim about the cause cites `file:line`, a log
line, or a command output. Inference is labelled as inference.

The fix itself follows the [`tdd`](../tdd/SKILL.md) skill: a failing test that reproduces
the bug comes first. Reference: [root-cause-tracing.md](root-cause-tracing.md). Read it
when the error appears deep in a call chain and the bad value's origin is unclear.

Adapted from the MIT-licensed superpowers systematic-debugging skill by Jesse Vincent.

## Workflow

Five phases, in order. No phase is skipped because the bug looks simple.

### 1. Evidence

1. Read the whole error: message, stack trace, line numbers, exit code. It often names the fix.
2. Reproduce on demand. Not reproducible: gather more data, do not guess.
3. Build the loop: one command that passes five checks.
   - Already run once, in this session, with its output read.
   - Fails on this bug and passes on a neighbouring input or revision.
   - Gives the same verdict every run.
   - Finishes in seconds.
   - Needs no human in the middle.
   Intermittent: raise the reproduction rate first. Loop the trigger, add load, narrow the timing window. Stop when the loop is reliable.
   No hypothesis before this command exists.
4. Check what changed: `git diff`, recent commits, new dependencies, config, environment.
5. Locate the code. Delegate to `ni:investigator` for "where is X", "what calls Y". It returns `path:line` rows only.
6. Multi-component systems (CI, build, service, database): log what enters and leaves each boundary, run once, read where it breaks. Then investigate that component only.
7. Tag every temporary log line with one prefix per investigation, such as `[DEBUG-7f3a]`.
8. Bad value deep in the stack: trace it back to its origin with [root-cause-tracing.md](root-cause-tracing.md).

### 2. Pattern

1. Find working code that does the same thing in this codebase.
2. When following a reference implementation, read it completely. No skimming.
3. List every difference between working and broken. None is too small to matter.
4. List the dependencies, settings, and assumptions the broken path relies on.

### 3. Minimise

1. Cut one element per run: an input, a caller, a configuration key, a data row.
2. Re-run the loop after each cut. Still red: keep the cut. Green: put the element back.
3. Stop when every remaining element is load-bearing.
4. The minimal case is the regression test of the Fix phase.

### 4. Hypothesis

1. State one hypothesis: "X is the root cause because Y", with the evidence cited.
2. Test it with the smallest change that can confirm or refute it. One variable at a time.
3. Refuted: form a new hypothesis. Never stack a second change on top of the first.
4. Not understood: say so. Ask, or gather more evidence. Never pretend.

### 5. Fix

1. Write the failing test that reproduces the bug ([`tdd`](../tdd/SKILL.md)). No test framework: a one-off script. The test exists before the fix.
2. One fix, at the source found in phase 1, not at the symptom. No "while I'm here" changes.
3. Run the whole test suite. Confirm the original symptom is gone, not only the new test.
4. Fix failed: count attempts. Under 3, return to phase 1 with the new information. At 3, stop and question the design (below).
5. Remove every probe by searching the prefix. None reaches the commit.
6. Commit with the [`git-conventions`](../git-conventions/SKILL.md) skill.

## Evidence block

The final summary is up to five sentences of prose: the cause and why the symptom
appears only where it does, the fix at `file:line`, each regression test as
`file::name`, and why the existing tests missed it. A claim about which inputs are or
are not affected must match a reproduction you ran; otherwise omit it. When the bug has
a threshold, include one boundary reproduction. Three plain text lines follow, not a
fenced block and not a list. No labelled bullet
list before the lines; no "not committed" line unless the user asked about commits. The
three lines carry the proof that the process happened, for a reviewer who sees only the
summary:

```
reproduced: <command → one line of failing output>
root cause before fix: <file:line — mechanism in one clause>
tests: red <N failed: test names> → green <N passed>
```

The fence above shows the template only; the reply writes the three lines bare.

A correct fix with an absent process trace reads as a guess to any reviewer.

## Three strikes

Three failed fixes is not a fourth hypothesis. It is a design problem. Signs: each fix
exposes new coupling somewhere else, each fix needs a large refactor, each fix creates a
new symptom. Stop. Write the evidence and the options down. Discuss with the user before
any further change. In a [`plan`](../plan/SKILL.md) workspace this is an outside-constitution
gap: draft the ADR.

## Red flags

Any of these thoughts means: stop, return to phase 1.

| Thought | Reality |
|---|---|
| "Quick fix now, investigate later" | The first fix sets the pattern. Investigate first. |
| "Just try changing X" | A guess. Form the hypothesis and cite the evidence. |
| "Change several things, run the tests" | Nothing isolates what worked. One variable. |
| "Skip the test, I'll check by hand" | Untested fixes regress. Failing test first. |
| "It's probably X" | Seeing a symptom is not knowing the cause. |
| "The reference is long, I'll adapt the pattern" | Partial reading guarantees a bug. Read it all. |
| "One more attempt" after two failures | Third failure means design. Stop and discuss. |

## Boundaries

This skill finds the cause and frames the fix. Writing the test is the `tdd` skill.
Locating code is the `ni:investigator` agent. Never apply a fix without a reproduced
failure and a cited cause. Never bundle a refactor with a fix. Security findings and
destructive steps are written in plain prose.
