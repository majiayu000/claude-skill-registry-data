---
name: debug-playbook
description: Hypothesis-driven debugging — reproduce, hypothesize, probe, locate, fix, guard. Use when something is broken and you don't yet know why.
---

# Debug playbook

The order of operations matters more than the tools.

## 1. Reproduce

Nothing else is useful until you can make the bug happen on demand.

- Exact command / action / input that triggers it
- Minimum conditions — strip away anything not required
- If you can't repro, narrow: which environments? which users? which data? which times?
- Unreproducible bugs are intermittent bugs, which are race / env / state leaks — treat them as such.

## 2. Hypothesize

List 2–3 concrete theories. For each:

- What you think is happening (one sentence)
- What observation would confirm it
- What observation would kill it

If you have only one hypothesis, you're not thinking hard enough — or it's so obvious you should skip to step 4.

## 3. Probe

Add the cheapest probe that separates your top two hypotheses.

- A targeted log line > reading the code again
- `git bisect` when the timeline is wide and the test is binary
- `strace` / `dtrace` / `perf` when the surface is the runtime, not the code
- Differential execution — run on a known-good input and a known-bad input, diff the trace

Resist the urge to add logs everywhere. Add *one* at the pivot point.

## 4. Locate

When observation singles out the hypothesis, point at the line. Not the region — the line.

Ask: why does this line break? What invariant did we assume here that isn't true?

## 5. Fix

Minimum change that resolves the root cause. Nothing adjacent.

- Not: "add a try/catch so we don't see the error"
- Not: "bump the retry so it eventually succeeds"
- Not: "rewrite this section while I'm here"

## 6. Guard

Add a test that fails without your fix and passes with it. The test should target the condition, not mimic the scenario.

## Anti-patterns

- **Shotgun debugging** — changing five things, one passed. Revert four of them and find which one.
- **Bandaid reflex** — catching exceptions you don't understand. You're hiding the bug, not fixing it.
- **Upgrade cure** — "upgrading the dep fixed it". Maybe. Or maybe it re-broke differently. Read the changelog.
- **"Works on my machine"** — an environment bug. Find the environmental difference.
- **Adding retries** — every retry hides a bug you didn't diagnose.

## Writing up the diagnosis

Short report:

```
What happened: <observable>
Root cause: <one sentence, concrete>
Why tests missed it: <honest answer>
Fix: <the change, minimum>
Regression guard: <the test>
```

If you can't write this report, you haven't finished debugging.
